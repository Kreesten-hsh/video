import os
import sys
import site
from pathlib import Path
from collections import deque

_user_site = os.path.expanduser("~/.local/lib/python3.12/site-packages")
if _user_site not in sys.path:
    site.addsitedir(_user_site)

import numpy as np
from PIL import Image, ImageFilter

def remove_flat_bg(img: Image.Image, bg_rgb=(229, 229, 229), tolerance=28) -> Image.Image:
    """Détoure le fond uni #E5E5E5 par flood-fill NumPy ultra-rapide."""
    img_rgba = img.convert("RGBA")
    arr = np.array(img_rgba)
    h, w, _ = arr.shape
    
    bg_ref = np.array(bg_rgb, dtype=np.float32)
    rgb = arr[:, :, :3].astype(np.float32)
    diff = np.sqrt(np.sum((rgb - bg_ref) ** 2, axis=-1))

    visited = np.zeros((h, w), dtype=bool)
    mask = np.zeros((h, w), dtype=bool)
    
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0)]
    queue = deque()
    for cx, cy in corners:
        queue.append((cy, cx))
        visited[cy, cx] = True

    while queue:
        y, x = queue.popleft()
        if diff[y, x] <= tolerance:
            mask[y, x] = True
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                    visited[ny, nx] = True
                    if diff[ny, nx] <= tolerance:
                        queue.append((ny, nx))

    arr[mask, 3] = 0
    return Image.fromarray(arr)

def fit_in_canvas(img: Image.Image, target_size=(700, 700), padding=40) -> Image.Image:
    """Recadre et centre dans un canevas 700x700 avec padding pour ne jamais couper les bords."""
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    tw, th = target_size
    avail_w = tw - 2 * padding
    avail_h = th - 2 * padding
    scale = min(avail_w / img.width, avail_h / img.height)
    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
    pos_x = (tw - new_w) // 2
    pos_y = th - new_h - padding
    canvas.paste(resized, (pos_x, pos_y), resized)
    return canvas

def apply_sticker_effect(nobg_700: Image.Image) -> Image.Image:
    """Génère la double bordure blanche + noire en pur MaxFilter (zéro scipy, zéro IA)."""
    alpha = nobg_700.split()[3]
    
    # 1. Bordure blanche interne via MaxFilter(25)
    alpha_white = alpha.filter(ImageFilter.MaxFilter(25))
    
    # 2. Bordure noire externe via MaxFilter(11) sur l'alpha blanc
    alpha_black = alpha_white.filter(ImageFilter.MaxFilter(11))
    
    w, h = nobg_700.size
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    black_layer = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    white_layer = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    
    # Superposition : calque noir -> calque blanc -> personnage
    result.paste(black_layer, (0, 0), alpha_black)
    result.paste(white_layer, (0, 0), alpha_white)
    result.paste(nobg_700, (0, 0), nobg_700)
    
    return result

def main():
    raw_dir = Path("raw_avatars")
    out_dir = Path("assets/avatars")
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_files = sorted(list(raw_dir.glob("*.jpg")) + list(raw_dir.glob("*.png")))
    print(f"[Build Stickers] Traitement ultra-léger de {len(raw_files)} avatars vers {out_dir}/...")

    for file_path in raw_files:
        name = file_path.stem
        out_path = out_dir / f"{name}.png"
        with Image.open(file_path) as raw:
            nobg = remove_flat_bg(raw)
            fitted = fit_in_canvas(nobg, target_size=(700, 700), padding=40)
            sticker = apply_sticker_effect(fitted)
            sticker.save(out_path, "PNG")

    # mini.png pour dialogue RPG (crop tête en 700x700)
    pointing_path = raw_dir / "pointing.jpg"
    if pointing_path.exists():
        with Image.open(pointing_path) as raw:
            nobg = remove_flat_bg(raw)
            w, h = nobg.size
            head = nobg.crop((int(w * 0.15), 0, int(w * 0.85), int(h * 0.52)))
            fitted = fit_in_canvas(head, target_size=(700, 700), padding=50)
            mini_sticker = apply_sticker_effect(fitted)
            mini_sticker.save(out_dir / "mini.png", "PNG")

    print(f"✓ Tous les 12 stickers sont prêts en pur Pillow/NumPy dans {out_dir}/")

if __name__ == "__main__":
    main()
