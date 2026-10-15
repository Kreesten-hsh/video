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

def remove_flat_bg_advanced(img: Image.Image, bg_rgb=(229, 229, 229), tolerance=28) -> Image.Image:
    """
    Détoure le fond uni #E5E5E5 extérieur ET les zones grises fermées entre les bras/corps.
    Protège les zones blanches de la chemise (haute luminosité) et la peau (haute saturation).
    """
    img_rgba = img.convert("RGBA")
    arr = np.array(img_rgba)
    h, w, _ = arr.shape
    
    bg_ref = np.array(bg_rgb, dtype=np.float32)
    rgb = arr[:, :, :3].astype(np.float32)
    diff = np.sqrt(np.sum((rgb - bg_ref) ** 2, axis=-1))

    # 1. Masque par flood-fill depuis l'extérieur
    visited = np.zeros((h, w), dtype=bool)
    mask_ext = np.zeros((h, w), dtype=bool)
    
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0)]
    queue = deque()
    for cx, cy in corners:
        queue.append((cy, cx))
        visited[cy, cx] = True

    while queue:
        y, x = queue.popleft()
        if diff[y, x] <= tolerance:
            mask_ext[y, x] = True
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                    visited[ny, nx] = True
                    if diff[ny, nx] <= tolerance:
                        queue.append((ny, nx))

    # 2. Détection des poches intérieures grises #E5E5E5 (faible saturation, 212 <= R,G,B <= 245)
    r = rgb[:, :, 0]
    g = rgb[:, :, 1]
    b = rgb[:, :, 2]
    
    is_neutral_grey = (
        (diff <= tolerance) &
        (np.abs(r - g) < 14) &
        (np.abs(g - b) < 14) &
        (np.abs(r - b) < 14) &
        (r >= 212) & (r <= 245) &
        (g >= 212) & (g <= 245) &
        (b >= 212) & (b <= 245)
    )

    final_mask = mask_ext | is_neutral_grey
    arr[final_mask, 3] = 0
    nobg = Image.fromarray(arr)
    return keep_largest_component(nobg)

def keep_largest_component(img: Image.Image) -> Image.Image:
    """Conserve UNIQUEMENT la plus grande composante connexe (alpha > 128) et élimine les îlots/taches grises isolées."""
    arr = np.array(img)
    alpha = arr[:, :, 3]
    fg_mask = alpha > 128
    
    try:
        from scipy.ndimage import label
        labeled_array, num_features = label(fg_mask)
        if num_features > 1:
            sizes = np.bincount(labeled_array.ravel())
            sizes[0] = 0  # ignore background
            largest_label = sizes.argmax()
            clean_mask = (labeled_array == largest_label)
            arr[~clean_mask, 3] = 0
    except Exception:
        # Fallback BFS pur Python/NumPy
        h, w = fg_mask.shape
        visited = np.zeros((h, w), dtype=bool)
        best_comp = []
        for y in range(h):
            for x in range(w):
                if fg_mask[y, x] and not visited[y, x]:
                    comp = []
                    q = deque([(y, x)])
                    visited[y, x] = True
                    while q:
                        cy, cx = q.popleft()
                        comp.append((cy, cx))
                        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < h and 0 <= nx < w and fg_mask[ny, nx] and not visited[ny, nx]:
                                visited[ny, nx] = True
                                q.append((ny, nx))
                    if len(comp) > len(best_comp):
                        best_comp = comp
        clean_mask = np.zeros((h, w), dtype=bool)
        for cy, cx in best_comp:
            clean_mask[cy, cx] = True
        arr[~clean_mask, 3] = 0

    return Image.fromarray(arr)

def fit_in_canvas(img: Image.Image, target_size=(900, 1050), padding_x=40, padding_top=40, stick_to_bottom=True) -> Image.Image:
    """
    Autocrop sur le canal alpha pour éliminer toute marge transparente inutile,
    puis redimensionne et place le personnage dans target_size.
    Si stick_to_bottom=True, collé exactement au bord inférieur (y = th - new_h).
    """
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    tw, th = target_size
    avail_w = tw - 2 * padding_x
    avail_h = (th - padding_top) if stick_to_bottom else (th - 2 * padding_top)
    scale = min(avail_w / img.width, avail_h / img.height)
    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
    pos_x = (tw - new_w) // 2
    pos_y = (th - new_h) if stick_to_bottom else (th - new_h) // 2
    canvas.paste(resized, (pos_x, pos_y), resized)
    return canvas

def apply_sticker_effect(nobg_canvas: Image.Image) -> Image.Image:
    """Génère la double bordure blanche + noire en pur MaxFilter (zéro scipy, zéro IA)."""
    alpha = nobg_canvas.split()[3]
    
    # 1. Bordure blanche interne via MaxFilter(25)
    alpha_white = alpha.filter(ImageFilter.MaxFilter(25))
    
    # 2. Bordure noire externe via MaxFilter(11) sur l'alpha blanc
    alpha_black = alpha_white.filter(ImageFilter.MaxFilter(11))
    
    w, h = nobg_canvas.size
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    black_layer = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    white_layer = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    
    result.paste(black_layer, (0, 0), alpha_black)
    result.paste(white_layer, (0, 0), alpha_white)
    result.paste(nobg_canvas, (0, 0), nobg_canvas)
    
    return result

def main():
    raw_dir = Path("raw_avatars")
    out_dir = Path("assets/avatars")
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_files = sorted(list(raw_dir.glob("*.jpg")) + list(raw_dir.glob("*.png")))
    print(f"[Build Stickers] Traitement et recadrage 900x1050 bas sur {len(raw_files)} avatars vers {out_dir}/...")

    for file_path in raw_files:
        name = file_path.stem
        out_path = out_dir / f"{name}.png"
        with Image.open(file_path) as raw:
            nobg = remove_flat_bg_advanced(raw)
            fitted = fit_in_canvas(nobg, target_size=(900, 1050), padding_x=40, padding_top=40, stick_to_bottom=True)
            sticker = apply_sticker_effect(fitted)
            sticker.save(out_path, "PNG")

    # mini.png pour dialogue RPG (crop tête en 700x700 centré)
    pointing_path = raw_dir / "pointing.jpg"
    if pointing_path.exists():
        with Image.open(pointing_path) as raw:
            nobg = remove_flat_bg_advanced(raw)
            w, h = nobg.size
            head = nobg.crop((int(w * 0.15), 0, int(w * 0.85), int(h * 0.52)))
            fitted = fit_in_canvas(head, target_size=(700, 700), padding_x=40, padding_top=40, stick_to_bottom=False)
            mini_sticker = apply_sticker_effect(fitted)
            mini_sticker.save(out_dir / "mini.png", "PNG")

    print(f"✓ Tous les 12 stickers sont régénérés avec poches fermées nettoyées dans {out_dir}/")

if __name__ == "__main__":
    main()
