"""
AGENT404 : Test de cohérence globale de la documentation et gouvernance.
Vérifie :
  1. Validité absolue de tous les liens relatifs entre fichiers .md de la racine et docs/
  2. Absence totale des motifs interdits : 250 € / 500 € / Pilote / Cyber-Mint / 00F5A0 / 0D1117 / video_02 / tirets cadratin (— / –)
  3. Concordance des offres réelles (150 €, 750 €, 200 €) et des dates (28 octobre 2026).
"""

import re
import unittest
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestDocsConsistency(unittest.TestCase):
    """Contrôle d'intégrité et de cohérence de l'ensemble des documentations."""

    def test_relative_links_in_docs(self):
        """Vérifie que tous les liens relatifs des .md de la racine et docs/ pointent vers des cibles existantes."""
        doc_dirs = [REPO_ROOT, REPO_ROOT / "docs"]
        broken_links = []
        tested_links_count = 0

        for d in doc_dirs:
            for md_file in d.glob("*.md"):
                text = md_file.read_text(encoding="utf-8")
                # Recherche des liens markdown [label](cible)
                matches = re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text)
                for m in matches:
                    target_raw = m.group(2).strip()
                    # Ignorer liens externes et ancres pures
                    if (
                        target_raw.startswith("http://")
                        or target_raw.startswith("https://")
                        or target_raw.startswith("mailto:")
                        or target_raw.startswith("#")
                    ):
                        continue
                    # Retirer l'ancre éventuelle
                    target_path_str = target_raw.split("#")[0]
                    if not target_path_str:
                        continue

                    target_path = (md_file.parent / target_path_str).resolve()
                    tested_links_count += 1
                    if not target_path.exists():
                        broken_links.append(f"{md_file.relative_to(REPO_ROOT)} -> lien rompu vers '{target_raw}'")

        self.assertEqual(broken_links, [], f"Liens rompus détectés dans la documentation :\n" + "\n".join(broken_links))
        self.assertGreater(tested_links_count, 10, "Au moins 10 liens relatifs doivent être audités.")

    def test_no_forbidden_patterns_in_project_docs(self):
        """Vérifie l'absence totale de motifs interdits ou obsolètes dans tous les .md suivis du projet."""
        try:
            res = subprocess.check_output(
                ["git", "ls-files", "*.md", ":!:references/*", ":!.agents/skills/*"],
                cwd=REPO_ROOT
            ).decode("utf-8")
            tracked_md_files = [REPO_ROOT / line.strip() for line in res.splitlines() if line.strip()]
        except Exception:
            tracked_md_files = [p for p in REPO_ROOT.glob("**/*.md") if "references" not in p.parts and ".agents/skills" not in str(p)]

        forbidden_patterns = [
            (r"(?<![0-9]\s)(?<![0-9])250\s*€", "tarif obsolète 250 €"),
            (r"(?<![0-9]\s)(?<![0-9])500\s*€", "tarif obsolète 500 €"),
            (r"\bPilote\b", "nom d'ancienne offre 'Pilote'"),
            (r"Cyber-Mint", "palette abandonnée 'Cyber-Mint'"),
            (r"00F5A0", "code hexadécimal abandonné #00F5A0"),
            (r"0D1117", "code hexadécimal abandonné #0D1117"),
            (r"video_02", "référence au projet supprimé video_02"),
            (r"[—–]", "tiret cadratin (—) ou demi-cadratin (–)"),
        ]

        violations = []
        for md_path in tracked_md_files:
            if not md_path.exists():
                continue
            content = md_path.read_text(encoding="utf-8", errors="ignore")
            for pattern, desc in forbidden_patterns:
                m = re.search(pattern, content)
                if m:
                    rel = md_path.relative_to(REPO_ROOT)
                    violations.append(f"{rel}: contient {desc} -> {m.group(0)!r}")

        self.assertEqual(violations, [], f"Motifs interdits trouvés dans la documentation :\n" + "\n".join(violations))

    def test_offers_and_dates_consistency(self):
        """Vérifie la cohérence stricte des offres et dates sur les documents directeurs."""
        offres_text = (REPO_ROOT / "OFFRES.md").read_text(encoding="utf-8")
        readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        arch_text = (REPO_ROOT / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
        fin_text = (REPO_ROOT / "docs" / "FINANCIAL_PLAN.md").read_text(encoding="utf-8")

        # Offres obligatoires
        for doc_name, text in [("OFFRES.md", offres_text), ("README.md", readme_text)]:
            self.assertIn("150 €", text, f"Test Découverte 150 € manquant dans {doc_name}")
            self.assertIn("750 €", text, f"Abonnement Studio 750 € manquant dans {doc_name}")
            self.assertIn("200 €", text, f"Ancre 200 € manquante dans {doc_name}")

        # Date 28 octobre 2026 sur les documents directeurs
        self.assertIn("28 octobre 2026", offres_text)
        self.assertIn("28 octobre 2026", arch_text)
        self.assertIn("28 octobre 2026", fin_text)

        # Trésorerie 0 € encaissés à date
        self.assertIn("0 € encaissés à ce jour", fin_text)


if __name__ == "__main__":
    unittest.main()
