"""
AGENT404 : Test de conformité et de qualité pour la Vidéo n° 2 (Loom B2B).
Vérifie la structure du projet, les contraintes de ciblage, l'absence de jargon/prix,
et la validité des composants et avatars.
"""

import os
import json
import unittest
from pathlib import Path

from build_master_timeline import load_project, validate_timeline

REPO_ROOT = Path(__file__).resolve().parent.parent
VIDEO_02_DIR = REPO_ROOT / "studio_perso" / "video_02"


class TestVideo02Spec(unittest.TestCase):
    """Vérifications strictes sur les règles de production de la vidéo n° 2."""

    def setUp(self):
        self.project_path = VIDEO_02_DIR / "project.json"

    def test_video02_project_json_exists_and_valid(self):
        """Vérifie l'existence et la validité du fichier project.json de la vidéo 2."""
        self.assertTrue(self.project_path.exists(), f"Fichier introuvable : {self.project_path}")
        with open(self.project_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data.get("video_number"), 2)
        self.assertEqual(data.get("gele"), False)
        self.assertEqual(data.get("rendu_deterministe"), True)
        self.assertIn("theme", data)
        self.assertIn("scenes", data)
        self.assertIn("scene_end_words", data)
        self.assertIn("reference_words", data)

    def test_video02_timeline_and_scenes_alignment(self):
        """Vérifie que les 35 scènes sont parfaitement alignées avec leurs mots de fin et reference_words."""
        with open(self.project_path, "r", encoding="utf-8") as f:
            project = json.load(f)

        ref_words = project["reference_words"]
        scene_end_words = project["scene_end_words"]
        scenes = project["scenes"]

        self.assertEqual(len(scenes), 35, "La vidéo 2 doit comporter exactement 35 scènes.")
        self.assertEqual(len(scene_end_words), 35, "Chaque scène doit avoir son mot de fin.")
        self.assertEqual(len(ref_words), 204, "Le texte de référence doit comporter 204 mots.")

        # Vérification séquentielle de chaque mot terminal dans les mots de référence
        cur_idx = 0
        for i, end_w in enumerate(scene_end_words):
            while cur_idx < len(ref_words) and ref_words[cur_idx] != end_w:
                cur_idx += 1
            self.assertLess(
                cur_idx, len(ref_words),
                f"Mot terminal '{end_w}' introuvable pour la scène #{i+1}"
            )
            cur_idx += 1

        self.assertEqual(scene_end_words[-1], ref_words[-1], "Le dernier mot terminal doit être le dernier mot du script.")

        # Test de simulation de timeline avec timestamps simulés pour valider step3_build_timeline
        from build_master_timeline import step3_build_timeline
        import tempfile
        mock_words = []
        for i, w in enumerate(ref_words):
            mock_words.append({"word": w, "start": round(i * 0.3, 3), "end": round((i + 1) * 0.3, 3)})
        total_dur = len(ref_words) * 0.3

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_timeline = Path(tmp_dir) / "timeline.js"
            step3_build_timeline(
                mock_words, scenes, scene_end_words, ref_words, total_dur,
                timeline_path=str(tmp_timeline),
                project_config=project
            )
            self.assertTrue(tmp_timeline.exists())

    def test_video02_no_technical_jargon(self):
        """Règle 'Zéro Jargon' : aucun terme technique (Python, JavaScript, FFmpeg, Whisper) dans les mots parlés."""
        with open(self.project_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        banned_jargon = {"python", "javascript", "ffmpeg", "whisper", "faster-whisper", "codebase"}
        words = [w.lower().strip(".,;:!?\"'«»()") for w in data.get("reference_words", [])]

        found_jargon = [w for w in words if w in banned_jargon]
        self.assertEqual(
            found_jargon, [],
            f"Termes de jargon technique interdits détectés dans le script : {found_jargon}"
        )

    def test_video02_no_prices_in_script(self):
        """Règle 'Zéro Prix dans la vidéo' : aucun prix (250, 500, €) dans le script."""
        with open(self.project_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        script_text = " ".join(data.get("reference_words", [])).lower()
        self.assertNotIn("250", script_text, "Aucun prix chiffré ne doit figurer dans le script.")
        self.assertNotIn("500", script_text, "Aucun prix chiffré ne doit figurer dans le script.")
        self.assertNotIn("€", script_text, "Le symbole euro est interdit dans le script.")
        self.assertNotIn("euro", script_text, "Le mot euro est interdit dans le script.")

    def test_video02_dm_call_to_action(self):
        """Vérifie que le CTA final oriente vers le mot-clé DEMO en message privé."""
        with open(self.project_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        last_scene = data["scenes"][-1]
        self.assertEqual(last_scene["type"], "dm_cta_sim")
        self.assertEqual(last_scene["data"].get("keyword"), "DEMO")

    def test_video02_all_avatars_exist(self):
        """Vérifie que tous les stickers/avatars requis par les scènes existent physiquement."""
        with open(self.project_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for sc in data["scenes"]:
            avatar = sc.get("data", {}).get("avatar")
            if avatar:
                avatar_path = REPO_ROOT / avatar
                self.assertTrue(avatar_path.exists(), f"Avatar requis manquant : {avatar_path} (scène {sc['id']})")

    def test_video02_no_duplicate_illustrations(self):
        """Règle qualité : aucune illustration ou avatar ne doit être utilisé deux fois dans la même vidéo."""
        with open(self.project_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        seen_avatars = []
        for sc in data["scenes"]:
            avatar = sc.get("data", {}).get("avatar")
            if avatar:
                self.assertNotIn(
                    avatar, seen_avatars,
                    f"Répétition interdite : l'illustration '{avatar}' est réutilisée dans la scène {sc['id']}."
                )
                seen_avatars.append(avatar)


if __name__ == "__main__":
    unittest.main()
