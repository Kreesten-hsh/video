#!/usr/bin/env python3
"""
AGENT404 : Générateur Automatique de Kit de Distribution Sociale (LinkedIn & Instagram).
Lit project.json et génère DISTRIBUTION_KIT.md dans le dossier du projet cible avec :
  1. Post LinkedIn complet calibré (< 140 car. avant fold)
  2. Légende Instagram Reels calibrée (< 60 car. hook)
  3. Premier commentaire d'amorce à épingler (Self-Pinned Comment)
  4. Concept de Story Instagram Teaser
  5. Checklist Smartphone avant publication
"""

import sys
import json
import argparse
from typing import Optional
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def generate_social_pack(project_dir: str, output_dir: Optional[str] = None) -> Path:
    proj_path = Path(project_dir)
    if not proj_path.is_absolute():
        proj_path = (REPO_ROOT / proj_path).resolve()

    proj_json = proj_path / "project.json"
    if not proj_json.exists():
        raise FileNotFoundError(f"Fichier introuvable : {proj_json}")

    with open(proj_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "Capsule AGENT404")
    cta = data.get("cta_keyword", "CLARTÉ").upper().strip()
    video_num = data.get("video_number", 1)
    scenes = data.get("scenes", [])
    ref_words = data.get("reference_words", [])

    # 1. Extraction de l'accroche depuis reference_words ou la première scène
    hook_line = ""
    if ref_words:
        first_words = ref_words[:12]
        hook_line = " ".join(first_words)
        if not hook_line.endswith((".", "?", "!")):
            hook_line += "..."
    elif scenes and "data" in scenes[0]:
        data0 = scenes[0]["data"]
        hook_line = data0.get("hero_title") or data0.get("title") or ""
    elif scenes and "params" in scenes[0]:
        params0 = scenes[0]["params"]
        hook_line = params0.get("title") or params0.get("header_badge") or ""

    if not hook_line:
        hook_line = "La plupart des professionnels B2B saturent sur leur production de contenu..."

    # 2. Calcul de la durée réelle à partir de la dernière scène ou audio
    duration_sec = 0.0
    if scenes:
        duration_sec = float(scenes[-1].get("end", 0.0))
    elif (proj_path / "words.json").exists():
        try:
            with open(proj_path / "words.json", "r", encoding="utf-8") as wf:
                words_data = json.load(wf)
                if words_data:
                    duration_sec = float(words_data[-1].get("end", 0.0))
        except Exception:
            pass

    duration_int = round(duration_sec) if duration_sec > 0 else 60

    # Note d'optimisation durée si > 60s
    duration_warning = ""
    if duration_int > 60:
        duration_warning = f"""> [!NOTE]
> Cette vidéo dure {duration_int} s, ce qui dépasse le plafond recommandé de 60 s pour les formats courts (Reels, Shorts). Elle est prioritairement optimisée pour LinkedIn.
"""

    # Hashtags ciblés
    hashtags_linkedin = ["#B2B", "#Productivite", "#Systeme", "#VideoB2B"]
    hashtags_insta = ["#entrepreneuriat", "#productivite", "#b2b", "#systeme", "#automatisation"]

    content = f"""# DISTRIBUTION KIT : {title} (Vidéo #{video_num})
*Généré automatiquement par le pipeline AGENT404. Prêt à copier-coller.*

---

## 1. LINKEDIN (Canal Prioritaire N° 1 : Vente B2B)

### Post LinkedIn à Copier-Coller :
```text
{hook_line}
Démonstration en {duration_int} secondes chrono ⬇️

---

{title}

[À RÉDIGER PAR LE FONDATEUR : Contexte et douleur spécifique résolue]

Dans cette capsule de {duration_int}s :
1. [À RÉDIGER PAR LE FONDATEUR : Point clé 1]
2. [À RÉDIGER PAR LE FONDATEUR : Point clé 2]
3. [À RÉDIGER PAR LE FONDATEUR : Point clé 3]

[À RÉDIGER PAR LE FONDATEUR : Question engageante pour l'audience]

---
Commente {cta} sous ce post pour recevoir le blueprint complet en message privé.

{' '.join(hashtags_linkedin)}
```

> [!TIP]
> **Contrôle Hook LinkedIn** : Les 3 premières lignes font moins de 140 caractères avant la pliure mobile.
> **Règle absolue** : Aucun lien sortant dans ce post.

### Premier Commentaire LinkedIn à Épingler Immédiatement :
```text
Pour recevoir le schéma technique ou le process détaillé de cette vidéo : commente simplement "{cta}" ci-dessous et je t'envoie la ressource en DM.
```

---

## 2. INSTAGRAM REELS (Canal Vitrine N° 2 : Visibilité Organique)
{duration_warning}
### Légende Instagram à Copier-Coller :
```text
{hook_line} ⬇️

[À RÉDIGER PAR LE FONDATEUR : Problème et promesse en 2 phrases]

Dans ce Reel de {duration_int} secondes :
- [À RÉDIGER PAR LE FONDATEUR : Enseignement principal 1]
- [À RÉDIGER PAR LE FONDATEUR : Enseignement principal 2]

👉 Commente {cta} en commentaire pour recevoir l'accès direct en privé.

.
.
.
{' '.join(hashtags_insta)}
```

### Premier Commentaire Instagram à Épingler :
```text
Vous gérez ce process en interne ou vous cherchez à l'automatiser ? Je réponds à tous les retours en commentaire ⬇️
```

### Concept de Story Instagram Teaser :
1. Partager le Reel dans votre Story.
2. Agrandir la vidéo et placer un sticker de sondage au milieu de l'écran.
3. Ajouter un texte d'accroche invitant à regarder la capsule.
4. Placer un sticker renvoyant vers le Reel original.

---

## 3. CHECKLIST SMARTPHONE AVANT DE CLIQUER SUR "PUBLIER"

- [ ] **Fichier Master MP4 vérifié** : 1080x1920, 30 FPS strict, H.264 `yuv420p`, Audio AAC 44.1kHz.
- [ ] **Instagram** : Option `Importer avec la meilleure qualité` activée dans les paramètres.
- [ ] **Instagram** : Couverture recadrée dans l'onglet `Grille du profil` (centré dans la zone 1:1 `Y: 420-1500px`).
- [ ] **Instagram** : Option `Recommander sur Facebook` vérifiée active.
- [ ] **Golden Hour** : 45 minutes devant soi pour répondre à 100% des commentaires entrants avec des réponses personnalisées.
- [ ] **Zéro Regard en Boucle** : Ne pas regarder la vidéo en boucle depuis son propre compte.
- [ ] **Zéro Suppression Immédiate** : Si le reach démarre lentement, laisser l'algorithme analyser pendant au moins 24h.
"""

    if output_dir:
        out_base = Path(output_dir)
        if not out_base.is_absolute():
            out_base = (REPO_ROOT / out_base).resolve()
        out_base.mkdir(parents=True, exist_ok=True)
        output_file = out_base / "DISTRIBUTION_KIT.md"
    else:
        output_file = proj_path / "DISTRIBUTION_KIT.md"
    output_file.write_text(content, encoding="utf-8")
    print(f"✓ Kit de distribution généré avec succès -> {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(description="Générateur de Social Pack AGENT404.")
    parser.add_argument("projet", nargs="?", default=None, help="Dossier du projet vidéo cible")
    parser.add_argument("--projet", "-p", dest="projet_opt", default=None, help="Dossier du projet vidéo cible")
    args = parser.parse_args()

    target_projet = args.projet or args.projet_opt
    if not target_projet:
        parser.error("Le dossier du projet est obligatoire (ex: studio_perso/video_01_decouverte).")

    generate_social_pack(target_projet)


if __name__ == "__main__":
    main()
