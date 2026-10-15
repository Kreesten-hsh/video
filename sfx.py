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

def generate_pop(sr=44100, duration=0.06):
    """Pop doux haute fréquence (450Hz -> 850Hz) avec enveloppe exponentielle."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    freq = np.linspace(450, 850, len(t))
    phase = 2 * np.pi * np.cumsum(freq) / sr
    envelope = np.exp(-t * 40)
    return (np.sin(phase) * envelope).astype(np.float32)

def generate_sub_impact(sr=44100, duration=0.18):
    """Impact grave percutant (90Hz -> 45Hz) pour rupture visuelle."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    freq = np.linspace(95, 45, len(t))
    phase = 2 * np.pi * np.cumsum(freq) / sr
    envelope = np.exp(-t * 20)
    return (np.sin(phase) * envelope).astype(np.float32)

def generate_click(sr=44100, duration=0.02):
    """Clic percussif sec type machine à écrire / clavier."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    envelope = np.exp(-t * 140)
    sine = np.sin(2 * np.pi * 1400 * t) * 0.6
    noise = np.random.uniform(-0.4, 0.4, len(t))
    return ((sine + noise) * envelope).astype(np.float32)

def load_scenes_from_timeline(timeline_path="timeline.js"):
    with open(timeline_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"window\.SCENES\s*=\s*(\[.*?\]);", content, re.DOTALL)
    if not match:
        return []
    return json.loads(match.group(1))

def mix_sfx(voix_path="voix.wav", out_path="audio_final.wav", timeline_path="timeline.js"):
    if not os.path.exists(voix_path):
        print(f"Erreur : {voix_path} introuvable.")
        return

    scenes = load_scenes_from_timeline(timeline_path)
    print(f"[SFX] {len(scenes)} scènes chargées depuis {timeline_path}")

    # Lecture du fichier audio source
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

    # Pré-génération des banques d'effets sonores
    pop_sfx = generate_pop(framerate) * 0.12          # -18 dB
    impact_sfx = generate_sub_impact(framerate) * 0.18 # -15 dB
    click_sfx = generate_click(framerate) * 0.08       # -22 dB

    for sc in scenes:
        t_start = sc.get("start", 0.0)
        t_end = sc.get("end", t_start + 1.0)
        sc_type = sc.get("type", "")
        bg = sc.get("data", {}).get("bg", "")

        idx_start = int(t_start * framerate)
        if idx_start >= total_samples:
            continue

        # 1. Pop doux sur les transitions de scènes visuelles
        if sc_type in ["face", "cards", "list"]:
            end_idx = min(total_samples, idx_start + len(pop_sfx))
            length = end_idx - idx_start
            audio[idx_start:end_idx] += pop_sfx[:length, np.newaxis] * 32767.0

        # 2. Impact grave lourd sur type 'big' avec fond rouge
        elif sc_type == "big" and bg == "red":
            end_idx = min(total_samples, idx_start + len(impact_sfx))
            length = end_idx - idx_start
            audio[idx_start:end_idx] += impact_sfx[:length, np.newaxis] * 32767.0

        # 3. Série de petits clics machine à écrire sur 'window'
        elif sc_type == "window":
            duration = t_end - t_start
            for dt in np.arange(0.08, min(duration, 1.6), 0.11):
                c_idx = int((t_start + dt) * framerate)
                if c_idx + len(click_sfx) < total_samples:
                    audio[c_idx:c_idx + len(click_sfx)] += click_sfx[:, np.newaxis] * 32767.0

    # Normalisation et clamp pour éviter toute distorsion
    np.clip(audio, -32767.0, 32767.0, out=audio)
    out_audio = audio.astype(np.int16)

    with wave.open(out_path, "wb") as wf:
        wf.setnchannels(nchannels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(out_audio.tobytes())

    print(f"✓ Mixage SFX UI terminé avec succès -> {out_path}")

if __name__ == "__main__":
    mix_sfx()
