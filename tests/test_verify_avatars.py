import os
import unittest
import tempfile
import subprocess
from pathlib import Path

from render import verify_rendered_avatars


class TestVerifyRenderedAvatars(unittest.TestCase):
    """Tests unitaires pour la fonction verify_rendered_avatars avec projet factice."""

    @classmethod
    def setUpClass(cls):
        # Création de vidéos factices (noire et beige uni) pour tester la détection d'absence d'avatar
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.black_video = os.path.join(cls.temp_dir.name, "black.mp4")
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=1.0:r=30",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                cls.black_video
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

        cls.beige_video = os.path.join(cls.temp_dir.name, "beige.mp4")
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", "color=c=#F5F2EB:s=1080x1920:d=1.0:r=30",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                cls.beige_video
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )

        cls.beige_with_avatar_video = os.path.join(cls.temp_dir.name, "beige_avatar.mp4")
        avatar_path = Path(__file__).resolve().parent.parent / "assets" / "avatars" / "question.png"
        if avatar_path.exists():
            subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-f", "lavfi", "-i", "color=c=#F5F2EB:s=1080x1920:d=1.0:r=30",
                    "-i", str(avatar_path),
                    "-filter_complex", "[0:v][1:v]overlay=(W-w)/2:1250",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    cls.beige_with_avatar_video
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def test_empty_scenes_list(self):
        """Vérifie qu'une liste de scènes vide renvoie True sans erreur."""
        self.assertTrue(verify_rendered_avatars(self.black_video, []))

    def test_mock_two_scenes_without_avatar(self):
        """Vérifie qu'un projet factice de 2 scènes sans avatar passe sans erreur même sur fond noir."""
        mock_scenes = [
            {"id": "sc_01", "type": "big", "start": 0.0, "end": 0.5, "data": {"text": "Titre"}},
            {"id": "sc_02", "type": "cards", "start": 0.5, "end": 1.0, "data": {"cards": []}},
        ]
        self.assertTrue(verify_rendered_avatars(self.black_video, mock_scenes))

    def test_mock_two_scenes_detects_missing_avatar(self):
        """Vérifie qu'un projet factice de 2 scènes dont une avec avatar échoue sur une vidéo noire."""
        mock_scenes = [
            {"id": "sc_01", "type": "big", "start": 0.0, "end": 0.5, "data": {"text": "Titre"}},
            {"id": "sc_02", "type": "face", "start": 0.5, "end": 1.0, "data": {"avatar": "assets/avatars/stop.png"}},
        ]
        with self.assertRaises(AssertionError) as ctx:
            verify_rendered_avatars(self.black_video, mock_scenes)
        self.assertIn("scène sc_02", str(ctx.exception).lower())

    def test_mock_two_scenes_valid_video_passes(self):
        """Vérifie qu'un projet factice de 2 scènes passe sur la vidéo maître là où l'avatar est présent."""
        video_ref = os.path.join("studio_perso", "video_01_decouverte", "video1.mp4")
        if not os.path.exists(video_ref):
            self.skipTest("Aucune vidéo video1.mp4 trouvée dans video_01_decouverte pour le test de conformité.")

        # Dans la vidéo Découverte, la scène 1 (t=0.0) a l'avatar question.png et est valide
        mock_scenes = [
            {"id": "sc_01", "type": "face", "start": 0.0, "end": 0.5, "data": {"avatar": "assets/avatars/question.png"}},
            {"id": "sc_02", "type": "big", "start": 0.5, "end": 1.0, "data": {"text": "Suite"}},
        ]
        self.assertTrue(verify_rendered_avatars(video_ref, mock_scenes))

    def test_synthetic_beige_detects_missing_avatar(self):
        """Vérifie qu'un fond beige uniforme sans avatar échoue bien avec détection d'absence."""
        mock_scenes = [
            {"id": "sc_01", "type": "big", "start": 0.0, "end": 0.5, "data": {"text": "Titre"}},
            {"id": "sc_02", "type": "face", "start": 0.5, "end": 1.0, "data": {"avatar": "assets/avatars/question.png"}},
        ]
        with self.assertRaises(AssertionError) as ctx:
            verify_rendered_avatars(self.beige_video, mock_scenes)
        self.assertIn("scène sc_02", str(ctx.exception).lower())

    def test_synthetic_beige_with_avatar_passes(self):
        """Vérifie qu'un fond beige avec avatar présent est validé avec succès."""
        if not os.path.exists(self.beige_with_avatar_video):
            self.skipTest("Vidéo synthétique avec avatar non disponible.")
        mock_scenes = [
            {"id": "sc_01", "type": "face", "start": 0.0, "end": 0.8, "data": {"avatar": "assets/avatars/question.png"}},
        ]
        self.assertTrue(verify_rendered_avatars(self.beige_with_avatar_video, mock_scenes))

    def test_missing_cv2_and_pil_raises_runtime_error(self):
        """Vérifie qu'une RuntimeError explicite est levée si ni OpenCV ni PIL ne sont disponibles."""
        import sys
        from unittest.mock import patch
        mock_scenes = [
            {"id": "sc_01", "type": "face", "start": 0.0, "end": 0.5, "data": {"avatar": "assets/avatars/question.png"}},
        ]
        with patch.dict(sys.modules, {"cv2": None, "PIL": None, "PIL.Image": None}):
            with self.assertRaises(RuntimeError) as ctx:
                verify_rendered_avatars(self.black_video, mock_scenes)
            self.assertIn("ni OpenCV ni Pillow/NumPy", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
