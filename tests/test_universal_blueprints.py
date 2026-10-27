#!/usr/bin/env python3
"""
SUITE DE TESTS : LES 8 BLUEPRINTS UNIVERSELS & ARCHITECTURE MULTI-TENANT
========================================================================
Vérifie rigoureusement :
1. Registre vectoriel SVG_ICONS (22 icônes vectorielles Néo-Brutalistes) et getSvgIcon
2. Les 8 renderers et 8 animators universels déclarés dans video.js
3. Résolution multi-tenant : brand.json, applyBrandConfig et resolveAvatarSrc
4. Pipeline d'injection : build_master_timeline.py et render.py
5. Conformité CSS Néo-Brutaliste dans style.css (zéro #FF2A5F, badges nowrap)
6. Scaffolding du kit prospect : studio_clients/_template_prospect/
"""

import json
import os
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestUniversalBlueprints(unittest.TestCase):

    def setUp(self):
        self.video_js = (REPO_ROOT / "video.js").read_text(encoding="utf-8")
        self.style_css = (REPO_ROOT / "style.css").read_text(encoding="utf-8")
        self.index_html = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
        self.build_timeline_py = (REPO_ROOT / "build_master_timeline.py").read_text(encoding="utf-8")
        self.render_py = (REPO_ROOT / "render.py").read_text(encoding="utf-8")
        self.template_dir = REPO_ROOT / "studio_clients" / "_template_prospect"

    def test_svg_icons_registry_contains_22_icons(self):
        """Vérifie que SVG_ICONS contient 18 symboles sémantiques et 4 réseaux sociaux."""
        expected_semantic = [
            "question", "lock", "camera", "bulb", "clapper", "clock",
            "scale", "check", "cross", "robot", "mic", "code",
            "bolt", "file", "chart", "calendar", "rocket", "gear"
        ]
        expected_social = ["linkedin", "tiktok", "reels", "shorts"]
        
        self.assertIn("const SVG_ICONS = {", self.video_js, "Registre SVG_ICONS absent de video.js")
        
        for icon in expected_semantic + expected_social:
            self.assertRegex(
                self.video_js,
                rf'\b{icon}\s*:\s*`<svg',
                f"Icône vectorielle '{icon}' manquante dans SVG_ICONS de video.js"
            )
            
        self.assertIn("function getSvgIcon(", self.video_js, "Fonction getSvgIcon manquante dans video.js")

    def test_eight_blueprint_renderers_declared(self):
        """Vérifie la présence et le dispatch des 8 renderers universels."""
        blueprints = [
            "bp_hook_question",
            "bp_friction_stack",
            "bp_stat_shock",
            "bp_versus_compare",
            "bp_code_window",
            "bp_grid_2x2",
            "bp_logo_carousel_rtl",
            "bp_cta_conversion"
        ]
        
        self.assertIn("const BLUEPRINT_RENDERERS = {", self.video_js)
        for bp in blueprints:
            self.assertIn(bp, self.video_js, f"Renderer pour {bp} non enregistré dans BLUEPRINT_RENDERERS")
            
        # Vérifie que les fonctions de rendu existent
        self.assertIn("function renderBpHookQuestion(", self.video_js)
        self.assertIn("function renderBpFrictionStack(", self.video_js)
        self.assertIn("function renderBpStatShock(", self.video_js)
        self.assertIn("function renderBpVersusCompare(", self.video_js)
        self.assertIn("function renderBpCodeWindow(", self.video_js)
        self.assertIn("function renderBpGrid2x2(", self.video_js)
        self.assertIn("function renderBpLogoCarouselRtl(", self.video_js)
        self.assertIn("function renderBpCtaConversion(", self.video_js)

    def test_eight_blueprint_animators_declared(self):
        """Vérifie la présence et le dispatch des 8 animateurs universels."""
        blueprints = [
            "bp_hook_question",
            "bp_friction_stack",
            "bp_stat_shock",
            "bp_versus_compare",
            "bp_code_window",
            "bp_grid_2x2",
            "bp_logo_carousel_rtl",
            "bp_cta_conversion"
        ]
        
        self.assertIn("const BLUEPRINT_ANIMATORS = {", self.video_js)
        for bp in blueprints:
            self.assertIn(bp, self.video_js, f"Animateur pour {bp} non enregistré dans BLUEPRINT_ANIMATORS")

        # Vérifie que les fonctions d'animation existent
        self.assertIn("function animateBpHookQuestion(", self.video_js)
        self.assertIn("function animateBpFrictionStack(", self.video_js)
        self.assertIn("function animateBpStatShock(", self.video_js)
        self.assertIn("function animateBpVersusCompare(", self.video_js)
        self.assertIn("function animateBpCodeWindow(", self.video_js)
        self.assertIn("function animateBpGrid2x2(", self.video_js)
        self.assertIn("function animateBpLogoCarouselRtl(", self.video_js)
        self.assertIn("function animateBpCtaConversion(", self.video_js)

    def test_multi_tenant_brand_resolution_in_video_js(self):
        """Vérifie l'application dynamique de brand.json et la résolution d'avatars."""
        self.assertIn("function applyBrandConfig(", self.video_js)
        self.assertIn('root.style.setProperty("--bg-canvas"', self.video_js)
        self.assertIn('root.style.setProperty("--surface-card"', self.video_js)
        self.assertIn('root.style.setProperty("--ink"', self.video_js)
        self.assertIn('root.style.setProperty("--accent-primary"', self.video_js)
        self.assertIn("function resolveAvatarSrc(", self.video_js)

    def test_build_master_timeline_supports_brand_config(self):
        """Vérifie que build_master_timeline.py injecte window.BRAND_CONFIG."""
        self.assertIn('brand_file = project_dir / "brand.json"', self.build_timeline_py)
        self.assertIn("window.BRAND_CONFIG =", self.build_timeline_py)
        self.assertIn("--project", self.build_timeline_py)

    def test_render_py_supports_project_and_client_output(self):
        """Vérifie que render.py gère le paramètre -p et la sortie dans studio_clients/."""
        self.assertIn("--project", self.render_py)
        self.assertIn("output_final.mp4", self.render_py)
        self.assertIn("studio_clients", self.render_py)

    def test_style_css_blueprint_classes_declared(self):
        """Vérifie que toutes les classes structurales des 8 blueprints sont déclarées."""
        classes = [
            ".bp-stage",
            ".bp-card-hook",
            ".bp-top-badge",
            ".bp-section-badge",
            ".bp-icon-box",
            ".bp-friction-items-container",
            ".bp-friction-item",
            ".bp-card-stat",
            ".bp-stat-number",
            ".bp-stat-label",
            ".bp-versus-container",
            ".bp-versus-card",
            ".bp-versus-badge",
            ".bp-window-frame",
            ".bp-waveform-bar",
            ".bp-code-line",
            ".bp-grid-tiles-wrap",
            ".bp-grid-tile",
            ".bp-grid-meter",
            ".bp-carousel-viewport",
            ".bp-carousel-card",
            ".bp-input-mockup",
            ".bp-doors-container",
            ".bp-door-card"
        ]
        for cls in classes:
            self.assertIn(cls, self.style_css, f"Classe CSS manquante : {cls}")

    def test_style_css_no_banned_pink(self):
        """Ratchet absolu : Zéro occurrence du rose banni (#FF2A5F) dans le code."""
        self.assertNotIn("#FF2A5F", self.style_css)
        self.assertNotIn("#ff2a5f", self.style_css)
        self.assertNotIn("#FF2A5F", self.video_js)
        self.assertNotIn("#ff2a5f", self.video_js)

    def test_template_prospect_starter_kit_validity(self):
        """Vérifie la validité des fichiers du template prospect."""
        self.assertTrue(self.template_dir.exists(), "Dossier _template_prospect inexistant")
        
        brand_path = self.template_dir / "brand.json"
        self.assertTrue(brand_path.exists(), "brand.json manquant dans _template_prospect")
        brand_data = json.loads(brand_path.read_text(encoding="utf-8"))
        self.assertIn("brand_name", brand_data)
        self.assertIn("theme", brand_data)
        self.assertIn("typography", brand_data)
        self.assertIn("avatars", brand_data)
        
        project_path = self.template_dir / "project.json"
        self.assertTrue(project_path.exists(), "project.json manquant dans _template_prospect")
        project_data = json.loads(project_path.read_text(encoding="utf-8"))
        self.assertIn("scenes", project_data)
        self.assertGreaterEqual(len(project_data["scenes"]), 6)
        
        words_path = self.template_dir / "words.json"
        self.assertTrue(words_path.exists(), "words.json manquant dans _template_prospect")
        
        audio_exists = (self.template_dir / "voix.mp3").exists() or (self.template_dir / "voix.wav").exists()
        self.assertTrue(audio_exists, "Fichier audio (voix.mp3 ou voix.wav) manquant dans _template_prospect")


if __name__ == "__main__":
    unittest.main()
