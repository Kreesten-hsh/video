#!/usr/bin/env python3
"""
ANALYSEUR DE RÉFÉRENCE VIDÉO (AGENT404)
=======================================
Télécharge, découpe et analyse n'importe quelle vidéo courte (Instagram Reel,
TikTok, YouTube Shorts ou fichier local MP4) pour en extraire la structure
narrative, le pacing des cuts et le script mot-à-mot via Whisper.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


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


def analyze_video(source: str, out_root: Path = Path("references"), browser_cookies: str = None):
    out_root.mkdir(parents=True, exist_ok=True)
    
    # Nom de dossier propre
    safe_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", os.path.basename(source.split("?")[0]))
    if not safe_name or safe_name == "_":
        safe_name = "ref_video"
    target_dir = out_root / safe_name
    target_dir.mkdir(parents=True, exist_ok=True)

    watch_script = Path(".agents/skills/watch/scripts/watch.py").resolve()
    if not watch_script.exists():
        raise FileNotFoundError(f"Skill watch introuvable à {watch_script}")

    print(f"\n[1/3] Ingestion et extraction de frames via /watch ({source})...")
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
    watch_output = res.stdout

    # Localiser le sous-dossier watch généré
    subdirs = [p for p in target_dir.iterdir() if p.is_dir() and p.name.startswith("watch-")]
    if not subdirs:
        work_dir = target_dir
    else:
        work_dir = subdirs[-1]

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

    print(f"[2/3] Extraction et transcription de la voix via Whisper ({len(frames)} frames extraites)...")
    transcript = ""
    words = []
    if video_file and video_file.exists():
        wav_tmp = work_dir / "audio_16k.wav"
        extract_audio_wav(video_file, wav_tmp)
        if wav_tmp.exists() and wav_tmp.stat().st_size > 1000:
            transcript, words = transcribe_audio_local(wav_tmp)

    print(f"[3/3] Calcul des métriques de rétention et synthèse...")
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

    word_count = len(words)
    wpm = round((word_count / (duration / 60))) if duration > 5 else 0
    cut_count = len(frames)
    pace_per_cut = round(duration / max(1, cut_count), 2) if cut_count > 0 else 0

    # Identifier les 3 premières secondes (Hook)
    hook_words = [w["word"] for w in words if w["start"] <= 3.2]
    hook_text = " ".join(hook_words) if hook_words else (transcript[:60] if transcript else "[Aucun audio détecté]")

    # Générer le rapport markdown
    report_file = target_dir / "ANALYSIS.md"
    report_lines = [
        f"# Rapport d'Analyse Vidéo Référence : `{safe_name}`",
        f"- **Source** : `{source}`",
        f"- **Durée** : `{duration:.1f}s`",
        f"- **Nombre de plans / Frames clés** : `{cut_count}`",
        f"- **Rythme moyen par plan** : `{pace_per_cut}s` par cut",
        f"- **Débit vocal** : `{wpm} mots/minute` ({word_count} mots au total)",
        "",
        "---",
        "",
        "## 1. Rétro-Ingénierie du Hook (0 à 3 secondes)",
        f"- **Phrase d'accroche (Whisper)** : « {hook_text} »",
        f"- **Première frame visuelle** : `{frames[0].name if frames else 'N/A'}`",
        "",
        "## 2. Découpage & Pacing des Scènes",
        "| Instant Estimé | Frame Clé | Contexte Vocale |",
        "| :--- | :--- | :--- |"
    ]

    for idx, f in enumerate(frames[:15]):
        t_est = round(idx * pace_per_cut, 1)
        nearby_words = [w["word"] for w in words if abs(w["start"] - t_est) < 1.2]
        snip = " ".join(nearby_words[:5]) if nearby_words else "-"
        report_lines.append(f"| `t={t_est:.1f}s` | [{f.name}](file://{f.resolve()}) | {snip} |")

    report_lines.extend([
        "",
        "## 3. Transcription Complète Détectée",
        f"> {transcript if transcript else '_Aucune parole détectée_'}",
        "",
        "## 4. Proposition d'Adaptation AGENT404 (Remix B2B)",
        "Voici comment transposer la structure de ce Reel viral pour le studio AGENT404 :",
        "",
        "### A. Hook Alternatif (Néo-Brutaliste 0-3s)",
        f"- **Transposition** : *« Arrête de faire {hook_text[:30]}... voici le système qui tourne en 60s. »*",
        "- **Mise en scène** : Kinetic Typography au centre (texte géant émeraude sur carbone).",
        "",
        "### B. Squelette de Scénario Recommandé",
        "1. **Scène 01 (0-3s)** : Kinetic Typography centré (le problème ou l'erreur courante).",
        "2. **Scène 02 (3-15s)** : Démonstration visuelle / Terminal (le piège manuel qui fait perdre du temps).",
        "3. **Scène 03 (15-45s)** : Schéma Avant / Après ou Comparatif 2 blocs.",
        "4. **Scène 04 (45-60s)** : CTA unique vers le mot-clé en message privé.",
        ""
    ])

    report_file.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\n✓ Rapport d'analyse complet généré avec succès dans : {report_file}")
    return report_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyseur et veille vidéo AGENT404")
    parser.add_argument("source", help="URL (Instagram Reel, TikTok, Shorts) ou chemin de fichier MP4 local")
    parser.add_argument("--cookies", help="Navigateur pour extraire les cookies yt-dlp (ex: chrome)", default=None)
    parser.add_argument("--out", help="Dossier de sortie", default="references")

    args = parser.parse_args()
    analyze_video(args.source, out_root=Path(args.out), browser_cookies=args.cookies)
