import os
import sys
import urllib.request
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
SFX_DIR = BASE_DIR / "assets" / "sfx"
BIN_FFMPEG = BASE_DIR / "bin" / "ffmpeg"
FFMPEG_CMD = str(BIN_FFMPEG) if BIN_FFMPEG.exists() else "ffmpeg"

SOURCES = {
    "whoosh": {
        "url": "https://raw.githubusercontent.com/Calinou/kenney-interface-sounds/master/addons/kenney_interface_sounds/maximize_001.wav",
        "filter": "highpass=f=90,lowpass=f=12000,equalizer=f=300:width_type=o:width=1.2:g=3,equalizer=f=3500:width_type=o:width=1.0:g=-2,afade=t=in:ss=0:d=0.015,afade=t=out:st=0.16:d=0.04,volume=-4dB"
    },
    "pop": {
        "url": "https://raw.githubusercontent.com/Boyquotes/kenney-digital-audio-for-godot/main/addons/kenney%20digital%20audio/pep_sound_1.ogg",
        "filter": "highpass=f=80,lowpass=f=10000,equalizer=f=160:width_type=o:width=1.0:g=4,equalizer=f=4500:width_type=o:width=1.2:g=-3,afade=t=out:st=0.08:d=0.03,volume=-3dB"
    },
    "click": {
        "url": "https://raw.githubusercontent.com/Calinou/kenney-interface-sounds/master/addons/kenney_interface_sounds/tick_001.wav",
        "filter": "highpass=f=150,lowpass=f=11000,equalizer=f=2200:width_type=o:width=1.0:g=3,acompressor=threshold=-16dB:ratio=2.5:attack=1:release=30,volume=-4dB"
    },
    "cash": {
        "url": "https://raw.githubusercontent.com/Boyquotes/kenney-rpg-audio-for-godot/main/addons/kenney%20rpg%20audio/handle_coins.ogg",
        "filter": "highpass=f=200,lowpass=f=13000,equalizer=f=4000:width_type=o:width=1.0:g=2,acompressor=threshold=-14dB:ratio=2:attack=3:release=45,afade=t=out:st=0.40:d=0.08,volume=-3dB"
    },
    "impact": {
        "url": "https://raw.githubusercontent.com/Boyquotes/kenney-rpg-audio-for-godot/main/addons/kenney%20rpg%20audio/book_place_1.ogg",
        "filter": "highpass=f=55,lowpass=f=9000,equalizer=f=110:width_type=o:width=1.0:g=5,equalizer=f=2500:width_type=o:width=1.0:g=-2,acompressor=threshold=-12dB:ratio=3:attack=2:release=60,afade=t=out:st=0.22:d=0.06,volume=-3dB"
    },
    "ding": {
        "url": "https://raw.githubusercontent.com/Calinou/kenney-interface-sounds/master/addons/kenney_interface_sounds/question_001.wav",
        "filter": "highpass=f=300,lowpass=f=14000,equalizer=f=3200:width_type=o:width=0.8:g=3,afade=t=out:st=0.32:d=0.08,volume=-4dB"
    }
}

def fetch_and_process():
    SFX_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[SFX Import] Téléchargement et traitement acoustique haute-fidélité dans {SFX_DIR}...")
    
    for name, item in SOURCES.items():
        url = item["url"]
        af = item["filter"]
        ext = ".ogg" if url.endswith(".ogg") else ".wav"
        temp_file = SFX_DIR / f"_temp_{name}{ext}"
        out_wav = SFX_DIR / f"{name}.wav"
        
        # 1. Téléchargement via urllib
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=10) as resp, open(temp_file, "wb") as f:
            f.write(resp.read())
            
        # 2. Normalisation 44100Hz mono + Chaîne acoustique de mastering
        cmd = [
            FFMPEG_CMD, "-y",
            "-i", str(temp_file),
            "-af", af,
            "-ar", "44100",
            "-ac", "1",
            str(out_wav)
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print(f"Erreur FFmpeg sur {name}: {res.stderr.decode('utf-8', errors='ignore')}")
            sys.exit(1)
            
        if temp_file.exists():
            temp_file.unlink()
            
        size_kb = out_wav.stat().st_size / 1024
        print(f"  ✓ {name}.wav généré ({size_kb:.1f} Ko) - 44100Hz mono")

    print("✓ Tous les 6 bruitages open-source ont été importés et masterisés avec succès.")

if __name__ == "__main__":
    fetch_and_process()
