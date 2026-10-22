# PLAYBOOK OFFICIEL DE DISTRIBUTION & ALGORITHMES 9:16 (AGENT404)
### Guide d'Ingénierie Sociale, Encodage Master & Maximisation du Reach

Date de référence : Octobre 2026  
Studio : AGENT404 // Cyber-Mint  
Format étalon : 1080 × 1920 pixels @ 30.00 FPS (9:16 Vertical)  
Priorité Commerciale Stratégique : **LinkedIn (80%)** & **Instagram Reels (20% avec Recommander sur Facebook activé)**.

> **Méthodologie de conformité** : Chaque paramètre ci-dessous distingue formellement la **[DOCUMENTATION OFFICIELLE]** (directives des équipes d'ingénierie et brevets publiés des plateformes) du **[REVERSE-ENGINEERING]** (mesures empiriques documentées par les créateurs et agences du top 1%).

---

## SOMMAIRE
1. [PARTIE 1 : Configuration Permanente des Applications (One-Time Setup)](#partie-1--configuration-permanente-des-applications-one-time-setup)
2. [PARTIE 2 : Spécifications Techniques d'Export AGENT404](#partie-2--spécifications-techniques-dexport-agent404)
3. [PARTIE 3 : Protocole de Publication Plateforme par Plateforme](#partie-3--protocole-de-publication-plateforme-par-plateforme)
4. [PARTIE 4 : La Golden Hour (Les 60 Minutes Post-Publication)](#partie-4--la-golden-hour-les-60-minutes-post-publication)
5. [Automatisation : Générateur de Social Pack (generate_social_pack.py)](#automatisation--générateur-de-social-pack)

---

## PARTIE 1 : Configuration Permanente des Applications (One-Time Setup)

À configurer **une seule fois** sur le smartphone de publication pour neutraliser la compression côté client et débloquer les fonctionnalités d'indexation.

### 1. Instagram
1. **Verrouillage de la qualité d'importation maximale** :
   - *Chemin* : `Profil` > Menu `☰` > `Paramètres et confidentialité` > `Utilisation des données et qualité des fichiers multimédias`
   - *Réglages* :
     - `Économiseur de données` > **DÉSACTIVER**.
     - `Importer avec la meilleure qualité` (Upload at highest quality) > **ACTIVER**.
   - *Pourquoi [DOC OFFICIELLE Meta]* : Force l'ingestion du fichier master à plein débit binaire sans compression bilinéaire anticipée.
2. **Type de compte** :
   - *Chemin* : `Paramètres et confidentialité` > `Type de compte et outils` > `Passer à un compte professionnel` > **Créateur** (*Creator*).
   - *Pourquoi [DOC OFFICIELLE Meta]* : Donne accès à 100% de la bibliothèque musicale grand public (sons tendances) tout en conservant l'accès aux Insights et aux webhooks messagerie / DM.
3. **Arrosage passif Facebook** :
   - *Chemin* : `Paramètres et confidentialité` > `Partage et remix` > `Recommander les Reels sur Facebook` > **ACTIVER**.

### 2. LinkedIn
1. **Lecture automatique & qualité** :
   - *Chemin* : Photo de profil (haut gauche) > `Préférences` > `Préférences du compte` > `Synchronisation et données` > `Lecture automatique des vidéos` > **Wi-Fi et données cellulaires**.
2. **Mode Créateur unifié** :
   - Configurer le profil avec le bouton d'action principal sur **Suivre** (Follow) plutôt que "Se connecter".
   - *Pourquoi [DOC OFFICIELLE LinkedIn Engineering]* : Dans le lecteur vidéo vertical mobile, LinkedIn incruste le bouton d'abonnement en 1 clic. En mode standard, le spectateur doit effectuer 2 clics, ce qui divise le taux de conversion par 2.5.

### 3. TikTok (Canal Secondaire)
1. **Économiseur de données global** :
   - *Chemin* : `Profil` > Menu `☰` > `Paramètres et confidentialité` > `Économiseur de données` > **DÉSACTIVER**.
2. **Upload HD à chaque publication (Vigilance)** :
   - *Chemin* : Écran final avant publication > `Plus d'options` > `Autoriser les téléversements de haute qualité` > **ACTIVER (Basculeur vert)**.

---

## PARTIE 2 : Spécifications Techniques d'Export AGENT404

Pour empêcher les serveurs CDN de ré-encoder votre master vidéo avec une compression médiocre, le fichier exporté par `render.py` correspond rigoureusement aux standards d'ingestion native des infrastructures CDN.

### 1. La Matrice d'Export Master

| Paramètre | Spécification AGENT404 | Source & Règle d'Ingénierie |
| :--- | :--- | :--- |
| **Résolution** | **1080 × 1920 pixels** (9:16 strict) | [DOC OFFICIELLE] Résolution standard universelle. L'export 4K est banni car downscalé agressivement par les serveurs mobiles. |
| **Framerate** | **30.00 FPS strict (CFR)** | [DOC OFFICIELLE] Constant Frame Rate obligatoire. Le VFR provoque un décalage audio/vidéo irréversible sur LinkedIn et Meta. |
| **Codec Vidéo** | **H.264 (libx264)** | [DOC OFFICIELLE] Profil High/Main, décodeur hardware garanti sur 100% des terminaux sans ré-encodage serveur. |
| **Container** | **MP4** | Standard ISO Base Media File Format universel. |
| **Sous-échantillonnage chromatique** | **yuv420p (4:2:0)** | [DOC OFFICIELLE] Obligatoire. yuv444p ou 10 bits déclenche un écran noir ou corrompt la colorimétrie sur mobile. |
| **Bitrate Vidéo** | **12 à 15 Mbps** (`-crf 18 -maxrate 15M -bufsize 30M`) | [REVERSE-ENGINEERING] Le sweet-spot exact : au-delà de 20 Mbps, le compresseur Meta/ByteDance détruit les détails fins. En dessous de 8 Mbps, les aplats néo-brutalistes pixellisent. |
| **Flag de streaming** | **`-movflags +faststart`** | [DOC OFFICIELLE] Place l'atome `moov` au début du fichier MP4. Permet aux plateformes de commencer la lecture et le parsing dès les premiers octets reçus. |
| **Codec Audio** | **AAC-LC (`aac`)** | Profil Low Complexity standard broadcast. |
| **Fréquence d'échantillonnage** | **44.1 kHz (`-ar 44100`)** | Fréquence de référence de la voix off studio ElevenLabs. |
| **Bitrate Audio** | **192 kbps (`-b:a 192k`)** | Clarté maximale pour les voix sans artefacts de phase. |

#### Commande FFmpeg Étalon intégrée dans `render.py` :
```bash
ffmpeg -y -f image2pipe -vcodec mjpeg -r 30 -i pipe:0 -i audio_path \
  -c:v libx264 -pix_fmt yuv420p -preset slow -crf 18 \
  -maxrate 15M -bufsize 30M \
  -c:a aac -b:a 192k -ar 44100 \
  -movflags +faststart -shortest output_master.mp4
```

---

### 2. Carte Universelle des Safe-Zones 9:16 (Canvas 1080 × 1920 PX)

```
 0 px  +-------------------------------------------------------------+
       |   ZONE DANGER HAUTE (220 px) : UI App, Search, Onglets      |
 220px +-------------------------------------------------------------+
       |   SOUS-TITRES ANCRÉS : Top 220px à 380px (Y: 220 à 380 px)  |
 380px +-------------------------------------------------------------+
       |                                              |              |
       |          UNIVERSAL SAFE CONTENT BOX          | ZONE DANGER  |
       |                                              | DROITE       |
       |          Largeur : 900 px (X: 50 à 950 px)   | (130 px)     |
       |          Hauteur : 1320 px (Y: 220 à 1540 px)|              |
       |                                              | Boutons Like,|
       |   * Zone Illustrations / Cartes :            | Comment,     |
       |     Y = 390 px à 1200 px                     | Bookmark,    |
       |   * Zone Avatar & Badges :                   | Share,       |
       |     Y = 1100 px à 1500 px                    | Audio disc   |
       |                                              |              |
       |                                              | (X: 950      |
       |                                              |  à 1080 px)  |
       |                                              |              |
1540px +-------------------------------------------------------------+
       |   ZONE DANGER BASSE (380 px) : Nom, Légende, Musique, Barre |
1920px +-------------------------------------------------------------+
       0 px                                           950 px 1080 px
```

#### Coordonnées Critiques du Studio AGENT404
- **Marge Haute de Sécurité (`--safe-top`)** : **`220 px`**.
  - La boîte de sous-titres (`#subtitles-zone`) est ancrée à `top: var(--safe-top)` pour éviter d'être masquée par les barres de recherche TikTok et les en-têtes d'applications mobiles.
- **Marge Basse de Sécurité (`--safe-bottom`)** : **`380 px`**.
  - L'avatar ancré au bas ne doit pas dépasser au-dessus de `bottom: 120px` pour éviter que ses mains ou badges ne soient recouverts par la description et le ticker audio.
- **Marge Droite de Sécurité (`--safe-right`)** : **`130 px`** (du pixel 950 au pixel 1080).
  - Aucun texte, badge ou KPI ne doit dépasser `X = 940 px`.
- **Marge Gauche de Sécurité (`--safe-left`)** : **`50 px`** (absorbe les arrondis d'écrans borderless).

#### Diagnostic Visuel en Direct
Ajouter `?safe_zones=1` à l'URL locale (ex: `index.html?timeline=studio_perso/video_02/timeline.js&safe_zones=1`) pour afficher en direct les calques de sécurité et les repères de recadrage Instagram sur le canvas.

---

### 3. Précaution Fondamentale : Le "Crop Grille" Instagram

Sur le profil Instagram, un Reel 9:16 apparaît sous deux formats additionnels :
1. **Grille du profil principale** : Crop carré **1:1** (`1080 × 1080 px`).
   - S'étend exactement de **`Y = 420 px` à `Y = 1500 px`** (calcul : `(1920 - 1080) / 2 = 420`).
   - **Règle absolue** : Si le titre d'accroche de la couverture ou la tête de l'avatar est au-dessus de `Y = 420 px` ou en dessous de `Y = 1500 px`, il sera **décapité sur le profil**.
2. **Flux d'actualité classique (Feed)** : Crop vertical **4:5** (`1080 × 1350 px`).
   - S'étend de **`Y = 285 px` à `Y = 1635 px`**.

#### Protocole Smartphone avant de cliquer sur "Partager" sur Instagram
1. Sur l'écran final de publication du Reel, appuyer sur le cadre vidéo `Couverture`.
2. Cliquer sur l'onglet **Grille du profil** en haut à droite.
3. Glisser l'image vers le haut ou le bas pour caler parfaitement le titre d'accroche et l'avatar au centre du carré 1:1.
4. Valider en appuyant sur `Terminé`.

---

## PARTIE 3 : Protocole de Publication Plateforme par Plateforme

---

### 1. LinkedIn (PRIORITÉ N° 1 - 80% du Focus Commercial)

| Paramètre | Règle Opérationnelle | Source & Rationale |
| :--- | :--- | :--- |
| **Hook Texte (Post)** | **140 caractères (Mobile) à 210 caractères (Desktop)** avant la coupure `...voir plus`. | [DOC OFFICIELLE LinkedIn Engineering] Le clic sur "voir plus" est un signal de Dwell Time positif majeur. Structure : Ligne 1 = Problème percutant, Ligne 2 = Contre-intuition, Ligne 3 = Promesse de la vidéo 60s. |
| **Hashtags & SEO** | **0 à 3 hashtags maximum**, placés en fin de post. | [DOC OFFICIELLE LinkedIn 2024-2025] LinkedIn a déprécié les hashtags au profit de l'indexation sémantique complète du texte et des compétences du profil de l'auteur. |
| **Choix Audio** | **100% Son Studio ElevenLabs Pur** (Zéro musique externe). | [REVERSE-ENGINEERING] 80% des vidéos sur LinkedIn sont regardées **SANS LE SON**. Les sous-titres mot-à-mot AGENT404 font 100% du travail de rétention. |
| **Pénalité Liens** | **ZÉRO LIEN DANS LE POST PRINCIPAL.** | [DOC OFFICIELLE LinkedIn Engineering] Les liens sortants divisent la portée initiale par 2. Renvoyer vers le premier commentaire ou les DM. |
| **Appel à l'Action (CTA)** | **Demander un mot-clé B2B en commentaire** (ex: *"Commente 'WORKFLOW' pour recevoir le schéma"*). | Les commentaires qualitatifs (> 5 mots) propulsent la vidéo dans le fil de niveau 1 et 2 du réseau de vos commentateurs. |

---

### 2. Instagram Reels (PRIORITÉ N° 2 - 20% du Focus Vitrine)

| Paramètre | Règle Opérationnelle | Source & Rationale |
| :--- | :--- | :--- |
| **Hook Texte (Légende)** | **55 à 60 caractères** visibles dans l'onglet Reels / **~125 caractères** dans le feed. | [DOC OFFICIELLE Meta] Seule la première ligne est visible sans tap. L'accroche doit poser une question directe ou une promesse tranchée. |
| **Hashtags & SEO** | **3 à 5 hashtags ciblés** dans la légende. | [DOC OFFICIELLE - Déclaration Adam Mosseri] *"Les hashtags n'augmentent pas la distribution, ils servent uniquement à catégoriser."* 30 tags déclenchent des filtres anti-spam. |
| **Choix Audio** | **Audio Trending en sourdine à 1-2%** : garder la voix studio à 100% et ajouter un son viral via l'éditeur Instagram à volume minime. | [REVERSE-ENGINEERING] Permet d'indexer la vidéo sur la page dédiée du son tendance sans parasiter la voix de l'avatar. |
| **Appel à l'Action (CTA)** | **Demander un mot-clé en commentaire pour envoi direct en DM** (ex: *"Écris 'SYSTEME' en commentaire"*). | [DOC OFFICIELLE Adam Mosseri] Le signal n°1 de distribution sur Instagram est le ratio **Sends per reach (Partages par message privé)**. L'envoi du lien en DM active la messagerie privée. |

---

### 3. Facebook Reels (Canal Passif via Cross-Postage Instagram)
- **Protocole** : **Zéro gestion manuelle**. Cocher l'option `Recommander sur Facebook` dans Instagram. Meta injecte automatiquement le Reel dans le flux Facebook Reels sans aucune charge de travail supplémentaire.

---

### 4. TikTok, X & Threads (Mis en Pause Temporaire)
- **TikTok** : Mis en pause le temps d'atteindre l'objectif financier de 2 000 000 FCFA (audience B2C volatile, conversion B2B proche de 0).
- **Threads** : Mis en pause (réseau textuel d'opinion, faible retour sur investissement vidéo).
- **X (Twitter)** : Mis en pause (pénalité sévère sur les comptes sans abonnement Premium payant).

---

## PARTIE 4 : La Golden Hour (Les 60 Minutes Post-Publication)

Les 60 premières minutes déterminent si l'algorithme classe votre vidéo dans le palier d'abandon (< 250 vues) ou dans la distribution exponentielle.

```
[PUBLICATION]
     │
     ├─► Minute 01 : Épinglage immédiat de son propre commentaire (Self-Pinned Comment)
     ├─► Minute 05 : Partage chirurgical en Story Instagram (Teaser masqué)
     ├─► Minutes 05-45 : Règle des "3X" (Répondre à 100% des commentaires en > 5 mots + Question)
     └─► Minute 60 : Audit du momentum et archivage dans le registre
```

### 1. Les 3 Actions Obligatoires Immédiates

#### Action 1 : L'épinglage du commentaire amorce (Minute 1)
- Dès la vidéo en ligne, poster le premier commentaire et l'épingler en haut du fil.
- Poser une question binaire ou polarisante qui réduit la friction cognitive de réponse :
  - *« Vous êtes plutôt automatisation radicale ou process manuel à 100% ? Je lis tous les avis ci-dessous. »*
  - *« Pour ceux qui veulent le schéma de la vidéo en haute résolution : commentez 'SCHEMA' ci-dessous. »*
- *Impact [DOC OFFICIELLE]* : Les spectateurs qui ouvrent les commentaires maintiennent la vidéo en lecture continue en arrière-plan, faisant exploser le Watch Time.

#### Action 2 : La Règle des "3X" sur les Premiers Commentaires (Minutes 5 à 45)
- Pendant les 45 premières minutes, répondre à **100% des commentaires reçus**.
- Règle d'or :
  1. Interdiction de répondre par un simple émoji ou un "Merci !".
  2. Rédiger une phrase de plus de 5 mots comprenant une question de relance.
  3. *Exemple* : *« Merci Thomas ! Tu as déjà essayé d'appliquer cette structure sur tes propres vidéos ou tu tournes encore à la caméra ? »*
- *Impact [DOC OFFICIELLE]* : Double le compteur de commentaires et génère une notification push qui renvoie le spectateur sur le post (seconde visite = signal de pertinence fort).

#### Action 3 : Le Partage en Story Instagram "Anti-Cannibalisation" (Minute 5)
- **L'erreur fatale** : Partager le Reel complet en Story sans modification. Les abonnés regardent tout dans la story et ne cliquent jamais sur le post original.
- **La technique AGENT404** : Partager le Reel en Story, masquer le bas de la vidéo avec un sticker sondage (*« Tu fais cette erreur ? »*) et ajouter un sticker de lien dirigeant vers le Reel original.

---

### 2. Ce qu'il est STRICTEMENT INTERDIT de Faire (Les 5 "Killers" de Distribution)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      LES 5 INTERDICTIONS ABSOLUES                             ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ 1. REGARDER SA PROPRE VIDÉO 50 FOIS EN BOUCLE DEPUIS LE MÊME COMPTE / IP      ║
║ 2. SUPPRIMER ET RE-PUBLIER IMMÉDIATEMENT UNE VIDÉO QUI DÉMARRE MAL            ║
║ 3. ÉDITER LA LÉGENDE OU LE TEXTE DANS LES 20 PREMIÈRES MINUTES                ║
║ 4. LAISSER UN WATERMARK OU LOGO D'APPLICATION TIERS SUR LA VIDÉO              ║
║ 5. COLLER UN LIEN SORTANT DIRECT DANS LE CORPS DU POST (LINKEDIN & X)         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

1. **Regarder sa propre vidéo 50 fois en boucle** : Les systèmes anti-fraude tracent l'ID de session et l'IP du compte créateur. L'activité est flaggée comme *Inauthentic Engagement Manipulation*, gelant le compteur de vues.
2. **Supprimer et re-publier immédiatement (< 24-48h)** : Les plateformes comparent l'empreinte binaire (hash perceptuel des frames). Un doublon immédiat est classé comme spam et plafonné à 0-10 vues. Attendre au minimum 24h, modifier légèrement la durée (+0.2s) et le hook visuel avant ré-export.
3. **Éditer la description dans les 20 premières minutes** : Réinitialise le pipeline NLP et suspend le test-batch d'impressions en cours.
4. **Watermarks tiers (CapCut, TikTok)** : Entraîne une exclusion automatique des recommandations pour non-abonnés (pénalité algorithmique documentée par Meta et YouTube).
5. **Liens externes dans le post principal LinkedIn** : Renvoyer vers le lien en premier commentaire ou en message privé (DM).

---

## AUTOMATISATION : Générateur de Social Pack

Pour ne plus jamais perdre de temps à rédiger des légendes et chercher des hashtags, exécutez simplement :

```bash
python3 generate_social_pack.py --projet studio_perso/video_02
```

Ce script lit `project.json` et génère automatiquement le fichier `DISTRIBUTION_KIT.md` directement dans le dossier du projet, contenant :
- Le post LinkedIn calibré à moins de 140 caractères avant troncature
- La légende Instagram Reels avec le hook de 55 caractères
- Les 3 à 5 hashtags sémantiques ciblés
- Le premier commentaire à épingler
- Le concept de story teaser
- La checklist smartphone pré-publication.
