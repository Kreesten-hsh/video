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
        # Création d'une vidéo factice noire de 1 seconde (30 fps) pour tester la détection d'absence d'avatar
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
        video_ref = "video1.mp4"
        if not os.path.exists(video_ref):
            video_ref = os.path.join("studio_perso", "video_01", "video1.mp4")
        if not os.path.exists(video_ref):
            self.skipTest("Aucune vidéo video1.mp4 trouvée pour le test de conformité.")

        # Dans la vidéo n°1, la scène 1 (t=0.0) a l'avatar stop.png et est valide
        mock_scenes = [
            {"id": "sc_01", "type": "face", "start": 0.0, "end": 0.5, "data": {"avatar": "assets/avatars/stop.png"}},
            {"id": "sc_02", "type": "big", "start": 0.5, "end": 1.0, "data": {"text": "Suite"}},
        ]
        self.assertTrue(verify_rendered_avatars(video_ref, mock_scenes))


if __name__ == "__main__":
    unittest.main()
