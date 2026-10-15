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

def setup_demo_assets():
    """Génère des images vectorielles d'avatars de test pour les composants face et rpg."""
    os.makedirs("assets/avatars", exist_ok=True)
    
    def create_svg(path, text, bg_color):
        svg = f"""<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="360" height="360" fill="{bg_color}" stroke="#000" stroke-width="16" rx="40"/>
            <circle cx="150" cy="150" r="28" fill="#000"/>
            <circle cx="250" cy="150" r="28" fill="#000"/>
            <path d="M 120 260 Q 200 320 280 260" stroke="#000" stroke-width="20" fill="none" stroke-linecap="round"/>
            <text x="200" y="360" font-family="sans-serif" font-weight="900" font-size="32" text-anchor="middle" fill="#000">{text}</text>
        </svg>"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)

    create_svg("assets/avatars/pointing.svg", "POINTING", "#FFE600")
    create_svg("assets/avatars/speaking.svg", "SPEAKING", "#2BD980")
    create_svg("assets/avatars/mini.svg", "DEV", "#E63926")

def generate_test_audio():
    """Génère une piste audio de test de 10 secondes (voix.wav)."""
    print("[Demo] Génération de l'audio test de 10s (voix.wav)...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "sine=frequency=440:duration=10",
        "-af", "volume=0.2",
        "voix.wav"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_timeline_data():
    """Génère words.json et timeline.js avec les 6 composants et fonds dynamiques."""
    words = [
        {"word": "Bienvenue", "start": 0.2, "end": 0.8},
        {"word": "dans", "start": 0.8, "end": 1.1},
        {"word": "ce", "start": 1.1, "end": 1.4},
        {"word": "moteur", "start": 1.4, "end": 1.9},
        {"word": "vidéo", "start": 1.9, "end": 2.5},
        {"word": "100%", "start": 2.5, "end": 3.1},
        {"word": "code,", "start": 3.1, "end": 3.6},
        {"word": "sans", "start": 3.6, "end": 4.1},
        {"word": "aucun", "start": 4.1, "end": 4.6},
        {"word": "framework", "start": 4.6, "end": 5.2},
        {"word": "lourd,", "start": 5.2, "end": 5.8},
        {"word": "avec", "start": 5.8, "end": 6.3},
        {"word": "performance", "start": 6.3, "end": 7.2},
        {"word": "maximale", "start": 7.2, "end": 8.0},
        {"word": "et", "start": 8.0, "end": 8.4},
        {"word": "style", "start": 8.4, "end": 9.0},
        {"word": "néo-brutaliste.", "start": 9.0, "end": 9.8}
    ]

    scenes = [
        {
            "start": 0.0,
            "end": 1.8,
            "type": "big",
            "data": {
                "text": "100% CODE",
                "sub": "ZÉRO REACT",
                "bg": "grid"
            }
        },
        {
            "start": 1.8,
            "end": 3.5,
            "type": "face",
            "data": {
                "avatar": "assets/avatars/pointing.svg",
                "label": "DEV SENIOR",
                "bg": "circles"
            }
        },
        {
            "start": 3.5,
            "end": 5.2,
            "type": "window",
            "data": {
                "title": "terminal@host: ~",
                "text": "$ python render.py --fps 30\n> Pipeline mémoire Playwright -> FFmpeg\n> Status: 100% FLUIDE [OK]",
                "bg": "diamonds"
            }
        },
        {
            "start": 5.2,
            "end": 7.0,
            "type": "cards",
            "data": {
                "cards": [
                    {"icon": "⚡", "title": "30 FPS"},
                    {"icon": "✂️", "title": "WHISPER"},
                    {"icon": "🎞️", "title": "FFMPEG"},
                    {"icon": "🎨", "title": "BRUTAL"}
                ],
                "bg": "grid"
            }
        },
        {
            "start": 7.0,
            "end": 8.5,
            "type": "list",
            "data": {
                "items": [
                    "Silence Removal",
                    "Whisper Timestamps",
                    "Headless Memory Pipe"
                ],
                "bg": "red"
            }
        },
        {
            "start": 8.5,
            "end": 10.0,
            "type": "rpg",
            "data": {
                "zone": "PRODUCTION",
                "quest": "TIKTOK REELS",
                "illustration": "🏆",
                "speaker": "ARCHITECT",
                "mini_avatar": "assets/avatars/mini.svg",
                "text": "Le rendu vidéo headless est prêt !",
                "bg": "grid"
            }
        }
    ]

    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2, ensure_ascii=False)

    timeline_js_content = (
        f"// Données générées automatiquement\n"
        f"window.WORDS = {json.dumps(words, ensure_ascii=False, indent=2)};\n\n"
        f"window.SCENES = {json.dumps(scenes, ensure_ascii=False, indent=2)};\n"
    )
    with open("timeline.js", "w", encoding="utf-8") as f:
        f.write(timeline_js_content)

    print("✓ Données écrites dans words.json et timeline.js (video.js préservé)")

def main():
    setup_demo_assets()
    generate_test_audio()
    generate_timeline_data()
    print("\n[Demo] Démarrage du rendu vidéo de test...")
    import render
    render.render_video()

if __name__ == "__main__":
    main()
