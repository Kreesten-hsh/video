import os
import sys
import site
from pathlib import Path
from collections import deque

_user_site = os.path.expanduser("~/.local/lib/python3.12/site-packages")
if _user_site not in sys.path:
    site.addsitedir(_user_site)

import numpy as np
from PIL import Image
from scipy import ndimage

def remove_flat_bg(img: Image.Image, bg_rgb=(229, 229, 229), tolerance=28) -> Image.Image:
    """
    Suppression d'arrière-plan ultra-rapide par flood-fill depuis les coins.
    Protège parfaitement les yeux et vêtements blancs à l'intérieur du contour noir.
    """
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

def create_sticker(
    nobg_img: Image.Image,
    white_border_px: int = 18,
    black_border_px: int = 8,
    target_size: tuple = (900, 900)
) -> Image.Image:
    """
    Applique par dilatation morphologique (distance transform + lissage gaussien) :
    - 18px bordure blanche (#FFFFFF)
    - 8px bordure noire (#000000)
    - Centrage propre en 900x900px
    """
    rgba = np.array(nobg_img)
    alpha = rgba[:, :, 3]
    char_mask = alpha > 40

    # Distance euclidienne à l'extérieur du personnage
    dist = ndimage.distance_transform_edt(~char_mask)

    total_border = white_border_px + black_border_px
    white_mask = dist <= white_border_px
    black_mask = dist <= total_border

    # Lissage gaussien pour adoucir les courbes du sticker
    black_float = ndimage.gaussian_filter(black_mask.astype(float), sigma=1.2)
    white_float = ndimage.gaussian_filter(white_mask.astype(float), sigma=1.2)

    black_smooth = black_float > 0.45
    white_smooth = white_float > 0.45

    h, w = alpha.shape
    out_arr = np.zeros((h, w, 4), dtype=np.uint8)

    # Couche noire externe
    out_arr[black_smooth] = [0, 0, 0, 255]
    # Couche blanche interne
    out_arr[white_smooth] = [255, 255, 255, 255]
    # Couche personnage (au-dessus)
    out_arr[char_mask] = rgba[char_mask]

    sticker_img = Image.fromarray(out_arr)

    # Centrage et redimensionnement en 900x900
    bbox = sticker_img.getbbox()
    if bbox:
        cropped = sticker_img.crop(bbox)
    else:
        cropped = sticker_img

    cw, ch = cropped.size
    tw, th = target_size
    margin = 30
    avail_w = tw - 2 * margin
    avail_h = th - 2 * margin

    scale = min(avail_w / cw, avail_h / ch)
    new_w = max(1, int(cw * scale))
    new_h = max(1, int(ch * scale))
    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
    pos_x = (tw - new_w) // 2
    pos_y = th - new_h - margin
    canvas.paste(resized, (pos_x, pos_y), resized)

    return canvas

def process_all():
    raw_dir = Path("raw_avatars")
    out_dir = Path("assets/avatars")
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_files = sorted(list(raw_dir.glob("*.jpg")) + list(raw_dir.glob("*.png")))
    print(f"[Build Stickers] Traitement de {len(raw_files)} avatars vers {out_dir}/...")

    for file_path in raw_files:
        name = file_path.stem
        out_path = out_dir / f"{name}.png"
        print(f"  -> Traitement {file_path.name} -> {out_path.name}")
        with Image.open(file_path) as raw:
            nobg = remove_flat_bg(raw)
            sticker = create_sticker(nobg, white_border_px=18, black_border_px=8, target_size=(900, 900))
            sticker.save(out_path, "PNG")

    # mini.png pour dialogue RPG (crop tête en 900x900)
    pointing_path = raw_dir / "pointing.jpg"
    if pointing_path.exists():
        print("  -> Génération mini.png (crop tête)...")
        with Image.open(pointing_path) as raw:
            nobg = remove_flat_bg(raw)
            w, h = nobg.size
            head = nobg.crop((int(w * 0.15), int(h * 0.0), int(w * 0.85), int(h * 0.52)))
            mini_sticker = create_sticker(head, white_border_px=14, black_border_px=6, target_size=(900, 900))
            mini_sticker.save(out_dir / "mini.png", "PNG")

    print("✓ Tous les stickers 900x900 avec double bordure (18px blanc / 8px noir) sont générés !")

if __name__ == "__main__":
    process_all()
