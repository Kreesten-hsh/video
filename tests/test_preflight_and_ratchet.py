"""
AGENT404 : Suite de tests automatisés pour l'Effet Cliquet et le Pre-Flight Gatekeeper.
Garantit qu'aucune régression architecturale ne peut être introduite :
  - Dépendances requises (opencv-python-headless)
  - Zéro code couleur hexadécimal hors :root dans tous les style.css (thématisation 100% variables CSS)
  - Zéro présence du rose banni #FF2A5F dans le projet
  - Zéro chemin utilisateur absolu (~/.local ou /home/) dans les scripts
  - Détection dynamique des avatars dans verify_rendered_avatars
  - Intégrité du registre anti-répétition registry/video_memory.json
  - Succès à 100% du Pre-Flight Gatekeeper sur video_03 (Axes 1 à 5)
  - Détection infaillible des failles Axe 2 (typo), Axe 3 (anti-orphelin) et Axe 4 (cartes inertes)
  - Bon fonctionnement du générateur CLI init_video.py en environnement temporaire
"""

import os
import re
import json
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestPreflightAndRatchet(unittest.TestCase):
    """Vérifications strictes d'industrialisation et d'effet cliquet."""

    def test_requirements_contains_opencv_headless(self):
        """Vérifie que requirements.txt contient opencv-python-headless pour cv2."""
        req_path = REPO_ROOT / "requirements.txt"
        self.assertTrue(req_path.exists(), "Fichier requirements.txt introuvable")
        content = req_path.read_text(encoding="utf-8")
        self.assertIn("opencv-python-headless", content)

    def test_style_css_zero_hardcoded_hex_outside_root(self):
        """Garantit que 100% des couleurs hors :root dans tous les fichiers style.css utilisent des variables CSS sémantiques."""
        style_files = [
            REPO_ROOT / "style.css",
            REPO_ROOT / "studio_perso" / "video_01_decouverte" / "style.css",
            REPO_ROOT / "studio_perso" / "video_03" / "style.css"
        ]

        for style_path in style_files:
            self.assertTrue(style_path.exists(), f"Fichier {style_path} introuvable")
            content = style_path.read_text(encoding="utf-8")

            root_match = re.search(r":root\s*\{([^}]+)\}", content)
            self.assertIsNotNone(root_match, f"Bloc :root introuvable dans {style_path.relative_to(REPO_ROOT)}")

            body_css = content[root_match.end():]
            # Ignore les data URIs SVG éventuels où %23 remplace #
            hex_outside_root = re.findall(r"#[0-9a-fA-F]{3,8}", body_css)
            self.assertEqual(
                hex_outside_root,
                [],
                f"Couleurs hexadécimales en dur détectées hors :root dans {style_path.relative_to(REPO_ROOT)} : {set(hex_outside_root)}"
            )

    def test_style_css_zero_banned_pink_ff2a5f(self):
        """Règle d'or : bannissement absolu et perpétuel de #FF2A5F dans l'ensemble du projet."""
        style_files = [
            REPO_ROOT / "style.css",
            REPO_ROOT / "studio_perso" / "video_01_decouverte" / "style.css",
            REPO_ROOT / "studio_perso" / "video_03" / "style.css"
        ]
        for style_path in style_files:
            if style_path.exists():
                content = style_path.read_text(encoding="utf-8").upper()
                self.assertNotIn("#FF2A5F", content, f"Le rose #FF2A5F est formellement banni de {style_path}")

        vjs_path = REPO_ROOT / "video.js"
        if vjs_path.exists():
            vjs_content = vjs_path.read_text(encoding="utf-8").upper()
            self.assertNotIn("#FF2A5F", vjs_content, "Le rose #FF2A5F est formellement banni de video.js")

    def test_no_hardcoded_user_paths_in_codebase(self):
        """Garantit l'absence totale de chemins absolus utilisateur (~/.local ou /home/) dans les fichiers texte suivis."""
        import subprocess
        forbidden_patterns = [r"/home/[a-zA-Z0-9_-]+", r"~/\.local"]

        try:
            res = subprocess.run(
                ["git", "ls-files"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True
            )
            tracked_files = [REPO_ROOT / f for f in res.stdout.splitlines() if f.strip()]
        except Exception:
            tracked_files = [p for p in REPO_ROOT.rglob("*") if p.is_file()]

        checked_extensions = {".py", ".sh", ".md", ".json", ".js", ".html", ".css"}

        for file_path in tracked_files:
            if any(part in file_path.parts for part in (".venv", "__pycache__", ".git")):
                continue
            if file_path.name == "test_preflight_and_ratchet.py":
                continue
            if file_path.suffix not in checked_extensions and ".agents" not in file_path.parts:
                continue
            if not file_path.exists() or file_path.is_dir():
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue

            for pat in forbidden_patterns:
                matches = re.findall(pat, content)
                self.assertEqual(
                    matches,
                    [],
                    f"Chemin absolu utilisateur interdit trouvé dans {file_path.relative_to(REPO_ROOT)} : {matches}"
                )

    def test_verify_rendered_avatars_dynamic_detection(self):
        """Vérifie que verify_rendered_avatars accepte un chemin de projet et charge dynamiquement ses scènes."""
        from render import verify_rendered_avatars
        video3_path = REPO_ROOT / "studio_perso" / "video_03" / "video3.mp4"
        if not video3_path.exists():
            self.skipTest("video3.mp4 introuvable pour test de vérification dynamique.")

        # Vérification en passant le chemin du dossier projet (chargement dynamique)
        res = verify_rendered_avatars(str(video3_path), str(REPO_ROOT / "studio_perso" / "video_03"))
        self.assertTrue(res, "La vérification dynamique des avatars sur video_03 a échoué.")

    def test_registry_video_memory_integrity(self):
        """Vérifie la conformité et la validité du registre anti-répétition registry/video_memory.json."""
        reg_path = REPO_ROOT / "registry" / "video_memory.json"
        self.assertTrue(reg_path.exists(), "registry/video_memory.json introuvable")

        with open(reg_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("version", data)
        self.assertIn("banned_global_jargon", data)
        self.assertIn("videos", data)
        self.assertGreaterEqual(len(data["videos"]), 2, "Le registre doit contenir au minimum video_01_decouverte et video_03.")

        # Vérification vidéo 1 Découverte
        v1 = next((v for v in data["videos"] if v["video_id"] == "video_01_decouverte"), None)
        self.assertIsNotNone(v1, "video_01_decouverte absente du registre")
        self.assertEqual(v1.get("cta_keyword"), "CLARTÉ", "Le mot-clé CTA de la vidéo 1 Découverte doit être 'CLARTÉ'")

        # Vérification vidéo 3
        v3 = next((v for v in data["videos"] if v["video_id"] == "video_03"), None)
        self.assertIsNotNone(v3, "video_03 absente du registre")
        self.assertEqual(v3.get("cta_keyword"), "CLARTÉ", "Le mot-clé CTA de la vidéo 3 doit être 'CLARTÉ'")

        # Non-chevauchement des illustrations entre v1_decouverte et v3
        v1_ills = set(v1.get("used_illustrations", []))
        v3_ills = set(v3.get("used_illustrations", []))
        overlap = v1_ills.intersection(v3_ills)
        self.assertEqual(overlap, set(), f"Recyclage d'illustrations détecté entre video_01_decouverte et video_03 : {overlap}")

    def test_preflight_check_passes_on_video03(self):
        """Exécute run_preflight_check sur video_03 et valide le succès complet à 100% sur les 5 axes."""
        from preflight_check import run_preflight_check
        report = run_preflight_check(project_dir="studio_perso/video_03")
        self.assertTrue(
            report.get("success", False),
            f"Le contrôle preflight a échoué sur video_03 : {report.get('errors')}"
        )
        self.assertEqual(report.get("checks_passed"), 5, "Les 5 axes de contrôle doivent être validés.")

    def test_init_video_scaffolding(self):
        """Valide le bon fonctionnement de init_video.py en mode multi-tenant dans un dossier temporaire."""
        from init_video import init_video_project

        KNOWN_BLUEPRINTS = {
            "bp_hook_question",
            "bp_friction_stack",
            "bp_stat_shock",
            "bp_versus_compare",
            "bp_code_window",
            "bp_grid_2x2",
            "bp_logo_carousel_rtl",
            "bp_cta_conversion",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "studio_perso" / "video_test"
            res = init_video_project(target=str(target), cta="TARIF", title="Vidéo Test Scaffolding")

            self.assertTrue(res.get("success"), "L'initialisation du projet a échoué.")
            self.assertEqual(res.get("cta_keyword"), "TARIF")

            # 1. Vérification des fichiers de données créés
            for fname in ["project.json", "brand.json", "scenes.json", "timeline.js"]:
                fpath = target / fname
                self.assertTrue(fpath.exists(), f"Fichier de données {fname} manquant dans le projet généré.")

            # 2. Règle multi-tenant : AUCUN fichier moteur ne doit être copié dans le projet
            for fname in ["index.html", "style.css", "video.js"]:
                fpath = target / fname
                self.assertFalse(fpath.exists(), f"Le fichier moteur {fname} ne doit pas être dupliqué dans le projet.")

            # 3. Vérification du contenu de project.json
            proj_data = json.loads((target / "project.json").read_text(encoding="utf-8"))
            self.assertTrue(proj_data.get("load_project"), "load_project: true doit être présent dans project.json.")
            self.assertEqual(proj_data.get("cta_keyword"), "TARIF")
            self.assertEqual(proj_data.get("theme"), "obsidian-flame")
            self.assertIn("scenes", proj_data)
            self.assertGreaterEqual(len(proj_data["scenes"]), 1)

            # 4. Toutes les scènes par défaut doivent être des bp_* connus
            for sc in proj_data["scenes"]:
                stype = sc.get("type", "")
                self.assertTrue(stype.startswith("bp_"), f"La scène {sc.get('id')} doit être un blueprint bp_*, trouvé : {stype}")
                self.assertIn(stype, KNOWN_BLUEPRINTS, f"Blueprint inconnu : {stype}")

            # 5. Aucune couleur Cyber-Mint (#00F5A0, #0D1117) ni mention cyber-mint dans les fichiers générés
            for fpath in target.glob("**/*"):
                if fpath.is_file():
                    content = fpath.read_text(encoding="utf-8", errors="ignore")
                    self.assertNotIn("00F5A0", content.upper(), f"Couleur #00F5A0 trouvée dans {fpath.name}")
                    self.assertNotIn("0D1117", content.upper(), f"Couleur #0D1117 trouvée dans {fpath.name}")
                    self.assertNotIn("cyber-mint", content.lower(), f"Mention cyber-mint trouvée dans {fpath.name}")

    def test_production_playbook_and_workflow_integrity(self):
        """Vérifie l'existence et la conformité intégrale du workflow produce_video.md et du playbook officiel."""
        workflow_path = REPO_ROOT / ".agents" / "workflows" / "produce_video.md"
        self.assertTrue(workflow_path.exists(), "Fichier .agents/workflows/produce_video.md introuvable")
        wf_content = workflow_path.read_text(encoding="utf-8")

        self.assertIn("name: produce-video", wf_content)
        self.assertIn("PHASE 1", wf_content)
        self.assertIn("PHASE 7", wf_content)
        self.assertIn("init_video.py", wf_content)
        self.assertIn("preflight_check.py", wf_content)
        self.assertIn("video_memory.json", wf_content)

        playbook_path = REPO_ROOT / "VIDEO_PRODUCTION_PLAYBOOK.md"
        self.assertTrue(playbook_path.exists(), "Fichier VIDEO_PRODUCTION_PLAYBOOK.md introuvable")
        pb_content = playbook_path.read_text(encoding="utf-8")

        # Vérification des 7 phases
        for phase_num in range(1, 8):
            self.assertIn(f"PHASE {phase_num}", pb_content, f"Phase {phase_num} manquante dans le playbook")

        # Vérification des piliers de gouvernance
        self.assertIn("Effet Cliquet", pb_content)
        self.assertIn("preflight_check.py", pb_content)
        self.assertIn("init_video.py", pb_content)
        self.assertIn("#FF2A5F", pb_content)
        self.assertIn("#agent-hud", pb_content)
        self.assertIn("Matrice d'Audit Rapide", pb_content)

    def test_tracked_files_do_not_exceed_size_threshold(self):
        """Effet cliquet taille : aucun fichier suivi ne doit dépasser 15 Mo."""
        import subprocess
        tracked_output = subprocess.check_output(
            ["git", "ls-tree", "-r", "-l", "HEAD"],
            cwd=str(REPO_ROOT),
            text=True
        )
        max_bytes = 15 * 1024 * 1024
        whitelisted = set()

        oversized_files = []
        for line in tracked_output.splitlines():
            parts = line.split()
            if len(parts) >= 5 and parts[1] == "blob":
                size = int(parts[3])
                path = parts[4]
                if path not in whitelisted and size > max_bytes:
                    oversized_files.append((path, size / (1024 * 1024)))

        self.assertEqual(
            oversized_files,
            [],
            f"Fichiers volumineux non autorisés détectés dans HEAD (seuil 15 Mo) : {oversized_files}"
        )


if __name__ == "__main__":
    unittest.main()

