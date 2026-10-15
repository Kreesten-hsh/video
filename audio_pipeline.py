import os
import sys
import site
import json
import re
import wave
import subprocess
from pathlib import Path

_user_site = os.path.expanduser("~/.local/lib/python3.12/site-packages")
if _user_site not in sys.path:
    site.addsitedir(_user_site)

_local_bin = str(Path(__file__).parent.resolve() / "bin")
if _local_bin not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{_local_bin}:{os.environ.get('PATH', '')}"

import numpy as np
from faster_whisper import WhisperModel

def normalize_word(text: str) -> str:
    """Nettoie le mot pour comparaison lexicale (insensible casse et ponctuation)."""
    return re.sub(r"[^a-zA-Z0-9àâäéèêëîïôöùûüç]", "", text.lower())

def pass1_studio_filter(input_path: str, temp_wav: str = "temp_clean.wav") -> str:
    """Passe 1 : Filtrage de Voix Studio Professionnel FFmpeg."""
    print(f"[Passe 1/4] Filtrage Voix Studio sur {input_path} -> {temp_wav}...")
    af_filter = (
        "highpass=f=85,lowpass=f=14000,afftdn=nf=-25,"
        "acompressor=threshold=-18dB:ratio=3:attack=5:release=50,"
        "equalizer=f=180:width_type=o:width=1:g=3,"
        "equalizer=f=3500:width_type=o:width=1:g=2,"
        "loudnorm=I=-16:TP=-1.5:LRA=11"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-af", af_filter,
        "-ar", "44100",
        "-ac", "2",
        temp_wav
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return temp_wav

def pass2_transcribe(temp_wav: str):
    """Passe 2 : Transcription guidée haute précision faster-whisper (modèle small)."""
    print("[Passe 2/4] Transcription guidée faster-whisper (small, language=fr)...")
    initial_prompt = (
        "Arrête de payer des monteurs vidéo ou des IA hors de prix. "
        "Premiere Pro, Veo, Kling, code, Python, JavaScript, milliseconde, "
        "avatar, terminaux, losanges, cercles, FFmpeg, SaaS, entrepreneurs."
    )
    model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
    segments_iter, _ = model.transcribe(
        temp_wav,
        word_timestamps=True,
        language="fr",
        initial_prompt=initial_prompt
    )
    
    words = []
    for s in segments_iter:
        for w in s.words:
            clean = w.word.strip()
            if clean:
                words.append({
                    "word": clean,
                    "start": round(w.start, 3),
                    "end": round(w.end, 3)
                })
    return words

def pass3_dedup_and_cut(words: list, temp_wav: str, output_wav: str = "voix.wav", words_json: str = "words.json"):
    """
    Passe 3 :
    - Détection et suppression automatique des bafouillages / répétitions de 3 mots consécutifs.
    - Découpage et concaténation des segments parlés actifs (silences > 0.25s coupés, marges -0.06s / +0.08s).
    - Recalcul exact des timestamps dans words.json et export audio voix.wav.
    """
    print("[Passe 3/4] Analyse des phrases, élimination des reprises et coupe des silences > 0.25s...")
    if not words:
        raise ValueError("Aucun mot transcrit.")

    # 1. Regroupement en phrases pour détecter les répétitions de début de phrase
    sentences = []
    curr = []
    for w in words:
        curr.append(w)
        if any(w["word"].endswith(p) for p in [".", "!", "?", "..."]):
            sentences.append(curr)
            curr = []
    if curr:
        sentences.append(curr)

    surviving_sentences = []
    i = 0
    while i < len(sentences):
        if i + 1 < len(sentences):
            s1_words = [normalize_word(w["word"]) for w in sentences[i] if normalize_word(w["word"])]
            s2_words = [normalize_word(w["word"]) for w in sentences[i+1] if normalize_word(w["word"])]
            if len(s1_words) >= 3 and len(s2_words) >= 3 and s1_words[:3] == s2_words[:3]:
                print(f"  [Dédoublonnage] Reprise détectée : '{' '.join(s1_words[:3])}', suppression de la première tentative.")
                i += 1
                continue
        surviving_sentences.append(sentences[i])
        i += 1

    clean_words = []
    for s in surviving_sentences:
        clean_words.extend(s)

    # 2. Regroupement en clusters de parole active (silence inter-mots <= 0.25s)
    clusters = []
    curr_cluster = [clean_words[0]]
    for w in clean_words[1:]:
        gap = w["start"] - curr_cluster[-1]["end"]
        if gap <= 0.25:
            curr_cluster.append(w)
        else:
            clusters.append(curr_cluster)
            curr_cluster = [w]
    if curr_cluster:
        clusters.append(curr_cluster)

    # 3. Lecture audio temp_clean.wav
    with wave.open(temp_wav, "rb") as wf:
        nchannels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        nframes = wf.getnframes()
        raw_bytes = wf.readframes(nframes)

    audio_data = np.frombuffer(raw_bytes, dtype=np.int16).reshape(-1, nchannels)
    total_samples = len(audio_data)
    total_duration = total_samples / framerate

    # 4. Calcul des plages de coupe avec marges (-0.06s avant, +0.08s après)
    ranges = []
    for c in clusters:
        c_start = max(0.0, c[0]["start"] - 0.06)
        c_end = min(total_duration, c[-1]["end"] + 0.08)
        ranges.append((c_start, c_end, c))

    # Fusion des plages qui se chevaucheraient éventuellement
    merged_ranges = []
    for r_start, r_end, c_words in ranges:
        if not merged_ranges:
            merged_ranges.append([r_start, r_end, list(c_words)])
        else:
            prev = merged_ranges[-1]
            if r_start <= prev[1]:
                prev[1] = max(prev[1], r_end)
                prev[2].extend(c_words)
            else:
                merged_ranges.append([r_start, r_end, list(c_words)])

    audio_chunks = []
    final_words = []
    current_time_offset = 0.0

    for r_start, r_end, c_words in merged_ranges:
        start_sample = int(round(r_start * framerate))
        end_sample = min(total_samples, int(round(r_end * framerate)))
        if end_sample <= start_sample:
            continue

        chunk = audio_data[start_sample:end_sample]
        audio_chunks.append(chunk)

        chunk_actual_start = start_sample / framerate
        for w in c_words:
            w_start_in_chunk = w["start"] - chunk_actual_start
            w_duration = w["end"] - w["start"]
            new_w_start = current_time_offset + max(0.0, w_start_in_chunk)
            new_w_end = new_w_start + w_duration
            final_words.append({
                "word": w["word"],
                "start": round(new_w_start, 3),
                "end": round(new_w_end, 3)
            })

        current_time_offset += len(chunk) / framerate

    final_audio = np.concatenate(audio_chunks, axis=0)

    # 5. Export voix.wav et words.json
    with wave.open(output_wav, "wb") as wf:
        wf.setnchannels(nchannels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(final_audio.tobytes())

    with open(words_json, "w", encoding="utf-8") as f:
        json.dump(final_words, f, indent=2, ensure_ascii=False)

    print(f"✓ Passe 3 terminée : {len(final_words)} mots recalculés, durée dynamique : {current_time_offset:.2f}s (vs {total_duration:.2f}s brute).")

def main():
    default_src = "data/vocal1.m4a" if os.path.exists("data/vocal1.m4a") else "vocal1.m4a"
    src = sys.argv[1] if len(sys.argv) > 1 else default_src
    if not os.path.exists(src):
        print(f"Erreur : {src} introuvable.")
        sys.exit(1)

    temp_wav = pass1_studio_filter(src, "temp_clean.wav")
    raw_words = pass2_transcribe(temp_wav)
    pass3_dedup_and_cut(raw_words, temp_wav, output_wav="voix.wav", words_json="words.json")
    print("✓ Pipeline complet exécuté avec succès.")

if __name__ == "__main__":
    main()
