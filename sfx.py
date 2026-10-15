import os
import re
import sys
import json
import wave
import site
from pathlib import Path

_user_site = os.path.expanduser("~/.local/lib/python3.12/site-packages")
if _user_site not in sys.path:
    site.addsitedir(_user_site)

import numpy as np

BASE_DIR = Path(__file__).parent.resolve()
SFX_DIR = BASE_DIR / "assets" / "sfx"

def load_wav(filepath: Path) -> np.ndarray:
    """Charge un fichier WAV mono 44100Hz en float32 normalisé [-1.0, 1.0]."""
    if not filepath.exists():
        return np.zeros(0, dtype=np.float32)
    with wave.open(str(filepath), "rb") as wf:
        nframes = wf.getnframes()
        raw_bytes = wf.readframes(nframes)
        samples = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32)
        if len(samples) > 0:
            max_val = np.max(np.abs(samples))
            if max_val > 0:
                samples = samples / 32768.0
        return samples

def load_scenes_from_timeline(timeline_path="timeline.js"):
    if not os.path.exists(timeline_path):
        return []
    with open(timeline_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"window\.SCENES\s*=\s*(\[.*?\]);", content, re.DOTALL)
    if not match:
        return []
    try:
        return json.loads(match.group(1))
    except Exception:
        return []

def mix_sfx(voix_path="voix.wav", out_path="audio_final.wav", timeline_path="timeline.js"):
    if not os.path.exists(voix_path):
        print(f"Erreur : {voix_path} introuvable.")
        return

    scenes = load_scenes_from_timeline(timeline_path)
    print(f"[SFX] {len(scenes)} scènes chargées depuis {timeline_path}")

    # Lecture de voix.wav
    with wave.open(voix_path, "rb") as wf:
        nchannels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        nframes = wf.getnframes()
        raw_bytes = wf.readframes(nframes)

    audio = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32)
    if nchannels == 2:
        audio = audio.reshape(-1, 2)
    else:
        audio = audio.reshape(-1, 1)

    total_samples = len(audio)

    # Chargement des 6 banques sonores de studio importées
    sfx_whoosh = load_wav(SFX_DIR / "whoosh.wav") * 0.28
    sfx_pop = load_wav(SFX_DIR / "pop.wav") * 0.32
    sfx_click = load_wav(SFX_DIR / "click.wav") * 0.20
    sfx_cash = load_wav(SFX_DIR / "cash.wav") * 0.34
    sfx_impact = load_wav(SFX_DIR / "impact.wav") * 0.38
    sfx_ding = load_wav(SFX_DIR / "ding.wav") * 0.30

    def add_sample(sample_arr, start_sec):
        idx = int(start_sec * framerate)
        if idx >= total_samples or len(sample_arr) == 0:
            return
        end_idx = min(total_samples, idx + len(sample_arr))
        length = end_idx - idx
        audio[idx:end_idx] += sample_arr[:length, np.newaxis] * 32767.0

    for i, sc in enumerate(scenes):
        t_start = sc.get("start", 0.0)
        t_end = sc.get("end", t_start + 1.0)
        sc_type = sc.get("type", "")
        sc_data = sc.get("data", {})
        bg = sc_data.get("bg", "")
        text = sc_data.get("text", "")
        avatar = sc_data.get("avatar", "")

        # 1. Scène d'intro forte (STOP) -> Impact brutal
        if i == 0 or "stop" in avatar:
            add_sample(sfx_impact, t_start)

        # 2. Scènes d'argent et prix -> Bruitage de pièces / caisse
        elif "HORS DE PRIX" in text or "0 €" in text or "money" in avatar or "fortune" in text:
            add_sample(sfx_cash, t_start)

        # 3. Scènes de révélation / milestone -> Ding cristallin
        elif "RÉVOLUTION" in text or sc_type == "speed_counter" or "100%" in text:
            add_sample(sfx_ding, t_start)

        # 4. Changements de fond majeurs ou gros titres -> Whoosh studio
        elif sc_type == "big" or bg in ["red", "diamonds", "circles"]:
            add_sample(sfx_whoosh, t_start)

        # 5. Machine à écrire / Terminal -> Série de micro-clics
        elif sc_type == "window":
            duration = t_end - t_start
            for dt in np.arange(0.08, min(duration, 1.4), 0.12):
                add_sample(sfx_click, t_start + dt)

        # 6. Cartes, morphing, split, avatars -> Pop mat dynamique
        else:
            add_sample(sfx_pop, t_start)

    # Normalisation et clamp strict sans saturation
    np.clip(audio, -32767.0, 32767.0, out=audio)
    out_audio = audio.astype(np.int16)

    with wave.open(out_path, "wb") as wf:
        wf.setnchannels(nchannels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(out_audio.tobytes())

    print(f"✓ Mixage SFX masterisé terminé avec succès -> {out_path} ({len(out_audio)/framerate:.2f}s)")

if __name__ == "__main__":
    mix_sfx()
