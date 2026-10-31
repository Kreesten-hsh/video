#!/usr/bin/env python3
"""
AGENT404 : Script de rendu automatisé des actifs du profil LinkedIn.
Génère à partir des templates originaux verrouillés (profil_linkedin/templates/) :
  1. profil_linkedin/banner_linkedin.png & assets/linkedin_banner_1584x396.png (1584x396 px)
  2. profil_linkedin/featured_card_1_fr.png (1200x675 px) - Présentation de l'offre
  3. profil_linkedin/featured_card_2_fr.png (1200x675 px) - Carte de conversion 48h
  4. profil_linkedin/carousel/slide_1.png à slide_5.png (1600x900 px) - Carrousel 5 slides
  5. profil_linkedin/carousel/carrousel_mecanisme_agent404.pdf (PDF 5 slides, 1200x675 pts)

Design 100% verrouillé (zéro modification de structure, de dégradé, de bordure ou d'icône).
Zéro tiret cadratin. Zéro mention de tarif public.
"""

import base64
from pathlib import Path
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
CAROUSEL_DIR = BASE_DIR / "carousel"
CAROUSEL_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)


def _img_to_data_uri(arr: np.ndarray) -> str:
    """Convertit un tableau RGB numpy en data URI PNG base64 sans fichier résiduel."""
    tmp_path = BASE_DIR / "_tmp_render_buf.png"
    Image.fromarray(arr).save(tmp_path)
    with open(tmp_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    if tmp_path.exists():
        tmp_path.unlink()
    return f"data:image/png;base64,{b64}"


def _interp_vertical(arr: np.ndarray, y_top: int, y_bot: int, x_left: int, x_right: int) -> None:
    """Interpole linéairement colonne par colonne entre y_top et y_bot pour préserver le dégradé radial."""
    for x in range(x_left, x_right):
        c_top = arr[y_top, x].astype(float)
        c_bot = arr[y_bot, x].astype(float)
        for y in range(y_top, y_bot + 1):
            t = (y - y_top) / max(1, (y_bot - y_top))
            arr[y, x] = np.round((1.0 - t) * c_top + t * c_bot).astype(np.uint8)


# =========================================================================
# 1. BANNIÈRE LINKEDIN (1584 x 396 px)
# =========================================================================
def prepare_banner_html() -> str:
    """Prépare la bannière en conservant 100% du design, des stickers et des dégradés."""
    orig_im = Image.open(TEMPLATES_DIR / "base_banner.png").convert("RGB")
    orig_arr = np.array(orig_im)
    arr = orig_arr.copy()

    # 1. Effacer uniquement le texte dans la pilule supérieure gauche (en gardant le point bleu à x < 90)
    pill_bg = orig_arr[55, 85]
    arr[52:81, 90:315] = pill_bg

    # 2. Effacer les 2 sous-lignes sous 'PUBLIEZ' par interpolation verticale sur le dégradé
    _interp_vertical(arr, 175, 210, 1055, 1460)
    _interp_vertical(arr, 210, 246, 1055, 1460)

    # 3. Effacer '100% Broadcast' dans le sticker 5 sans toucher à l'épaule du costume
    sticker_bg = orig_arr[212, 1005]
    for x in range(874, 995):
        y_top = int(round(190 + max(0, x - 910) * 10 / 85))
        if x < 900:
            y_bot = int(round(196 + (x - 870) * 19 / 30))
        else:
            y_bot = 221
        arr[y_top:y_bot, x] = sticker_bg

    banner_uri = _img_to_data_uri(arr)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800;900&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 1584px;
  height: 396px;
  overflow: hidden;
  background-image: url('{banner_uri}');
  background-size: 1584px 396px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  position: relative;
}}
.top-text {{
  position: absolute;
  left: 95px;
  top: 60.5px;
  font-size: 13px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: 0.4px;
  text-transform: uppercase;
  white-space: nowrap;
}}
.sub-1 {{
  position: absolute;
  left: 1062px;
  top: 179px;
  font-size: 23px;
  font-weight: 800;
  color: #111827;
  letter-spacing: -0.2px;
  text-transform: uppercase;
  line-height: 1.25;
  white-space: nowrap;
}}
.sub-2 {{
  position: absolute;
  left: 1062px;
  top: 213px;
  font-size: 22px;
  font-weight: 800;
  color: #111827;
  letter-spacing: -0.2px;
  text-transform: uppercase;
  line-height: 1.25;
  white-space: nowrap;
}}
.sticker-5 {{
  position: absolute;
  left: 895px;
  top: 195px;
  transform: rotate(4.2deg);
  transform-origin: left center;
  font-size: 14.5px;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.1px;
  white-space: nowrap;
}}
</style>
</head>
<body>
<div class="top-text">DM POUR VOTRE VIDÉO PILOTE</div>
<div class="sub-1">DES VIDÉOS VERTICALES SUR LINKEDIN</div>
<div class="sub-2">SANS TOURNAGE NI MONTAGE</div>
<div class="sticker-5">Prêtes à publier</div>
</body>
</html>"""


def postprocess_banner_shoulder(banner_path: Path) -> None:
    """Restaure au pixel près le contour de l'épaule du costume devant le sticker 5."""
    orig_arr = np.array(Image.open(TEMPLATES_DIR / "base_banner.png").convert("RGB"))
    out_arr = np.array(Image.open(banner_path).convert("RGB"))
    for x in range(865, 902):
        y_sh = int(round(196 + (x - 870) * 19 / 30))
        out_arr[y_sh:250, x] = orig_arr[y_sh:250, x]
    Image.fromarray(out_arr).save(banner_path)


# =========================================================================
# 2. CARTES FEATURED (1200 x 675 px) - SUR TEMPLATES ORIGINAUX VERROUILLÉS
# =========================================================================
def prepare_card_1_html() -> str:
    """Prépare la Carte Featured 1 sur base_card_1.png (icônes, cartes décalées et badges conservés)."""
    im = Image.open(TEMPLATES_DIR / "base_card_1.png").convert("RGB")
    arr = np.array(im)

    # Effacer uniquement les zones de texte à l'intérieur des 3 cartes blanches (#FFFFFF)
    # Carte 1 (x=158..422, y=212..268)
    arr[212:268, 158:422] = [255, 255, 255]
    # Carte 2 décalée (x=194..458, y=315..390) - le texte ZÉRO TOURNAGE, ZÉRO CAMÉRA reste identique, sous-texte mis à jour
    arr[315:390, 194:458] = [255, 255, 255]
    # Carte 3 (x=158..422, y=438..515)
    arr[438:515, 158:422] = [255, 255, 255]

    uri = _img_to_data_uri(arr)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 1200px;
  height: 675px;
  overflow: hidden;
  background-image: url('{uri}');
  background-size: 1200px 675px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  position: relative;
}}
.c1-title {{
  position: absolute;
  left: 161px;
  top: 215px;
  font-size: 18px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: -0.2px;
  line-height: 1.2;
}}
.c1-sub {{
  position: absolute;
  left: 161px;
  top: 243px;
  font-size: 12.5px;
  font-weight: 500;
  color: #64748B;
}}
.c2-title {{
  position: absolute;
  left: 198px;
  top: 317px;
  font-size: 18px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: -0.2px;
  line-height: 1.22;
}}
.c2-sub {{
  position: absolute;
  left: 198px;
  top: 369px;
  font-size: 12.5px;
  font-weight: 500;
  color: #64748B;
}}
.c3-title {{
  position: absolute;
  left: 161px;
  top: 448px;
  font-size: 18px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: -0.2px;
  line-height: 1.22;
}}
.c3-sub {{
  position: absolute;
  left: 161px;
  top: 478px;
  font-size: 12.5px;
  font-weight: 500;
  color: #64748B;
}}
</style>
</head>
<body>
<div class="c1-title">1 VIDÉO, 4 PLATEFORMES</div>
<div class="c1-sub">LinkedIn, TikTok, Reels et Shorts</div>

<div class="c2-title">ZÉRO TOURNAGE, ZÉRO<br>CAMÉRA</div>
<div class="c2-sub">À partir d'un post ou d'une note vocale</div>

<div class="c3-title">4 OU 8 VIDÉOS PAR MOIS</div>
<div class="c3-sub">Animation, voix off et sous-titres</div>
</body>
</html>"""


def prepare_card_2_html() -> str:
    """Prépare la Carte Featured 2 sur base_card_2.png (boutons, badge 48h et bordure jaune conservés)."""
    im = Image.open(TEMPLATES_DIR / "base_card_2.png").convert("RGB")
    arr = np.array(im)

    # 1. Effacer 'FORMAT ÉTALON · 60S' (en gardant le point vert à gauche x < 126 et la ligne y=218)
    arr[172:200, 128:310] = [255, 255, 255]
    # 2. Effacer le titre et la description (entre la ligne y=218 et les boutons y=390)
    arr[232:372, 108:580] = [255, 255, 255]

    uri = _img_to_data_uri(arr)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800;900&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 1200px;
  height: 675px;
  overflow: hidden;
  background-image: url('{uri}');
  background-size: 1200px 675px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  position: relative;
}}
.top-label {{
  position: absolute;
  left: 130px;
  top: 182.5px;
  font-size: 11.5px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: 0.4px;
  text-transform: uppercase;
}}
.headline {{
  position: absolute;
  left: 112px;
  top: 238px;
  font-size: 24px;
  font-weight: 900;
  color: #0F172A;
  line-height: 1.25;
  letter-spacing: -0.4px;
  text-transform: uppercase;
}}
.cursor {{
  color: #F59E0B;
  font-weight: 400;
  margin-left: 2px;
}}
.desc {{
  position: absolute;
  left: 112px;
  top: 312px;
  width: 465px;
  font-size: 13.8px;
  font-weight: 500;
  color: #475569;
  line-height: 1.5;
}}
</style>
</head>
<body>
<div class="top-label">VIDÉO PILOTE · 60S</div>
<div class="headline">VOTRE POST LINKEDIN<br>EN VIDÉO ANIMÉE<span class="cursor">|</span></div>
<div class="desc">Envoyez-moi un post récent ou une note vocale de 2 minutes. Nous structurons le script et produisons une vidéo verticale prête à publier.</div>
</body>
</html>"""


# =========================================================================
# 3. GESTION DES 5 SLIDES DU CARROUSEL (1600 x 900 px)
# =========================================================================

def prepare_slide_1() -> str:
    """Slide 1 : VOS ÉCRITS, AUDIOS ET DOCUMENTS DEVIENNENT DES VIDÉOS DE 60S."""
    im = Image.open(TEMPLATES_DIR / "base_slide_1.png").convert("RGB")
    arr = np.array(im)

    # Effacement sans couture par interpolation verticale entre les lignes saines y=205 et y=345
    _interp_vertical(arr, 205, 345, 65, 835)

    uri = _img_to_data_uri(arr)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@800;900&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 1600px;
  height: 900px;
  overflow: hidden;
  background-image: url('{uri}');
  background-size: 1600px 900px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  position: relative;
}}
.slide-title {{
  position: absolute;
  left: 71px;
  top: 218px;
  font-size: 48px;
  font-weight: 900;
  color: #0F172A;
  letter-spacing: -1px;
  text-transform: uppercase;
  line-height: 1.14;
  display: flex;
  flex-direction: column;
}}
.highlight {{
  background: #F5D34F;
  color: #0F172A;
  padding: 2px 14px;
  border-radius: 6px;
  display: inline-block;
  width: fit-content;
}}
.line-2 {{
  display: flex;
  align-items: center;
  gap: 12px;
}}
</style>
</head>
<body>
<div class="slide-title">
  <div>VOS ÉCRITS, AUDIOS ET DOCUMENTS</div>
  <div class="line-2">DEVIENNENT DES <span class="highlight">VIDÉOS DE 60S.</span></div>
</div>
</body>
</html>"""


def prepare_slide_2() -> str:
    """Slide 2 : 100% identique au design validé (aucun changement requis)."""
    im = Image.open(TEMPLATES_DIR / "base_slide_2.png").convert("RGB")
    uri = _img_to_data_uri(np.array(im))
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 1600px;
  height: 900px;
  overflow: hidden;
  background-image: url('{uri}');
  background-size: 1600px 900px;
}}
</style>
</head>
<body></body>
</html>"""


def prepare_slide_3() -> str:
    """Slide 3 : UNE IDÉE FORTE. UNE VIDÉO CLAIRE DE 60S."""
    im = Image.open(TEMPLATES_DIR / "base_slide_3.png").convert("RGB")
    arr = np.array(im)

    # Interpolation verticale entre y=185 et y=252 pour préserver le dégradé
    _interp_vertical(arr, 185, 252, 65, 1000)

    uri = _img_to_data_uri(arr)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@800;900&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 1600px;
  height: 900px;
  overflow: hidden;
  background-image: url('{uri}');
  background-size: 1600px 900px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  position: relative;
}}
.slide-title {{
  position: absolute;
  left: 71px;
  top: 193px;
  font-size: 42px;
  font-weight: 900;
  color: #0F172A;
  letter-spacing: -0.8px;
  text-transform: uppercase;
  line-height: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.highlight {{
  background: #F5D34F;
  color: #0F172A;
  padding: 4px 14px;
  border-radius: 6px;
}}
</style>
</head>
<body>
<div class="slide-title">
  UNE IDÉE FORTE. <span class="highlight">UNE VIDÉO CLAIRE DE 60S.</span>
</div>
</body>
</html>"""


def prepare_slide_4() -> str:
    """Slide 4 : TROIS STYLES. UNE IDENTITÉ COHÉRENTE."""
    im = Image.open(TEMPLATES_DIR / "base_slide_4.png").convert("RGB")
    arr = np.array(im)

    # 1. Effacer le titre (y=188..260) et les 2 lignes de sous-titre (y=260..348) par interpolation verticale
    _interp_vertical(arr, 188, 260, 65, 1050)
    _interp_vertical(arr, 260, 348, 65, 1050)

    # 2. Effacer uniquement l'intérieur blanc (#FFFFFF) des 3 cartes sans déborder ni toucher au badge STYLE NÉO-BRUTALISTE
    arr[380:510, 100:1260] = [255, 255, 255]
    arr[570:700, 95:760] = [255, 255, 255]
    arr[570:700, 835:1500] = [255, 255, 255]

    uri = _img_to_data_uri(arr)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 1600px;
  height: 900px;
  overflow: hidden;
  background-image: url('{uri}');
  background-size: 1600px 900px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  position: relative;
}}
.slide-title {{
  position: absolute;
  left: 71px;
  top: 198px;
  font-size: 42px;
  font-weight: 900;
  color: #0F172A;
  letter-spacing: -0.8px;
  text-transform: uppercase;
  line-height: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.highlight {{
  background: #F5D34F;
  color: #0F172A;
  padding: 4px 14px;
  border-radius: 6px;
}}
.slide-subtitle {{
  position: absolute;
  left: 71px;
  top: 268px;
  font-size: 19px;
  font-weight: 500;
  color: #475569;
  line-height: 1.4;
}}
.pillar-pill {{
  display: inline-block;
  background: #0F172A;
  color: #F5D34F;
  font-size: 11px;
  font-weight: 800;
  padding: 5px 12px;
  border-radius: 6px;
  letter-spacing: 0.6px;
  text-transform: uppercase;
}}
/* Carte Mascotte (Haut) */
.top-card-tag {{
  position: absolute;
  left: 105px;
  top: 384px;
}}
.top-card-title {{
  position: absolute;
  left: 105px;
  top: 420px;
  font-size: 21px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: -0.3px;
}}
.top-card-desc {{
  position: absolute;
  left: 105px;
  top: 454px;
  width: 1140px;
  font-size: 14.8px;
  font-weight: 500;
  color: #475569;
  line-height: 1.48;
}}
/* Carte Éditorial (Bas Gauche) */
.bl-card-tag {{
  position: absolute;
  left: 101px;
  top: 575px;
}}
.bl-card-title {{
  position: absolute;
  left: 101px;
  top: 611px;
  font-size: 21px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: -0.3px;
}}
.bl-card-desc {{
  position: absolute;
  left: 101px;
  top: 645px;
  width: 630px;
  font-size: 14.8px;
  font-weight: 500;
  color: #475569;
  line-height: 1.48;
}}
/* Carte Démonstration (Bas Droite) */
.br-card-tag {{
  position: absolute;
  left: 840px;
  top: 575px;
}}
.br-card-title {{
  position: absolute;
  left: 840px;
  top: 611px;
  font-size: 21px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: -0.3px;
}}
.br-card-desc {{
  position: absolute;
  left: 840px;
  top: 645px;
  width: 630px;
  font-size: 14.8px;
  font-weight: 500;
  color: #475569;
  line-height: 1.48;
}}
</style>
</head>
<body>
<div class="slide-title">
  TROIS STYLES. <span class="highlight">UNE IDENTITÉ COHÉRENTE.</span>
</div>
<div class="slide-subtitle">
  Trois directions artistiques adaptées à votre image.
</div>

<div class="top-card-tag pillar-pill">PILIER 01 · DIRECTION INCARNÉE</div>
<div class="top-card-title">Mascotte : Avatar Illustré Sur Mesure</div>
<div class="top-card-desc">Votre double illustré change de posture et d'expression au fil du propos (explication, coupe, démonstration, conclusion). Votre audience vous reconnaît en une fraction de seconde dans son fil d'actualité.</div>

<div class="bl-card-tag pillar-pill">PILIER 02 · DIRECTION ÉDITORIALE</div>
<div class="bl-card-title">Éditorial : Typographie & Data</div>
<div class="bl-card-desc">Schémas animés, visuels d'appui et typographies fortes synchronisées au mot près pour convertir les décideurs qui consultent LinkedIn en mode muet.</div>

<div class="br-card-tag pillar-pill">PILIER 03 · DIRECTION TECHNIQUE</div>
<div class="br-card-title">Démonstration : Workflows & Interfaces</div>
<div class="br-card-desc">Captures de vos logiciels, architectures et démonstrations concrètes rythmées par un sound design précis avec autorité.</div>
</body>
</html>"""


def prepare_slide_5() -> str:
    """Slide 5 : 8 VIDÉOS PAR MOIS. 4 PLATEFORMES (4 plateformes et logos 100% conservés)."""
    im = Image.open(TEMPLATES_DIR / "base_slide_5.png").convert("RGB")
    arr = np.array(im)

    # Interpolation verticale entre y=185 et y=250 pour préserver le dégradé
    _interp_vertical(arr, 185, 250, 65, 880)

    uri = _img_to_data_uri(arr)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@800;900&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 1600px;
  height: 900px;
  overflow: hidden;
  background-image: url('{uri}');
  background-size: 1600px 900px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  position: relative;
}}
.slide-title {{
  position: absolute;
  left: 71px;
  top: 190px;
  font-size: 42px;
  font-weight: 900;
  color: #0F172A;
  letter-spacing: -0.8px;
  text-transform: uppercase;
  line-height: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.highlight {{
  background: #F5D34F;
  color: #0F172A;
  padding: 4px 14px;
  border-radius: 6px;
}}
</style>
</head>
<body>
<div class="slide-title">
  8 VIDÉOS PAR MOIS. <span class="highlight">4 PLATEFORMES.</span>
</div>
</body>
</html>"""


# =========================================================================
# 4. EXÉCUTION DU RENDU COMPLET
# =========================================================================
def render_all_assets():
    print("▶ Démarrage du moteur de rendu des actifs LinkedIn AGENT404...")

    required_bases = [
        "base_banner.png",
        "base_card_1.png",
        "base_card_2.png",
        "base_slide_1.png",
        "base_slide_2.png",
        "base_slide_3.png",
        "base_slide_4.png",
        "base_slide_5.png",
    ]
    for r in required_bases:
        if not (TEMPLATES_DIR / r).exists():
            raise FileNotFoundError(f"Template manquant : {TEMPLATES_DIR / r}")

    banner_html = prepare_banner_html()
    card_1_html = prepare_card_1_html()
    card_2_html = prepare_card_2_html()
    slide_1_html = prepare_slide_1()
    slide_2_html = prepare_slide_2()
    slide_3_html = prepare_slide_3()
    slide_4_html = prepare_slide_4()
    slide_5_html = prepare_slide_5()

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # 1. Bannière LinkedIn (1584 x 396)
        print("  • Rendu Bannière LinkedIn (1584x396)...")
        page_banner = browser.new_page(viewport={"width": 1584, "height": 396}, device_scale_factor=1)
        page_banner.set_content(banner_html)
        banner_out = BASE_DIR / "banner_linkedin.png"
        page_banner.screenshot(path=str(banner_out))
        page_banner.close()
        postprocess_banner_shoulder(banner_out)

        assets_banner_out = BASE_DIR.parent / "assets" / "linkedin_banner_1584x396.png"
        if assets_banner_out.parent.exists():
            Image.open(banner_out).save(assets_banner_out)

        # 2. Carte Featured 1 (1200 x 675)
        print("  • Rendu Carte Featured 1 (1200x675)...")
        page_c1 = browser.new_page(viewport={"width": 1200, "height": 675}, device_scale_factor=1)
        page_c1.set_content(card_1_html)
        page_c1.screenshot(path=str(BASE_DIR / "featured_card_1_fr.png"))
        page_c1.close()

        # 3. Carte Featured 2 (1200 x 675)
        print("  • Rendu Carte Featured 2 (1200x675)...")
        page_c2 = browser.new_page(viewport={"width": 1200, "height": 675}, device_scale_factor=1)
        page_c2.set_content(card_2_html)
        page_c2.screenshot(path=str(BASE_DIR / "featured_card_2_fr.png"))
        page_c2.close()

        # 4. Slides du carrousel (1600 x 900)
        slides_specs = [
            (slide_1_html, CAROUSEL_DIR / "slide_1.png", "Slide 1"),
            (slide_2_html, CAROUSEL_DIR / "slide_2.png", "Slide 2"),
            (slide_3_html, CAROUSEL_DIR / "slide_3.png", "Slide 3"),
            (slide_4_html, CAROUSEL_DIR / "slide_4.png", "Slide 4"),
            (slide_5_html, CAROUSEL_DIR / "slide_5.png", "Slide 5"),
        ]

        slide_images = []
        for html, out_path, label in slides_specs:
            print(f"  • Rendu Carrousel {label} (1600x900)...")
            page_slide = browser.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=1)
            page_slide.set_content(html)
            page_slide.screenshot(path=str(out_path))
            slide_images.append(Image.open(out_path).convert("RGB"))
            page_slide.close()

        # 5. Compilation du PDF Carrousel (5 pages, 1200 x 675 pts)
        print("  • Compilation du Carrousel PDF (5 pages, ratio 16:9)...")
        pdf_out = CAROUSEL_DIR / "carrousel_mecanisme_agent404.pdf"
        slide_images[0].save(
            str(pdf_out),
            save_all=True,
            append_images=slide_images[1:],
            resolution=96.0,
        )

        browser.close()

    print("✔ Rendu terminé avec succès. Tous les actifs sont alignés et conformes.")


if __name__ == "__main__":
    render_all_assets()
