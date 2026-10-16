import os
import sys
import json
import wave
import site
from pathlib import Path

_user_site = os.path.expanduser("~/.local/lib/python3.12/site-packages")
if _user_site not in sys.path:
    site.addsitedir(_user_site)

_local_bin = str(Path(__file__).parent.resolve() / "bin")
if _local_bin not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{_local_bin}:{os.environ.get('PATH', '')}"

import numpy as np

def step1_fuse_and_correct(words_path="words.json"):
    print("[1/3] A) Correction orthographique exacte et fusion des apostrophes...")
    candidates = ["data/words_base.json", "words_base.json", words_path]
    actual_path = next((p for p in candidates if os.path.exists(p)), words_path)
    with open(actual_path, "r", encoding="utf-8") as f:
        raw_words = json.load(f)

    # 1. Fusions d'apostrophes et de mots composés
    fused = []
    i = 0
    n = len(raw_words)
    while i < n:
        w1 = raw_words[i]["word"]
        # 3 mots : j + 'en + résiste -> j'enregistre
        if i + 2 < n and w1 == "j" and raw_words[i+1]["word"] == "'en" and raw_words[i+2]["word"] == "résiste":
            fused.append({"word": "j'enregistre", "start": raw_words[i]["start"], "end": raw_words[i+2]["end"]})
            i += 3
            continue
        # 2 mots
        if i + 1 < n:
            w2 = raw_words[i+1]["word"]
            if w1 == "n" and w2 == "'ai":
                fused.append({"word": "n'ai", "start": raw_words[i]["start"], "end": raw_words[i+1]["end"]})
                i += 2
                continue
            if w1 == "j" and w2 == "'ai":
                fused.append({"word": "j'ai", "start": raw_words[i]["start"], "end": raw_words[i+1]["end"]})
                i += 2
                continue
            if w1 == "l" and w2 == "'émotion,":
                fused.append({"word": "l'émotion,", "start": raw_words[i]["start"], "end": raw_words[i+1]["end"]})
                i += 2
                continue
            if w1 == "c" and w2 == "'est":
                fused.append({"word": "c'est", "start": raw_words[i]["start"], "end": raw_words[i+1]["end"]})
                i += 2
                continue
            if w1 == "100" and w2 == "%":
                fused.append({"word": "100%", "start": raw_words[i]["start"], "end": raw_words[i+1]["end"]})
                i += 2
                continue
            if w1 == "entrepreneurs" and w2 == "?":
                fused.append({"word": "entrepreneurs ?", "start": raw_words[i]["start"], "end": raw_words[i+1]["end"]})
                i += 2
                continue
            if w1 == "envoie" and w2 == "moi":
                fused.append({"word": "envoie-moi", "start": raw_words[i]["start"], "end": raw_words[i+1]["end"]})
                i += 2
                continue
        fused.append(dict(raw_words[i]))
        i += 1

    # 2. Remplacements et corrections orthographiques précises
    for idx, item in enumerate(fused):
        w = item["word"]
        if w == "dans" and 4.8 < item["start"] < 5.8:
            item["word"] = "en"
        elif w == "monté":
            item["word"] = "montée"
        elif w == "codeé":
            item["word"] = "codé"
        elif w == "séances":
            item["word"] = "silences"
        elif w == "transcribe":
            item["word"] = "transcrit"
        elif w == "gênait":
            item["word"] = "génère"
        elif w == "restructurées":
            item["word"] = "structurées,"
        elif w == "de" and idx + 1 < len(fused) and fused[idx+1]["word"] == "corps":
            item["word"] = "le"
        elif w == "corps" and idx > 0 and fused[idx-1]["word"] == "le":
            item["word"] = "décor"
        elif w == "losange":
            item["word"] = "losanges"
        elif w == "seig":
            item["word"] = "cercles,"
        elif w == "complique":
            item["word"] = "compile"
        elif w == "en" and idx + 1 < len(fused) and fused[idx+1]["word"] == "30":
            item["word"] = "à"
        elif w == "résolution":
            item["word"] = "révolution"
        elif w == "classées":
            item["word"] = "classiques"
        elif w == "coupent":
            item["word"] = "coûtent"
        elif w == "erreurs" and idx > 0 and fused[idx-1]["word"] == "des" and idx > 1 and fused[idx-2]["word"] == "prennent":
            item["word"] = "heures"
        elif w == "euros.":
            item["word"] = "euro."
        elif w == "déplace":
            item["word"] = "déploie"
        elif w == "le" and idx > 0 and fused[idx-1]["word"] == "déploie":
            item["word"] = "ce"
        elif w == "chat":
            item["word"] = "charte"
        elif w == "code" and idx > 0 and fused[idx-1]["word"] == "envoie-moi":
            item["word"] = "« CODE »"

    print(f"✓ Fusions et corrections terminées : {len(fused)} mots consolidés.")
    return fused

def filter_and_crop_silences(raw_silences, words_base_path="data/words_base.json", voix_base_path="data/voix_base.wav"):
    """
    Filtre et recadre chaque tuple (s_start, s_end) de raw_silences :
    - Charge les mots de words_base_path (zone vocale intouchable [w["start"] - 0.16, w["end"] + 0.09]).
    - Découpe/réduit chaque plage de silence pour ne JAMAIS empiéter sur aucune zone intouchable.
    - Analyse RMS par fenêtres de 10ms sur voix_base_path : recule les bornes si de la voix est présente.
    - Si la plage recadrée fait moins de 0.14s, l'ignore complètement.
    """
    candidates_w = ["data/words_base.json", "words_base.json", words_base_path]
    actual_w = next((p for p in candidates_w if os.path.exists(p)), words_base_path)
    with open(actual_w, "r", encoding="utf-8") as f:
        base_words = json.load(f)

    # Zones vocales intouchables
    untouchable = []
    for w in base_words:
        s_u = max(0.0, float(w["start"]) - 0.16)
        e_u = float(w["end"]) + 0.09
        untouchable.append((s_u, e_u))

    # Fusion des zones intouchables chevauchantes
    merged_u = []
    for s_u, e_u in sorted(untouchable):
        if not merged_u:
            merged_u.append([s_u, e_u])
        else:
            if s_u <= merged_u[-1][1]:
                merged_u[-1][1] = max(merged_u[-1][1], e_u)
            else:
                merged_u.append([s_u, e_u])

    # Découpe des plages de silence brutes par rapport aux zones intouchables
    def clip_silence(s, e, forbidden):
        segments = [(s, e)]
        for f_s, f_e in forbidden:
            new_segs = []
            for seg_s, seg_e in segments:
                if f_e <= seg_s or f_s >= seg_e:
                    new_segs.append((seg_s, seg_e))
                else:
                    if f_s > seg_s:
                        new_segs.append((seg_s, f_s))
                    if f_e < seg_e:
                        new_segs.append((f_e, seg_e))
            segments = new_segs
        return segments

    candidate_segs = []
    for s_raw, e_raw in raw_silences:
        clipped = clip_silence(s_raw, e_raw, merged_u)
        candidate_segs.extend(clipped)

    # Analyse RMS sur fenêtres de 10ms
    candidates_v = ["data/voix_base.wav", "voix_base.wav", voix_base_path]
    actual_v = next((p for p in candidates_v if os.path.exists(p)), voix_base_path)
    
    rms_arr = None
    noise_floor = 45.0
    if os.path.exists(actual_v):
        with wave.open(actual_v, "rb") as wf:
            sr = wf.getframerate()
            nc = wf.getnchannels()
            raw_b = wf.readframes(wf.getnframes())
            audio_f = np.frombuffer(raw_b, dtype=np.int16).astype(np.float32)
            mono = audio_f.reshape(-1, nc).mean(axis=1) if nc > 1 else audio_f.flatten()
            win = int(sr * 0.01)
            num_w = len(mono) // win
            if num_w > 0:
                rms_arr = np.sqrt(np.mean(mono[:num_w * win].reshape(-1, win)**2, axis=1))
                noise_floor = max(40.0, float(np.percentile(rms_arr, 12)))

    def get_rms(t):
        if rms_arr is None:
            return 0.0
        idx = int(t / 0.01)
        if 0 <= idx < len(rms_arr):
            return rms_arr[idx]
        return 0.0

    safe_silences = []
    for s, e in candidate_segs:
        # Reculer s si voix détectée
        while s < e and get_rms(s) > noise_floor:
            s += 0.01
        # Reculer e si voix détectée
        while e > s and get_rms(e - 0.01) > noise_floor:
            e -= 0.01
        dur = e - s
        if dur >= 0.14:
            safe_silences.append((round(s, 3), round(e, 3)))
        else:
            print(f"  [Sécurité Audio] Silence ({s:.2f}s - {e:.2f}s, dur={dur:.3f}s) ignoré car < 0.14s ou mordu sur la voix.")

    print(f"  -> {len(safe_silences)} plages de silence validées après filtrage strict.")
    return safe_silences

def step2_rms_silence_cut(words, voix_path="voix.wav"):
    print("[2/3] B) Découpe chirurgicale sécurisée avec protection absolue des mots...")
    candidates = ["data/voix_base.wav", "voix_base.wav", voix_path]
    src_wav = next((p for p in candidates if os.path.exists(p)), voix_path)
    with wave.open(src_wav, "rb") as wf:
        sr = wf.getframerate()
        nc = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        nframes = wf.getnframes()
        raw_bytes = wf.readframes(nframes)

    audio = np.frombuffer(raw_bytes, dtype=np.int16).reshape(-1, nc).astype(np.float32)
    total_samples = len(audio)
    total_dur = total_samples / sr

    # Plages candidates initiales
    raw_silences = [
        (25.85, 26.45), # silence après "Ensuite,"
        (34.15, 34.48), # silence après "structurées," (garder "et change" intact)
        (37.42, 37.90), # silence après "cercles," (garder "et il compile" intact)
        (43.05, 43.42), # silence après "seconde." (garder "Pourquoi" intact)
        (47.15, 49.30), # bafouillage "Parce que les z-i... les..." (garder "Parce" 100% entier)
        (68.82, 69.36), # bruit de bouche après "caméra,"
        (73.46, 74.02), # silence après "avatar"
    ]

    # Application du filtrage et recadrage de sécurité automatique
    silences = filter_and_crop_silences(raw_silences, "data/words_base.json", src_wav)

    # Micro-fondu (crossfade linéaire de 10ms) aux jonctions des segments
    fade_len = int(sr * 0.010)
    fade_in = np.linspace(0.0, 1.0, fade_len).reshape(-1, 1)
    fade_out = np.linspace(1.0, 0.0, fade_len).reshape(-1, 1)

    active_intervals = []
    prev_end = 0.0
    for s_start, s_end in silences:
        if s_start > prev_end:
            active_intervals.append((prev_end, s_start))
        prev_end = s_end
    if prev_end < total_dur:
        active_intervals.append((prev_end, total_dur))

    cut_audio_chunks = []
    for s_act, e_act in active_intervals:
        idx_s = int(s_act * sr)
        idx_e = min(total_samples, int(e_act * sr))
        if idx_e <= idx_s:
            continue
        chunk = audio[idx_s:idx_e].copy()
        if len(active_intervals) > 1:
            if idx_s > 0 and len(chunk) > fade_len * 2:
                chunk[:fade_len] *= fade_in
            if idx_e < total_samples and len(chunk) > fade_len * 2:
                chunk[-fade_len:] *= fade_out
        cut_audio_chunks.append(chunk)

    if cut_audio_chunks:
        final_audio = np.concatenate(cut_audio_chunks, axis=0)
    else:
        final_audio = audio

    final_dur = len(final_audio) / sr

    # Recalcul mathématique des timestamps de chaque mot
    def map_old_to_new(t):
        removed = 0.0
        for s, e in silences:
            if t >= e:
                removed += (e - s)
            elif t > s:
                removed += (t - s)
                break
            else:
                break
        return max(0.0, t - removed)

    for w in words:
        w["start"] = round(map_old_to_new(w["start"]), 3)
        w["end"] = round(map_old_to_new(w["end"]), 3)

    # Sauvegarde de l'audio dynamique coupé
    out_audio = np.clip(final_audio, -32767.0, 32767.0).astype(np.int16)
    with wave.open(voix_path, "wb") as wf:
        wf.setnchannels(nc)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sr)
        wf.writeframes(out_audio.tobytes())

    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2, ensure_ascii=False)

    print(f"✓ Audio compacté chirurgicalement : {final_dur:.2f}s (gain de {total_dur - final_dur:.2f}s).")
    return words, final_dur

def step3_build_timeline(words, total_audio_dur, timeline_path="timeline.js"):
    print("[3/3] C) Génération des 35 scènes sur-mesure dans timeline.js...")

    # Mots terminaux des 35 scènes
    scene_end_words = [
        "vidéo",             # 1
        "prix.",             # 2
        "moment,",           # 3
        "Pro",               # 4
        "Kling,",            # 5
        "code.",             # 6
        "moteur",            # 7
        "JavaScript.",       # 8
        "simple,",           # 9
        "téléphone,",        # 10
        "silences",          # 11
        "milliseconde.",     # 12
        "scène,",            # 13
        "l'émotion,",        # 14
        "terminaux,",        # 15
        "structurées,",      # 16
        "losanges",          # 17
        "cercles,",          # 18
        "FFmpeg",            # 19
        "seconde.",          # 20
        "révolution",        # 21
        "entrepreneurs ?",   # 22
        "fortune,",          # 23
        "visuelles",         # 24
        "corriger.",         # 25
        "complète",          # 26
        "générer",           # 27
        "euro.",             # 28
        "logiciel,",         # 29
        "offre",             # 30
        "caméra,",           # 31
        "automatisé.",       # 32
        "avatar",            # 33
        "graphique,",        # 34
        "privé."             # 35
    ]

    # Données exactes des 35 scènes demandées (Charte AGENT404 // CYBER-MINT)
    scenes_configs = [
        # Scène 1 (Douleur)
        {"type": "face", "data": {"avatar": "assets/avatars/stop.png", "label": "STOP AUX MONTEURS 🛑", "bg": "alert"}},
        # Scène 2 (Douleur)
        {"type": "big", "data": {"text": "💸 HORS DE PRIX", "sub": "FACTURES IA EXPLOSÉES", "bg": "alert"}},
        # Scène 3
        {"type": "face", "data": {"avatar": "assets/avatars/pointing.png", "label": "CETTE VIDÉO 👇", "bg": "grid"}},
        # Scène 4
        {"type": "cards", "data": {"cards": [{"icon": "🎬", "title": "PREMIERE PRO", "sub": "ZÉRO MONTAGE MANUEL ❌"}], "bg": "grid"}},
        # Scène 5
        {"type": "cards", "data": {"cards": [{"icon": "🤖", "title": "VEO / KLING", "sub": "AUCUNE IA VIDÉO ❌"}, {"icon": "🚫", "title": "ZÉRO PROMPT", "sub": "AUCUN ARTEFACT VISUEL"}], "bg": "grid"}},
        # Scène 6 (Puissance)
        {"type": "big", "data": {"text": "100% CODE", "sub": "GÉNÉRÉ PAR ALGORITHME ⚡", "bg": "mint"}},
        # Scène 7
        {"type": "face", "data": {"avatar": "assets/avatars/laptop.png", "label": "MOTEUR SUR-MESURE 💻", "bg": "grid"}},
        # Scène 8 : NOUVEAU COMPOSANT ENGINE ARCH
        {"type": "engine_arch", "data": {"bg": "grid"}},
        # Scène 9
        {"type": "face", "data": {"avatar": "assets/avatars/idea.png", "label": "ULTRA SIMPLE 💡", "bg": "grid"}},
        # Scène 10
        {"type": "face", "data": {"avatar": "assets/avatars/mic.png", "label": "1. MÉMO VOCAL 📱", "bg": "grid"}},
        # Scène 11
        {"type": "audio_wave", "data": {"title": "vocal1.m4a — NETTOYAGE STUDIO", "sub": "✂️ SILENCES SUPPRIMÉS AUTOMATIQUEMENT", "bg": "grid"}},
        # Scène 12 : NOUVEAU COMPOSANT SYNC TIMER
        {"type": "sync_timer", "data": {"bg": "grid"}},
        # Scène 13
        {"type": "big", "data": {"text": "MISE EN SCÈNE", "sub": "100% PILOTÉE PAR LE CODE 🎬", "bg": "grid"}},
        # Scène 14 : NOUVEAU COMPOSANT EMOTION MORPH
        {"type": "emotion_morph", "data": {"bg": "grid"}},
        # Scène 15 : TERMINAL AGENT404
        {"type": "window", "data": {"title": "agent404_terminal.sh", "lines": ["$ ./agent404 --deploy-matrix", "✓ Protocole Cyber-Mint #00F5A0", "✓ Système 100% Anonyme : ACTIF"], "bg": "grid"}},
        # Scène 16
        {"type": "list", "data": {"header": "COMPOSANTS DYNAMIQUES", "items": ["1. Terminaux & Code", "2. Listes à rebond", "3. Cartes & Comparatifs"], "bg": "grid"}},
        # Scène 17 (Losanges Cyber-Mint)
        {"type": "big", "data": {"text": "◆ LOSANGES ◆", "sub": "CHANGEMENT DE DÉCOR EN DIRECT", "bg": "diamonds"}},
        # Scène 18 (Cercles Cyber-Mint)
        {"type": "big", "data": {"text": "● CERCLES ●", "sub": "ANIMATION HAUTE VITESSE", "bg": "circles"}},
        # Scène 19 : NOUVEAU COMPOSANT FFMPEG RENDER
        {"type": "ffmpeg_render", "data": {"bg": "grid"}},
        # Scène 20 (Puissance)
        {"type": "big", "data": {"text": "30 FPS", "sub": "1080x1920 FULL HD FLUIDE 🔥", "bg": "mint"}},
        # Scène 21
        {"type": "face", "data": {"avatar": "assets/avatars/shock.png", "label": "UNE RÉVOLUTION 🚀", "bg": "grid"}},
        # Scène 22
        {"type": "cards", "data": {"cards": [{"icon": "💻", "title": "FONDATEURS SAAS", "sub": "DÉMOS PRODUIT & ONBOARDING"}, {"icon": "📈", "title": "ENTREPRENEURS", "sub": "CONTENU B2B QUOTIDIEN"}], "bg": "grid"}},
        # Scène 23 (Douleur)
        {"type": "face", "data": {"avatar": "assets/avatars/skeptic.png", "label": "IA VIDÉO = RUINEUX 💸", "bg": "alert"}},
        # Scène 24 (Douleur)
        {"type": "list", "data": {"header": "PROBLÈMES DES IA VIDÉO ❌", "items": ["❌ Visages & mains déformés", "❌ Texte illisible à l'écran", "❌ Impossible à modifier"], "bg": "alert"}},
        # Scène 25 (Douleur)
        {"type": "face", "data": {"avatar": "assets/avatars/stop.png", "label": "DES HEURES PERDUES ⏳", "bg": "alert"}},
        # Scène 26
        {"type": "split", "data": {"leftTitle": "IA / MONTEUR ❌", "leftItems": ["3h de montage", "50€ à 150€ / vidéo", "Aléatoire"], "rightTitle": "CODE PYTHON ✅", "rightItems": ["Prêt en 2 min", "Coût : 0,00 €", "Sur-mesure"], "bg": "grid"}},
        # Scène 27 : NOUVEAU COMPOSANT SPEED COUNTER
        {"type": "speed_counter", "data": {"bg": "grid"}},
        # Scène 28
        {"type": "face", "data": {"avatar": "assets/avatars/money.png", "label": "COÛT MARGINAL : 0,00 € 🔥", "bg": "diamonds"}},
        # Scène 29
        {"type": "cards", "data": {"cards": [{"icon": "⚡", "title": "1. TON LOGICIEL", "sub": "DÉMOS PRODUIT ULTRA CLAIRES"}], "bg": "grid"}},
        # Scène 30
        {"type": "cards", "data": {"cards": [{"icon": "⚡", "title": "1. TON LOGICIEL", "sub": "DÉMOS PRODUIT ULTRA CLAIRES"}, {"icon": "🎯", "title": "2. TON OFFRE B2B", "sub": "VIDÉOS DE VENTE QUI CONVERTISSENT"}], "bg": "grid"}},
        # Scène 31
        {"type": "face", "data": {"avatar": "assets/avatars/scissors.png", "label": "SANS CAMÉRA • 100% RÉGULIER 🎥", "bg": "grid"}},
        # Scène 32 (Puissance)
        {"type": "big", "data": {"text": "100% AUTOMATISÉ", "sub": "PIPELINE VIDÉO CLÉ EN MAIN ⚙️", "bg": "mint"}},
        # Scène 33
        {"type": "face", "data": {"avatar": "assets/avatars/prof.png", "label": "TON AVATAR SUR-MESURE 👔", "bg": "grid"}},
        # Scène 34
        {"type": "face", "data": {"avatar": "assets/avatars/pointing.png", "label": "TA CHARTE GRAPHIQUE 🎨", "bg": "diamonds"}},
        # Scène 35 (CTA Agent404)
        {"type": "big", "data": {"text": "ENVOIE « CODE »", "sub": "EN DM À @AGENT404 📩", "bg": "circles"}}
    ]

    scenes = []
    cur_word_idx = 0
    num_scenes = len(scenes_configs)

    for i in range(num_scenes):
        cfg = scenes_configs[i]
        end_w = scene_end_words[i]

        start_word_idx = cur_word_idx
        while cur_word_idx < len(words) and words[cur_word_idx]["word"] != end_w:
            cur_word_idx += 1

        end_word_idx = cur_word_idx
        cur_word_idx += 1

        # Timestamps avec continuité parfaite
        if i == 0:
            sc_start = 0.0
        else:
            sc_start = scenes[i - 1]["end"]

        if i == num_scenes - 1:
            sc_end = max(words[-1]["end"], round(total_audio_dur, 3))
        else:
            sc_end = words[end_word_idx]["end"]

        scenes.append({
            "id": f"scene_{i + 1:02d}",
            "type": cfg["type"],
            "start": round(sc_start, 3),
            "end": round(sc_end, 3),
            "data": cfg["data"]
        })

    # Export JS
    js_content = f"// TIMELINE VIDÉO PROGRAMMATIQUE SUR-MESURE (35 SCÈNES)\n"
    js_content += f"// Généré automatiquement par build_master_timeline.py\n\n"
    js_content += f"window.WORDS = {json.dumps(words, indent=2, ensure_ascii=False)};\n\n"
    js_content += f"window.SCENES = {json.dumps(scenes, indent=2, ensure_ascii=False)};\n"

    with open(timeline_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"✓ 35 scènes générées dans {timeline_path} sans aucun trou temporel.")

def main():
    words = step1_fuse_and_correct("words.json")
    words, total_dur = step2_rms_silence_cut(words, "voix.wav")
    step3_build_timeline(words, total_dur, "timeline.js")
    print("✓ build_master_timeline.py terminé avec succès.")

if __name__ == "__main__":
    main()
