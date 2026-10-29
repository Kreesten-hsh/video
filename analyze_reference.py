#!/usr/bin/env python3
"""
ANALYSEUR DE RÉFÉRENCE VIDÉO (AGENT404)
=======================================
Télécharge, découpe et analyse n'importe quelle vidéo courte (Instagram Reel,
TikTok, YouTube Shorts ou fichier local MP4) pour en extraire la structure
narrative, le pacing des cuts et le script mot-à-mot via Whisper et les modules
d'analyse spécialisés (hook.py, pacing.py, report.py).

Génère dans references/analyzed/<slug>/ :
  - AUTOPSIE_FORMAT.md
  - blueprint_template.json
"""

from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Résolution des modules spécialisés de watch/scripts
WATCH_SCRIPTS = Path(__file__).resolve().parent / ".agents" / "skills" / "watch" / "scripts"
if str(WATCH_SCRIPTS) not in sys.path and WATCH_SCRIPTS.is_dir():
    sys.path.insert(0, str(WATCH_SCRIPTS))

try:
    from hook import analyze_hook
    from pacing import analyze_pacing
    from report import generate_autopsie_and_template
except ImportError:
    analyze_hook = None
    analyze_pacing = None
    generate_autopsie_and_template = None


def run_cmd(cmd, check=True):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Erreur commande ({' '.join(cmd)}): {res.stderr}")
    return res


def extract_audio_wav(video_path: Path, wav_path: Path):
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(wav_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def transcribe_audio_local(wav_path: Path):
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
        segments, info = model.transcribe(str(wav_path), word_timestamps=True, temperature=0.0)
        
        words = []
        full_text = []
        for s in segments:
            full_text.append(s.text.strip())
            for w in s.words:
                clean = w.word.strip()
                if clean:
                    words.append({
                        "word": clean,
                        "start": round(w.start, 2),
                        "end": round(w.end, 2)
                    })
        return " ".join(full_text), words
    except Exception as e:
        print(f"[Avertissement] Whisper local non disponible: {e}")
        return "", []


def analyze_video(
    source: str,
    slug: str | None = None,
    out_root: Path = Path("references/analyzed"),
    browser_cookies: str | None = None
):
    out_root.mkdir(parents=True, exist_ok=True)
    
    # Détermination du slug propre
    if not slug:
        clean_src = source.split("?")[0].rstrip("/")
        slug = re.sub(r"[^a-zA-Z0-9_\-]", "_", os.path.basename(clean_src))
        if not slug or slug == "_":
            slug = "ref_video"

    target_dir = out_root / slug
    target_dir.mkdir(parents=True, exist_ok=True)

    watch_script = WATCH_SCRIPTS / "watch.py"
    if not watch_script.exists():
        raise FileNotFoundError(f"Skill watch introuvable à {watch_script}")

    print(f"\n[1/4] Ingestion et extraction de frames via /watch ({source})...")
    watch_cmd = [
        sys.executable, str(watch_script),
        source,
        "--detail", "balanced",
        "--no-whisper",
        "--out-dir", str(target_dir)
    ]
    if browser_cookies:
        watch_cmd.extend(["--cookies-from-browser", browser_cookies])

    res = run_cmd(watch_cmd, check=True)

    # Localiser le sous-dossier watch généré
    subdirs = [p for p in target_dir.iterdir() if p.is_dir() and p.name.startswith("watch-")]
    work_dir = subdirs[-1] if subdirs else target_dir

    frames_dir = work_dir / "frames"
    frames = sorted(list(frames_dir.glob("*.jpg"))) if frames_dir.exists() else []

    # Trouver le fichier vidéo téléchargé ou source
    video_file = None
    if os.path.isfile(source):
        video_file = Path(source)
    else:
        for f in work_dir.glob("*.*"):
            if f.suffix.lower() in [".mp4", ".mov", ".mkv", ".webm"]:
                video_file = f
                break
        if not video_file and (work_dir / "download").exists():
            for f in (work_dir / "download").glob("**/*.*"):
                if f.suffix.lower() in [".mp4", ".mov", ".mkv", ".webm"]:
                    video_file = f
                    break

    print(f"[2/4] Extraction et transcription de la voix ({len(frames)} frames extraites)...")
    transcript = ""
    words = []
    if video_file and video_file.exists():
        wav_tmp = work_dir / "audio_16k.wav"
        extract_audio_wav(video_file, wav_tmp)
        if wav_tmp.exists() and wav_tmp.stat().st_size > 1000:
            transcript, words = transcribe_audio_local(wav_tmp)

    print(f"[3/4] Mesure de la durée et diagnostic...")
    duration = 0.0
    if video_file:
        probe_cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(video_file)
        ]
        pres = run_cmd(probe_cmd, check=False)
        try:
            duration = float(pres.stdout.strip())
        except ValueError:
            duration = 0.0

    print(f"[4/4] Exécution des modules spécialisés hook.py, pacing.py et report.py...")
    if analyze_hook and analyze_pacing and generate_autopsie_and_template:
        hook_data = analyze_hook(words, transcript, duration, frames)
        pacing_data = analyze_pacing(duration, frames, words)
        autopsie_p, template_p = generate_autopsie_and_template(
            source=source,
            slug=slug,
            duration=duration,
            transcript=transcript,
            words=words,
            hook_data=hook_data,
            pacing_data=pacing_data,
            out_dir=target_dir
        )
        print(f"✓ Autopsie de format générée : {autopsie_p}")
        print(f"✓ Squelette Blueprint généré : {template_p}")
        return autopsie_p
    else:
        # Fallback si modules non importables
        legacy_file = target_dir / "ANALYSIS.md"
        legacy_file.write_text(f"# Analyse {slug}\nDurée: {duration}s\nTranscription: {transcript}\n", encoding="utf-8")
        print(f"✓ Analyse basique générée : {legacy_file}")
        return legacy_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyseur et veille vidéo AGENT404")
    parser.add_argument("source", nargs="?", default=None, help="URL ou fichier source (positionnel)")
    parser.add_argument("--input", "-i", dest="input_source", default=None, help="Chemin d'entrée ou URL")
    parser.add_argument("--name", "-n", dest="slug", default=None, help="Nom/Slug du dossier d'analyse dans references/analyzed/<name>")
    parser.add_argument("--out", help="Dossier racine de sortie", default="references/analyzed")
    parser.add_argument("--cookies", help="Navigateur pour extraire les cookies yt-dlp (ex: chrome)", default=None)

    args = parser.parse_args()
    source_to_use = args.input_source or args.source
    if not source_to_use:
        parser.error("Veuillez fournir une source soit en argument positionnel, soit via --input.")

    analyze_video(source_to_use, slug=args.slug, out_root=Path(args.out), browser_cookies=args.cookies)
