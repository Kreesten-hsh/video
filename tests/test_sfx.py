"""
AGENT404 - Tests unitaires du moteur de Sound Design SFX (sfx.py)
Vérifie le découplage temporel total, les repères déclaratifs relatifs,
la préservation déterministe et l'absence de régression acoustique.
"""

import unittest
import tempfile
import hashlib
from pathlib import Path

import sfx


class TestSfxEngine(unittest.TestCase):
    """Suite de validation du moteur acoustique et repères sonores déclaratifs."""

    def test_declarative_sfx_cues_structure(self):
        """Vérifie la validité structurelle de la table déclarative SFX_CUES."""
        self.assertIsInstance(sfx.SFX_CUES, dict)
        valid_sfx_types = {"pop", "whoosh", "stamp", "click"}

        for sc_type, cues in sfx.SFX_CUES.items():
            self.assertIsInstance(cues, list, f"Cues pour {sc_type} doit être une liste")
            for cue in cues:
                self.assertEqual(len(cue), 3, f"Chaque repère doit être un triplet (type, offset, gain) dans {sc_type}")
                sfx_name, offset, gain = cue
                self.assertIn(sfx_name, valid_sfx_types, f"Type SFX '{sfx_name}' inconnu dans {sc_type}")
                self.assertGreaterEqual(offset, 0.0, f"Offset négatif interdit ({offset}) dans {sc_type}")
                self.assertGreater(gain, 0.0, f"Gain invalide ({gain}) dans {sc_type}")

    def test_platforms_popin_exact_relative_offsets(self):
        """Vérifie que ob_platforms_popin utilise strictement les décalages relatifs (0.0, 0.64, 1.34, 1.94)."""
        sc = {
            "type": "ob_platforms_popin",
            "start": 10.0,
            "end": 20.0,
            "data": {},
        }
        cues = sfx.get_scene_cues(sc)
        whoosh_offsets = [round(dt, 2) for sfx_type, dt, _ in cues if sfx_type == "whoosh"]
        expected_offsets = [0.0, 0.64, 1.34, 1.94]
        self.assertEqual(whoosh_offsets, expected_offsets)

    def test_scene_shift_shifts_cues_by_exact_offset(self):
        """
        Règle d'or : le décalage temporel d'une scène de +10s décale l'ensemble
        de ses repères acoustiques absolus de rigoureusement +10s.
        """
        test_scenes = [
            {
                "type": "ob_platforms_popin",
                "start": 5.0,
                "end": 12.0,
                "data": {},
            },
            {
                "type": "ob_final_delivery_cta",
                "start": 20.0,
                "end": 25.0,
                "data": {},
            },
            {
                "type": "bp_friction_stack",
                "start": 15.0,
                "end": 22.0,
                "params": {
                    "items": [
                        {"appear_at_offset": 0.0},
                        {"appear_at_offset": 1.2},
                        {"appear_at_offset": 2.5},
                    ]
                },
            },
            {
                "type": "bp_logo_carousel_rtl",
                "start": 30.0,
                "end": 40.0,
                "params": {
                    "items": [
                        {"logo": "a", "at_time": 0.0},
                        {"logo": "b", "at_time": 1.5},
                        {"logo": "c", "at_time": 3.0},
                    ]
                },
            },
            {
                "type": "ob_three_struggles_stack",
                "start": 8.0,
                "end": 14.0,
                "data": {},
            },
        ]

        time_shift = 10.0

        for sc in test_scenes:
            with self.subTest(scene_type=sc["type"]):
                cues_orig = sfx.get_absolute_scene_cues(sc)
                self.assertGreater(len(cues_orig), 0, f"La scène {sc['type']} doit avoir des repères sonores")

                shifted_sc = dict(sc)
                shifted_sc["start"] = sc["start"] + time_shift
                shifted_sc["end"] = sc["end"] + time_shift
                if "params" in sc:
                    shifted_sc["params"] = sc["params"]

                cues_shifted = sfx.get_absolute_scene_cues(shifted_sc)
                self.assertEqual(len(cues_orig), len(cues_shifted))

                for (sfx1, t1, g1), (sfx2, t2, g2) in zip(cues_orig, cues_shifted):
                    self.assertEqual(sfx1, sfx2)
                    self.assertEqual(g1, g2)
                    self.assertAlmostEqual(t2 - t1, time_shift, places=5)

    def test_deterministic_audio_hash_baseline(self):
        """Vérifie l'invariance absolue bit-à-bit des rendus audio de référence."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_v1 = Path(tmp_dir) / "v1_audio.wav"
            sfx.mix_sfx(project_path="studio_perso/video_01_decouverte", out_path=str(out_v1))
            with open(out_v1, "rb") as f:
                h1 = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(
                h1,
                "af2ae496414ad6380988d86d7d893386e718026cce51a3272c0e5ec620e6d038",
                "Régression acoustique détectée sur studio_perso/video_01_decouverte",
            )

            out_v3 = Path(tmp_dir) / "v3_audio.wav"
            sfx.mix_sfx(project_path="studio_perso/video_03", out_path=str(out_v3))
            with open(out_v3, "rb") as f:
                h3 = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(
                h3,
                "4ea3ab807f11cebde3f7b788292a2dab8d7d8dc9768c7aba273b1ef55146f05f",
                "Régression acoustique détectée sur studio_perso/video_03",
            )


if __name__ == "__main__":
    unittest.main()
