import os
import re
import json
import wave
import shutil
import subprocess
import tempfile
import unittest
import numpy as np
from pathlib import Path

import make_video
import render
import sfx

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestReproducibility(unittest.TestCase):
    """Tests vérifiant le respect des règles de gel, d'isolation de sortie et de reproductibilité."""

    def test_frozen_project_refusal_without_forcer_and_execution_with_sortie(self):
        """Vérifie le refus d'écrasement sur projet gelé sans --forcer et l'exécution sans altération avec --sortie."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            p_dir = tmp_path / "projet_factice"
            p_dir.mkdir()
            out_dir = tmp_path / "sortie_isolee"
            out_dir.mkdir()

            # Création d'un audio WAV court de 0.5s (22050 échantillons)
            wav_path = p_dir / "audio.wav"
            with wave.open(str(wav_path), "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(44100)
                samples = np.zeros(22050, dtype=np.int16)
                wf.writeframes(samples.tobytes())

            # Transcription factice pour éviter Whisper
            words = [
                {"word": "Test", "start": 0.0, "end": 0.25},
                {"word": "court.", "start": 0.25, "end": 0.5}
            ]
            with open(p_dir / "words.json", "w", encoding="utf-8") as f:
                json.dump(words, f)

            # Configuration project.json avec gele: true
            p_data = {
                "video_number": 1,
                "title": "Projet Factice Test",
                "audio_path": str(wav_path),
                "gele": True,
                "reference_words": ["Test", "court."],
                "scenes": [
                    {"type": "big", "data": {"text": "A", "bg": "grid"}},
                    {"type": "big", "data": {"text": "B", "bg": "grid"}}
                ],
                "scene_end_words": ["Test", "court."],
                "phonetic_map": {}
            }
            with open(p_dir / "project.json", "w", encoding="utf-8") as f:
                json.dump(p_data, f)

            # 1. Vérification du refus immédiat sans --forcer ni --sortie
            with self.assertRaises(SystemExit) as ctx:
                make_video.make_video(str(p_dir))
            self.assertEqual(ctx.exception.code, 1)

            # 2. Vérification de l'exécution propre avec --sortie sans modifier le dossier projet
            p_files_before = set(os.listdir(p_dir))
            make_video.make_video(str(p_dir), output_dir=str(out_dir))
            p_files_after = set(os.listdir(p_dir))

            self.assertEqual(
                p_files_before,
                p_files_after,
                f"Le dossier du projet a été altéré lors du rendu redirigé : {p_files_after - p_files_before}"
            )
            self.assertTrue((out_dir / "video1.mp4").exists(), "Vidéo de sortie non générée dans --sortie")
            self.assertTrue((out_dir / "timeline.js").exists(), "Timeline non générée dans --sortie")
            self.assertTrue((out_dir / "audio_final.wav").exists(), "Audio final non généré dans --sortie")

    @unittest.skipIf(
        os.environ.get("AGENT404_SKIP_SLOW") in ("1", "true", "True"),
        "Test de rendu vidéo 6s sauté car AGENT404_SKIP_SLOW est actif."
    )
    def test_deterministic_render_six_seconds(self):
        """Vérifie que deux rendus successifs de 6 secondes avec rendu_deterministe=True sont identiques bit-à-bit."""
        v1_dir = REPO_ROOT / "studio_perso" / "video_01"
        audio_src = v1_dir / "audio_final.wav"
        if not audio_src.exists():
            self.skipTest(f"Audio source {audio_src} non disponible.")

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            audio_6s = tmp_path / "audio_6s.wav"

            # 1. Troncature audio à 6s
            subprocess.run([
                "ffmpeg", "-y", "-i", str(audio_src),
                "-t", "6.0",
                "-c:a", "pcm_s16le",
                str(audio_6s)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # 2. Timeline tronquée à 6s
            with open(v1_dir / "words.json", "r", encoding="utf-8") as f:
                all_words = json.load(f)
            words_6s = [w for w in all_words if w["start"] < 6.0]
            for w in words_6s:
                if w["end"] > 6.0:
                    w["end"] = 6.0

            with open(v1_dir / "timeline.js", "r", encoding="utf-8") as f:
                t_content = f.read()
            m = re.search(r"window\.SCENES\s*=\s*(\[.*?\]);", t_content, re.DOTALL)
            all_scenes = json.loads(m.group(1))
            scenes_6s = []
            for sc in all_scenes:
                if sc["start"] < 6.0:
                    sc_copy = dict(sc)
                    if sc_copy["end"] > 6.0:
                        sc_copy["end"] = 6.0
                    scenes_6s.append(sc_copy)

            timeline_6s = tmp_path / "timeline.js"
            with open(timeline_6s, "w", encoding="utf-8") as f:
                f.write(f"window.WORDS = {json.dumps(words_6s, ensure_ascii=False)};\n")
                f.write(f"window.SCENES = {json.dumps(scenes_6s, ensure_ascii=False)};\n")

            out_run1 = tmp_path / "render1.mp4"
            out_run2 = tmp_path / "render2.mp4"

            render.render_video(
                project_path=None,
                html_path=str(REPO_ROOT / "index.html"),
                audio_path=str(audio_6s),
                timeline_path=str(timeline_6s),
                output_path=str(out_run1),
                fps=30,
                verify_avatars=False,
                scenes=scenes_6s,
                rendu_deterministe=True
            )

            render.render_video(
                project_path=None,
                html_path=str(REPO_ROOT / "index.html"),
                audio_path=str(audio_6s),
                timeline_path=str(timeline_6s),
                output_path=str(out_run2),
                fps=30,
                verify_avatars=False,
                scenes=scenes_6s,
                rendu_deterministe=True
            )

            # Vérification des images décodées via framemd5
            md5_1 = subprocess.check_output([
                "ffmpeg", "-v", "error", "-i", str(out_run1), "-f", "framemd5", "-"
            ]).decode()
            md5_2 = subprocess.check_output([
                "ffmpeg", "-v", "error", "-i", str(out_run2), "-f", "framemd5", "-"
            ]).decode()

            self.assertEqual(
                md5_1, md5_2,
                "Les images décodées des deux rendus déterministes de 6s ne sont pas strictement identiques !"
            )

            # Vérification PSNR infini
            psnr_output = subprocess.check_output([
                "ffmpeg", "-i", str(out_run1), "-i", str(out_run2),
                "-lavfi", "psnr", "-f", "null", "-"
            ], stderr=subprocess.STDOUT).decode()

            self.assertIn("average:inf", psnr_output, f"Le PSNR entre les deux rendus n'est pas infini : {psnr_output}")


if __name__ == "__main__":
    unittest.main()
