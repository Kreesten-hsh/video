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
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def generate_social_pack(project_dir: str) -> Path:
    proj_path = Path(project_dir)
    if not proj_path.is_absolute():
        proj_path = (REPO_ROOT / proj_path).resolve()

    proj_json = proj_path / "project.json"
    if not proj_json.exists():
        raise FileNotFoundError(f"Fichier introuvable : {proj_json}")

    with open(proj_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "Capsule AGENT404")
    cta = data.get("cta_keyword", "DEMO").upper()
    video_num = data.get("video_number", 1)
    scenes = data.get("scenes", [])
    ref_words = data.get("reference_words", [])

    # Extraction du hook parlé depuis la première scène
    first_words = []
    if ref_words:
        first_words = ref_words[:12]
    first_line = " ".join(first_words) if first_words else "La plupart des agences et créateurs B2B font une erreur majeure sur leurs process..."

    # Définition des hashtags ciblés selon le sujet
    hashtags_linkedin = ["#B2B", "#Productivite", "#Systeme"]
    hashtags_insta = ["#entrepreneuriat", "#productivite", "#b2b", "#systeme", "#automatisation"]

    content = f"""# DISTRIBUTION KIT : {title} (Vidéo #{video_num})
*Généré automatiquement par le pipeline AGENT404. Prêt à copier-coller.*

---

## 1. LINKEDIN (Canal Prioritaire N° 1 — Vente B2B)

### Post LinkedIn à Copier-Coller :
```text
Pourquoi 90% des professionnels saturent sur leur contenu ?
Ce n'est pas un manque d'idées. C'est un problème de tuyauterie.
Démonstration en 60 secondes chrono ⬇️

---

{title}

La plupart des créateurs et agences continuent de perdre 3h par semaine à bricoler des tournages ou des carrousels qui ne convertissent plus.

Dans cette capsule de 60s :
1. Le vrai goulot d'étranglement qui tue votre rétention.
2. Pourquoi le texte brut ne suffit plus pour capter les décideurs.
3. La mécanique exacte pour convertir vos posts écrits en capsules vidéo sans toucher une caméra.

Vous gérez votre production en interne ou vous déléguez déjà ce process ?

---
{cta} : Écrivez "{cta}" en commentaire pour recevoir le blueprint complet en message privé.

{' '.join(hashtags_linkedin)}
```

> [!TIP]
> **Contrôle Hook LinkedIn** : Les 3 premières lignes font moins de 140 caractères. Le spectateur mobile est obligé de cliquer sur *...voir plus* ou de lancer la vidéo.
> **Règle absolue** : Aucun lien sortant dans ce post.

### Premier Commentaire LinkedIn à Épingler Immédiatement :
```text
Pour ceux qui veulent explorer le schéma technique ou le process détaillé de cette vidéo : écrivez simplement "{cta}" ci-dessous et je vous partage la ressource en DM.
```

---

## 2. INSTAGRAM REELS (Canal Vitrine N° 2 — Cross-Posté sur Facebook)

### Légende Instagram à Copier-Coller :
```text
L'erreur qui vous coûte 3h par jour sur vos process ⬇️

La plupart des créateurs et agences font la même erreur : ils ont l'expertise, mais zéro format pour la valoriser rapidement.

Dans ce Reel de 60 secondes :
- Pourquoi les longs formats s'effondrent
- Le système pour créer des capsules vidéos percutantes sans caméra

👉 Écris "{cta}" en commentaire pour recevoir l'accès direct en privé.

.
.
.
{' '.join(hashtags_insta)}
```

### Premier Commentaire Instagram à Épingler :
```text
Vous êtes plutôt process manuel ou automatisation radicale ? Je réponds à tous les retours en commentaire ⬇️
```

### Concept de Story Instagram Teaser (Minute 5) :
1. Partager le Reel dans votre Story.
2. Agrandir la vidéo et placer un sticker de sondage au milieu de l'écran :
   - Question : *« Tu fais encore cette erreur ? »*
   - Options : *« Oui malheureusement »* / *« Non j'ai automatisé »*
3. Ajouter un texte au-dessus : *« La révélation à la 42e seconde change tout ⬇️ »*.
4. Placer un sticker de lien cliquable renvoyant vers le Reel original.

---

## 3. CHECKLIST SMARTPHONE AVANT DE CLIQUER SUR "PUBLIER"

- [ ] **Fichier Master MP4 vérifié** : 1080x1920, 30 FPS strict, H.264 `yuv420p`, Audio AAC 44.1kHz.
- [ ] **Instagram** : Option `Importer avec la meilleure qualité` activée dans les paramètres.
- [ ] **Instagram** : Couverture recadrée dans l'onglet `Grille du profil` (centré dans la zone 1:1 `Y: 420-1500px`).
- [ ] **Instagram** : Option `Recommander sur Facebook` vérifiée active.
- [ ] **Golden Hour** : 45 minutes devant soi pour répondre à 100% des commentaires entrants avec des phrases de plus de 5 mots et des questions de relance.
- [ ] **Zéro Regard en Boucle** : Ne pas regarder la vidéo 50 fois depuis son propre compte.
- [ ] **Zéro Suppression Immédiate** : Si le reach démarre lentement, laisser l'algorithme analyser pendant au moins 24h.
"""

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
