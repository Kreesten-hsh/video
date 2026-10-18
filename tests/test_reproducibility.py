"""
Tests unitaires de reproductibilité et de protection contre l'écrasement.
"""

import os
import json
import wave
import shutil
import tempfile
import unittest
import numpy as np
from pathlib import Path

import make_video
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


if __name__ == "__main__":
    unittest.main()
