#!/usr/bin/env python3
"""
AGENT404 : Générateur de Projet Vidéo Autonome (CLI Scaffolding Multi-Tenant).
Initialise une arborescence légère pour une nouvelle vidéo (studio_perso ou studio_clients) :
  - Respect strict des 5 règles du Gatekeeper dès l'initialisation
  - 100% zéro HUD, zéro #FF2A5F, zéro Cyber-Mint (#00F5A0, #0D1117)
  - Thème officiel Obsidian Flame (#FF4F18, fond beige #F5F2EB, encre #111111)
  - Scènes 100% basées sur les blueprints universels (bp_*)
  - Multi-tenant : les fichiers moteur (index.html, style.css, video.js) restent à la racine.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def load_video_memory():
    """Charge le registre d'unicité et jargon banni."""
    mem_path = REPO_ROOT / "registry" / "video_memory.json"
    if not mem_path.exists():
        return {
            "version": "1.0.0",
            "banned_global_jargon": [],
            "videos": []
        }
    try:
        with open(mem_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Warning] Impossible de lire {mem_path} : {e}")
        return {"banned_global_jargon": [], "videos": []}


def init_video_project(target: str, cta: str = "CLARTÉ", title: str = "", topic: str = "") -> dict:
    """Crée l'arborescence et les fichiers de données pour un nouveau projet vidéo multi-tenant."""
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = (REPO_ROOT / target_path).resolve()

    target_path.mkdir(parents=True, exist_ok=True)
    (target_path / "assets").mkdir(parents=True, exist_ok=True)

    video_id = target_path.name

    # Extraction du numéro de vidéo si présent dans le nom du dossier
    num_match = re.search(r"video_?(\d+)", video_id, re.IGNORECASE)
    video_number = int(num_match.group(1)) if num_match else 1

    if not title:
        title = f"Projet {video_id} - AGENT404"
    if not topic:
        topic = "Capsule B2B chirurgicale à forte rétention"

    cta_keyword = cta.upper().strip() if cta else "CLARTÉ"

    default_scenes = [
        {
            "id": "scene_01",
            "type": "bp_hook_question",
            "start": 0.0,
            "end": 4.5,
            "caption_mode": "center_slam",
            "avatar_mode": "hero",
            "params": {
                "box_color": "var(--tile-yellow)",
                "icon": "question",
                "title": "ARRÊTE DE PERDRE TES PROSPECTS",
                "subtitle": "Ton expertise reste invisible sans vidéo percutante.",
                "stamp_text": "HOOK",
                "avatar": "idea"
            }
        },
        {
            "id": "scene_02",
            "type": "bp_cta_conversion",
            "start": 4.5,
            "end": 9.0,
            "caption_mode": "single_line_top",
            "avatar_mode": "hero",
            "params": {
                "keyword": cta_keyword,
                "instruction": f"Commente {cta_keyword} sous ce post pour recevoir la méthode.",
                "badge_text": "ACTION",
                "avatar": "pointing"
            }
        }
    ]

    # 1. Génération de project.json
    project_data = {
        "title": title,
        "author": "AGENT404",
        "slug": video_id,
        "video_number": video_number,
        "format": "9:16",
        "fps": 30,
        "width": 1080,
        "height": 1920,
        "theme": "obsidian-flame",
        "load_project": True,
        "cta_keyword": cta_keyword,
        "topic": topic,
        "scenes": default_scenes
    }

    proj_json_path = target_path / "project.json"
    with open(proj_json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)

    # 2. Génération de brand.json
    brand_data = {
        "brand_name": "AGENT404",
        "theme": {
            "bg_canvas": "#F5F2EB",
            "surface_card": "#FFFFFF",
            "ink": "#111111",
            "accent_primary": "#FF4F18",
            "tile_1": "#FEF08A",
            "tile_2": "#BFDBFE",
            "tile_3": "#A7F3D0"
        },
        "typography": {
            "font_heading": "Montserrat",
            "font_body": "Inter",
            "font_mono": "JetBrains Mono"
        },
        "avatars": {
            "base_path": "assets/avatars/",
            "default": "idea.png",
            "poses": {
                "idea": "idea.png",
                "pointing": "pointing.png"
            }
        }
    }

    brand_json_path = target_path / "brand.json"
    with open(brand_json_path, "w", encoding="utf-8") as f:
        json.dump(brand_data, f, indent=2, ensure_ascii=False)

    # 3. Génération de scenes.json
    scenes_json_path = target_path / "scenes.json"
    with open(scenes_json_path, "w", encoding="utf-8") as f:
        json.dump(default_scenes, f, indent=2, ensure_ascii=False)

    # 4. Génération de timeline.js
    scenes_js_str = json.dumps(default_scenes, indent=2, ensure_ascii=False)
    timeline_js_content = f"""// TIMELINE DU PROJET {video_id}
// Conforme au moteur multi-tenant racine AGENT404

window.PROJECT_CONFIG = {{
  "video_id": "{video_id}",
  "cta_keyword": "{cta_keyword}",
  "theme": "obsidian-flame"
}};

window.WORDS = [
  {{ "word": "Bienvenue", "start": 0.0, "end": 0.5 }},
  {{ "word": "sur", "start": 0.5, "end": 0.8 }},
  {{ "word": "AGENT404", "start": 0.8, "end": 1.4 }}
];

window.SCENES = {scenes_js_str};
"""
    (target_path / "timeline.js").write_text(timeline_js_content, encoding="utf-8")

    return {
        "success": True,
        "target_dir": str(target_path),
        "files_created": [
            "project.json",
            "brand.json",
            "scenes.json",
            "timeline.js"
        ],
        "cta_keyword": cta_keyword,
        "video_id": video_id
    }


def main():
    parser = argparse.ArgumentParser(description="AGENT404 Video Project Initializer (Multi-Tenant)")
    parser.add_argument("target_pos", nargs="?", default=None, help="Chemin du nouveau projet (positionnel)")
    parser.add_argument("--target", "-t", default=None, help="Chemin du nouveau projet (optionnel)")
    parser.add_argument("--cta", "-c", default="CLARTÉ", help="Mot-clé CTA unique (défaut : CLARTÉ)")
    parser.add_argument("--title", help="Titre du projet")
    parser.add_argument("--topic", help="Thématique de la vidéo")
    args = parser.parse_args()

    target = args.target or args.target_pos
    if not target:
        parser.error("L'argument --target ou le chemin positionnel du projet est obligatoire.")

    print(f"[InitVideo] Initialisation du projet vidéo dans '{target}'...")
    res = init_video_project(target=target, cta=args.cta, title=args.title, topic=args.topic)
    print(f"✓ Projet initialisé avec succès : {res['target_dir']}")
    print(f"  - Mot-clé CTA configuré : {res['cta_keyword']}")
    print(f"  - Fichiers créés : {', '.join(res['files_created'])}")


if __name__ == "__main__":
    main()
