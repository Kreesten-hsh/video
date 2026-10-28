#!/usr/bin/env python3
"""
AGENT404 : Tests de gouvernance globale du projet.
Valide les règles d'intégrité architecturale :
  1. Zéro doublon binaire d'avatars dans assets/avatars
  2. Bannissement strict et perpétuel du HUD supérieur (#agent-hud)
"""

import hashlib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestGovernance(unittest.TestCase):
    """Vérifications de gouvernance et règles d'or architecturales."""

    def test_avatars_binary_uniqueness(self):
        """Règle d'or : 100% des stickers avatars dans assets/avatars ont un hash SHA-256 unique (zéro doublon binaire)."""
        avatars_dir = REPO_ROOT / "assets" / "avatars"
        hashes = {}
        for p in avatars_dir.glob("*.png"):
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            self.assertNotIn(
                h, hashes,
                f"Doublon binaire détecté : {p.name} est identique à {hashes.get(h)}"
            )
            hashes[h] = p.name

    def test_hud_banned_from_project(self):
        """Règle absolue : le bandeau supérieur HUD (#agent-hud, .hud-brand, .hud-timer) est strictement banni du projet."""
        index_html_path = REPO_ROOT / "index.html"
        style_css_path = REPO_ROOT / "style.css"
        video_js_path = REPO_ROOT / "video.js"

        if index_html_path.exists():
            content = index_html_path.read_text(encoding="utf-8")
            self.assertNotIn("agent-hud", content, "Le HUD supérieur (#agent-hud) est strictement banni de index.html")
            self.assertNotIn("hud-timer", content, "Le HUD supérieur (hud-timer) est strictement banni de index.html")
            self.assertNotIn("hud-brand", content, "Le HUD supérieur (hud-brand) est strictement banni de index.html")

        if style_css_path.exists():
            content = style_css_path.read_text(encoding="utf-8")
            self.assertNotIn("#agent-hud", content, "#agent-hud ne doit pas être défini dans style.css")
            self.assertNotIn(".hud-timer", content, ".hud-timer ne doit pas être défini dans style.css")

        if video_js_path.exists():
            content = video_js_path.read_text(encoding="utf-8")
            self.assertNotIn("hud-progress-fill", content, "video.js ne doit pas piloter le HUD banni")
            self.assertNotIn("hud-timer", content, "video.js ne doit pas piloter le HUD banni")


if __name__ == "__main__":
    unittest.main()
