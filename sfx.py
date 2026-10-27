import os
import re
import sys
import json
import wave
import zlib

import numpy as np

def generate_soft_whoosh(sr=44100, duration=0.040, rng=None) -> np.ndarray:
    """
    Whoosh feutré de transition (40ms) :
    Bruit rose/blanc filtré passe-bas avec enveloppe en cloche douce (Hann).
    Atténuation : ~ -24 dB.
    """
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # Bruit aléatoire lissé par moyenne mobile (filtre passe-bas acoustique ~1200Hz)
    if rng is not None:
        noise = rng.uniform(-1.0, 1.0, n_samples)
    else:
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

def generate_micro_click(sr=44100, duration=0.008, rng=None) -> np.ndarray:
    """
    Micro-clic mécanique discret (8ms) pour typewriter :
    Impulsion amortie 650Hz sans stridence.
    Niveau sonore : -26 dB.
    """
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    envelope = np.exp(-t * 550)
    sine = np.sin(2 * np.pi * 650 * t) * 0.7
    if rng is not None:
        noise = rng.uniform(-0.3, 0.3, n_samples)
    else:
        noise = np.random.uniform(-0.3, 0.3, n_samples)
    click = (sine + noise) * envelope * 0.050  # -26 dB
    return click.astype(np.float32)

def generate_neo_pop_60ms(sr=44100) -> np.ndarray:
    """
    Pop percussif doux (60ms) :
    Glissement sinusoïdal 190Hz -> 55Hz avec attaque douce et décroissance exponentielle.
    """
    duration = 0.060
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    freq = np.linspace(190.0, 55.0, n_samples)
    phase = 2 * np.pi * np.cumsum(freq) / sr
    envelope = np.sin(np.pi * np.minimum(t / 0.006, 1.0) * 0.5) * np.exp(-t * 48.0)
    wave_arr = np.sin(phase) * envelope
    peak = np.max(np.abs(wave_arr)) or 1.0
    return (wave_arr / peak).astype(np.float32)


def generate_neo_whoosh_140ms(sr=44100, rng=None) -> np.ndarray:
    """
    Souffle rapide de transition et slide RTL (140ms) :
    Bruit filtré passe-bande/passe-bas avec enveloppe Hann asymétrique.
    """
    duration = 0.140
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    if rng is not None:
        noise = rng.uniform(-1.0, 1.0, n_samples)
    else:
        det_rng = np.random.default_rng(404)
        noise = det_rng.uniform(-1.0, 1.0, n_samples)
    kernel = np.hanning(28)
    kernel = kernel / np.sum(kernel)
    filtered = np.convolve(noise, kernel, mode="same")
    sweep_tone = np.sin(2 * np.pi * np.cumsum(np.linspace(260.0, 95.0, n_samples)) / sr) * 0.35
    envelope = (np.sin(np.pi * t / duration) ** 1.6)
    wave_arr = (filtered * 0.65 + sweep_tone) * envelope
    peak = np.max(np.abs(wave_arr)) or 1.0
    return (wave_arr / peak).astype(np.float32)


def generate_neo_stamp_120ms(sr=44100, rng=None) -> np.ndarray:
    """
    Impact sourd de tampon Néo-Brutaliste (120ms) :
    Sub-punch 115Hz -> 34Hz + transitoire mat d'impact papier/bois.
    """
    duration = 0.120
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    freq = np.linspace(115.0, 34.0, n_samples)
    phase = 2 * np.pi * np.cumsum(freq) / sr
    body = np.sin(phase) * np.exp(-t * 28.0)
    if rng is not None:
        noise = rng.uniform(-1.0, 1.0, n_samples)
    else:
        det_rng = np.random.default_rng(808)
        noise = det_rng.uniform(-1.0, 1.0, n_samples)
    kernel = np.ones(10) / 10.0
    thud_transient = np.convolve(noise, kernel, mode="same") * np.exp(-t * 95.0) * 0.45
    wave_arr = np.tanh((body + thud_transient) * 1.4)
    peak = np.max(np.abs(wave_arr)) or 1.0
    return (wave_arr / peak).astype(np.float32)


def generate_neo_click_40ms(sr=44100, rng=None) -> np.ndarray:
    """
    Clic mécanique franc de souris / bouton Néo-Brutaliste (40ms) :
    Double transitoire mécanique (press + release court) amorti.
    """
    duration = 0.040
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    if rng is not None:
        noise = rng.uniform(-1.0, 1.0, n_samples)
    else:
        det_rng = np.random.default_rng(101)
        noise = det_rng.uniform(-1.0, 1.0, n_samples)
    click1 = (np.sin(2 * np.pi * 880.0 * t) * 0.7 + noise * 0.3) * np.exp(-t * 260.0)
    t2 = np.maximum(0.0, t - 0.016)
    mask2 = (t >= 0.016).astype(np.float32)
    click2 = (np.sin(2 * np.pi * 620.0 * t2) * 0.5) * np.exp(-t2 * 320.0) * mask2
    wave_arr = click1 + click2
    peak = np.max(np.abs(wave_arr)) or 1.0
    return (wave_arr / peak).astype(np.float32)


def _write_mono_wav(path_str: str, samples: np.ndarray, sr: int = 44100):
    os.makedirs(os.path.dirname(path_str), exist_ok=True)
    pcm = np.clip(samples * 32767.0 * 0.90, -32767.0, 32767.0).astype(np.int16)
    with wave.open(path_str, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def ensure_sfx_files(sfx_dir: str = "assets/audio/sfx", sr: int = 44100) -> dict:
    """
    Garantit la présence des 4 fichiers WAV de Sound Design dans assets/audio/sfx/ :
      - pop.wav (60ms)
      - whoosh.wav (140ms)
      - stamp.wav (120ms)
      - click.wav (40ms)
    """
    from pathlib import Path
    repo_root = Path(__file__).resolve().parent
    base_dir = Path(sfx_dir)
    if not base_dir.is_absolute():
        base_dir = repo_root / base_dir
    base_dir.mkdir(parents=True, exist_ok=True)

    specs = {
        "pop": (base_dir / "pop.wav", lambda: generate_neo_pop_60ms(sr)),
        "whoosh": (base_dir / "whoosh.wav", lambda: generate_neo_whoosh_140ms(sr)),
        "stamp": (base_dir / "stamp.wav", lambda: generate_neo_stamp_120ms(sr)),
        "click": (base_dir / "click.wav", lambda: generate_neo_click_40ms(sr)),
    }
    paths = {}
    for key, (f_path, gen_fn) in specs.items():
        if not f_path.exists():
            _write_mono_wav(str(f_path), gen_fn(), sr=sr)
        paths[key] = str(f_path)
    return paths


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


def mix_sfx(
    voix_path: str = None,
    out_path: str = None,
    timeline_path: str = None,
    project_path: str = None,
    seed: int = None
):
    from pathlib import Path

    ensure_sfx_files()

    p_dir = None
    rendu_deterministe = None
    if project_path:
        p_dir = Path(project_path)
        if p_dir.is_file():
            p_dir = p_dir.parent
        voix_path = voix_path or str(p_dir / "voix.wav")
        out_path = out_path or str(p_dir / "audio_final.wav")
        timeline_path = timeline_path or str(p_dir / "timeline.js")
        proj_file = p_dir / "project.json"
        if proj_file.exists():
            try:
                with open(proj_file, "r", encoding="utf-8") as f:
                    p_data = json.load(f)
                    rendu_deterministe = p_data.get("rendu_deterministe")
            except Exception:
                pass
    else:
        voix_path = voix_path or "voix.wav"
        out_path = out_path or "audio_final.wav"
        timeline_path = timeline_path or "timeline.js"

    # Détermination de la graine aléatoire pour les bruitages
    rng = None
    if seed is not None:
        rng = np.random.default_rng(seed)
    elif rendu_deterministe is False:
        rng = None  # Comportement aléatoire non déterministe historique préservé
    else:
        # Dérivation stable de la graine via zlib.crc32 du nom du projet
        proj_id = p_dir.name if p_dir else Path(out_path).stem
        stable_seed = zlib.crc32(proj_id.encode("utf-8"))
        rng = np.random.default_rng(stable_seed)

    if not os.path.exists(voix_path):
        raise FileNotFoundError(f"Erreur : fichier voix '{voix_path}' introuvable.")

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

    # Banques historiques (video_01 / video_02)
    whoosh_sfx = generate_soft_whoosh(framerate, rng=rng)
    pop_sfx = generate_organic_pop(framerate)
    click_sfx = generate_micro_click(framerate, rng=rng)

    # Banques Néo-Brutalistes à -14 dB (amplitude linéaire = 10^(-14/20) ≈ 0.1995)
    amp_minus_14db = float(10.0 ** (-14.0 / 20.0))
    neo_pop = generate_neo_pop_60ms(framerate) * amp_minus_14db
    neo_whoosh = generate_neo_whoosh_140ms(framerate, rng=rng) * amp_minus_14db
    neo_stamp = generate_neo_stamp_120ms(framerate, rng=rng) * amp_minus_14db
    neo_click = generate_neo_click_40ms(framerate, rng=rng) * amp_minus_14db

    def overlay_sfx(sfx_arr: np.ndarray, timestamp_sec: float, gain: float = 1.0):
        idx_s = int(round(timestamp_sec * framerate))
        if idx_s < 0 or idx_s >= total_samples:
            return
        idx_e = min(total_samples, idx_s + len(sfx_arr))
        seg_len = idx_e - idx_s
        if seg_len > 0:
            audio[idx_s:idx_e] += (sfx_arr[:seg_len, np.newaxis] * gain * 32767.0)

    for sc in scenes:
        t_start = float(sc.get("start", 0.0))
        t_end = float(sc.get("end", t_start + 1.0))
        sc_type = sc.get("type", "")
        bg = sc.get("data", {}).get("bg", "")

        idx_start = int(t_start * framerate)
        if idx_start >= total_samples:
            continue

        # --- Scènes Néo-Brutalistes (ob_*) mixées à -14 dB ---
        if sc_type.startswith("ob_"):
            if sc_type == "ob_post_counter":
                for dt in (0.02, 0.45, 0.90, 1.35):
                    if t_start + dt < t_end:
                        overlay_sfx(neo_pop, t_start + dt)
            elif sc_type == "ob_zero_stamp":
                overlay_sfx(neo_whoosh, t_start)
                overlay_sfx(neo_stamp, t_start + 0.06)
            elif sc_type == "ob_assets_stack":
                for dt in (0.20, 1.20, 2.20):
                    if t_start + dt < t_end:
                        overlay_sfx(neo_pop, t_start + dt)
            elif sc_type == "ob_camera_sigh":
                overlay_sfx(neo_pop, t_start + 0.04)
            elif sc_type == "ob_camera_chaos":
                for dt in (0.10, 0.90, 1.80):
                    if t_start + dt < t_end:
                        overlay_sfx(neo_pop, t_start + dt)
            elif sc_type == "ob_abandon_slam":
                overlay_sfx(neo_stamp, t_start + 0.05)
            elif sc_type == "ob_refuse_clones":
                overlay_sfx(neo_pop, t_start + 0.05)
                overlay_sfx(neo_stamp, t_start + 0.70)
                overlay_sfx(neo_stamp, t_start + 1.50)
            elif sc_type == "ob_clone_grid":
                for dt in (0.05, 0.25, 0.45):
                    if t_start + dt < t_end:
                        overlay_sfx(neo_pop, t_start + dt)
            elif sc_type == "ob_trust_drop":
                overlay_sfx(neo_whoosh, t_start)
                overlay_sfx(neo_stamp, t_start + 1.20)
            elif sc_type == "ob_not_content":
                overlay_sfx(neo_pop, t_start + 0.05)
            elif sc_type == "ob_text_wall_stamp":
                overlay_sfx(neo_pop, t_start + 0.05)
                overlay_sfx(neo_stamp, t_start + 0.45)
            elif sc_type == "ob_reverse_switch":
                overlay_sfx(neo_whoosh, t_start + 0.05)
                overlay_sfx(neo_click, t_start + 0.35)
            elif sc_type == "ob_step_one_voice":
                overlay_sfx(neo_pop, t_start + 0.05)
                overlay_sfx(neo_pop, t_start + 1.20)
            elif sc_type == "ob_step_two_structure":
                for dt in (0.40, 1.40, 2.30):
                    if t_start + dt < t_end:
                        overlay_sfx(neo_pop, t_start + dt)
            elif sc_type == "ob_step_three_proof":
                overlay_sfx(neo_whoosh, t_start)
                for dt in np.arange(0.40, min(t_end - t_start, 2.0), 0.22):
                    overlay_sfx(neo_click, t_start + float(dt), gain=0.65)
                overlay_sfx(neo_pop, t_start + 2.30)
            elif sc_type == "ob_unique_identity":
                overlay_sfx(neo_whoosh, t_start)
                for dt in np.arange(0.25, min(t_end - t_start, 1.8), 0.22):
                    overlay_sfx(neo_click, t_start + float(dt), gain=0.65)
            elif sc_type == "ob_four_palettes_grid":
                for dt in (0.20, 1.10, 2.10, 3.10):
                    if t_start + dt < t_end:
                        overlay_sfx(neo_pop, t_start + dt)
            elif sc_type == "ob_chrono_48h":
                overlay_sfx(neo_whoosh, t_start)
                overlay_sfx(neo_pop, t_start + 0.30)
            elif sc_type == "ob_platforms_popin":
                # 4 slides RTL des logos officiels : 54.26s, 54.90s, 55.60s, 56.20s
                for slide_t in (54.26, 54.90, 55.60, 56.20):
                    if t_start - 0.05 <= slide_t <= t_end:
                        overlay_sfx(neo_whoosh, slide_t)
                        overlay_sfx(neo_pop, slide_t + 0.08, gain=0.75)
            elif sc_type == "ob_final_pitch":
                overlay_sfx(neo_whoosh, t_start)
                overlay_sfx(neo_pop, t_start + 0.06)
            elif sc_type == "ob_final_delivery_cta":
                overlay_sfx(neo_pop, t_start + 0.04)
                for dt in (0.10, 0.17, 0.24, 0.31, 0.38, 0.45):
                    overlay_sfx(neo_click, t_start + dt, gain=0.60)
                # Clic mécanique franc à 01:01.3 (61.30s) sur ENVOYER "CLARTÉ"
                click_moment = 61.30 if (t_start <= 61.30 <= t_end) else (t_start + 0.76)
                overlay_sfx(neo_click, click_moment, gain=1.0)
            continue

        # 1. Pop organique mat sur apparitions visuelles & rupture rouge
        if sc_type in ["face", "cards", "split", "audio_wave", "blueprint_overwhelm", "blueprint_compare_split", "blueprint_spatial_pan", "face_to_dm_cta"]:
            end_idx = min(total_samples, idx_start + len(pop_sfx))
            length = end_idx - idx_start
            audio[idx_start:end_idx] += pop_sfx[:length, np.newaxis] * 32767.0

        # 2. Whoosh feutré doux sur transitions big ou kinetic type ou changements de fond majeurs
        elif sc_type in ["big", "blueprint_kinetic_type"] or bg in ["red", "diamonds", "circles"]:
            end_idx = min(total_samples, idx_start + len(whoosh_sfx))
            length = end_idx - idx_start
            audio[idx_start:end_idx] += whoosh_sfx[:length, np.newaxis] * 32767.0

        # 3. Micro-clics mécaniques sur terminal ou machine à écrire
        elif sc_type in ["window", "blueprint_terminal_scene"]:
            duration = t_end - t_start
            for dt in np.arange(0.08, min(duration, 1.4), 0.12):
                c_idx = int((t_start + dt) * framerate)
                if c_idx + len(click_sfx) < total_samples:
                    audio[c_idx:c_idx + len(click_sfx)] += click_sfx[:, np.newaxis] * 32767.0

        # 4. Clic d'interface sur blueprint_cursor_ui
        elif sc_type == "blueprint_cursor_ui":
            click_at = sc.get("data", {}).get("click_at", t_start + 0.4)
            c_idx = int(click_at * framerate)
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
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Mixage SFX vidéo programmatique AGENT404.")
    parser.add_argument("--projet", "-p", default=None, help="Chemin du dossier projet")
    parser.add_argument("--voix", default=None, help="Chemin voix.wav")
    parser.add_argument("--out", default=None, help="Chemin audio_final.wav")
    parser.add_argument("--timeline", default=None, help="Chemin timeline.js")
    parser.add_argument("--seed", type=int, default=None, help="Graine aléatoire pour bruitages déterministes")
    args = parser.parse_args()

    default_proj = args.projet
    if default_proj is None and not args.voix:
        if os.path.exists("studio_perso/video_03"):
            default_proj = "studio_perso/video_03"
        elif os.path.exists("studio_perso/video_01"):
            default_proj = "studio_perso/video_01"

    mix_sfx(
        voix_path=args.voix,
        out_path=args.out,
        timeline_path=args.timeline,
        project_path=default_proj,
        seed=args.seed
    )
