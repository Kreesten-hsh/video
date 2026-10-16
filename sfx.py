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

def generate_soft_whoosh(sr=44100, duration=0.040) -> np.ndarray:
    """
    Whoosh feutré de transition (40ms) :
    Bruit rose/blanc filtré passe-bas avec enveloppe en cloche douce (Hann).
    Atténuation : ~ -24 dB.
    """
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # Bruit aléatoire lissé par moyenne mobile (filtre passe-bas acoustique ~1200Hz)
    noise = np.random.uniform(-1.0, 1.0, n_samples)
    window_len = 16
    kernel = np.ones(window_len) / window_len
    smoothed_noise = np.convolve(noise, kernel, mode="same")
    
    # Enveloppe en cloche Hann
    envelope = np.sin(np.pi * t / duration) ** 2
    whoosh = smoothed_noise * envelope * 0.063  # -24 dB
    return whoosh.astype(np.float32)

def generate_organic_pop(sr=44100, duration=0.035) -> np.ndarray:
    """
    Pop organique mat (35ms) :
    Impulsion sinusoïdale grave pure glissant de 90Hz à 40Hz, zéro composante aiguë.
    Niveau sonore : -22 dB.
    """
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    freq = np.linspace(90, 40, n_samples)
    phase = 2 * np.pi * np.cumsum(freq) / sr
    envelope = (np.sin(np.pi * t / duration) ** 1.5) * np.exp(-t * 30)
    
    pop = np.sin(phase) * envelope * 0.079  # -22 dB
    return pop.astype(np.float32)

def generate_micro_click(sr=44100, duration=0.008) -> np.ndarray:
    """
    Micro-clic mécanique discret (8ms) pour typewriter :
    Impulsion amortie 650Hz sans stridence.
    Niveau sonore : -26 dB.
    """
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    envelope = np.exp(-t * 550)
    sine = np.sin(2 * np.pi * 650 * t) * 0.7
    noise = np.random.uniform(-0.3, 0.3, n_samples)
    click = (sine + noise) * envelope * 0.050  # -26 dB
    return click.astype(np.float32)

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

    # Génération des banques acoustiques douces
    whoosh_sfx = generate_soft_whoosh(framerate)
    pop_sfx = generate_organic_pop(framerate)
    click_sfx = generate_micro_click(framerate)

    for sc in scenes:
        t_start = sc.get("start", 0.0)
        t_end = sc.get("end", t_start + 1.0)
        sc_type = sc.get("type", "")
        bg = sc.get("data", {}).get("bg", "")

        idx_start = int(t_start * framerate)
        if idx_start >= total_samples:
            continue

        # 1. Pop organique mat sur apparitions visuelles & rupture rouge
        if sc_type in ["face", "cards", "split", "audio_wave"]:
            end_idx = min(total_samples, idx_start + len(pop_sfx))
            length = end_idx - idx_start
            audio[idx_start:end_idx] += pop_sfx[:length, np.newaxis] * 32767.0

        # 2. Whoosh feutré doux sur transitions big ou changements de fond majeurs
        elif sc_type == "big" or bg in ["red", "diamonds", "circles"]:
            end_idx = min(total_samples, idx_start + len(whoosh_sfx))
            length = end_idx - idx_start
            audio[idx_start:end_idx] += whoosh_sfx[:length, np.newaxis] * 32767.0

        # 3. Micro-clics mécaniques sur machine à écrire (window)
        elif sc_type == "window":
            duration = t_end - t_start
            for dt in np.arange(0.08, min(duration, 1.4), 0.12):
                c_idx = int((t_start + dt) * framerate)
                if c_idx + len(click_sfx) < total_samples:
                    audio[c_idx:c_idx + len(click_sfx)] += click_sfx[:, np.newaxis] * 32767.0

    # Normalisation et clamp strict sans saturation
    np.clip(audio, -32767.0, 32767.0, out=audio)
    out_audio = audio.astype(np.int16)

    with wave.open(out_path, "wb") as wf:
        wf.setnchannels(nchannels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(out_audio.tobytes())

    print(f"✓ Mixage SFX feutré terminé avec succès -> {out_path} ({len(out_audio)/framerate:.2f}s)")

if __name__ == "__main__":
    mix_sfx()
