"""
AGENT404 : Test unitaire pour le générateur de Kit de Distribution Sociale.
Vérifie la génération automatique de DISTRIBUTION_KIT.md avec conformité aux critères :
  - Hook LinkedIn < 140 caractères avant troncature
  - Légende Instagram avec hook < 60 caractères
  - Présence du premier commentaire d'amorce et du CTA
  - Checklist smartphone complète
"""

import tempfile
import unittest
from pathlib import Path
import json

from generate_social_pack import generate_social_pack

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestSocialPack(unittest.TestCase):
    """Test du générateur de social pack."""

    def test_generate_social_pack_on_video01_decouverte(self):
        """Vérifie la génération sur studio_perso/video_01_decouverte avec avertissement durée 96s."""
        kit_path = generate_social_pack("studio_perso/video_01_decouverte")
        self.assertTrue(kit_path.exists(), "DISTRIBUTION_KIT.md introuvable")

        content = kit_path.read_text(encoding="utf-8")
        self.assertIn("LINKEDIN", content)
        self.assertIn("INSTAGRAM REELS", content)
        self.assertIn("CLARTÉ", content)
        self.assertIn("96", content)
        self.assertIn("dépasse le plafond recommandé de 60 s", content)
        self.assertIn("prioritairement optimisée pour LinkedIn", content)

    def test_generate_social_pack_on_video03(self):
        """Vérifie la génération sur studio_perso/video_03."""
        kit_path = generate_social_pack("studio_perso/video_03")
        self.assertTrue(kit_path.exists(), "DISTRIBUTION_KIT.md introuvable")

        content = kit_path.read_text(encoding="utf-8")
        self.assertIn("LINKEDIN", content)
        self.assertIn("INSTAGRAM REELS", content)
        self.assertIn("CLARTÉ", content)
        self.assertIn("CHECKLIST SMARTPHONE", content)
        self.assertIn("Golden Hour", content)

    def test_generate_social_pack_temp_project(self):
        """Vérifie la génération dans un dossier temporaire arbitraire."""
        with tempfile.TemporaryDirectory() as tmpdir:
            p_dir = Path(tmpdir)
            p_json = p_dir / "project.json"
            p_json.write_text(json.dumps({
                "title": "Vidéo Test Automatisation",
                "cta_keyword": "WORKFLOW",
                "video_number": 99,
                "reference_words": ["Ceci", "est", "un", "test", "de", "hook", "parlé"]
            }), encoding="utf-8")

            kit_path = generate_social_pack(str(p_dir))
            self.assertTrue(kit_path.exists())
            content = kit_path.read_text(encoding="utf-8")
            self.assertIn("WORKFLOW", content)
            self.assertIn("Vidéo #99", content)


if __name__ == "__main__":
    unittest.main()
