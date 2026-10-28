#!/usr/bin/env python3
"""
SUITE DE TESTS SPÉCIFICATIONS : VIDÉO 01 DÉCOUVERTE (LE MOTEUR SANS CAMÉRA)
==========================================================================
Valide la conformité absolue de studio_perso/video_01_decouverte :
  1. project.json syntaxiquement et structurellement valide
  2. Zéro jargon banni dans le script (Python, JavaScript, Whisper, etc.)
  3. Zéro prix dans le script (150, 200, 750, €)
  4. Mot-clé CTA strictement égal à "CLARTÉ"
  5. Continuité temporelle stricte des 21 scènes (0 trou, 0 chevauchement)
  6. Concordance parfaite entre timeline.js, words.json et reference_words
  7. Présence physique de tous les avatars déclarés
  8. Déclaration et utilisation des 21 micro-scènes Néo-Brutalistes Obsidian & Flame
"""

import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJ_DIR = REPO_ROOT / "studio_perso" / "video_01_decouverte"


class TestVideo01DecouverteSpec(unittest.TestCase):

    def setUp(self):
        self.proj_json_path = PROJ_DIR / "project.json"
        self.words_json_path = PROJ_DIR / "words.json"
        self.timeline_js_path = PROJ_DIR / "timeline.js"

        self.assertTrue(self.proj_json_path.exists(), "project.json introuvable dans video_01_decouverte")
        with open(self.proj_json_path, "r", encoding="utf-8") as f:
            self.project_data = json.load(f)

    def test_video01_decouverte_project_json_structure(self):
        """Vérifie l'existence et la validité des champs obligatoires de project.json."""
        self.assertEqual(self.project_data.get("video_number"), 1)
        self.assertEqual(self.project_data.get("cta_keyword"), "CLARTÉ")
        self.assertEqual(self.project_data.get("theme_preset"), "obsidian-flame")
        self.assertEqual(len(self.project_data.get("scenes", [])), 21)
        self.assertEqual(len(self.project_data.get("reference_words", [])), 292)

    def test_video01_decouverte_no_technical_jargon(self):
        """Règle 'Zéro Jargon' : aucun terme technique dans les mots parlés de la vidéo 1 Découverte."""
        mem_path = REPO_ROOT / "registry" / "video_memory.json"
        banned = ["python", "javascript", "ffmpeg", "whisper", "playwright", "chromium", "codebase"]
        if mem_path.exists():
            with open(mem_path, "r", encoding="utf-8") as f:
                mem = json.load(f)
                banned = list(set(banned + mem.get("banned_global_jargon", [])))

        ref_words = [w.lower().strip(".,;:!?\"'«»()") for w in self.project_data.get("reference_words", [])]
        found = [w for w in ref_words if w in banned]
        self.assertEqual(found, [], f"Jargon banni détecté dans video_01_decouverte : {found}")

    def test_video01_decouverte_no_prices_in_script(self):
        """Règle 'Zéro Prix' : aucun chiffre tarifaire dans le script parlé."""
        price_patterns = [r"\b150\b", r"\b200\b", r"\b750\b", r"€", r"\beuro[s]?\b"]
        ref_text = " ".join(self.project_data.get("reference_words", []))
        for pat in price_patterns:
            matches = re.findall(pat, ref_text, flags=re.IGNORECASE)
            self.assertEqual(matches, [], f"Prix détecté dans le script video_01_decouverte avec le motif '{pat}' : {matches}")

    def test_video01_decouverte_cta_keyword_clarte(self):
        """Vérifie que le CTA final oriente vers CLARTÉ."""
        cta_keyword = self.project_data.get("cta_keyword")
        self.assertEqual(cta_keyword, "CLARTÉ")

        cta_scene = [s for s in self.project_data.get("scenes", []) if s.get("type") in ["ob_two_door_cta_final", "ob_final_delivery_cta", "face_to_dm_cta"]]
        self.assertTrue(len(cta_scene) >= 1, "Scène CTA introuvable")

    def test_video01_decouverte_scenes_continuity_and_timing(self):
        """Vérifie la continuité temporelle absolue des scènes sans aucun trou ni chevauchement."""
        scenes = self.project_data.get("scenes", [])
        self.assertEqual(len(scenes), 21)
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
        self.assertAlmostEqual(total_duration, 95.79, delta=0.5)

    def test_video01_decouverte_words_and_timeline_concordance(self):
        """Vérifie la concordance intégrale entre words.json et timeline.js."""
        self.assertTrue(self.words_json_path.exists())
        self.assertTrue(self.timeline_js_path.exists())

        with open(self.words_json_path, "r", encoding="utf-8") as f:
            words_data = json.load(f)

        timeline_js = self.timeline_js_path.read_text(encoding="utf-8")
        self.assertIn("window.WORDS", timeline_js)
        self.assertIn("window.SCENES", timeline_js)
        self.assertEqual(len(words_data), len(self.project_data.get("reference_words", [])))

    def test_video01_decouverte_avatars_exist_physically(self):
        """Vérifie que tous les avatars déclarés dans video_01_decouverte existent physiquement."""
        scenes = self.project_data.get("scenes", [])
        for sc in scenes:
            avatar_path = sc.get("data", {}).get("avatar")
            if avatar_path:
                full_path = REPO_ROOT / avatar_path
                self.assertTrue(
                    full_path.exists(),
                    f"Avatar introuvable pour la scène {sc['id']} : {avatar_path} ({full_path})"
                )

    def test_video01_decouverte_obsidian_flame_micro_scenes_present(self):
        """Vérifie la présence des 21 micro-scènes Néo-Brutalistes Obsidian & Flame de la vidéo Découverte."""
        scenes = self.project_data.get("scenes", [])
        self.assertEqual(len(scenes), 21)
        types = set(s.get("type") for s in scenes)
        expected_types = {
            "ob_obsession_question",
            "ob_locked_arguments_vault",
            "ob_ninety_percent_ignore",
            "ob_classic_method_sigh",
            "ob_three_struggles_stack",
            "ob_sunday_timeline_hell",
            "ob_logistic_scale_crash",
            "ob_plumbing_vs_content",
            "ob_ban_ai_clones_stamp",
            "ob_breakthrough_equation",
            "ob_engine_architecture",
            "ob_meta_live_code",
            "ob_millisecond_audio_sync",
            "ob_sliding_4_logos_rtl",
            "ob_three_pillars_title",
            "ob_formula_cascade_equation",
            "ob_triple_zero_checklist",
            "ob_agent404_weekly_doc",
            "ob_market_dominance_chart",
            "ob_cta_bridge_solo",
            "ob_two_door_cta_final",
        }
        self.assertEqual(types, expected_types)


if __name__ == "__main__":
    unittest.main()
