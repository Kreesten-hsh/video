#!/usr/bin/env python3
"""
AGENT404 : Générateur de Projet Vidéo Autonome (CLI Scaffolding).
Initialise une arborescence complète pour une nouvelle vidéo (studio_perso ou studio_clients) :
  - Respect strict des 5 règles du Gatekeeper dès l'initialisation
  - 100% zéro HUD, zéro #FF2A5F
  - Héritage automatique des variables CSS :root sémantiques et Safe Zone 9:16
  - Intégration des contraintes du registre anti-répétition (registry/video_memory.json)
"""

import os
import sys
import json
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


def extract_root_css():
    """Extrait le bloc :root sémantique depuis le style.css racine."""
    root_style_path = REPO_ROOT / "style.css"
    if not root_style_path.exists():
        return ":root {\n  --accent-primary: #00F5A0;\n}\n"
    content = root_style_path.read_text(encoding="utf-8")
    import re
    match = re.search(r":root\s*\{[^}]+\}", content)
    if match:
        return match.group(0)
    return ":root {\n  --accent-primary: #00F5A0;\n}\n"


def init_video_project(target: str, cta: str = "DEMO", title: str = "", topic: str = "") -> dict:
    """Crée l'arborescence et les fichiers initiaux pour un nouveau projet vidéo."""
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = (REPO_ROOT / target_path).resolve()

    target_path.mkdir(parents=True, exist_ok=True)

    # Calcul du chemin relatif vers REPO_ROOT pour les liens d'assets
    try:
        rel_root = os.path.relpath(REPO_ROOT, target_path)
    except ValueError:
        rel_root = "."

    video_id = target_path.name
    # Détection de l'entité parente (ex: studio_perso, studio_clients/acme)
    parent_rel = str(target_path.parent.relative_to(REPO_ROOT)) if target_path.is_relative_to(REPO_ROOT) else "studio_perso"

    # Lecture de la mémoire d'unicité
    memory = load_video_memory()
    banned_jargon = memory.get("banned_global_jargon", [])
    past_illustrations = []
    for v in memory.get("videos", []):
        past_illustrations.extend(v.get("used_illustrations", []))

    if not title:
        title = f"Projet {video_id} - AGENT404"
    if not topic:
        topic = "Capsule B2B chirurgicale à forte rétention"

    # 1. Génération de project_config.json et project.json
    project_meta = {
        "video_id": video_id,
        "target": parent_rel,
        "title": title,
        "topic": topic,
        "cta_keyword": cta.upper().strip(),
        "reference_words": [],
        "scenes": [
            {
                "id": "scene_01",
                "type": "face",
                "start": 0.0,
                "end": 4.5,
                "data": {
                    "avatar": f"{rel_root}/assets/avatars/stop.png",
                    "hero_title": "ARRÊTE DE PERDRE TES PROSPECTS",
                    "highlight_word": "PROSPECTS"
                }
            },
            {
                "id": "scene_02",
                "type": "illustration_hero",
                "start": 4.5,
                "end": 10.0,
                "data": {
                    "title": "DÉMONSTRATION CHIRURGICALE B2B"
                }
            }
        ]
    }

    config_path = target_path / "project_config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(project_meta, f, indent=2, ensure_ascii=False)

    # Rétrocompatibilité project.json
    proj_json_path = target_path / "project.json"
    with open(proj_json_path, "w", encoding="utf-8") as f:
        json.dump(project_meta, f, indent=2, ensure_ascii=False)

    # 2. Génération de index.html (Strictement sans HUD)
    index_html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="{rel_root}/assets/fonts/fonts.css">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div id="video-canvas" class="bg-grid">

    <!-- Zone Sous-titres (Top 96px, Safe Zone 9:16) -->
    <header id="subtitles-zone">
      <div id="subtitles-container">
        <div id="subtitles-box" class="sub-line"></div>
      </div>
    </header>

    <!-- Zone centrale & inférieure : Rendu des composants (Safe Zone 9:16) -->
    <main id="scene-zone">
      <div id="scene-container"></div>
    </main>
  </div>

  <script src="timeline.js"></script>
  <script src="video.js"></script>
</body>
</html>
"""
    (target_path / "index.html").write_text(index_html_content, encoding="utf-8")

    # 3. Génération de style.css (Bloc :root complet + Safe Zone 9:16 + 0 code hex hors :root)
    root_block = extract_root_css()
    style_css_content = f"""/* ==========================================================================
   FEUILLE DE STYLE PROGRAMMATIQUE : {video_id}
   Format : 1080 x 1920 (9:16 Vertical)
   Règles :
     - 100% de variables CSS sémantiques depuis :root (Zéro hex hors :root)
     - Safe Zone 9:16 : Top 96px, Bottom 240px, Left/Right 48px
     - Typographie : >= 20px général, >= 28px titres scènes d'illustration
   ========================================================================== */

{root_block}

/* Reset & Dimensions Globales */
*, *::before, *::after {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  width: 1080px;
  height: 1920px;
  overflow: hidden;
  background-color: var(--bg-dark);
  color: var(--white);
  font-family: 'Montserrat', sans-serif;
  user-select: none;
  -webkit-font-smoothing: antialiased;
}}

#video-canvas {{
  width: 1080px;
  height: 1920px;
  position: relative;
  overflow: hidden;
  background: var(--bg-dark);
}}

/* Safe Zones 9:16 */
#subtitles-zone {{
  position: absolute;
  top: 96px;
  left: 48px;
  right: 48px;
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}}

#subtitles-box {{
  font-size: 38px;
  font-weight: 900;
  color: var(--white);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: -0.02em;
}}

#scene-zone {{
  position: absolute;
  top: 260px;
  bottom: 240px;
  left: 48px;
  right: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
}}

#scene-container {{
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}}

/* Conteneurs standards d'illustration (>= 840x520px) */
.comp-container-standard {{
  width: 920px;
  min-height: 600px;
  background: var(--bg-carbon);
  border: 4px solid var(--border-subtle);
  border-radius: 24px;
  box-shadow: 0 16px 40px var(--shadow-ambient);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}}

.master-header {{
  height: 96px;
  background: var(--accent-primary);
  color: var(--bg-dark);
  font-size: 32px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: -0.01em;
  white-space: nowrap;
}}

.tag-badge {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 20px;
  font-weight: 800;
  padding: 6px 14px;
  border-radius: 8px;
  white-space: nowrap;
}}
"""
    (target_path / "style.css").write_text(style_css_content, encoding="utf-8")

    # 4. Génération de timeline.js squelette
    timeline_js_content = f"""// TIMELINE DU PROJET {video_id}
// Conforme au format standard window.SCENES

window.PROJECT_CONFIG = {{
  "video_id": "{video_id}",
  "cta_keyword": "{cta.upper().strip()}",
  "theme": {{
    "mint": "var(--accent-primary)",
    "bg_carbon": "var(--bg-carbon)",
    "bg_dark": "var(--bg-dark)"
  }}
}};

window.WORDS = [
  {{ "word": "Bienvenue", "start": 0.0, "end": 0.5 }},
  {{ "word": "sur", "start": 0.5, "end": 0.8 }},
  {{ "word": "AGENT404", "start": 0.8, "end": 1.4 }}
];

window.SCENES = [
  {{
    "id": "scene_01",
    "type": "face",
    "start": 0.0,
    "end": 4.5,
    "data": {{
      "avatar": "{rel_root}/assets/avatars/stop.png",
      "hero_title": "ARRÊTE DE PERDRE TES PROSPECTS",
      "highlight_word": "PROSPECTS"
    }}
  }},
  {{
    "id": "scene_02",
    "type": "illustration_hero",
    "start": 4.5,
    "end": 10.0,
    "data": {{
      "title": "DÉMONSTRATION CHIRURGICALE B2B"
    }}
  }}
];
"""
    (target_path / "timeline.js").write_text(timeline_js_content, encoding="utf-8")

    # 5. Génération de video.js avec avertissements anti-recyclage
    illustrations_list_str = "\n".join(f" *   - {ill}" for ill in past_illustrations) if past_illustrations else " *   (Aucune vidéo antérieure)"
    jargon_list_str = ", ".join(banned_jargon) if banned_jargon else "aucun"

    video_js_content = f"""/**
 * MOTEUR D'AFFICHAGE VIDÉO PROGRAMMATIQUE - {video_id}
 * 
 * =========================================================================
 * REGISTRE ANTI-RÉPÉTITION & RÈGLES DE VALIDATION VISUELLE (EFFET CLIQUET) :
 * =========================================================================
 * 1. MOT-CLÉ CTA UNIQUE DÉDIÉ : "{cta.upper().strip()}"
 * 2. JARGON TECHNIQUE BANNI DU SCRIPT / OVERLAYS :
 *    [{jargon_list_str}]
 * 3. COMPOSANTS / ILLUSTRATIONS DÉJÀ UTILISÉS DANS LES VIDÉOS ANTÉRIEURES :
 *    ATTENTION : INTERDICTION FORMELLE DE LES RECYCLER TEL QUEL DANS CE PROJET :
{illustrations_list_str}
 * 
 * 4. RÈGLES VISUELLES PRE-FLIGHT (PREFLIGHT_CHECK.PY) :
 *    - Axe 1 (Géométrie) : Conteneurs centraux >= 840x520px (cadrage 1080x1920)
 *    - Axe 2 (Typographie) : >= 20px pour textes descriptifs/badges, >= 28px pour titre de scène
 *    - Axe 3 (Anti-Orphelin) : Badges [ ... ] et KPIs courts sur 1 seule ligne (white-space: nowrap)
 *    - Axe 4 (Dynamique) : Dans les scènes multi-cartes, CHAQUE carte doit s'allumer séquentiellement
 *    - Axe 5 (Gouvernance) : ZÉRO HUD (#agent-hud proscrit), ZÉRO #FF2A5F
 * =========================================================================
 */

(function () {{
  'use strict';

  let currentSceneIndex = -1;

  function renderScene(sc, t, progress) {{
    const container = document.getElementById('scene-container');
    if (!container) return;

    if (sc.type === 'face') {{
      container.innerHTML = `
        <div class="comp-face-stage">
          <div class="hero-title" style="font-size: 48px; font-weight: 900; text-align: center;">
            ${{sc.data.hero_title || 'TITRE PRINCIPAL'}}
          </div>
        </div>
      `;
    }} else {{
      container.innerHTML = `
        <div class="comp-container-standard">
          <div class="master-header">
            ${{sc.data.title || 'TITRE SCÈNE D\\'ILLUSTRATION'}}
          </div>
          <div style="padding: 32px; display: flex; gap: 16px; justify-content: center;">
            <div class="tag-badge" style="background: var(--surface-card); border: 2px solid var(--border-subtle);">
              [ ÉTAPE 01 ]
            </div>
            <div class="tag-badge" style="background: var(--surface-card); border: 2px solid var(--border-subtle);">
              [ ÉTAPE 02 ]
            </div>
          </div>
        </div>
      `;
    }}
  }}

  window.setTime = function (t) {{
    const scenes = window.SCENES || [];
    for (let i = 0; i < scenes.length; i++) {{
      const sc = scenes[i];
      if (t >= sc.start && t < sc.end) {{
        if (currentSceneIndex !== i) {{
          currentSceneIndex = i;
        }}
        const duration = sc.end - sc.start;
        const progress = duration > 0 ? (t - sc.start) / duration : 0;
        renderScene(sc, t, progress);
        return;
      }}
    }}
  }};

  window.addEventListener('DOMContentLoaded', () => {{
    window.setTime(0);
  }});
}})();
"""
    (target_path / "video.js").write_text(video_js_content, encoding="utf-8")

    return {
        "success": True,
        "target_dir": str(target_path),
        "files_created": [
            "project_config.json",
            "project.json",
            "index.html",
            "style.css",
            "timeline.js",
            "video.js"
        ],
        "cta_keyword": cta.upper().strip(),
        "video_id": video_id
    }


def main():
    parser = argparse.ArgumentParser(description="AGENT404 Video Project Initializer")
    parser.add_argument("--target", "-t", required=True, help="Chemin du nouveau projet (ex: studio_perso/video_03)")
    parser.add_argument("--cta", "-c", default="DEMO", help="Mot-clé CTA unique (ex: CODE, DEMO, TARIF)")
    parser.add_argument("--title", help="Titre du projet")
    parser.add_argument("--topic", help="Thématique de la vidéo")
    args = parser.parse_args()

    print(f"[InitVideo] Initialisation du projet vidéo dans '{args.target}'...")
    res = init_video_project(target=args.target, cta=args.cta, title=args.title, topic=args.topic)
    print(f"✓ Projet initialisé avec succès : {res['target_dir']}")
    print(f"  - Mot-clé CTA configuré : {res['cta_keyword']}")
    print(f"  - Fichiers créés : {', '.join(res['files_created'])}")


if __name__ == "__main__":
    main()
