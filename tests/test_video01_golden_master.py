"""
AGENT404 : Test automatisé de non-régression Golden Master (Vidéo n° 1 Découverte)
Protège les mots, les scènes et la cohérence de la timeline de référence.
Ce test effectue uniquement des vérifications en lecture seule et ne modifie aucun artefact.
"""

import os
import re
import io
import json
import shutil
import hashlib
import unittest
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_MASTER_DIR = REPO_ROOT / "tests" / "golden_master" / "video_01_decouverte"


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
    """Suite de non-régression pour la vidéo n° 1 Découverte AGENT404."""

    def setUp(self):
        self.manifest_path = GOLDEN_MASTER_DIR / "manifest.json"
        self.words_ref_path = GOLDEN_MASTER_DIR / "words.reference.json"
        self.scenes_ref_path = GOLDEN_MASTER_DIR / "scenes.reference.json"

        cand_timeline = REPO_ROOT / "studio_perso" / "video_01_decouverte" / "timeline.js"
        self.timeline_js_path = cand_timeline if cand_timeline.exists() else REPO_ROOT / "timeline.js"

        cand_words = REPO_ROOT / "studio_perso" / "video_01_decouverte" / "words.json"
        self.words_json_path = cand_words if cand_words.exists() else REPO_ROOT / "words.json"

        rel_video = "video1.mp4"
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, "r", encoding="utf-8") as f:
                    m_data = json.load(f)
                rel_video = m_data.get("measured_facts", {}).get("output_mp4", {}).get("path", "video1.mp4")
            except Exception:
                pass

        cand_vid_studio = REPO_ROOT / "studio_perso" / "video_01_decouverte" / Path(rel_video).name
        self.output_mp4_path = cand_vid_studio

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
                msg=f"Divergence mot #{idx} : actuel='{cur['word']}' vs référence='{ref['word']}'",
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

    def test_06_video_mp4_and_external_backup_integrity(self):
        """Vérifie l'intégrité de la vidéo de référence dans le dépôt si présente."""
        self.assertTrue(
            self.manifest_path.exists(), "manifest.json introuvable pour test d'intégrité"
        )
        if not self.output_mp4_path.exists():
            self.skipTest(f"Fichier vidéo non suivi dans le dépôt : {self.output_mp4_path}")

        # Si le fichier MP4 existe localement, vérification des faits techniques ffprobe
        ffprobe_bin = shutil.which("ffprobe") or str(REPO_ROOT / "bin" / "ffprobe")
        if not Path(ffprobe_bin).exists():
            self.skipTest("Binaire ffprobe introuvable pour vérification des faits vidéo")

        cmd = [
            ffprobe_bin, "-v", "error",
            "-show_entries", "stream=width,height,r_frame_rate,codec_name",
            "-of", "json",
            str(self.output_mp4_path)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(res.returncode, 0, f"Échec ffprobe : {res.stderr}")
        data = json.loads(res.stdout)
        streams = data.get("streams", [])
        v_stream = next((s for s in streams if s.get("codec_name") == "h264"), None)
        self.assertIsNotNone(v_stream, "Flux vidéo h264 introuvable")
        self.assertEqual(v_stream.get("width"), 1080)
        self.assertEqual(v_stream.get("height"), 1920)
        self.assertEqual(v_stream.get("r_frame_rate"), "30/1")

    def test_07_visual_reference_frames_tolerance(self):
        """Vérifie la conformité visuelle des 5 frames de référence avec tolérance mesurée (seuil diff > 40 <= 0.8%)."""
        ffmpeg_bin = shutil.which("ffmpeg") or str(REPO_ROOT / "bin" / "ffmpeg")
        if not Path(ffmpeg_bin).exists():
            self.skipTest("Binaire ffmpeg introuvable pour comparaison visuelle")

        if not self.output_mp4_path.exists():
            self.skipTest(f"{self.output_mp4_path.name} non suivi dans le dépôt (skip comparaison visuelle)")

        with open(self.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        ref_frames_meta = manifest["measured_facts"]["visual_reference_frames"]
        frames_to_check = [
            ("frame_01_0001s.png", ref_frames_meta["frame_01_0001s.png"]["timestamp"]),
            ("frame_02_1050s.png", ref_frames_meta["frame_02_1050s.png"]["timestamp"]),
            ("frame_03_2200s.png", ref_frames_meta["frame_03_2200s.png"]["timestamp"]),
            ("frame_04_4700s.png", ref_frames_meta["frame_04_4700s.png"]["timestamp"]),
            ("frame_05_6200s.png", ref_frames_meta["frame_05_6200s.png"]["timestamp"]),
        ]

        for frame_name, timestamp in frames_to_check:
            ref_path = GOLDEN_MASTER_DIR / frame_name
            self.assertTrue(ref_path.exists(), f"Image de référence introuvable : {frame_name}")
            ref_img = Image.open(ref_path).convert("RGB")
            ref_arr = np.array(ref_img, dtype=np.int32)

            cmd = [
                ffmpeg_bin, "-y", "-ss", str(timestamp), "-i", str(self.output_mp4_path),
                "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(res.returncode, 0, f"Échec extraction ffmpeg pour {frame_name} à t={timestamp}s")

            cur_img = Image.open(io.BytesIO(res.stdout)).convert("RGB")
            cur_arr = np.array(cur_img, dtype=np.int32)

            self.assertEqual(ref_arr.shape, cur_arr.shape, f"Dimensions divergentes pour {frame_name}")

            diff = np.abs(cur_arr - ref_arr)
            max_channel_diff = np.max(diff, axis=-1)
            diff_ratio = np.mean(max_channel_diff > 40) * 100.0

            # Tolérance mesurée : écarts observés entre 0.28% et 0.72%, seuil max 0.8%
            self.assertLessEqual(
                diff_ratio,
                0.8,
                f"Écart visuel excessif pour {frame_name} à t={timestamp}s : {diff_ratio:.4f}% > 0.8% (seuil max toléré)",
            )


if __name__ == "__main__":
    unittest.main()
