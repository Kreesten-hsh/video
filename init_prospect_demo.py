#!/usr/bin/env python3
"""
AGENT404 : Initialisateur de Démo Prospect B2B (Outbound Visual Trojan Horse).

Lit `prospects/prospects_top20.json` et configure automatiquement le studio client :
- Crée `studio_clients/<slug_prospect>/`
- Génère `brand.json` aux couleurs de marque du prospect
- Calibre `project.json` (teaser 15.10s sur 3 Blueprints universels)
- Découpe et calibre `voix.wav` et `words.json` pour validation temporelle parfaite
- Compile automatiquement `timeline.js` via `build_master_timeline.py`

Usage :
  python3 init_prospect_demo.py --id 1
  python3 init_prospect_demo.py --id 01
  python3 init_prospect_demo.py --list
  python3 init_prospect_demo.py --all
"""

import os
import sys
import wave
import json
import shutil
import argparse
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
PROSPECTS_JSON_PATH = REPO_ROOT / "prospects" / "prospects_top20.json"
TEMPLATE_DIR = REPO_ROOT / "studio_clients" / "_template_prospect"


def load_prospects() -> list:
    """Charge le fichier source des 20 prospects qualifiés."""
    if not PROSPECTS_JSON_PATH.exists():
        print(f"[Information] Fichier de prospection introuvable : {PROSPECTS_JSON_PATH}")
        print("Les données de prospection privées ne sont pas suivies dans le dépôt public.")
        sys.exit(0)
    try:
        with open(PROSPECTS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Erreur] Impossible de parser {PROSPECTS_JSON_PATH} : {e}")
        sys.exit(1)


def list_prospects(prospects: list):
    """Affiche la liste récapitulative des prospects disponibles."""
    print("=" * 88)
    print("AGENT404 : TOP 20 PROSPECTS B2B ULTRA-QUALIFIÉS (OUTBOUND INTELLIGENCE)")
    print("=" * 88)
    for p in prospects:
        pid = f"#{p['id']:02d}"
        name = p['identity']['full_name']
        company = p['identity']['company']
        topic = p['visual_trojan_horse']['teaser_topic']
        slug = p['slug']
        dest_dir = REPO_ROOT / "studio_clients" / slug
        status = "[PRÊT]" if (dest_dir / "timeline.js").exists() else "[NON INIT]"
        print(f" {pid} | {name:<20} | {company:<25} | {status} | {topic[:30]}...")
    print("=" * 88)
    print("Pour initialiser un prospect : python3 init_prospect_demo.py --id <num>")


def trim_wav_pure_python(in_wav: Path, out_wav: Path, duration_sec: float):
    """Découpe un fichier WAV sans dépendance externe via le module standard wave."""
    with wave.open(str(in_wav), "rb") as f_in:
        params = f_in.getparams()
        n_frames = min(f_in.getnframes(), int(params.framerate * duration_sec))
        frames = f_in.readframes(n_frames)
    with wave.open(str(out_wav), "wb") as f_out:
        f_out.setparams(params)
        f_out.writeframes(frames)


def init_prospect(prospect: dict, force: bool = False, compile_timeline: bool = True) -> Path:
    """Initialise le dossier client et ses configurations."""
    slug = prospect["slug"]
    target_dir = REPO_ROOT / "studio_clients" / slug

    if target_dir.exists() and not force:
        print(f"ℹ️ Le dossier {target_dir.name} existe déjà. Utilisez --force pour écraser.")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Dossier inspect_frames
    (target_dir / "inspect_frames").mkdir(exist_ok=True)

    # 2. Génération de brand.json
    brand_data = prospect["visual_trojan_horse"]["brand_preset"]
    brand_path = target_dir / "brand.json"
    with open(brand_path, "w", encoding="utf-8") as f:
        json.dump(brand_data, f, indent=2, ensure_ascii=False)
    print(f"  [OK] brand.json généré ({brand_data['brand_name']})")

    # 3. Calibration audio 15.10s et words.json (49 mots)
    target_dur = 15.10
    template_wav = TEMPLATE_DIR / "voix.wav"
    template_mp3 = TEMPLATE_DIR / "voix.mp3"
    template_words = TEMPLATE_DIR / "words.json"

    dst_wav = target_dir / "voix.wav"
    dst_words = target_dir / "words.json"

    if template_wav.exists():
        trim_wav_pure_python(template_wav, dst_wav, target_dur)
        # Copie optionnelle du mp3 si présent
        if template_mp3.exists() and not (target_dir / "voix.mp3").exists():
            shutil.copy2(template_mp3, target_dir / "voix.mp3")
        print(f"  [OK] voix.wav calibré à {target_dur}s")

    # Découpe des mots synchronisés pour correspondre exactement aux 3 scènes
    # Scène 1 : 0.0s -> 5.14s (mot final: "Pourtant", idx 15)
    # Scène 2 : 5.14s -> 11.06s (mot final: "lumière", idx 35)
    # Scène 3 : 11.06s -> 15.10s (mot final: "refuser", idx 48)
    words_data = []
    if template_words.exists():
        with open(template_words, "r", encoding="utf-8") as wf:
            all_words = json.load(wf)
            words_data = all_words[:49]
        with open(dst_words, "w", encoding="utf-8") as wf:
            json.dump(words_data, wf, indent=2, ensure_ascii=False)
        print(f"  [OK] words.json synchronisé ({len(words_data)} mots)")

    ref_words = [w["word"] for w in words_data]
    scene_end_words = ["Pourtant", "lumière", "refuser"]

    # 4. Calibrer les scènes avec les timestamps exacts
    raw_scenes = prospect["visual_trojan_horse"]["scenes"]
    calibrated_scenes = []

    timestamps = [
        (0.0, 5.14),
        (5.14, 11.06),
        (11.06, 15.10)
    ]

    for idx, sc in enumerate(raw_scenes[:3]):
        st, en = timestamps[idx]
        sc_copy = dict(sc)
        sc_copy["start"] = st
        sc_copy["end"] = en
        # S'assurer que le chemin d'avatar pointe vers assets/avatars/
        if "data" not in sc_copy:
            sc_copy["data"] = {}
        if not sc_copy["data"].get("avatar"):
            sc_copy["data"]["avatar"] = "assets/avatars/idea.png"
        calibrated_scenes.append(sc_copy)

    project_data = {
        "video_number": prospect["id"],
        "title": f"Teaser 15s - {prospect['identity']['full_name']} ({prospect['identity']['company']})",
        "audio_path": "voix.wav",
        "theme": "claude",
        "theme_preset": "claude",
        "phonetic_map": {},
        "special_cases": {},
        "scene_end_words": scene_end_words,
        "reference_words": ref_words,
        "scenes": calibrated_scenes
    }

    project_path = target_dir / "project.json"
    with open(project_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)
    print(f"  [OK] project.json configuré ({len(calibrated_scenes)} scènes Blueprints)")

    # 5. Fiche récapitulative prospect dans le dossier client
    readme_path = target_dir / "PROSPECT_BRIEF.md"
    readme_content = f"""# FICHE PROSPECT & STRATÉGIE OUTBOUND : {prospect['identity']['full_name']}

- **ID Prospect** : #{prospect['id']:02d}
- **Titre** : {prospect['identity']['title']}
- **Entreprise** : {prospect['identity']['company']} ({prospect['identity']['company_size']})
- **LinkedIn** : {prospect['contact_channels']['linkedin_url']}
- **Site Web** : {prospect['contact_channels']['website_url']}
- **Email Pro** : `{prospect['contact_channels']['work_email']}`

---

## 🎯 Diagnostic Contenu
- **Contenu écrit** : {prospect['content_diagnostic']['written_content_summary']}
- **Angle mort vidéo** : {prospect['content_diagnostic']['video_gap_reason']}

---

## 🚀 Cheval de Troie Visuel (Teaser 15s)
- **Sujet** : {prospect['visual_trojan_horse']['teaser_topic']}
- **Blueprints mobilisés** :
  1. `0.0s - 5.14s` : `{calibrated_scenes[0]['type']}` ({calibrated_scenes[0]['params'].get('title', '')})
  2. `5.14s - 11.06s` : `{calibrated_scenes[1]['type']}`
  3. `11.06s - 15.10s` : `{calibrated_scenes[2]['type']}`

---

## 💬 Message Privé LinkedIn (DM < 400 car.)
> **Note d'invitation ({prospect['linkedin_dm']['invite_note_char_count']}/200)** :  
> {prospect['linkedin_dm']['invite_note']}  
>  
> **Message 1 ({prospect['linkedin_dm']['first_message_char_count']} car.)** :  
> {prospect['linkedin_dm']['first_message']}

---

## ✉️ Cold Email J+1
**Objet :** `{prospect['cold_email_d1']['subject']}`

{prospect['cold_email_d1']['full_body']}

---

## 🎬 Commandes de Rendu Vidéo
```bash
# 1. Vérification de la timeline
python3 build_master_timeline.py -p studio_clients/{slug}

# 2. Rendu de la vidéo MP4
python3 render.py -p studio_clients/{slug} -o studio_clients/{slug}/output_demo_15s.mp4 --fast
```
"""
    readme_path.write_text(readme_content, encoding="utf-8")
    print("  [OK] PROSPECT_BRIEF.md généré avec argumentaire et messages prêts")

    # 6. Compilation automatique de timeline.js si demandé
    if compile_timeline:
        build_script = REPO_ROOT / "build_master_timeline.py"
        if build_script.exists():
            cmd = [sys.executable, str(build_script), "-p", str(target_dir)]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print("  [OK] timeline.js compilé avec succès (100% sans erreur) !")
            else:
                print(f"  [Warning] Échec de compilation timeline.js : {res.stderr}")

    return target_dir


def main():
    parser = argparse.ArgumentParser(description="Initialisateur de Démo Prospect AGENT404.")
    parser.add_argument("--id", type=str, help="ID du prospect (1 à 20 ou '01' à '20')")
    parser.add_argument("--list", action="store_true", help="Lister les 20 prospects qualifiés")
    parser.add_argument("--all", action="store_true", help="Initialiser tous les 20 prospects")
    parser.add_argument("--force", action="store_true", help="Écraser les dossiers existants")
    parser.add_argument("--no-compile", action="store_true", help="Ne pas compiler timeline.js")

    args = parser.parse_args()
    prospects = load_prospects()

    if args.list or (not args.id and not args.all):
        list_prospects(prospects)
        return

    if args.all:
        print(f"🚀 Initialisation complète des {len(prospects)} prospects B2B...")
        for p in prospects:
            print(f"\n📁 [{p['id']:02d}/20] {p['identity']['full_name']} ({p['identity']['company']})")
            init_prospect(p, force=args.force, compile_timeline=not args.no_compile)
        print("\n✅ Tous les dossiers prospects ont été créés dans studio_clients/ !")
        return

    # Recherche par ID
    try:
        target_id = int(args.id)
    except ValueError:
        print(f"[Erreur] ID invalide : {args.id}. Veuillez fournir un entier entre 1 et 20.")
        sys.exit(1)

    matched = [p for p in prospects if p["id"] == target_id]
    if not matched:
        print(f"[Erreur] Aucun prospect trouvé avec l'ID #{target_id:02d}.")
        sys.exit(1)

    prospect = matched[0]
    print(f"\n🚀 Initialisation de la démo pour #{prospect['id']:02d} - {prospect['identity']['full_name']} ({prospect['identity']['company']})")
    target_dir = init_prospect(prospect, force=args.force, compile_timeline=not args.no_compile)
    print(f"\n✨ Démo prête dans : {target_dir.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
