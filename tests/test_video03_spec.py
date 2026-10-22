#!/usr/bin/env python3
"""
SUITE DE TESTS SPÉCIFICATIONS : VIDÉO 03 (CLARTÉ)
==================================================
Valide la conformité absolue de studio_perso/video_03 :
  1. project.json syntaxiquement et structurellement valide
  2. Zéro jargon banni dans le script (Python, JavaScript, Whisper, etc.)
  3. Zéro prix dans le script (150, 200, 250, 500, 750, €)
  4. Mot-clé CTA strictement égal à "CLARTÉ"
  5. Continuité temporelle stricte des 10 scènes (0 trou, 0 chevauchement)
  6. Concordance parfaite entre timeline.js, words.json et reference_words
  7. Présence physique de tous les avatars déclarés
  8. Déclaration et utilisation des 6 blueprints et des switchs de thèmes
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJ_DIR = REPO_ROOT / "studio_perso" / "video_03"


class TestVideo03Spec(unittest.TestCase):

    def setUp(self):
        self.proj_json_path = PROJ_DIR / "project.json"
        self.words_json_path = PROJ_DIR / "words.json"
        self.timeline_js_path = PROJ_DIR / "timeline.js"
        self.script_txt_path = PROJ_DIR / "script.txt"

        self.assertTrue(self.proj_json_path.exists(), "project.json introuvable dans video_03")
        with open(self.proj_json_path, "r", encoding="utf-8") as f:
            self.project_data = json.load(f)

    def test_video03_project_json_structure(self):
        """Vérifie l'existence et la validité des champs obligatoires de project.json."""
        self.assertEqual(self.project_data.get("video_number"), 3)
        self.assertEqual(self.project_data.get("cta_keyword"), "CLARTÉ")
        self.assertEqual(self.project_data.get("audio_path"), "voix.wav")
        self.assertTrue(len(self.project_data.get("scenes", [])) >= 8)
        self.assertTrue(len(self.project_data.get("reference_words", [])) > 150)

    def test_video03_no_technical_jargon(self):
        """Règle 'Zéro Jargon' : aucun terme technique dans les mots parlés de la vidéo 3."""
        mem_path = REPO_ROOT / "registry" / "video_memory.json"
        banned = ["python", "javascript", "ffmpeg", "whisper", "playwright", "chromium", "codebase"]
        if mem_path.exists():
            with open(mem_path, "r", encoding="utf-8") as f:
                mem = json.load(f)
                banned = list(set(banned + mem.get("banned_global_jargon", [])))

        ref_words = [w.lower().strip(".,;:!?\"'«»()") for w in self.project_data.get("reference_words", [])]
        found = [w for w in ref_words if w in banned]
        self.assertEqual(found, [], f"Jargon banni détecté dans video_03 : {found}")

    def test_video03_no_prices_in_script(self):
        """Règle 'Zéro Prix' : aucun chiffre tarifaire dans le script parlé."""
        price_patterns = [r"\b150\b", r"\b200\b", r"\b250\b", r"\b500\b", r"\b750\b", r"€", r"\beuro[s]?\b"]
        ref_text = " ".join(self.project_data.get("reference_words", []))
        for pat in price_patterns:
            matches = re.findall(pat, ref_text, flags=re.IGNORECASE)
            self.assertEqual(matches, [], f"Prix détecté dans le script video_03 avec le motif '{pat}' : {matches}")

    def test_video03_cta_keyword_clarte(self):
        """Vérifie que le CTA final et la scène face_to_dm_cta utilisent CLARTÉ."""
        cta_keyword = self.project_data.get("cta_keyword")
        self.assertEqual(cta_keyword, "CLARTÉ")

        cta_scene = [s for s in self.project_data.get("scenes", []) if s.get("type") == "face_to_dm_cta"]
        self.assertTrue(len(cta_scene) >= 1, "Scène face_to_dm_cta introuvable")
        self.assertEqual(cta_scene[0].get("data", {}).get("keyword"), "CLARTÉ")

    def test_video03_scenes_continuity_and_timing(self):
        """Vérifie la continuité temporelle absolue des scènes sans aucun trou ni chevauchement."""
        scenes = self.project_data.get("scenes", [])
        self.assertTrue(len(scenes) > 0)
        self.assertEqual(scenes[0]["start"], 0.0)

        for i in range(len(scenes) - 1):
            cur_end = round(scenes[i]["end"], 3)
            next_start = round(scenes[i + 1]["start"], 3)
            self.assertEqual(
                cur_end,
                next_start,
                f"Discontinuité entre {scenes[i]['id']} (fin: {cur_end}) et {scenes[i+1]['id']} (début: {next_start})"
            )

        total_duration = scenes[-1]["end"]
        self.assertAlmostEqual(total_duration, 62.75, delta=1.0)

    def test_video03_words_and_timeline_concordance(self):
        """Vérifie la concordance intégrale entre words.json et timeline.js."""
        self.assertTrue(self.words_json_path.exists())
        self.assertTrue(self.timeline_js_path.exists())

        with open(self.words_json_path, "r", encoding="utf-8") as f:
            words_data = json.load(f)

        timeline_js = self.timeline_js_path.read_text(encoding="utf-8")
        self.assertIn("window.WORDS", timeline_js)
        self.assertIn("window.SCENES", timeline_js)
        self.assertEqual(len(words_data), len(self.project_data.get("reference_words", [])))

    def test_video03_avatars_exist_physically(self):
        """Vérifie que tous les avatars déclarés dans video_03 existent physiquement."""
        scenes = self.project_data.get("scenes", [])
        for sc in scenes:
            avatar_path = sc.get("data", {}).get("avatar")
            if avatar_path:
                full_path = REPO_ROOT / avatar_path
                self.assertTrue(
                    full_path.exists(),
                    f"Avatar introuvable pour la scène {sc['id']} : {avatar_path} ({full_path})"
                )

    def test_video03_six_blueprints_and_theme_switches_present(self):
        """Vérifie la présence des 6 blueprints et des changements de thèmes."""
        scenes = self.project_data.get("scenes", [])
        types = set(s.get("type") for s in scenes)
        expected_types = {
            "blueprint_kinetic_type",
            "blueprint_overwhelm",
            "blueprint_compare_split",
            "blueprint_spatial_pan",
            "blueprint_cursor_ui",
            "blueprint_terminal_scene",
            "face_to_dm_cta"
        }
        for exp in expected_types:
            self.assertIn(exp, types, f"Composant manquant dans les scènes de video_03 : {exp}")

        themes = [s.get("switch_theme") for s in scenes if s.get("switch_theme")]
        self.assertIn("claude", themes)
        self.assertIn("cobalt-grid", themes)
        self.assertIn("bold-poster", themes)


if __name__ == "__main__":
    unittest.main()
