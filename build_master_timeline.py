import os
import sys
import re
import json
import wave
import shutil
import subprocess
from pathlib import Path

# Ajout dynamique du répertoire bin local du dépôt au PATH si présent
_local_bin = str(Path(__file__).parent.resolve() / "bin")
_path_elements = os.environ.get("PATH", "").split(os.pathsep) if os.environ.get("PATH") else []
if _local_bin not in _path_elements and Path(_local_bin).is_dir():
    _path_elements.insert(0, _local_bin)
os.environ["PATH"] = os.pathsep.join(_path_elements)

import numpy as np

def validate_timeline(words, scenes, total_audio_dur, reference_words, scene_end_words):
    """
    Validation automatique rigoureuse de la timeline :
    1. Couverture stricte de la transcription (aucun mot inventé ou omis).
    2. Timestamps strictement chronologiques et start < end pour chaque mot.
    3. Bornes temporelles contenues dans la durée réelle audio.
    4. Exactement 35 scènes dans le bon ordre chronologique.
    5. Chaque mot terminal de scène correspond exactement au repère textuel.
    6. Continuité parfaite des scènes : aucun trou, aucun chevauchement.
    7. Durée finale cohérente avec l'audio réel.
    """
    print("\n--- [CONTRÔLES AUTOMATIQUES DE VALIDATION TEMPORELLE] ---")
    
    # 1. Vérification du nombre et contenu des mots
    if len(words) != len(reference_words):
        raise ValueError(
            f"ÉCHEC VALIDATION : Nombre de mots ({len(words)}) différent de la référence ({len(reference_words)})."
        )
    for idx, (w, ref_w) in enumerate(zip(words, reference_words)):
        if w["word"] != ref_w:
            raise ValueError(f"ÉCHEC VALIDATION : Mot {idx} '{w['word']}' ne correspond pas à la référence '{ref_w}'.")
        s = float(w["start"])
        e = float(w["end"])
        if s >= e:
            raise ValueError(f"ÉCHEC VALIDATION : Mot {idx} '{w['word']}' invalide (start {s:.3f} >= end {e:.3f}).")
        if s < 0.0 or e > total_audio_dur + 0.15:
            raise ValueError(
                f"ÉCHEC VALIDATION : Mot {idx} '{w['word']}' [{s:.3f}s -> {e:.3f}s] hors bornes audio [0, {total_audio_dur:.3f}s]."
            )
        if idx > 0:
            prev_s = float(words[idx - 1]["start"])
            if s < prev_s:
                raise ValueError(
                    f"ÉCHEC VALIDATION : Décalage non-chronologique mot {idx} '{w['word']}' (start {s:.3f} < {prev_s:.3f})."
                )

    print(f"✓ {len(words)} mots validés : ordre strictement chronologique, bornés [0.0s, {total_audio_dur:.2f}s].")

    # 2. Vérification des 35 scènes
    if len(scenes) != 35:
        raise ValueError(f"ÉCHEC VALIDATION : {len(scenes)} scènes trouvées au lieu des 35 attendues.")

    for i, sc in enumerate(scenes):
        sc_s = float(sc["start"])
        sc_e = float(sc["end"])
        if sc_s >= sc_e:
            raise ValueError(f"ÉCHEC VALIDATION : Scène {sc['id']} durée invalide [{sc_s:.3f}s -> {sc_e:.3f}s].")
        if i == 0:
            if sc_s != 0.0:
                raise ValueError(f"ÉCHEC VALIDATION : La scène 1 doit débuter à 0.0s (trouvé: {sc_s}s).")
        else:
            prev_e = float(scenes[i - 1]["end"])
            if abs(sc_s - prev_e) > 0.001:
                raise ValueError(
                    f"ÉCHEC VALIDATION : Rupture de continuité entre scène {i} ({prev_e:.3f}s) et scène {i+1} ({sc_s:.3f}s)."
                )

    final_sc_end = float(scenes[-1]["end"])
    if abs(final_sc_end - total_audio_dur) > 0.1:
        raise ValueError(
            f"ÉCHEC VALIDATION : Fin de la timeline ({final_sc_end:.3f}s) divergente de la durée audio ({total_audio_dur:.3f}s)."
        )

    print(f"✓ 35 scènes validées sans aucun trou ni chevauchement (durée totale : {final_sc_end:.3f}s).")

    # 3. Rapport de diagnostic lisible
    print("\n--- [RAPPORT DE DIAGNOSTIC DE SYNCHRONISATION DES 35 SCÈNES] ---")
    print(f"{'Scène':<10} | {'Début':<8} | {'Fin':<8} | {'Durée':<7} | {'Mot Terminal':<18} | {'Type':<14} | {'Décor'}")
    print("-" * 88)
    for i, sc in enumerate(scenes):
        sc_s = float(sc["start"])
        sc_e = float(sc["end"])
        dur = sc_e - sc_s
        end_w = scene_end_words[i]
        sc_type = sc["type"]
        sc_bg = sc["data"].get("bg", "default")
        print(f"{sc['id']:<10} | {sc_s:6.3f}s  | {sc_e:6.3f}s  | {dur:5.2f}s  | {end_w:<18} | {sc_type:<14} | {sc_bg}")
    print("-" * 88 + "\n")

def step3_build_timeline(words, total_audio_dur, timeline_path="timeline.js"):
    print("[3/3] C) Génération des 35 scènes synchronisées dans timeline.js...")

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

    # Découpage strict et garanti des tranches de mots pour chaque scène
    scene_slices = []
    cur_idx = 0
    num_scenes = len(scenes_configs)
    for i, end_w in enumerate(scene_end_words):
        start_idx = cur_idx
        while cur_idx < len(words) and words[cur_idx]["word"] != end_w:
            cur_idx += 1
        if cur_idx >= len(words):
            raise ValueError(f"ERREUR : Mot terminal '{end_w}' introuvable pour la scène {i + 1}.")
        end_idx = cur_idx
        cur_idx += 1
        scene_slices.append((start_idx, end_idx))

    # Construction des scènes avec synchronisation exacte sur l'amorce du discours
    scenes = []
    for i in range(num_scenes):
        cfg = scenes_configs[i]
        s_idx, e_idx = scene_slices[i]

        # La scène débute exactement au premier mot prononcé de son sujet
        if i == 0:
            sc_start = 0.0
        else:
            sc_start = words[s_idx]["start"]

        # La scène se termine exactement à l'amorce du sujet suivant (ou fin de fichier)
        if i == num_scenes - 1:
            sc_end = max(words[-1]["end"], round(total_audio_dur, 3))
        else:
            next_s_idx = scene_slices[i + 1][0]
            sc_end = words[next_s_idx]["start"]

        scenes.append({
            "id": f"scene_{i + 1:02d}",
            "type": cfg["type"],
            "start": round(sc_start, 3),
            "end": round(sc_end, 3),
            "data": cfg["data"]
        })

    # Contrôles automatiques obligatoires avant écriture
    validate_timeline(words, scenes, total_audio_dur, REFERENCE_WORDS, scene_end_words)

    # Export JS
    js_content = f"// TIMELINE VIDÉO PROGRAMMATIQUE SUR-MESURE (35 SCÈNES)\n"
    js_content += f"// Généré automatiquement par build_master_timeline.py\n\n"
    js_content += f"window.WORDS = {json.dumps(words, indent=2, ensure_ascii=False)};\n\n"
    js_content += f"window.SCENES = {json.dumps(scenes, indent=2, ensure_ascii=False)};\n"

    with open(timeline_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"✓ 35 scènes validées et exportées dans {timeline_path}.")

# Transcription de référence validée (220 mots)
REFERENCE_WORDS = [
    # Phrase 1: [excited] Arrête de payer des monteurs vidéo et des IA hors de prix.
    "Arrête", "de", "payer", "des", "monteurs", "vidéo", "et", "des", "IA", "hors", "de", "prix.",
    # Phrase 2: [short pause] Cette vidéo que tu regardes en ce moment, je ne l'ai pas montée sur Premiere Pro et je n'ai pas utilisé une IA vidéo comme Veo ou Kling, elle est générée à 100% par du code.
    "Cette", "vidéo", "que", "tu", "regardes", "en", "ce", "moment,", "je", "ne", "l'ai", "pas", "montée", "sur", "Premiere", "Pro", "et", "je", "n'ai", "pas", "utilisé", "une", "IA", "vidéo", "comme", "Veo", "ou", "Kling,", "elle", "est", "générée", "à", "100%", "par", "du", "code.",
    # Phrase 3: [thoughtful] En fait, j'ai codé mon propre moteur en Python et JavaScript.
    "En", "fait,", "j'ai", "codé", "mon", "propre", "moteur", "en", "Python", "et", "JavaScript.",
    # Phrase 4: [happy] Le principe est ultra simple : j'enregistre ma voix sur mon téléphone, mon script coupe automatiquement tous les silences et transcrit chaque mot à la milliseconde.
    "Le", "principe", "est", "ultra", "simple,", "j'enregistre", "ma", "voix", "sur", "mon", "téléphone,", "mon", "script", "coupe", "automatiquement", "tous", "les", "silences", "et", "transcrit", "chaque", "mot", "à", "la", "milliseconde.",
    # Phrase 5: [energetic] Ensuite, le code génère toute la mise en scène : il anime mon avatar en costume selon l'émotion, il ouvre les terminaux, il affiche des listes structurées, et change le décor en losanges ou en cercles, et il compile tout avec FFmpeg à 30 images par seconde.
    "Ensuite,", "le", "code", "génère", "toute", "la", "mise", "en", "scène,", "il", "anime", "mon", "avatar", "en", "costume", "selon", "l'émotion,", "il", "ouvre", "les", "terminaux,", "il", "affiche", "des", "listes", "structurées,", "et", "change", "le", "décor", "en", "losanges", "ou", "en", "cercles,", "et", "il", "compile", "tout", "avec", "FFmpeg", "à", "30", "images", "par", "seconde.",
    # Phrase 6: [thoughtful] Pourquoi c'est une révolution pour les fondateurs SaaS et les entrepreneurs ?
    "Pourquoi", "c'est", "une", "révolution", "pour", "les", "fondateurs", "SaaS", "et", "les", "entrepreneurs ?",
    # Phrase 7: [sighs] Parce que les IA vidéo classiques coûtent une fortune, font des erreurs visuelles et prennent des heures à corriger.
    "Parce", "que", "les", "IA", "vidéo", "classiques", "coûtent", "une", "fortune,", "font", "des", "erreurs", "visuelles", "et", "prennent", "des", "heures", "à", "corriger.",
    # Phrase 8: [excited] Avec du code, une vidéo complète me prend deux minutes à générer et coûte 0 euro.
    "Avec", "du", "code,", "une", "vidéo", "complète", "me", "prend", "deux", "minutes", "à", "générer", "et", "coûte", "0", "euro.",
    # Phrase 9: [persuasive] Que ce soit pour expliquer ton logiciel, présenter ton offre ou publier tous les jours sans jamais allumer ta caméra, tout est automatisé.
    "Que", "ce", "soit", "pour", "expliquer", "ton", "logiciel,", "présenter", "ton", "offre", "ou", "publier", "tous", "les", "jours", "sans", "jamais", "allumer", "ta", "caméra,", "tout", "est", "automatisé.",
    # Phrase 10: [whisper] Si tu veux que je déploie ce système avec ton propre avatar et ta charte graphique, envoie-moi « CODE » en message privé.
    "Si", "tu", "veux", "que", "je", "déploie", "ce", "système", "avec", "ton", "propre", "avatar", "et", "ta", "charte", "graphique,", "envoie-moi", "« CODE »", "en", "message", "privé."
]

def align_reference_audio(audio_mp3_path="assets/audio/agent404_voiceover.mp3", output_words_json="words.json", output_voix_wav="voix.wav"):
    """
    Alignement forcé déterministe et vérifié du texte de référence (220 mots)
    sur la voix off ElevenLabs exacte, sans fabrication ni interpolation artificielle.
    """
    import unicodedata

    if not os.path.exists(audio_mp3_path):
        raise FileNotFoundError(
            f"ERREUR CRITIQUE : La source audio de référence '{audio_mp3_path}' est introuvable. "
            "Le pipeline refuse de basculer silencieusement vers un ancien audio."
        )

    if not os.path.exists(output_voix_wav) or os.path.getmtime(audio_mp3_path) > os.path.getmtime(output_voix_wav):
        print(f"[Audio Reference] Conversion technique en PCM WAV : {output_voix_wav}...")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(audio_mp3_path),
            "-c:a", "pcm_s16le",
            "-ar", "44100",
            "-ac", "1",
            output_voix_wav
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    with wave.open(output_voix_wav, "rb") as wf:
        sr = wf.getframerate()
        nc = wf.getnchannels()
        sw = wf.getsampwidth()
        nframes = wf.getnframes()
        total_dur = nframes / sr

    print(f"[Audio Reference] Alignement acoustique forcé sur {output_voix_wav} ({total_dur:.2f}s @ {sr}Hz)...")
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
    segments, _ = model.transcribe(output_voix_wav, word_timestamps=True, language="fr", temperature=0.0)

    raw_words = []
    for s in segments:
        for w in s.words:
            clean = w.word.strip()
            if clean:
                raw_words.append({
                    "word": clean,
                    "start": round(w.start, 3),
                    "end": round(w.end, 3)
                })

    def strip_accents(text):
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

    def norm(s):
        s = strip_accents(s.lower())
        s = s.replace('œ', 'oe').replace('æ', 'ae')
        return re.sub(r'[^a-z0-9]', '', s)

    # Variantes phonétiques de transcription Whisper sans glissement lexical
    phonetic_map = {
        'prix': 'pris',
        'veo': 'vo',
        'losanges': 'losange',
        'cercles': 'cercle',
        'saas': 'sass',
        'classiques': 'classique',
        'code': 'code'
    }

    aligned_words = []
    r_idx = 0
    w_idx = 0
    n_ref = len(REFERENCE_WORDS)
    n_raw = len(raw_words)

    while r_idx < n_ref and w_idx < n_raw:
        rw = REFERENCE_WORDS[r_idx]
        ww = raw_words[w_idx]["word"]
        r_n = norm(rw)
        w_n = norm(ww)

        # 1. Ignorer les bruits purs / soupirs de respiration hors texte
        if w_n == '' or w_n in ['ah', 'euh']:
            w_idx += 1
            continue

        # 2. Cas spécifique des devises combinées : '0€.' dans Whisper pour ['0', 'euro.']
        if rw == '0' and r_idx + 1 < n_ref and 'euro' in REFERENCE_WORDS[r_idx + 1].lower() and '€' in ww:
            t_s = float(raw_words[w_idx]["start"])
            t_e = float(raw_words[w_idx]["end"])
            mid = round((t_s + t_e) / 2.0, 3)
            aligned_words.append({"word": REFERENCE_WORDS[r_idx], "start": t_s, "end": mid})
            aligned_words.append({"word": REFERENCE_WORDS[r_idx + 1], "start": mid, "end": t_e})
            r_idx += 2
            w_idx += 1
            continue

        # 3. Correspondance directe ou phonétique validée
        if r_n == w_n or phonetic_map.get(r_n) == w_n:
            aligned_words.append({
                "word": rw,
                "start": float(raw_words[w_idx]["start"]),
                "end": float(raw_words[w_idx]["end"])
            })
            r_idx += 1
            w_idx += 1
            continue

        # 4. Mots composés / contractions découpées par Whisper (ex: l'ai, j'ai, c'est, envoie-moi)
        if r_n.startswith(w_n):
            start_t = float(raw_words[w_idx]["start"])
            end_t = float(raw_words[w_idx]["end"])
            accum = w_n
            w_next = w_idx + 1
            while w_next < n_raw and len(accum) < len(r_n):
                next_norm = norm(raw_words[w_next]["word"])
                if next_norm == '':
                    end_t = max(end_t, float(raw_words[w_next]["end"]))
                    w_next += 1
                    continue
                accum += next_norm
                end_t = float(raw_words[w_next]["end"])
                w_next += 1

            if accum == r_n:
                aligned_words.append({
                    "word": rw,
                    "start": start_t,
                    "end": end_t
                })
                r_idx += 1
                w_idx = w_next
                continue

        # En cas de divergence non résolue, arrêt immédiat sans fabrication de timestamps
        context_ref = REFERENCE_WORDS[max(0, r_idx - 2):min(n_ref, r_idx + 3)]
        context_raw = [rw_item["word"] for rw_item in raw_words[max(0, w_idx - 2):min(n_raw, w_idx + 3)]]
        raise RuntimeError(
            f"ERREUR D'ALIGNEMENT ACOUSTIQUE : divergence stricte détectée à l'index {r_idx}.\n"
            f"  Mot référence attendu : '{rw}' (norm: '{r_n}')\n"
            f"  Token Whisper détecté : '{ww}' (norm: '{w_n}')\n"
            f"  Contexte référence   : {context_ref}\n"
            f"  Contexte Whisper     : {context_raw}\n"
            "Arrêt immédiat : le pipeline refuse d'inventer des timestamps."
        )

    # Règle absolue : aucun mot manquant n'est toléré
    if len(aligned_words) != n_ref:
        raise RuntimeError(
            f"ERREUR D'ALIGNEMENT ACOUSTIQUE : {len(aligned_words)}/{n_ref} mots alignés. "
            "Tous les mots de référence doivent correspondre à l'audio réel."
        )

    # Sauvegarde de words.json
    with open(output_words_json, "w", encoding="utf-8") as f:
        json.dump(aligned_words, f, indent=2, ensure_ascii=False)

    print(f"✓ Alignement forcé 100% réussi : {len(aligned_words)}/220 mots synchronisés dans {output_words_json}.")
    return aligned_words, total_dur

def main():
    print("=== PIPELINE VIDÉO PROGRAMMATIQUE AGENT404 (Master Audio) ===")
    words, total_dur = align_reference_audio(
        audio_mp3_path="assets/audio/agent404_voiceover.mp3",
        output_words_json="words.json",
        output_voix_wav="voix.wav"
    )
    step3_build_timeline(words, total_dur, "timeline.js")

    print(f"✓ build_master_timeline.py terminé avec succès ({total_dur:.2f}s).")

if __name__ == "__main__":
    main()
