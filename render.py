import os
import sys
import gc
import json
import math
import shutil
import subprocess
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


def setup_render_page(browser, html_abs_uri: str):
    """Crée une page isolée hors réseau, attend les polices locales et pré-décode les avatars."""
    context = browser.new_context(
        viewport={"width": 1080, "height": 1920},
        device_scale_factor=1,
        offline=True
    )
    page = context.new_page()
    page.goto(html_abs_uri)
    page.wait_for_load_state("networkidle")

    # Pré-décodage complet de toutes les images d'avatar et attente des polices locales
    page.evaluate("""async () => {
        await document.fonts.ready;
        const avatars = [
            'assets/avatars/happy.png', 'assets/avatars/idea.png', 'assets/avatars/laptop.png',
            'assets/avatars/mic.png', 'assets/avatars/mini.png', 'assets/avatars/money.png',
            'assets/avatars/pointing.png', 'assets/avatars/prof.png', 'assets/avatars/scissors.png',
            'assets/avatars/shock.png', 'assets/avatars/skeptic.png', 'assets/avatars/stop.png',
            'assets/pfp/pfp_agent404_pro_slate.png'
        ];
        await Promise.all(avatars.map(src => {
            const img = new Image();
            img.src = src;
            return img.decode().catch(() => {});
        }));
    }""")
    return context, page


def verify_rendered_avatars(video_path: str, scenes: list) -> bool:
    """Vérifie automatiquement après rendu qu'aucune scène avec avatar ne présente une zone vide."""
    if not scenes:
        print("[Vérification] Aucune scène fournie pour validation des avatars.")
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
        if not avatar or "mini" in avatar:
            continue

        # Vérifier dès la toute première frame de la scène
        t_sample = float(sc["start"])
        frame_idx = int(round(t_sample * fps))

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame_bgr = cap.read()
        if not ret:
            failed_scenes.append((sc.get("id", "?"), t_sample, "Échec de lecture de l'image"))
            continue

        # Zone avatar (y: 1200..1800, x: 250..830)
        avatar_crop = frame_bgr[1200:1800, 250:830]
        mean_lum = float(np.mean(avatar_crop))
        std_lum = float(np.std(avatar_crop))

        # Fond vide (#0D1117) présente une luminance moyenne < 32 et un écart-type très faible (< 10)
        if mean_lum < 32.0 and std_lum < 10.0:
            failed_scenes.append(
                (sc.get("id", "?"), t_sample, f"Avatar absent (luminance moyenne={mean_lum:.2f}, std={std_lum:.2f})")
            )

    cap.release()

    if failed_scenes:
        details = "\n".join([f" - Scène {s_id} (t={ts:.2f}s) : {reason}" for s_id, ts, reason in failed_scenes])
        raise AssertionError(f"Vérification post-rendu échouée : avatar absent dans les scènes suivantes :\n{details}")

    print(f"✓ Vérification avatars réussie sur {len(scenes)} scène(s).")
    return True


def render_video(
    html_path: str = "index.html",
    audio_path: str = "audio_final.wav",
    output_path: str = "output.candidate.mp4",
    fps: int = 30,
    verify_avatars: bool = True,
    scenes: list = None
):
    check_dependencies()

    html_abs = Path(html_path).resolve().as_uri()
    if not Path(audio_path).exists():
        if Path("voix.wav").exists():
            audio_path = "voix.wav"
        else:
            raise FileNotFoundError(f"Fichier audio ({audio_path} ou voix.wav) introuvable.")

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

        context, page = setup_render_page(browser, html_abs)

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
                context, page = setup_render_page(browser, html_abs)

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


if __name__ == "__main__":
    out_target = sys.argv[1] if len(sys.argv) > 1 else "output.candidate.mp4"
    render_video(output_path=out_target)
