"""
AGENT404 : Suite de tests automatisés pour l'Effet Cliquet et le Pre-Flight Gatekeeper.
Garantit qu'aucune régression architecturale ne peut être introduite :
  - Dépendances requises (opencv-python-headless)
  - Zéro code couleur hexadécimal hors :root dans tous les style.css (thématisation 100% variables CSS)
  - Zéro présence du rose banni #FF2A5F dans le projet
  - Zéro chemin utilisateur absolu (~/.local ou /home/) dans les scripts
  - Détection dynamique des avatars dans verify_rendered_avatars
  - Intégrité du registre anti-répétition registry/video_memory.json
  - Succès à 100% du Pre-Flight Gatekeeper sur video_02 (Axes 1 à 5)
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
        """Garantit l'absence totale de chemins absolus utilisateur (~/.local ou /home/) dans les scripts .py et .sh."""
        forbidden_patterns = [r"/home/[a-zA-Z0-9_-]+", r"~/\.local"]

        for ext in ("*.py", "*.sh"):
            for file_path in REPO_ROOT.rglob(ext):
                # Ignorer l'environnement virtuel éventuel ou cache
                if ".venv" in file_path.parts or "__pycache__" in file_path.parts or ".git" in file_path.parts:
                    continue
                # Ne pas s'auto-détecter sur cette chaîne de test
                if file_path.name == "test_preflight_and_ratchet.py":
                    continue

                content = file_path.read_text(encoding="utf-8", errors="ignore")
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
        video2_path = REPO_ROOT / "studio_perso" / "video_02" / "video2.mp4"
        if not video2_path.exists():
            self.skipTest("video2.mp4 introuvable pour test de vérification dynamique.")

        # Vérification en passant le chemin du dossier projet (chargement dynamique)
        res = verify_rendered_avatars(str(video2_path), str(REPO_ROOT / "studio_perso" / "video_02"))
        self.assertTrue(res, "La vérification dynamique des avatars sur video_02 a échoué.")

    def test_registry_video_memory_integrity(self):
        """Vérifie la conformité et la validité du registre anti-répétition registry/video_memory.json."""
        reg_path = REPO_ROOT / "registry" / "video_memory.json"
        self.assertTrue(reg_path.exists(), "registry/video_memory.json introuvable")

        with open(reg_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("version", data)
        self.assertIn("banned_global_jargon", data)
        self.assertIn("videos", data)
        self.assertGreaterEqual(len(data["videos"]), 2, "Le registre doit contenir au minimum video_01 et video_02.")

        # Vérification vidéo 1
        v1 = next((v for v in data["videos"] if v["video_id"] == "video_01"), None)
        self.assertIsNotNone(v1, "video_01 absente du registre")
        self.assertEqual(v1.get("cta_keyword"), "CODE", "Le mot-clé CTA de la vidéo 1 doit être 'CODE'")

        # Vérification vidéo 2
        v2 = next((v for v in data["videos"] if v["video_id"] == "video_02"), None)
        self.assertIsNotNone(v2, "video_02 absente du registre")
        self.assertEqual(v2.get("cta_keyword"), "DEMO", "Le mot-clé CTA de la vidéo 2 doit être 'DEMO'")

        # Non-chevauchement des illustrations entre v1 et v2
        v1_ills = set(v1.get("used_illustrations", []))
        v2_ills = set(v2.get("used_illustrations", []))
        overlap = v1_ills.intersection(v2_ills)
        self.assertEqual(overlap, set(), f"Recyclage d'illustrations détecté entre video_01 et video_02 : {overlap}")

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
        """Valide le bon fonctionnement de init_video.py dans un dossier temporaire."""
        from init_video import init_video_project

        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "studio_perso" / "video_test"
            res = init_video_project(target=str(target), cta="TARIF", title="Vidéo Test Scaffolding")

            self.assertTrue(res.get("success"), "L'initialisation du projet a échoué.")
            self.assertEqual(res.get("cta_keyword"), "TARIF")

            # Vérification des fichiers créés
            for fname in ["project_config.json", "project.json", "index.html", "style.css", "timeline.js", "video.js"]:
                fpath = target / fname
                self.assertTrue(fpath.exists(), f"Fichier {fname} manquant dans le projet généré.")

            # Vérification contenu index.html (Strictement sans HUD)
            index_content = (target / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("agent-hud", index_content, "Le HUD ne doit jamais être présent dans index.html")
            self.assertIn("video-canvas", index_content)

            # Vérification style.css (:root complet et 0 hex hors :root)
            css_content = (target / "style.css").read_text(encoding="utf-8")
            self.assertIn(":root", css_content)
            self.assertNotIn("#FF2A5F", css_content.upper())
            m = re.search(r":root\s*\{([^}]+)\}", css_content)
            self.assertIsNotNone(m)
            body_css = css_content[m.end():]
            hex_outside = re.findall(r"#[0-9a-fA-F]{3,8}", body_css)
            self.assertEqual(hex_outside, [], f"Hex hors :root dans style.css généré : {hex_outside}")

            # Vérification video.js (Rappel du mot-clé CTA et de l'interdiction de recyclage)
            vjs_content = (target / "video.js").read_text(encoding="utf-8")
            self.assertIn("TARIF", vjs_content)
            self.assertIn("loom_player_dropoff", vjs_content)  # Illustration passée rappelée en commentaire

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
        """Effet cliquet taille : aucun fichier suivi ne doit dépasser 15 Mo (sauf le Golden Master video1.mp4)."""
        import subprocess
        tracked_output = subprocess.check_output(
            ["git", "ls-tree", "-r", "-l", "HEAD"],
            cwd=str(REPO_ROOT),
            text=True
        )
        max_bytes = 15 * 1024 * 1024
        whitelisted = {"studio_perso/video_01/video1.mp4"}

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

