#!/usr/bin/env python3
"""
GÉNÉRATEUR DE RAPPORT D'AUTOPSIE & BLUEPRINT TEMPLATE
===================================================
Produit les artéfacts standardisés pour references/analyzed/<slug>/ :
1. AUTOPSIE_FORMAT.md : Découpage chirurgical, leviers psychologiques et adaptation Agent404.
2. blueprint_template.json : Squelette JSON prêt à l'emploi pour project.json.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any


PILLARS_MAPPING = {
    "split_screen": {
        "title": "Pilier 1 : Trajectoire / Split-Screen Temporel",
        "blueprint": "bp_split_timeline",
        "psychology": "Biais de Contraste & Projection Temporelle (Avant vs Après sur 6-12 mois)"
    },
    "backstage": {
        "title": "Pilier 2 : Autopsie / Coulisses Brutes",
        "blueprint": "bp_code_window",
        "psychology": "Effet de Transparence & Preuve Technique (Montrer le terminal sans fard)"
    },
    "case_study": {
        "title": "Pilier 3 : Preuve Technique / Étude de Cas Chiffrée",
        "blueprint": "bp_stat_shock",
        "psychology": "Biais d'Ancrage & Preuve Sociale (Chiffres concrets après récit)"
    },
    "myth_bust": {
        "title": "Pilier 4 : Manifeste / Destruction de Mythe B2B",
        "blueprint": "bp_versus_compare",
        "psychology": "Aversion à la Perte & Rupture de Croyance (Casser l'erreur coûteuse)"
    }
}


def detect_pillar(slug: str, hook_data: dict[str, Any], transcript: str) -> dict[str, str]:
    """Détecte le pilier narratif dominant."""
    text = (slug + " " + hook_data.get("hook_text", "") + " " + transcript).lower()
    if any(k in text for k in ["split", "jun_yuh", "duel", "versus", "timeline", "mois", "day"]):
        return PILLARS_MAPPING["split_screen"]
    if any(k in text for k in ["code", "claude", "terminal", "coulisses", "astuce", "système"]):
        return PILLARS_MAPPING["backstage"]
    if any(k in text for k in ["chiffre", "euros", "100k", "followers", "résultat", "vues", "caption"]):
        return PILLARS_MAPPING["case_study"]
    return PILLARS_MAPPING["myth_bust"]


def generate_autopsie_and_template(
    source: str,
    slug: str,
    duration: float,
    transcript: str,
    words: list[dict[str, Any]],
    hook_data: dict[str, Any],
    pacing_data: dict[str, Any],
    out_dir: Path
) -> tuple[Path, Path]:
    """Génère AUTOPSIE_FORMAT.md et blueprint_template.json dans out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    pillar = detect_pillar(slug, hook_data, transcript)

    # 1. Rédaction de AUTOPSIE_FORMAT.md
    autopsie_lines = [
        f"# Autopsie de Format Viral : `{slug}`",
        f"- **Source originale** : `{source}`",
        f"- **Pilier narratif Agent404** : **{pillar['title']}**",
        f"- **Blueprint privilégié** : `{pillar['blueprint']}`",
        f"- **Levier psychologique dominant** : `{pillar['psychology']}`",
        "",
        "---",
        "",
        "## 1. Métriques Clés & Rythme de Rétention",
        f"- **Durée totale** : `{duration:.1f} secondes`",
        f"- **Nombre de plans / Cuts** : `{pacing_data['cuts_count']}`",
        f"- **Cadence moyenne** : `1 cut toutes les {pacing_data['seconds_per_cut']:.2f}s` ({pacing_data['pacing_level']})",
        f"- **Débit vocal** : `{pacing_data['words_per_minute']} mots/minute` ({pacing_data['word_count']} mots au total)",
        f"- **Diagnostic Rétention** : *{pacing_data['retention_diagnosis']}*",
        "",
        "---",
        "",
        "## 2. Rétro-Ingénierie du Hook (0 à 3 secondes)",
        f"- **Phrase articulée** : « {hook_data['hook_text']} »",
        f"- **Formule détectée** : **{hook_data['formula_name']}** (Score de rétention : `{hook_data['hook_score']}/100`)",
        f"- **Analyse stratégique** : {hook_data['formula_advice']}",
        f"- **Transposition B2B pour Agent404** : {hook_data['b2b_transposition']}",
        "",
        "---",
        "",
        "## 3. Découpage Scène par Scène & Psychologie de Vente",
        "| Palier / Scène | Timing | Ce qui est dit | Mécanique visuelle | Levier `@marketing-psychology` |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    scenes = pacing_data.get("scenes_breakdown", [])
    if not scenes:
        scenes = [{
            "scene_index": 1,
            "start": 0.0,
            "end": duration,
            "dialogue_snippet": transcript[:60] if transcript else "Vidéo complète",
            "frame_preview": "preview.jpg"
        }]

    for sc in scenes:
        idx = sc["scene_index"]
        t_str = f"t={sc['start']:.1f}s à {sc['end']:.1f}s"
        words_sample = sc["dialogue_snippet"]
        visual = "Split-Screen 2 colonnes avec progression" if "split" in pillar["blueprint"] else "Carte Néo-Brutaliste avec punch de métrique"
        lever = "Aversion à la perte (montrer la galère)" if idx % 2 != 0 else "Preuve d'autorité & soulagement (la solution)"
        autopsie_lines.append(f"| Scène {idx:02d} | `{t_str}` | {words_sample} | {visual} | {lever} |")

    autopsie_lines.extend([
        "",
        "---",
        "",
        "## 4. Transcription Complète Relevée",
        f"> {transcript if transcript else '_Aucune parole détectée_'}",
        "",
        "---",
        "",
        "## 5. Cahier d'Adaptation AGENT404 (Remix B2B)",
        "Pour adapter cette référence dans le moteur sans tournage :",
        f"1. **Blueprint cible** : Intégrer `{pillar['blueprint']}` pour la phase centrale d'argumentation.",
        "2. **Esthétique** : Palette Néo-Brutaliste Beige Mat `#F5F2EB` avec accents Vert Menthe `#A7F3D0` et Orange Flamme `#FF4F18`.",
        "3. **Call-to-Action** : Clôturer par `bp_cta_conversion` orienté vers un mot-clé unique en DM (ex: `CLARTÉ` ou `STUDIO`).",
        ""
    ])

    autopsie_path = out_dir / "AUTOPSIE_FORMAT.md"
    autopsie_path.write_text("\n".join(autopsie_lines), encoding="utf-8")

    # 2. Génération de blueprint_template.json
    template_data = {
        "reference_slug": slug,
        "recommended_blueprint": pillar["blueprint"],
        "estimated_duration": duration,
        "scenes": [
            {
                "id": "scene_01",
                "type": "bp_hook_question",
                "start": 0.0,
                "end": 3.5,
                "params": {
                    "top_badge": "QUESTION B2B",
                    "title": hook_data.get("b2b_transposition", "Pourquoi tes prospects ignorent tes posts ?").strip("«» "),
                    "subtitle": "Le constat brutal sur 6 mois",
                    "box_color": "var(--tile-yellow)",
                    "icon": "question",
                    "stamp_text": "LE TEST"
                }
            },
            {
                "id": "scene_02",
                "type": pillar["blueprint"],
                "start": 3.5,
                "end": max(15.0, round(duration * 0.7, 1)),
                "params": {
                    "milestone_label": "LE DUEL B2B",
                    "progress_percent": 65,
                    "left_col": {
                        "header": "TOURNAGE CLASSIQUE",
                        "icon": "camera",
                        "status": "cross",
                        "action_text": "20 PRISES, 4H DE MONTAGE, ABANDON",
                        "metric_label": "RÉSULTAT",
                        "metric_value": "0 LEAD"
                    },
                    "right_col": {
                        "header": "STUDIO AGENT404",
                        "icon": "rocket",
                        "status": "check",
                        "action_text": "1 VOCAL WHATSAPP = 2 VIDÉOS PAR SEMAINE",
                        "metric_label": "RÉSULTAT",
                        "metric_value": "24 VIDÉOS"
                    },
                    "footer_stamp": "SANS CAMÉRA"
                }
            },
            {
                "id": "scene_03",
                "type": "bp_cta_conversion",
                "start": max(15.0, round(duration * 0.7, 1)),
                "end": max(20.0, duration),
                "params": {
                    "top_badge": "PASSER À L'ACTION",
                    "title": "Reçois ta vidéo test en 48 heures",
                    "keyword": "CLARTÉ",
                    "door_1": {
                        "title": "AUDIT EXPRESS",
                        "desc": "On analyse ton meilleur post"
                    },
                    "door_2": {
                        "title": "STUDIO CLÉ EN MAIN",
                        "desc": "8 vidéos / mois sans tournage"
                    }
                }
            }
        ]
    }

    template_path = out_dir / "blueprint_template.json"
    template_path.write_text(json.dumps(template_data, indent=2, ensure_ascii=False), encoding="utf-8")

    return autopsie_path, template_path
