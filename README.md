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
La suite valide l'intégrité temporelle des mots, la continuité des scènes, la conformité de la vidéo master et la tolérance visuelle des captures de référence.

### Orchestration complète de production vidéo
```bash
# Génère timeline, SFX, rendu vidéo et vérifications en une seule commande
python3 make_video.py studio_clients/<nom_client>/video_01

# Redirection vers un dossier de sortie isolé (sans modifier le dossier projet)
python3 make_video.py studio_perso/video_01 --sortie /tmp/sortie_isolee

# Forcer la réécriture sur un projet gelé ("gele": true) ou une vidéo existante
python3 make_video.py studio_perso/video_01 --forcer
```

Les projets marqués `"gele": true` dans `project.json` refusent toute écriture dans leur propre dossier sans `--forcer` ou `--sortie`. Le mode `"rendu_deterministe": true` (actif par défaut pour tout nouveau projet) neutralise les transitions CSS et dérive une graine stable (CRC32) pour les bruitages afin de garantir des rendus rigoureusement reproductibles bit-à-bit.

### Création d'un projet client (studio_clients)
Pour initialiser un nouveau projet client dans `studio_clients/` :
1. Créer le dossier du client : `mkdir -p studio_clients/<nom_client>/video_01`.
2. Copier le modèle de configuration :
   ```bash
   cp studio_perso/video_01/project.json studio_clients/<nom_client>/video_01/project.json
   ```
3. Adapter `project.json` :
   - `video_number` : numéro de la vidéo (ex: 1).
   - `title` : titre du projet.
   - `audio_path` : chemin du fichier audio source (WAV ou MP3).
   - `reference_words` : liste ordonnée des mots du texte de référence.
   - `scenes` : liste des scènes avec leurs types (`face`, `big`, `cards`, `window`, etc.) et décors (`grid`, `mint`, `diamonds`, `circles`, `alert`).
   - `scene_end_words` : liste des mots terminaux marquant la coupure de chaque scène (même longueur que `scenes`).
   - `phonetic_map` : dictionnaire des équivalences phonétiques de transcription Whisper éventuelles.
4. Lancer la production :
   ```bash
   python3 make_video.py studio_clients/<nom_client>/video_01
   ```
La vidéo finale sera générée directement dans `studio_clients/<nom_client>/video_01/video1.mp4`.

---

## 5. Documentation de Référence

- Grille tarifaire et conditions : [OFFRES.md](OFFRES.md)
- Architecture technique du moteur : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Modèle et planification financière : [docs/FINANCIAL_PLAN.md](docs/FINANCIAL_PLAN.md)
