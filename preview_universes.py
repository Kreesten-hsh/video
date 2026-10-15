import os
import sys
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent.resolve()
HTML_OUT = BASE_DIR / "comparatif_univers.html"
PNG_OUT = BASE_DIR / "comparatif_univers.png"
AVATAR_PATH = (BASE_DIR / "assets" / "avatars" / "pointing.png").as_uri()

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=2160, height=1920, initial-scale=1.0">
  <title>Comparatif 4 Univers Graphiques</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Syne:wght@800;900&family=JetBrains+Mono:wght@700;800&family=Space+Grotesk:wght@700;800&display=swap" rel="stylesheet">
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-font-smoothing: antialiased;
    }}
    body {{
      width: 2160px;
      height: 1920px;
      overflow: hidden;
      display: flex;
      flex-direction: row;
      background: #000000;
      font-family: 'Montserrat', sans-serif;
    }}

    /* PANNEAU GÉNÉRIQUE (540x1920) */
    .panel {{
      width: 540px;
      height: 1920px;
      position: relative;
      overflow: hidden;
      border-right: 4px solid #000000;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 50px 24px 0 24px;
    }}
    .panel:last-child {{
      border-right: none;
    }}

    /* BANDEAU EN-TÊTE UNIVERS */
    .panel-header {{
      width: 100%;
      text-align: center;
      padding: 16px 12px;
      border-radius: 12px;
      font-weight: 900;
      font-size: 26px;
      text-transform: uppercase;
      letter-spacing: -0.5px;
      border: 3px solid #000000;
      box-shadow: 4px 4px 0px #000000;
      margin-bottom: 50px;
      z-index: 10;
    }}

    /* SOUS-TITRES (TOP) */
    .sub-box {{
      width: 100%;
      border-radius: 16px;
      padding: 18px 16px;
      display: inline-flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: center;
      gap: 10px 14px;
      text-align: center;
      margin-bottom: 60px;
      z-index: 10;
    }}
    .sub-word {{
      font-size: 34px;
      font-weight: 800;
      margin: 0 4px;
      letter-spacing: -0.5px;
    }}
    .sub-word.active {{
      transform: scale(1.12);
      font-weight: 900;
    }}

    /* CARTE STATS (MILIEU) */
    .middle-zone {{
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
      z-index: 10;
    }}
    .stat-card {{
      width: 100%;
      padding: 24px 20px;
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .stat-val {{
      font-size: 46px;
      font-weight: 900;
      line-height: 1.1;
      letter-spacing: -1.5px;
    }}
    .stat-sub {{
      font-size: 20px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    /* ZONE AVATAR (BAS ANCRÉ) */
    .avatar-zone {{
      position: absolute;
      bottom: 0;
      left: 0;
      width: 540px;
      height: 960px;
      display: flex;
      justify-content: center;
      align-items: flex-end;
      pointer-events: none;
      z-index: 5;
    }}
    .avatar-img {{
      height: 820px;
      width: auto;
      object-fit: contain;
      filter: drop-shadow(0 15px 30px rgba(0,0,0,0.5));
    }}
    .avatar-badge {{
      position: absolute;
      bottom: 60px;
      padding: 14px 28px;
      border-radius: 999px;
      font-weight: 900;
      font-size: 26px;
      letter-spacing: -0.5px;
      z-index: 20;
      pointer-events: auto;
    }}

    /* ==========================================================================
       PANNEAU 1 : CYBER-MINT (Noir & Émeraude)
       ========================================================================== */
    #panel-1 {{
      background-color: #0D1117;
      background-image: radial-gradient(#1F2937 2px, transparent 2px);
      background-size: 26px 26px;
    }}
    #panel-1 .panel-header {{
      background: #00F5A0;
      color: #0D1117;
      border-color: #000000;
      box-shadow: 4px 4px 0px #000000;
    }}
    #panel-1 .sub-box {{
      background: #FFFFFF;
      border: 4px solid #00F5A0;
      box-shadow: 6px 6px 0px #00F5A0;
      color: #0D1117;
    }}
    #panel-1 .sub-word.active {{
      color: #00BA76;
    }}
    #panel-1 .stat-card.c1 {{
      background: #FFFFFF;
      color: #0D1117;
      border: 4px solid #000000;
      box-shadow: 6px 6px 0px #00F5A0;
    }}
    #panel-1 .stat-card.c2 {{
      background: #00F5A0;
      color: #0D1117;
      border: 4px solid #000000;
      box-shadow: 6px 6px 0px #000000;
    }}
    #panel-1 .avatar-badge {{
      background: #00F5A0;
      color: #0D1117;
      border: 4px solid #000000;
      box-shadow: 6px 6px 0px #000000;
    }}

    /* ==========================================================================
       PANNEAU 2 : DOSSIER CLASSIFIÉ (Kraft, Noir & Orange)
       ========================================================================== */
    #panel-2 {{
      background-color: #E8E2D5;
      background-image: 
        linear-gradient(rgba(0,0,0,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,0,0,0.06) 1px, transparent 1px);
      background-size: 32px 32px;
      font-family: 'JetBrains Mono', monospace;
    }}
    #panel-2 .panel-header {{
      background: #FF4F00;
      color: #FFFFFF;
      border-color: #1C1917;
      box-shadow: 4px 4px 0px #1C1917;
      font-family: 'JetBrains Mono', monospace;
    }}
    #panel-2 .sub-box {{
      background: #FFFFFF;
      border: 4px solid #1C1917;
      box-shadow: 6px 6px 0px #1C1917;
      color: #1C1917;
    }}
    #panel-2 .sub-word.active {{
      color: #FF4F00;
      text-decoration: underline;
    }}
    #panel-2 .stat-card.c1 {{
      background: #F4F0E8;
      color: #1C1917;
      border: 4px solid #1C1917;
      box-shadow: 6px 6px 0px #1C1917;
      position: relative;
    }}
    #panel-2 .stat-card.c1::after {{
      content: "CLASSÉ";
      position: absolute;
      top: 10px;
      right: 14px;
      background: #10B981;
      color: #FFFFFF;
      font-size: 14px;
      padding: 4px 8px;
      font-weight: 800;
      border: 2px solid #1C1917;
    }}
    #panel-2 .stat-card.c2 {{
      background: #FF4F00;
      color: #FFFFFF;
      border: 4px solid #1C1917;
      box-shadow: 6px 6px 0px #1C1917;
    }}
    #panel-2 .avatar-badge {{
      background: #10B981;
      color: #FFFFFF;
      border: 4px solid #1C1917;
      box-shadow: 6px 6px 0px #1C1917;
      font-family: 'JetBrains Mono', monospace;
    }}

    /* ==========================================================================
       PANNEAU 3 : POP-ACID (Violet Électrique & Citron)
       ========================================================================== */
    #panel-3 {{
      background-color: #EEF2F6;
      background-image: radial-gradient(#6D28D9 1.5px, transparent 1.5px);
      background-size: 28px 28px;
    }}
    #panel-3 .panel-header {{
      background: #CCFF00;
      color: #6D28D9;
      border-color: #6D28D9;
      box-shadow: 4px 4px 0px #6D28D9;
      font-family: 'Syne', sans-serif;
    }}
    #panel-3 .sub-box {{
      background: #FFFFFF;
      border: 4px solid #6D28D9;
      box-shadow: 6px 6px 0px #CCFF00;
      color: #1E1B4B;
    }}
    #panel-3 .sub-word.active {{
      color: #6D28D9;
      background: #CCFF00;
      padding: 2px 10px;
      border-radius: 8px;
    }}
    #panel-3 .stat-card.c1 {{
      background: #FFFFFF;
      color: #6D28D9;
      border: 4px solid #6D28D9;
      box-shadow: 6px 6px 0px #6D28D9;
    }}
    #panel-3 .stat-card.c2 {{
      background: #6D28D9;
      color: #CCFF00;
      border: 4px solid #000000;
      box-shadow: 6px 6px 0px #CCFF00;
    }}
    #panel-3 .avatar-badge {{
      background: #CCFF00;
      color: #6D28D9;
      border: 4px solid #6D28D9;
      box-shadow: 6px 6px 0px #6D28D9;
      font-family: 'Syne', sans-serif;
    }}

    /* ==========================================================================
       PANNEAU 4 : BLUEPRINT (Bleu Architecte & Cyan)
       ========================================================================== */
    #panel-4 {{
      background-color: #0A192F;
      background-image: 
        linear-gradient(rgba(0, 229, 255, 0.2) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 229, 255, 0.2) 1px, transparent 1px),
        linear-gradient(rgba(0, 229, 255, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 229, 255, 0.08) 1px, transparent 1px);
      background-size: 80px 80px, 80px 80px, 20px 20px, 20px 20px;
      font-family: 'Space Grotesk', sans-serif;
    }}
    #panel-4 .panel-header {{
      background: #00E5FF;
      color: #0A192F;
      border-color: #FFFFFF;
      box-shadow: 4px 4px 0px #FFB800;
    }}
    #panel-4 .sub-box {{
      background: #0F2744;
      border: 4px solid #00E5FF;
      box-shadow: 6px 6px 0px rgba(0, 229, 255, 0.5);
      color: #FFFFFF;
    }}
    #panel-4 .sub-word.active {{
      color: #FFB800;
    }}
    #panel-4 .stat-card.c1 {{
      background: #FFFFFF;
      color: #0A192F;
      border: 4px solid #00E5FF;
      box-shadow: 6px 6px 0px #00E5FF;
    }}
    #panel-4 .stat-card.c2 {{
      background: #00E5FF;
      color: #0A192F;
      border: 4px solid #FFFFFF;
      box-shadow: 6px 6px 0px #FFB800;
    }}
    #panel-4 .avatar-badge {{
      background: #FFB800;
      color: #0A192F;
      border: 4px solid #000000;
      box-shadow: 6px 6px 0px #00E5FF;
    }}
  </style>
</head>
<body>

  <!-- 1. CYBER-MINT -->
  <div class="panel" id="panel-1">
    <div class="panel-header">1. CYBER-MINT</div>
    <div class="sub-box">
      <span class="sub-word">Arrête</span>
      <span class="sub-word">de</span>
      <span class="sub-word active">payer</span>
      <span class="sub-word">des</span>
    </div>
    <div class="middle-zone">
      <div class="stat-card c1">
        <div class="stat-val">3 000 € / MOIS</div>
        <div class="stat-sub">MONTEURS CLASSIQUES 🛑</div>
      </div>
      <div class="stat-card c2">
        <div class="stat-val">0 € FACTURE</div>
        <div class="stat-sub">100% CODE AUTOMATISÉ ⚡</div>
      </div>
    </div>
    <div class="avatar-zone">
      <img src="{AVATAR_PATH}" class="avatar-img" alt="Avatar Pointing">
      <div class="avatar-badge">MOTEUR 100% IA ⚡</div>
    </div>
  </div>

  <!-- 2. DOSSIER CLASSIFIÉ -->
  <div class="panel" id="panel-2">
    <div class="panel-header">2. DOSSIER CLASSIFIÉ</div>
    <div class="sub-box">
      <span class="sub-word">Arrête</span>
      <span class="sub-word">de</span>
      <span class="sub-word active">payer</span>
      <span class="sub-word">des</span>
    </div>
    <div class="middle-zone">
      <div class="stat-card c1">
        <div class="stat-val">3 000 € / MOIS</div>
        <div class="stat-sub">AGENCE VIDÉO 📁</div>
      </div>
      <div class="stat-card c2">
        <div class="stat-val">DÉCLASSIFIÉ</div>
        <div class="stat-sub">PIPELINE PYTHON DIRECT 🎯</div>
      </div>
    </div>
    <div class="avatar-zone">
      <img src="{AVATAR_PATH}" class="avatar-img" alt="Avatar Pointing">
      <div class="avatar-badge">DOSSIER VALIDÉ ✓</div>
    </div>
  </div>

  <!-- 3. POP-ACID -->
  <div class="panel" id="panel-3">
    <div class="panel-header">3. POP-ACID</div>
    <div class="sub-box">
      <span class="sub-word">Arrête</span>
      <span class="sub-word">de</span>
      <span class="sub-word active">payer</span>
      <span class="sub-word">des</span>
    </div>
    <div class="middle-zone">
      <div class="stat-card c1">
        <div class="stat-val">48H DÉLAI</div>
        <div class="stat-sub">VIBE OBSOLÈTE 🐌</div>
      </div>
      <div class="stat-card c2">
        <div class="stat-val">2 MINUTES</div>
        <div class="stat-sub">GÉNÉRATION INSTANTANÉE 🍋</div>
      </div>
    </div>
    <div class="avatar-zone">
      <img src="{AVATAR_PATH}" class="avatar-img" alt="Avatar Pointing">
      <div class="avatar-badge">100% IA FAST ⚡</div>
    </div>
  </div>

  <!-- 4. BLUEPRINT -->
  <div class="panel" id="panel-4">
    <div class="panel-header">4. BLUEPRINT</div>
    <div class="sub-box">
      <span class="sub-word">Arrête</span>
      <span class="sub-word">de</span>
      <span class="sub-word active">payer</span>
      <span class="sub-word">des</span>
    </div>
    <div class="middle-zone">
      <div class="stat-card c1">
        <div class="stat-val">3 000 € / MOIS</div>
        <div class="stat-sub">COÛT PRODUCTION 📐</div>
      </div>
      <div class="stat-card c2">
        <div class="stat-val">0 € / CODE</div>
        <div class="stat-sub">PIPELINE HEADLESS 🚀</div>
      </div>
    </div>
    <div class="avatar-zone">
      <img src="{AVATAR_PATH}" class="avatar-img" alt="Avatar Pointing">
      <div class="avatar-badge">SPEC ARCHITECTURE 📐</div>
    </div>
  </div>

</body>
</html>
"""

def render_preview():
    print("[Playwright] Écriture du template de comparaison...")
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    print("[Playwright] Lancement sécurisé (--disable-gpu, --no-sandbox) en 2160x1920...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--js-flags=--max-old-space-size=1024"
            ]
        )
        context = browser.new_context(viewport={"width": 2160, "height": 1920}, device_scale_factor=1)
        page = context.new_page()
        page.goto(HTML_OUT.as_uri())
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)

        print(f"[Playwright] Capture de {PNG_OUT} (2160x1920)...")
        page.screenshot(path=str(PNG_OUT), full_page=True)
        browser.close()

    if HTML_OUT.exists():
        HTML_OUT.unlink()

    print(f"✓ Planche visuelle générée avec succès : {PNG_OUT}")
    
    # Ouverture automatique via xdg-open
    try:
        subprocess.Popen(["xdg-open", str(PNG_OUT)])
        print("✓ Aperçu ouvert automatiquement via xdg-open.")
    except Exception as e:
        print(f"Note xdg-open: {e}")

if __name__ == "__main__":
    render_preview()
