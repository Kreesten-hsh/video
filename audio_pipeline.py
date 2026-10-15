import os
import sys
import site
from pathlib import Path

_user_site = os.path.expanduser("~/.local/lib/python3.12/site-packages")
if _user_site not in sys.path:
    site.addsitedir(_user_site)

_local_bin = str(Path(__file__).parent.resolve() / "bin")
if _local_bin not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{_local_bin}:{os.environ.get('PATH', '')}"

import json
import subprocess
from faster_whisper import WhisperModel

def process_audio(input_path: str, output_wav: str = "voix.wav", words_json: str = "words.json"):
    """
    1. Normalisation sonore EBU R128 (loudnorm) PUIS découpage des silences (> 0.35s sous -35dB).
    2. Transcription Whisper mot-à-mot précise.
    """
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Fichier introuvable: {input_path}")

    print(f"[1/2] Traitement audio FFmpeg (loudnorm -> silence cut) sur {input_file}...")
    
    # loudnorm EN PREMIER pour ramener la voix à un niveau standard (-16 LUFS)
    # puis silenceremove pour couper proprement les silences sans tronquer les syllabes douces
    af_filter = (
        "loudnorm=I=-16:TP=-1.5:LRA=11,"
        "silenceremove=start_periods=1:start_duration=0.05:start_threshold=-35dB:"
        "stop_periods=-1:stop_duration=0.35:stop_threshold=-35dB"
    )

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", str(input_file),
        "-af", af_filter,
        "-ar", "44100",
        "-ac", "2",
        output_wav
    ]
    
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    print(f"[2/2] Alignement Whisper mot-à-mot -> {words_json}...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(output_wav, word_timestamps=True, language="fr")

    words = []
    for segment in segments:
        for word in segment.words:
            clean = word.word.strip()
            if clean:
                words.append({
                    "word": clean,
                    "start": round(word.start, 3),
                    "end": round(word.end, 3)
                })

    with open(words_json, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2, ensure_ascii=False)

    print(f"✓ Pipeline audio terminé : {len(words)} mots horodatés enregistrés dans {words_json}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "input_raw.wav"
    process_audio(src)
