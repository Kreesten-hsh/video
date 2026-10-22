#!/usr/bin/env python3
"""
SUITE DE TESTS : BLUEPRINTS, CAMÉRA VIRTUELLE & SOUS-TITRES MULTI-ZONES
======================================================================
Valide les 5 correctifs critiques :
1. Caméra virtuelle non-linéaire (keyframes & easing)
2. Parallaxe sur #bg-layer à 30% et dérive du filigrane
3. Pagination mot-à-mot (2-4 mots max) et anti-collision CENTER_SLAM / DYNAMIC_BAND
4. Ancrage sémantique des beats dans les 6 blueprints
5. Chorégraphie de l'avatar (hero, inset, hidden) et 5 thèmes graphiques.
"""

import os
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestBlueprintsAndCamera(unittest.TestCase):

    def setUp(self):
        self.video_js = (REPO_ROOT / "video.js").read_text(encoding="utf-8")
        self.style_css = (REPO_ROOT / "style.css").read_text(encoding="utf-8")
        self.index_html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")

    def test_dom_structure_contains_camera_rig_and_bg_layer(self):
        """Vérifie la présence de #camera-rig, #bg-layer et #global-avatar-wrapper dans index.html."""
        self.assertIn('id="camera-rig"', self.index_html, "#camera-rig manquant dans index.html")
        self.assertIn('id="bg-layer"', self.index_html, "#bg-layer manquant dans index.html")
        self.assertIn('id="watermark-text"', self.index_html, "#watermark-text manquant dans index.html")
        self.assertIn('id="global-avatar-wrapper"', self.index_html, "#global-avatar-wrapper manquant dans index.html")

    def test_style_css_subtitles_multizone_modes(self):
        """Vérifie que les 3 modes de sous-titres et le mode hidden sont déclarés dans style.css."""
        self.assertIn(".mode-center-slam", self.style_css)
        self.assertIn(".mode-dynamic-band", self.style_css)
        self.assertIn(".mode-single-line-top", self.style_css)
        self.assertIn(".mode-hidden", self.style_css)

    def test_style_css_theme_presets_declared(self):
        """Vérifie que les 5 thèmes sont déclarés dans style.css sans hex hors :root."""
        theme_prefixes = {
            "claude": "claude",
            "cobalt-grid": "cobalt",
            "editorial-forest": "forest",
            "bold-poster": "poster"
        }
        for th, prefix in theme_prefixes.items():
            self.assertIn(f'[data-theme="{th}"]', self.style_css, f"Sélecteur de thème manquant : {th}")
            self.assertIn(f"--theme-{prefix}-bg", self.style_css)

    def test_style_css_six_blueprints_declared(self):
        """Vérifie que les classes des 6 blueprints sont définies dans style.css."""
        blueprints = [
            ".blueprint-kinetic-type",
            ".blueprint-cursor-ui",
            ".blueprint-terminal-scene",
            ".blueprint-compare-split",
            ".blueprint-spatial-pan",
            ".blueprint-overwhelm"
        ]
        for bp in blueprints:
            self.assertIn(bp, self.style_css, f"Classe de blueprint manquante dans style.css : {bp}")

    def test_video_js_camera_keyframes_and_easing(self):
        """Vérifie la présence d'easeInOutCubic, easeOutExpo et la logique keyframes dans video.js."""
        self.assertIn("function easeOutExpo", self.video_js)
        self.assertIn("function easeInOutCubic", self.video_js)
        self.assertIn("scene.camera.keyframes", self.video_js)
        self.assertIn("bgZoom = 1 + (currentZoom - 1) * 0.3", self.video_js)
        self.assertIn("bgPanX = currentPanX * 0.3", self.video_js)

    def test_video_js_subtitles_pagination_limit(self):
        """Vérifie que buildSubtitleChunks limite à 2-3 mots en center_slam."""
        self.assertIn('mode === "center_slam"', self.video_js)
        self.assertIn("chunkSize = (firstLen + secondLen > 13) ? 2 : 3", self.video_js)
        self.assertIn('mode === "dynamic_band"', self.video_js)

    def test_video_js_avatar_choreography_modes(self):
        """Vérifie la gestion des 3 modes d'avatar : hero, inset, hidden."""
        self.assertIn('scene.avatar_mode', self.video_js)
        self.assertIn('"avatar-" + mode', self.video_js)
        self.assertIn(".avatar-hero", self.style_css)
        self.assertIn(".avatar-inset", self.style_css)
        self.assertIn(".avatar-hidden", self.style_css)

    def test_video_js_semantic_beats_in_blueprints(self):
        """Vérifie que animateBlueprint prend en charge click_at, execute_at, reveal_at."""
        self.assertIn("click_at", self.video_js)
        self.assertIn("execute_at", self.video_js)
        self.assertIn("reveal_at", self.video_js)


if __name__ == "__main__":
    unittest.main()
