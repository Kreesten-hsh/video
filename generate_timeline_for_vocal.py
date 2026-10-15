import json
from pathlib import Path

def build_timeline():
    with open("words.json", "r", encoding="utf-8") as f:
        words = json.load(f)

    total_duration = words[-1]["end"] + 0.4
    print(f"Total words: {len(words)}, Duration: {total_duration:.2f}s")

    # Définition des repères sémantiques basés sur les mots clés du script
    # Chaque section définit le mot déclencheur approximatif ou le timestamp visé
    cue_points = [
        # 1. Accroche
        {"target_word": "Arrête", "type": "face", "data": {"avatar": "assets/avatars/stop.png", "label": "ARRÊTE DE PAYER", "bg": "red"}},
        {"target_word": "montés", "type": "big", "data": {"text": "MONTEURS CHERS", "sub": "350€ À 1500€", "bg": "red"}},
        {"target_word": "vidéo", "type": "face", "data": {"avatar": "assets/avatars/money.png", "label": "IA HORS DE PRIX", "bg": "grid"}},
        {"target_word": "regardes", "type": "face", "data": {"avatar": "assets/avatars/pointing.png", "label": "REGARDE BIEN", "bg": "diamonds"}},
        {"target_word": "premier", "type": "cards", "data": {"cards": [{"icon": "❌", "title": "PREMIERE"}, {"icon": "❌", "title": "IA VEO/KLING"}], "bg": "grid"}},
        {"target_word": "100", "type": "big", "data": {"text": "100% CODE", "sub": "ZÉRO MONTAGE", "bg": "red"}},
        
        # 2. Explication technique
        {"target_word": "codé", "type": "face", "data": {"avatar": "assets/avatars/laptop.png", "label": "DEV SENIOR", "bg": "grid"}},
        {"target_word": "pittant", "type": "window", "data": {"title": "video_engine.py", "text": "$ python render.py\n> Stack: Python + Playwright\n> Zero React / Zero Remotion\n> Memory Pipe -> FFmpeg", "bg": "circles"}},
        {"target_word": "simple", "type": "list", "data": {"items": ["1. AUDIO VOCAL PHONE", "2. SILENCE REMOVAL", "3. WHISPER MOT À MOT"], "bg": "diamonds"}},
        {"target_word": "téléphone", "type": "face", "data": {"avatar": "assets/avatars/mic.png", "label": "DICTAPHONE TÉL", "bg": "grid"}},
        {"target_word": "coupe", "type": "face", "data": {"avatar": "assets/avatars/scissors.png", "label": "CUT SILENCES", "bg": "grid"}},
        {"target_word": "transcrit", "type": "cards", "data": {"cards": [{"icon": "⚡", "title": "FASTER-WHISPER"}, {"icon": "⏱️", "title": "TIMESTAMPS"}], "bg": "circles"}},
        
        # 3. Mise en scène automatique
        {"target_word": "Ensuite", "type": "face", "data": {"avatar": "assets/avatars/idea.png", "label": "AUTOMATISATION", "bg": "grid"}},
        {"target_word": "avatar", "type": "face", "data": {"avatar": "assets/avatars/shock.png", "label": "STICKERS DYNAMIQUES", "bg": "diamonds"}},
        {"target_word": "théminos", "type": "window", "data": {"title": "terminal@dev", "text": "$ ffmpeg -i pipe:0\n> libx264 yuv420p\n> 30 FPS FLUIDE", "bg": "grid"}},
        {"target_word": "structurés", "type": "list", "data": {"items": ["• AVATARS STICKERS", "• MACHINE À ÉCRIRE", "• SOUS-TITRES DYNAMIQUES"], "bg": "grid"}},
        {"target_word": "rosenge", "type": "cards", "data": {"cards": [{"icon": "🔷", "title": "DIAMONDS"}, {"icon": "⚪", "title": "CIRCLES"}, {"icon": "🟥", "title": "RED IMPACT"}, {"icon": "📐", "title": "GRID"}], "bg": "diamonds"}},
        {"target_word": "ffmp", "type": "big", "data": {"text": "FFMPEG 30 FPS", "sub": "PIPE RAM DIRECT", "bg": "red"}},
        
        # 4. Pourquoi c'est une révolution B2B
        {"target_word": "résolution", "type": "face", "data": {"avatar": "assets/avatars/prof.png", "label": "RÉVOLUTION SAAS", "bg": "grid"}},
        {"target_word": "entrepreneurs", "type": "cards", "data": {"cards": [{"icon": "🚀", "title": "FONDATEURS SAAS"}, {"icon": "💼", "title": "ENTREPRENEURS"}], "bg": "circles"}},
        {"target_word": "fortune", "type": "face", "data": {"avatar": "assets/avatars/skeptic.png", "label": "TROP CHER ?", "bg": "diamonds"}},
        {"target_word": "visuels", "type": "big", "data": {"text": "STOP ERREURS", "sub": "HALLUCINATIONS IA", "bg": "red"}},
        {"target_word": "corriger", "type": "face", "data": {"avatar": "assets/avatars/stop.png", "label": "PERTE DE TEMPS", "bg": "grid"}},
        {"target_word": "minutes", "type": "big", "data": {"text": "2 MINUTES", "sub": "GÉNÉRATION ÉCLAIR", "bg": "red"}},
        {"target_word": "euros", "type": "face", "data": {"avatar": "assets/avatars/happy.png", "label": "0€ DE COÛT", "bg": "grid"}},
        
        # 5. Cas d'usage et Call to action
        {"target_word": "expliquant", "type": "window", "data": {"title": "saas-app.com", "text": "DEMO LOGICIEL\n> Taux de conversion : +45%\n> Engagement x3", "bg": "circles"}},
        {"target_word": "caméra", "type": "face", "data": {"avatar": "assets/avatars/laptop.png", "label": "ZÉRO CAMÉRA", "bg": "diamonds"}},
        {"target_word": "automatiques", "type": "rpg", "data": {"zone": "PRODUCTION B2B", "quest": "100K VUES", "illustration": "🏆", "speaker": "KREESTEN", "mini_avatar": "assets/avatars/mini.png", "text": "Tout est 100% automatisé par du code.", "bg": "grid"}},
        {"target_word": "système", "type": "face", "data": {"avatar": "assets/avatars/pointing.png", "label": "POUR TON BIZ", "bg": "grid"}},
        {"target_word": "graphique", "type": "cards", "data": {"cards": [{"icon": "🎨", "title": "TON AVATAR"}, {"icon": "📐", "title": "TA CHARTE"}], "bg": "circles"}},
        {"target_word": "accord", "type": "big", "data": {"text": "ENVOIE 'CODE'", "sub": "EN MESSAGE PRIVÉ", "bg": "red"}},
        {"target_word": "privé.", "type": "face", "data": {"avatar": "assets/avatars/pointing.png", "label": "DM MAINTENANT", "bg": "grid"}}
    ]

    # Trouver les index de mots correspondants dans words
    scenes = []
    current_word_idx = 0

    for i, cp in enumerate(cue_points):
        target = cp["target_word"].lower()
        found_idx = -1
        for w_idx in range(current_word_idx, len(words)):
            if target in words[w_idx]["word"].lower():
                found_idx = w_idx
                break
        
        if found_idx != -1:
            start_t = words[found_idx]["start"]
            current_word_idx = found_idx + 1
        else:
            # Fallback temporel linéaire
            start_t = (i / len(cue_points)) * (total_duration - 2.0)

        # Si c'est la première scène, start = 0.0
        if i == 0:
            start_t = 0.0
        
        # Ajuste la fin de la scène précédente
        if scenes:
            scenes[-1]["end"] = round(start_t, 3)
            # Garantir un minimum de 1.2s par scène
            if scenes[-1]["end"] - scenes[-1]["start"] < 1.2:
                scenes[-1]["end"] = round(scenes[-1]["start"] + 1.2, 3)
                start_t = scenes[-1]["end"]

        scenes.append({
            "start": round(start_t, 3),
            "end": round(start_t + 2.0, 3),
            "type": cp["type"],
            "data": cp["data"]
        })

    # Dernière scène : fin = fin du dernier mot + 0.5s
    scenes[-1]["end"] = round(total_duration, 3)

    # Vérification stricte de la continuité absolue (Rule 1)
    scenes[0]["start"] = 0.0
    for idx in range(1, len(scenes)):
        scenes[idx]["start"] = scenes[idx - 1]["end"]
        # Vérifier durée
        if scenes[idx]["end"] <= scenes[idx]["start"]:
            scenes[idx]["end"] = round(scenes[idx]["start"] + 1.5, 3)

    scenes[-1]["end"] = round(total_duration, 3)

    print(f"Génération de {len(scenes)} scènes parfaitement continues.")

    timeline_content = (
        f"// timeline.js - Synchronisation automatique pour vocal1.m4a\n"
        f"window.WORDS = {json.dumps(words, ensure_ascii=False, indent=2)};\n\n"
        f"window.SCENES = {json.dumps(scenes, ensure_ascii=False, indent=2)};\n"
    )

    with open("timeline.js", "w", encoding="utf-8") as f:
        f.write(timeline_content)

    print("✓ timeline.js écrit avec succès !")

if __name__ == "__main__":
    build_timeline()
