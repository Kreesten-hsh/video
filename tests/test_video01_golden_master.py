"""
AGENT404 — Test automatisé de non-régression Golden Master (Vidéo n° 1)
Protège les 220 mots, les 35 scènes et la cohérence de la timeline de référence.
Ce test effectue uniquement des vérifications en lecture seule et ne modifie aucun artefact.
"""

import os
import re
import json
import hashlib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_MASTER_DIR = REPO_ROOT / "tests" / "golden_master" / "video_01"


def extract_timeline_js_data(timeline_path: Path):
    """
    Extrait window.WORDS et window.SCENES depuis timeline.js de manière robuste
    en isolant les structures JSON délimitées par point-virgule.
    """
    if not timeline_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {timeline_path}")

    content = timeline_path.read_text(encoding="utf-8")

    words_match = re.search(r"window\.WORDS\s*=\s*(\[.*?\]);", content, re.DOTALL)
    if not words_match:
        raise ValueError(f"Impossible d'extraire 'window.WORDS' depuis {timeline_path}")

    scenes_match = re.search(r"window\.SCENES\s*=\s*(\[.*?\]);", content, re.DOTALL)
    if not scenes_match:
        raise ValueError(f"Impossible d'extraire 'window.SCENES' depuis {timeline_path}")

    words = json.loads(words_match.group(1))
    scenes = json.loads(scenes_match.group(1))
    return words, scenes


def compute_sha256(file_path: Path) -> str:
    """Calcule l'empreinte SHA-256 d'un fichier en lecture binaire par blocs."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()


class TestVideo01GoldenMaster(unittest.TestCase):
    """Suite de non-régression pour la vidéo n° 1 AGENT404."""

    def setUp(self):
        self.manifest_path = GOLDEN_MASTER_DIR / "manifest.json"
        self.words_ref_path = GOLDEN_MASTER_DIR / "words.reference.json"
        self.scenes_ref_path = GOLDEN_MASTER_DIR / "scenes.reference.json"
        self.timeline_js_path = REPO_ROOT / "timeline.js"
        self.words_json_path = REPO_ROOT / "words.json"
        self.output_mp4_path = REPO_ROOT / "output.mp4"

    def test_01_reference_artifacts_exist(self):
        """Vérifie la présence et la non-vacuité de tous les artefacts Golden Master."""
        self.assertTrue(
            self.manifest_path.exists(),
            f"Manifeste manquant : {self.manifest_path}",
        )
        self.assertTrue(
            self.words_ref_path.exists(),
            f"Fichier de référence des mots manquant : {self.words_ref_path}",
        )
        self.assertTrue(
            self.scenes_ref_path.exists(),
            f"Fichier de référence des scènes manquant : {self.scenes_ref_path}",
        )

        expected_frames = [
            "frame_01_0001s.png",
            "frame_02_1050s.png",
            "frame_03_2200s.png",
            "frame_04_4700s.png",
            "frame_05_6200s.png",
        ]
        for frame_name in expected_frames:
            frame_path = GOLDEN_MASTER_DIR / frame_name
            self.assertTrue(
                frame_path.exists(),
                f"Frame de référence visuelle manquante : {frame_name}",
            )
            self.assertGreater(
                frame_path.stat().st_size,
                1000,
                f"Frame de référence anormalement petite ou vide : {frame_name}",
            )

    def test_02_current_words_match_golden_reference(self):
        """Vérifie que words.json correspond exactement au Golden Master (ordre, texte, timestamps)."""
        self.assertTrue(
            self.words_json_path.exists(),
            f"Fichier words.json introuvable : {self.words_json_path}",
        )

        with open(self.words_json_path, "r", encoding="utf-8") as f:
            cur_words = json.load(f)

        with open(self.words_ref_path, "r", encoding="utf-8") as f:
            ref_words = json.load(f)

        self.assertEqual(
            len(cur_words),
            len(ref_words),
            f"Écart sur le nombre de mots : actuel={len(cur_words)} vs référence={len(ref_words)}",
        )

        for idx, (cur, ref) in enumerate(zip(cur_words, ref_words)):
            self.assertEqual(
                cur["word"],
                ref["word"],
                f"Divergence lexicale au mot #{idx} : actuel='{cur['word']}' vs référence='{ref['word']}'",
            )
            self.assertAlmostEqual(
                float(cur["start"]),
                float(ref["start"]),
                places=3,
                msg=f"Divergence timestamp start au mot #{idx} '{cur['word']}' : {cur['start']}s vs {ref['start']}s",
            )
            self.assertAlmostEqual(
                float(cur["end"]),
                float(ref["end"]),
                places=3,
                msg=f"Divergence timestamp end au mot #{idx} '{cur['word']}' : {cur['end']}s vs {ref['end']}s",
            )
            self.assertLess(
                float(cur["start"]),
                float(cur["end"]),
                msg=f"Timestamp invalide au mot #{idx} '{cur['word']}' : start ({cur['start']}) >= end ({cur['end']})",
            )

    def test_03_timeline_js_concordance_with_words_json(self):
        """Vérifie que window.WORDS dans timeline.js est en stricte concordance avec words.json."""
        self.assertTrue(
            self.timeline_js_path.exists(),
            f"Fichier timeline.js introuvable : {self.timeline_js_path}",
        )

        timeline_words, _ = extract_timeline_js_data(self.timeline_js_path)

        with open(self.words_json_path, "r", encoding="utf-8") as f:
            direct_words = json.load(f)

        self.assertEqual(
            len(timeline_words),
            len(direct_words),
            f"Nombre de mots divergent entre timeline.js ({len(timeline_words)}) et words.json ({len(direct_words)})",
        )

        for idx, (tw, dw) in enumerate(zip(timeline_words, direct_words)):
            self.assertEqual(
                tw["word"],
                dw["word"],
                f"Incohérence interne mot #{idx} : timeline.js='{tw['word']}' vs words.json='{dw['word']}'",
            )
            self.assertAlmostEqual(
                float(tw["start"]),
                float(dw["start"]),
                places=3,
                msg=f"Incohérence start mot #{idx} : timeline.js={tw['start']} vs words.json={dw['start']}",
            )
            self.assertAlmostEqual(
                float(tw["end"]),
                float(dw["end"]),
                places=3,
                msg=f"Incohérence end mot #{idx} : timeline.js={tw['end']} vs words.json={dw['end']}",
            )

    def test_04_current_scenes_match_golden_reference(self):
        """Vérifie que window.SCENES dans timeline.js correspond exactement au Golden Master."""
        _, cur_scenes = extract_timeline_js_data(self.timeline_js_path)

        with open(self.scenes_ref_path, "r", encoding="utf-8") as f:
            ref_scenes = json.load(f)

        self.assertEqual(
            len(cur_scenes),
            len(ref_scenes),
            f"Nombre de scènes divergent : actuel={len(cur_scenes)} vs référence={len(ref_scenes)}",
        )

        for idx, (cur, ref) in enumerate(zip(cur_scenes, ref_scenes)):
            self.assertEqual(
                cur["id"],
                ref["id"],
                f"Divergence identifiant scène #{idx} : actuel='{cur['id']}' vs référence='{ref['id']}'",
            )
            self.assertEqual(
                cur["type"],
                ref["type"],
                f"Divergence type scène #{idx} ('{cur['id']}') : actuel='{cur['type']}' vs référence='{ref['type']}'",
            )
            self.assertAlmostEqual(
                float(cur["start"]),
                float(ref["start"]),
                places=3,
                msg=f"Divergence début scène #{idx} ('{cur['id']}') : actuel={cur['start']}s vs référence={ref['start']}s",
            )
            self.assertAlmostEqual(
                float(cur["end"]),
                float(ref["end"]),
                places=3,
                msg=f"Divergence fin scène #{idx} ('{cur['id']}') : actuel={cur['end']}s vs référence={ref['end']}s",
            )
            self.assertEqual(
                cur["data"],
                ref["data"],
                f"Divergence données de scène #{idx} ('{cur['id']}') : actuel={cur['data']} vs référence={ref['data']}",
            )

    def test_05_scenes_temporal_continuity(self):
        """Vérifie l'absence absolue de trous et de chevauchements entre scènes consécutives."""
        _, cur_scenes = extract_timeline_js_data(self.timeline_js_path)

        self.assertGreater(len(cur_scenes), 0, "Aucune scène trouvée dans timeline.js")
        self.assertEqual(
            float(cur_scenes[0]["start"]),
            0.0,
            f"La première scène doit débuter à 0.0s (trouvé: {cur_scenes[0]['start']}s)",
        )

        for idx in range(len(cur_scenes)):
            sc = cur_scenes[idx]
            s = float(sc["start"])
            e = float(sc["end"])
            self.assertLess(
                s,
                e,
                f"Scène #{idx} ('{sc['id']}') durée négative ou nulle : [{s}s -> {e}s]",
            )
            if idx > 0:
                prev_e = float(cur_scenes[idx - 1]["end"])
                diff = abs(s - prev_e)
                self.assertLessEqual(
                    diff,
                    0.001,
                    f"Rupture de continuité entre scène {idx-1} (fin {prev_e}s) et scène {idx} (début {s}s, écart={diff:.4f}s)",
                )

    def test_06_external_backup_and_output_mp4_integrity(self):
        """Vérifie l'intégrité de la sauvegarde externe et du fichier output.mp4."""
        self.assertTrue(
            self.manifest_path.exists(), "manifest.json introuvable pour test d'intégrité"
        )
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        backup_info = manifest["measured_facts"]["external_backup"]
        backup_path = Path(backup_info["absolute_path"])
        expected_sha = backup_info["sha256"]

        self.assertTrue(
            backup_path.exists(),
            f"Fichier de sauvegarde externe introuvable : {backup_path}",
        )
        self.assertEqual(
            backup_path.stat().st_size,
            backup_info["size_bytes"],
            "La taille du fichier de sauvegarde externe a été altérée",
        )

        backup_sha = compute_sha256(backup_path)
        self.assertEqual(
            backup_sha,
            expected_sha,
            "L'empreinte SHA-256 de la sauvegarde externe ne correspond pas au manifeste",
        )

        if self.output_mp4_path.exists():
            original_sha = compute_sha256(self.output_mp4_path)
            self.assertEqual(
                original_sha,
                expected_sha,
                "output.mp4 dans le dépôt a été modifié par rapport à sa référence de sauvegarde",
            )


if __name__ == "__main__":
    unittest.main()
