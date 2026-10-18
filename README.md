# AGENT404 : Moteur de Vidéo Programmatique

Projet détenu et opéré par Kreesten AGBOTON (Abomey-Calavi, Bénin).  
Objectif directeur : commercialiser les premières productions vidéo et encaisser 2 000 000 FCFA (environ 3 049 € au taux fixe 1 EUR = 655,957 FCFA) avant le 31 décembre 2026.

---

## 1. Présentation

AGENT404 est un pipeline de production vidéo vertical (1080x1920, 30 FPS, format 9:16) entièrement piloté par le code (Python, FFmpeg, Playwright/Chromium, Vanilla HTML5/CSS/JavaScript).  
Il transforme une note vocale en une vidéo rythmée : avatar sticker découpé, sous-titres dynamiques synchronisés au mot près, animations néo-brutalistes et sound design procédural.

---

## 2. Offres Commerciales Actives

Le modèle commercial repose exclusivement sur deux offres :
1. **Pilote Payant** : **250 €** (environ 163 989 FCFA) pour 3 vidéos verticales (délai cible : 48 h ouvrées).
2. **Forfait Studio Mensuel** : **500 € par mois** (environ 327 979 FCFA par mois) pour 8 vidéos verticales (délai cible : 72 h ouvrées).

Consulter [OFFRES.md](OFFRES.md) pour le détail des prestations et les conditions.

---

## 3. Installation et Prérequis

### Prérequis système
- Linux x86_64 (ou environnement compatible)
- Python 3.12+
- `ffmpeg` et `ffprobe` accessibles dans le PATH
- Navigateur Chromium (via Playwright ou Google Chrome système)

### Installation
```bash
# Installation des dépendances Python
pip install -r requirements.txt

# Installation du navigateur Chromium pour Playwright
playwright install chromium
```

---

## 4. Utilisation et Commandes

### Exécution des tests de non-régression (Golden Master)
```bash
python3 -m unittest -v
```
La suite valide l'intégrité temporelle des mots, la continuité des 35 scènes, la conformité de la vidéo master et la tolérance visuelle des captures de référence.

### Lancement du rendu vidéo
```bash
# Génère la vidéo finale
python3 render.py video1.mp4
```

Le script vérifie la présence des binaires, attend le chargement complet des polices locales et le décodage des images, puis valide automatiquement qu'aucun avatar n'est absent.

---

## 5. Documentation de Référence

- Grille tarifaire et conditions : [OFFRES.md](OFFRES.md)
- Architecture technique du moteur : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Modèle et planification financière : [docs/FINANCIAL_PLAN.md](docs/FINANCIAL_PLAN.md)
