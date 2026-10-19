# AGENT404 : Clarté Visuelle B2B Programmatique

Projet détenu et opéré par Kreesten AGBOTON (Abomey-Calavi, Bénin).  
Objectif directeur : commercialiser les premières productions vidéo et encaisser 2 000 000 FCFA (environ 3 049 € au taux fixe 1 EUR = 655,957 FCFA) avant le 31 décembre 2026.

---

## 1. Positionnement Stratégique & Ciblage Chirurgical

> **Règle d'or de positionnement** : Arrêter de vendre « du code Python ». Vendre de la **clarté visuelle B2B qui remplace la caméra et fait signer des clients**.

AGENT404 résout la douleur exacte des entreprises technologiques : leurs fonctionnalités sont puissantes mais complexes, leurs prospects ne lisent pas la documentation et abandonnent les Looms de 10 minutes après 30 secondes. AGENT404 les remplace par des capsules vidéo chirurgicales de 45 à 60 secondes au format 9:16, rythmées et sans face-caméra amateur.

### Répartition des efforts de prospection :
1. **Cible n° 1 (Priorité absolue — 70 % des efforts)** : **Fondateurs de SaaS B2B & Outils Tech bootstrappés rentables** (ex: Typebot, Piloterr, Breakcold, Pharow, Tally).
   - *Painkiller* : Fonctionnalités techniques puissantes, Looms ignorés. Besoin de démos produit de 45s ultra-claires pour convertir sur leur site et sur LinkedIn.
   - *Offre naturelle* : Pilote 250 € (3 vidéos) → Forfait Studio 500 €/mois pour chaque release/feature.
2. **Cible n° 2 (30 % des efforts)** : **Agences B2B expertes & Organismes Tech** (ex: Digidop, Noqode, Contournement, Ottho).
   - *Painkiller* : Beaucoup de publications écrites de valeur mais pas le temps de tourner en vidéo face caméra chaque semaine.
   - *Offre naturelle* : Forfait Studio 500 €/mois (8 vidéos) à partir de leurs posts écrits ou notes vocales.
3. **À ÉCARTER (Exclusion stricte)** : Freelances débutants (pas de budget 250 €), créateurs IA sans produit, grosses licornes (Pennylane, Gorgias, Strapi qui disposent d'équipes internes).

---

## 2. Les 5 Concepts Directeurs du Projet

L'ensemble de l'ingénierie logicielle, des scripts de vente et des vidéos produites est régi par ces 5 concepts obligatoires :

1. **Concept 1 : Définir le problème précis plutôt qu'une idée vague**  
   *« Tu ne décris plus une idée. Tu définis le problème à résoudre. »*  
   - Nous ciblons le problème chirurgical du prospect (décideurs qui ferment les vidéos trop longues) plutôt qu'un concept abstrait d'animation.
2. **Concept 2 : Décrire les gestes et le fonctionnement étape par étape**  
   *« Tu passes d'un concept à un fonctionnement que tu peux vérifier, étape par étape. »*  
   - Pipeline transparent et sans effet boîte noire : ingestion audio → alignement forcé Whisper mot-à-mot → sound design procédural → rendu frame-par-frame Playwright → encodage FFmpeg.
3. **Concept 3 : Définir explicitement ce qu'on refuse (Les non-objectifs)**  
   *« Dis aussi ce que tu ne veux pas. La clarté, c'est aussi décider ce qui peut attendre. »*  
   - Zéro jargon technique dans les vidéos commerciales. Zéro prix affiché dans les vidéos publiques. Zéro HUD à l'écran. Refus des cibles non rentables ou hors-sujet.
4. **Concept 4 : Remplacer « ça ne marche pas » par un constat précis mesuré**  
   *« Identifie l'écart entre le résultat attendu et le résultat obtenu. »*  
   - Diagnostics basés exclusivement sur des métriques : PSNR infini, framemd5, durée millimétrique ffprobe, analyse de contraste et de surface avatar OpenCV.
5. **Concept 5 : Des décisions claires avec critères d'acceptation testables**  
   *« Je saurai que ça fonctionne si... Un brief précis ne garantit pas un code fiable : il faut encore le tester. »*  
   - 100 % des tests unitaires et de spécification (`pytest tests/`) doivent être au vert avant validation d'une vidéo ou mise en production.

---

## 3. Offres Commerciales Actives

Le modèle commercial repose exclusivement sur deux offres :
1. **Pilote Payant** : **250 €** (environ 163 989 FCFA) pour 3 vidéos verticales (délai cible : 48 h ouvrées).
2. **Forfait Studio Mensuel** : **500 € par mois** (environ 327 979 FCFA par mois) pour 8 vidéos verticales (délai cible : 72 h ouvrées).

Consulter [OFFRES.md](OFFRES.md) pour le détail des prestations et les conditions.

---

## 4. Pipeline Technique & Architecture

AGENT404 est un pipeline de production vidéo vertical (1080x1920, 30 FPS, format 9:16) entièrement piloté par le code (Python, FFmpeg, Playwright/Chromium, Vanilla HTML5/CSS/JavaScript).  
Il transforme une note vocale ou un texte en une vidéo rythmée : avatar sticker découpé, sous-titres dynamiques synchronisés au mot près, animations néo-brutalistes et sound design procédural.

---

## 5. Installation et Prérequis

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

## 6. Utilisation et Commandes

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

## 7. Documentation de Référence

- Grille tarifaire et conditions : [OFFRES.md](OFFRES.md)
- Architecture technique du moteur : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Modèle et planification financière : [docs/FINANCIAL_PLAN.md](docs/FINANCIAL_PLAN.md)
- Standard de qualité et non-régression : [.agents/rules/video_quality_standard.md](.agents/rules/video_quality_standard.md)
- Constitution et principes directeurs : [.specify/memory/constitution.md](.specify/memory/constitution.md)
