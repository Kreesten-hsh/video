import os
import sys
import site
from pathlib import Path

# Inclusion automatique du site-packages utilisateur (~/.local)
_user_site = os.path.expanduser("~/.local/lib/python3.12/site-packages")
if _user_site not in sys.path:
    site.addsitedir(_user_site)

# Inclusion du dossier bin local pour ffmpeg / ffprobe
_local_bin = str(Path(__file__).parent.resolve() / "bin")
if _local_bin not in os.environ.get("PATH", ""):
    os.environ["PATH"] = f"{_local_bin}:{os.environ.get('PATH', '')}"

import subprocess
from playwright.sync_api import sync_playwright

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

def render_video(
    html_path: str = "index.html",
    audio_path: str = "audio_final.wav",
    output_path: str = "output.mp4",
    fps: int = 30
):
    html_abs = Path(html_path).resolve().as_uri()
    if not Path(audio_path).exists():
        if Path("voix.wav").exists():
            audio_path = "voix.wav"
        else:
            raise FileNotFoundError(f"Fichier audio ({audio_path} ou voix.wav) introuvable.")

    duration = get_audio_duration(audio_path)
    total_frames = int(duration * fps)
    print(f"[Render] Durée audio : {duration:.2f}s | {total_frames} frames à générer ({fps} FPS).")

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "image2pipe",
        "-vcodec", "mjpeg",
        "-r", str(fps),
        "-i", "pipe:0",
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto(html_abs)
        page.wait_for_load_state("networkidle")

        print("[Render] Capture et encodage direct en mémoire RAM...")
        for i in range(total_frames):
            t = i / float(fps)
            page.evaluate(f"window.setTime({t:.4f})")
            frame_bytes = page.screenshot(type="jpeg", quality=95)
            proc.stdin.write(frame_bytes)

            if i % 15 == 0 or i == total_frames - 1:
                percent = int((i + 1) / total_frames * 100)
                bar = "=" * (percent // 5) + ">" + " " * (20 - (percent // 5))
                sys.stdout.write(f"\r[{bar}] {percent}% ({i+1}/{total_frames} frames) t={t:.2f}s")
                sys.stdout.flush()

        browser.close()

    proc.stdin.close()
    proc.wait()
    print(f"\n✓ Rendu terminé avec succès -> {output_path}")

if __name__ == "__main__":
    render_video()
