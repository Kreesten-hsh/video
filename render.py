import os
import sys
import gc
import json
import math
import shutil
import subprocess
import re
from typing import Union
from pathlib import Path
from playwright.sync_api import sync_playwright

# Ajout dynamique du répertoire bin local du dépôt au PATH si présent
_local_bin = str(Path(__file__).parent.resolve() / "bin")
_path_elements = os.environ.get("PATH", "").split(os.pathsep) if os.environ.get("PATH") else []
if _local_bin not in _path_elements and Path(_local_bin).is_dir():
    _path_elements.insert(0, _local_bin)
os.environ["PATH"] = os.pathsep.join(_path_elements)


def check_dependencies():
    """Vérifie la disponibilité de ffmpeg, ffprobe et d'un binaire Chromium."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "Erreur : 'ffmpeg' est introuvable dans le PATH. "
            "Veuillez installer ffmpeg pour permettre l'encodage vidéo."
        )
    if not shutil.which("ffprobe"):
        raise RuntimeError(
            "Erreur : 'ffprobe' est introuvable dans le PATH. "
            "Veuillez installer ffprobe pour permettre l'analyse de l'audio."
        )


def get_browser_launch_kwargs():
    """Détecte les options optimales pour lancer Chromium sans saturation GPU/mémoire."""
    candidates = [
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
    ]
    exec_path = None
    for cand in candidates:
        if cand and Path(cand).is_file() and os.access(cand, os.X_OK):
            exec_path = str(Path(cand).resolve())
            break

    args = [
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--js-flags=--max-old-space-size=1024",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-default-apps",
        "--disable-sync",
    ]
    kwargs = {"headless": True, "args": args}
    if exec_path:
        kwargs["executable_path"] = exec_path
    return kwargs


def get_audio_duration(audio_file: str) -> float:
    """Lit la durée exacte en secondes d'un fichier audio via ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_file
    ]
    res = subprocess.check_output(cmd).decode().strip()
    return float(res)


def setup_render_page(browser, html_abs_uri: str, timeline_path: str = None, rendu_deterministe: bool = True, scenes: list = None):
    """Crée une page isolée hors réseau, injecte la timeline locale, attend les polices et pré-décode dynamiquement les avatars."""
    context = browser.new_context(
        viewport={"width": 1080, "height": 1920},
        device_scale_factor=1,
        offline=True
    )
    page = context.new_page()

    if timeline_path and Path(timeline_path).exists():
        page.add_init_script(path=str(Path(timeline_path).resolve()))

    target_url = html_abs_uri
    if timeline_path and Path(timeline_path).exists():
        target_url = f"{html_abs_uri}?timeline={Path(timeline_path).resolve().as_uri()}"

    page.goto(target_url)
    page.wait_for_load_state("networkidle")

    if rendu_deterministe:
        page.add_style_tag(
            content="*, *::before, *::after { transition: none !important; animation: none !important; }"
        )

    # Pré-décodage dynamique de tous les avatars référencés dans le projet et attente des polices locales
    avatars_to_predecode = [
        'assets/avatars/happy.png', 'assets/avatars/idea.png', 'assets/avatars/laptop.png',
        'assets/avatars/mic.png', 'assets/avatars/mini.png', 'assets/avatars/money.png',
        'assets/avatars/pointing.png', 'assets/avatars/prof.png', 'assets/avatars/scissors.png',
        'assets/avatars/shock.png', 'assets/avatars/skeptic.png', 'assets/avatars/stop.png',
        'assets/pfp/pfp_agent404_pro_slate.png'
    ]
    if scenes:
        for sc in scenes:
            av = sc.get("data", {}).get("avatar")
            if av and av not in avatars_to_predecode:
                avatars_to_predecode.append(av)

    page.evaluate("""async (avatars) => {
        await document.fonts.ready;
        await Promise.all(avatars.map(src => {
            const img = new Image();
            img.src = src;
            return img.decode().catch(() => {});
        }));
    }""", avatars_to_predecode)
    return context, page


def verify_rendered_avatars(video_path: str, scenes: Union[list, str, Path] = None) -> bool:
    """Vérifie automatiquement après rendu qu'aucune scène avec avatar (buste ou PiP) ne présente une zone vide.
    Charge dynamiquement les scènes depuis project.json ou timeline.js si un chemin est fourni."""
    if scenes is None:
        print("[Vérification] Aucune scène fournie pour validation des avatars.")
        return True

    if isinstance(scenes, (str, Path)):
        p = Path(scenes)
        target_dir = p if p.is_dir() else p.parent
        proj_json = target_dir / "project.json"
        timeline_js = target_dir / "timeline.js"
        loaded_scenes = None
        if proj_json.exists():
            try:
                with open(proj_json, "r", encoding="utf-8") as f:
                    loaded_scenes = json.load(f).get("scenes")
            except Exception:
                pass
        if loaded_scenes is None and timeline_js.exists():
            try:
                with open(timeline_js, "r", encoding="utf-8") as f:
                    c = f.read()
                m = re.search(r"window\.SCENES\s*=\s*(\[.*?\]);", c, re.DOTALL)
                if m:
                    loaded_scenes = json.loads(m.group(1))
            except Exception:
                pass
        scenes = loaded_scenes or []

    if not scenes:
        print("[Vérification] Aucune scène exploitable pour validation des avatars.")
        return True

    import cv2
    import numpy as np

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Impossible d'ouvrir la vidéo {video_path} pour vérification des avatars.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    failed_scenes = []

    for sc in scenes:
        data = sc.get("data", {})
        avatar = data.get("avatar")
        avatar_pip = data.get("avatar_pip")
        sc_type = sc.get("type", "")

        has_bust = (avatar and "mini" not in str(avatar)) or (sc_type == "face" and avatar)
        has_pip = bool(avatar_pip)

        if not has_bust and not has_pip:
            continue

        if "start" not in sc:
            continue

        t_start = float(sc["start"])
        t_end = float(sc.get("end", t_start + 1.0))
        t_sample = min(t_start + 0.15, (t_start + t_end) / 2.0)
        frame_idx = int(round(t_sample * fps))

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame_bgr = cap.read()
        if not ret:
            failed_scenes.append((sc.get("id", "?"), t_sample, "Échec de lecture de l'image"))
            continue

        # 1. Vérification Avatar Buste Plein Écran (y: 1200..1800, x: 250..830)
        if has_bust:
            avatar_crop = frame_bgr[1200:1800, 250:830]
            mean_lum = float(np.mean(avatar_crop))
            std_lum = float(np.std(avatar_crop))

            # Fond vide (#0D1117) présente une luminance moyenne < 32 et un écart-type très faible (< 10)
            if mean_lum < 32.0 and std_lum < 10.0:
                failed_scenes.append(
                    (sc.get("id", "?"), t_sample, f"Avatar buste absent (luminance moyenne={mean_lum:.2f}, std={std_lum:.2f})")
                )

        # 2. Vérification Avatar Médaillon PiP (y: 1200..1750, x: 680..1020)
        if has_pip:
            pip_crop = frame_bgr[1200:1750, 680:1020]
            mean_lum = float(np.mean(pip_crop))
            std_lum = float(np.std(pip_crop))
            if mean_lum < 28.0 and std_lum < 8.0:
                failed_scenes.append(
                    (sc.get("id", "?"), t_sample, f"Avatar PiP absent (luminance moyenne={mean_lum:.2f}, std={std_lum:.2f})")
                )

    cap.release()

    if failed_scenes:
        details = "\n".join([f" - Scène {s_id} (t={ts:.2f}s) : {reason}" for s_id, ts, reason in failed_scenes])
        raise AssertionError(f"Vérification post-rendu échouée : avatar absent dans les scènes suivantes :\n{details}")

    print(f"✓ Vérification avatars réussie sur {len(scenes)} scène(s).")
    return True


def render_video(
    project_path: str = None,
    html_path: str = "index.html",
    audio_path: str = None,
    timeline_path: str = None,
    output_path: str = None,
    fps: int = 30,
    verify_avatars: bool = True,
    scenes: list = None,
    rendu_deterministe: bool = None,
    preflight: bool = True
):
    check_dependencies()

    if project_path:
        p_dir = Path(project_path)
        if p_dir.is_file():
            p_dir = p_dir.parent
        proj_file = p_dir / "project.json"
        video_num = 1
        if proj_file.exists():
            try:
                with open(proj_file, "r", encoding="utf-8") as f:
                    p_data = json.load(f)
                    video_num = p_data.get("video_number", 1)
                    if scenes is None:
                        scenes = p_data.get("scenes")
                    if rendu_deterministe is None:
                        rendu_deterministe = p_data.get("rendu_deterministe", True)
            except Exception:
                pass

        output_path = output_path or str(p_dir / f"video{video_num}.mp4")
        if not audio_path:
            cand_final = p_dir / "audio_final.wav"
            cand_voix = p_dir / "voix.wav"
            audio_path = str(cand_final) if cand_final.exists() else str(cand_voix)
        timeline_path = timeline_path or str(p_dir / "timeline.js")

    if rendu_deterministe is None:
        rendu_deterministe = True

    if not output_path:
        raise ValueError("Aucun chemin de sortie spécifié pour render_video. Renseignez --projet ou --output.")

    if not audio_path or not Path(audio_path).exists():
        raise FileNotFoundError(f"Fichier audio introuvable : '{audio_path}'.")

    if not timeline_path or not Path(timeline_path).exists():
        raise FileNotFoundError(f"Fichier timeline.js introuvable : '{timeline_path}'.")

    # Contrôle de qualité pré-vol automatique (Pre-Flight Gatekeeper < 3s)
    if preflight and project_path:
        print("[Gatekeeper] Contrôle qualité pré-vol (preflight check)...")
        try:
            from preflight_check import run_preflight_check
            report = run_preflight_check(project_dir=project_path, timeline_path=timeline_path, html_path=html_path)
            if not report.get("success", False):
                errors = "\n".join([f" - {err}" for err in report.get("errors", [])])
                raise RuntimeError(f"Échec des contrôles pre-flight pour '{project_path}' :\n{errors}")
            print("✓ Contrôles pre-flight validés avec succès.")
        except ImportError:
            pass

    if scenes is None:
        try:
            with open(timeline_path, "r", encoding="utf-8") as f:
                c = f.read()
            m = re.search(r"window\.SCENES\s*=\s*(\[.*?\]);", c, re.DOTALL)
            if m:
                scenes = json.loads(m.group(1))
        except Exception:
            pass

    html_abs = Path(html_path).resolve().as_uri()
    duration = get_audio_duration(audio_path)
    total_frames = math.ceil(duration * fps)
    print(f"[Render] Durée audio : {duration:.2f}s | {total_frames} frames à générer ({fps} FPS).")
    print(f"[Render] Cible de sortie : {output_path}")

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "image2pipe",
        "-vcodec", "mjpeg",
        "-r", str(fps),
        "-i", "pipe:0",
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-threads", "2",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    with sync_playwright() as p:
        launch_kwargs = get_browser_launch_kwargs()
        try:
            browser = p.chromium.launch(**launch_kwargs)
        except Exception as e:
            raise RuntimeError(
                f"Erreur : échec du lancement de Chromium ({e}). "
                "Veuillez exécuter 'playwright install chromium' ou vérifier l'installation du navigateur."
            )

        context, page = setup_render_page(browser, html_abs, timeline_path=timeline_path, rendu_deterministe=rendu_deterministe, scenes=scenes)

        print("[Render] Capture et encodage déterministe avec synchronisation totale des images et polices...")
        for i in range(total_frames):
            t = i / float(fps)
            page.evaluate(f"""async () => {{
                window.setTime({t:.4f});
                await document.fonts.ready;
                const imgs = Array.from(document.querySelectorAll('img'));
                await Promise.all(imgs.map(img => {{
                    if (!img.src) return Promise.resolve();
                    if (img.complete) return img.decode().catch(() => {{}});
                    return new Promise(resolve => {{
                        img.onload = () => img.decode().then(resolve).catch(resolve);
                        img.onerror = resolve;
                    }});
                }}));
            }}""")

            frame_bytes = page.screenshot(type="jpeg", quality=90)
            proc.stdin.write(frame_bytes)

            # Recyclage périodique pour libérer la mémoire V8/Skia
            if (i + 1) % 150 == 0 and (i + 1) < total_frames:
                page.close()
                context.close()
                gc.collect()
                context, page = setup_render_page(browser, html_abs, timeline_path=timeline_path, rendu_deterministe=rendu_deterministe, scenes=scenes)

            if i % 15 == 0 or i == total_frames - 1:
                percent = int((i + 1) / total_frames * 100)
                bar = "=" * (percent // 5) + ">" + " " * (20 - (percent // 5))
                sys.stdout.write(f"\r[{bar}] {percent}% ({i+1}/{total_frames} frames) t={t:.2f}s")
                sys.stdout.flush()

        browser.close()

    proc.stdin.close()
    proc.wait()
    print(f"\n✓ Rendu terminé avec succès -> {output_path}")

    if verify_avatars and scenes is not None:
        verify_rendered_avatars(output_path, scenes)

    return output_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Moteur de rendu vidéo headless AGENT404.")
    parser.add_argument("--projet", "-p", default=None, help="Chemin du dossier projet")
    parser.add_argument("--output", "-o", default=None, help="Chemin du fichier MP4 de sortie")
    parser.add_argument("--audio", "-a", default=None, help="Chemin du fichier audio")
    parser.add_argument("--timeline", "-t", default=None, help="Chemin de timeline.js")
    parser.add_argument("--fps", type=int, default=30, help="Images par seconde")
    parser.add_argument("--no-verify-avatars", action="store_true", help="Désactive la vérification des avatars")
    parser.add_argument("--no-preflight", action="store_true", help="Désactive le contrôle pré-vol Gatekeeper")
    parser.add_argument("--rendu-deterministe", dest="rendu_deterministe", action="store_true", default=None, help="Active le rendu déterministe (par défaut)")
    parser.add_argument("--no-rendu-deterministe", dest="rendu_deterministe", action="store_false", help="Désactive le rendu déterministe")
    args = parser.parse_args()

    default_proj = args.projet
    if default_proj is None and not args.output and os.path.exists("studio_perso/video_01"):
        default_proj = "studio_perso/video_01"

    render_video(
        project_path=default_proj,
        audio_path=args.audio,
        timeline_path=args.timeline,
        output_path=args.output,
        fps=args.fps,
        verify_avatars=not args.no_verify_avatars,
        rendu_deterministe=args.rendu_deterministe,
        preflight=not args.no_preflight
    )
