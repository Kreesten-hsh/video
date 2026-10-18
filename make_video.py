import os
import sys
import time
import json
import argparse
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.resolve()
_local_bin = str(REPO_ROOT / "bin")
_path_elements = os.environ.get("PATH", "").split(os.pathsep) if os.environ.get("PATH") else []
if _local_bin not in _path_elements and Path(_local_bin).is_dir():
    _path_elements.insert(0, _local_bin)
os.environ["PATH"] = os.pathsep.join(_path_elements)

import build_master_timeline
import sfx
import render


def run_ffprobe_checks(video_path: Path):
    """Vérifie les caractéristiques techniques requises de la vidéo (1080x1920, h264, aac, 30 fps)."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_type,codec_name,width,height,avg_frame_rate,r_frame_rate",
        "-show_entries", "format=duration,size",
        "-of", "json",
        str(video_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    probe = json.loads(res.stdout)

    streams = probe.get("streams", [])
    v_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    a_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    if not v_stream:
        raise AssertionError(f"Flux vidéo introuvable dans {video_path}")
    if not a_stream:
        raise AssertionError(f"Flux audio introuvable dans {video_path}")

    # Résolution 1080x1920
    w = int(v_stream.get("width", 0))
    h = int(v_stream.get("height", 0))
    if w != 1080 or h != 1920:
        raise AssertionError(f"Résolution invalide : {w}x{h} au lieu de 1080x1920")

    # Codec vidéo h264
    v_codec = v_stream.get("codec_name", "").lower()
    if "h264" not in v_codec:
        raise AssertionError(f"Codec vidéo invalide : {v_codec} au lieu de h264")

    # Codec audio aac
    a_codec = a_stream.get("codec_name", "").lower()
    if "aac" not in a_codec:
        raise AssertionError(f"Codec audio invalide : {a_codec} au lieu de aac")

    # Cadence 30 fps
    fps_raw = v_stream.get("r_frame_rate") or v_stream.get("avg_frame_rate") or "0/1"
    num, den = map(int, fps_raw.split("/"))
    fps = num / float(den) if den > 0 else 0.0
    if abs(fps - 30.0) > 0.05:
        raise AssertionError(f"Cadence d'images invalide : {fps:.2f} fps au lieu de 30 fps")

    duration = float(probe.get("format", {}).get("duration", 0.0))
    size_bytes = int(probe.get("format", {}).get("size", 0))
    return {
        "width": w,
        "height": h,
        "v_codec": v_codec,
        "a_codec": a_codec,
        "fps": fps,
        "duration": duration,
        "size_bytes": size_bytes
    }


def make_video(
    project_path_str: str,
    force_realign: bool = False,
    output_dir: str = None,
    forcer: bool = False
):
    total_start_time = time.time()
    p_dir, p_data = build_master_timeline.load_project(project_path_str)
    video_num = p_data.get("video_number", 1)
    scenes = p_data.get("scenes", [])
    is_frozen = p_data.get("gele", False)
    default_video_path = p_dir / f"video{video_num}.mp4"

    # Vérification 1 : Projet gelé sans redirection vers un dossier de sortie et sans --forcer
    if is_frozen and not output_dir and not forcer:
        sys.stderr.write(
            f"ERREUR : Le projet '{p_dir.name}' est gelé ('gele': true). "
            "Écriture dans le dossier du projet refusée sans l'option --forcer ou redirection via --sortie <dossier>.\n"
        )
        sys.exit(1)

    # Vérification 2 : Écrasement d'une vidéo existante sans --forcer ni --sortie
    if not output_dir and default_video_path.exists() and not forcer:
        sys.stderr.write(
            f"ERREUR : La vidéo cible '{default_video_path}' existe déjà. "
            "Écrasement refusé sans l'option --forcer ou redirection via --sortie <dossier>.\n"
        )
        sys.exit(1)

    if output_dir:
        out_dir = Path(output_dir).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        target_timeline_path = out_dir / "timeline.js"
        target_audio_path = out_dir / "audio_final.wav"
        target_video_path = out_dir / f"video{video_num}.mp4"
    else:
        out_dir = p_dir
        target_timeline_path = p_dir / "timeline.js"
        target_audio_path = p_dir / "audio_final.wav"
        target_video_path = default_video_path

    print("================================================================================")
    print(f"🎬 ORCHESTRATEUR DE PRODUCTION VIDÉO AGENT404 : {p_dir.name} (Vidéo #{video_num})")
    print(f"   Titre : {p_data.get('title')}")
    if output_dir:
        print(f"   Sortie redirigée vers : {out_dir}")
    print("================================================================================")

    # 1. Génération de la timeline
    t0 = time.time()
    print("\n[Étape 1/5] Génération et validation de la timeline...")
    build_master_timeline.run_pipeline(
        str(p_dir),
        force_realign=force_realign,
        output_timeline_js=str(target_timeline_path),
        output_voix_wav=str(out_dir / "voix.wav") if output_dir else None
    )
    time_timeline = time.time() - t0
    print(f"✓ Étape 1 terminée en {time_timeline:.2f}s")

    # 2. Bruitages SFX
    t0 = time.time()
    print("\n[Étape 2/5] Mixage acoustique et bruitages feutrés...")
    source_voix = str(out_dir / "voix.wav") if (out_dir / "voix.wav").exists() else str(p_dir / "voix.wav")
    sfx.mix_sfx(
        voix_path=source_voix,
        out_path=str(target_audio_path),
        timeline_path=str(target_timeline_path),
        project_path=str(p_dir)
    )
    time_sfx = time.time() - t0
    print(f"✓ Étape 2 terminée en {time_sfx:.2f}s")

    # 3. Rendu vidéo headless
    t0 = time.time()
    print("\n[Étape 3/5] Rendu vidéo déterministe Playwright + FFmpeg...")
    render.render_video(
        project_path=str(p_dir),
        audio_path=str(target_audio_path),
        timeline_path=str(target_timeline_path),
        output_path=str(target_video_path),
        verify_avatars=False,  # Exécuté explicitement à l'étape 4 pour mesure séparée
        scenes=scenes
    )
    time_render = time.time() - t0
    print(f"✓ Étape 3 terminée en {time_render:.2f}s")

    # 4. Vérification des avatars sur les scènes du projet
    t0 = time.time()
    print("\n[Étape 4/5] Vérification automatique de la présence des avatars...")
    timeline_scenes = sfx.load_scenes_from_timeline(str(target_timeline_path))
    render.verify_rendered_avatars(str(target_video_path), timeline_scenes)
    time_avatars = time.time() - t0
    print(f"✓ Étape 4 terminée en {time_avatars:.2f}s")

    # 5. Contrôle technique ffprobe
    t0 = time.time()
    print("\n[Étape 5/5] Contrôle technique de conformité de l'encodage (ffprobe)...")
    probe_stats = run_ffprobe_checks(target_video_path)
    time_ffprobe = time.time() - t0
    print(
        f"✓ Étape 5 terminée en {time_ffprobe:.2f}s "
        f"({probe_stats['width']}x{probe_stats['height']}, {probe_stats['v_codec']}/{probe_stats['a_codec']}, "
        f"{probe_stats['fps']:.1f} fps, {probe_stats['duration']:.2f}s, {probe_stats['size_bytes']:,} octets)"
    )

    total_time = time.time() - total_start_time
    print("\n================================================================================")
    print("BILAN D'EXÉCUTION DU RENDU")
    print(f" - Étape 1 (Timeline) : {time_timeline:.2f}s")
    print(f" - Étape 2 (SFX)      : {time_sfx:.2f}s")
    print(f" - Étape 3 (Rendu)    : {time_render:.2f}s")
    print(f" - Étape 4 (Avatars)  : {time_avatars:.2f}s")
    print(f" - Étape 5 (FFprobe)  : {time_ffprobe:.2f}s")
    print(f" TEMPS TOTAL PIPELINE : {total_time:.2f}s ({total_time / 60.0:.2f} min)")
    print(f" Fichier produit      : {target_video_path} ({probe_stats['size_bytes']} octets)")
    print("================================================================================")
    return target_video_path, probe_stats


def main():
    parser = argparse.ArgumentParser(description="Orchestrateur complet de production vidéo AGENT404.")
    parser.add_argument("projet", nargs="?", default="studio_perso/video_01", help="Chemin du dossier projet")
    parser.add_argument("--realigner", action="store_true", help="Force le réalignement acoustique Whisper")
    parser.add_argument("--sortie", "-s", default=None, help="Dossier de sortie dédié pour ne pas modifier le projet")
    parser.add_argument("--forcer", "-f", action="store_true", help="Force l'écrasement ou l'écriture sur un projet gelé")
    args = parser.parse_args()

    make_video(
        args.projet,
        force_realign=args.realigner,
        output_dir=args.sortie,
        forcer=args.forcer
    )


if __name__ == "__main__":
    main()
