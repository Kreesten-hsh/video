# PLAYBOOK OFFICIEL DE PRODUCTION VIDÉO AGENT404
## Guide d'Ingénierie & Protocole Standardisé en 7 Phases (Loi d'Effet Cliquet $N+1 > N$)

Ce document constitue la **référence absolue** pour la création de toute vidéo au sein du studio (capsules personnelles dans `studio_perso/` ou capsules sur-mesure pour clients dans `studio_clients/`).
Tout agent ou développeur intervenant sur la chaîne de production **doit exécuter les 7 phases séquentiellement sans en sauter aucune**.

---

### SOMMAIRE
1. [Principes Directeurs & Effet Cliquet](#principes-directeurs--effet-cliquet)
2. [PHASE 1 : Lecture du Script Tagué & Audit Éditorial](#phase-1--lecture-du-script-tagu%C3%A9--audit-%C3%A9ditorial)
3. [PHASE 2 : Récupération de l'Audio ElevenLabs & Alignement Millimétré](#phase-2--r%C3%A9cup%C3%A9ration-de-laudio-elevenlabs--alignement-millim%C3%A9tr%C3%A9)
4. [PHASE 3 : Direction d'Acteur & Poses d'Avatars (Arbitrage Strict)](#phase-3--direction-dacteur--poses-davatars-arbitrage-strict)
5. [PHASE 4 : Conception du Storyboard & Illustrations 100% Inédites](#phase-4--conception-du-storyboard--illustrations-100-in%C3%A9dites)
6. [PHASE 5 : Scaffolding CLI & Implémentation CSS/JS Propre](#phase-5--scaffolding-cli--impl%C3%A9mentation-cssjs-propre)
7. [PHASE 6 : Validation Pre-Flight Bloquante (< 3s) AVANT Rendu](#phase-6--validation-pre-flight-bloquante--3s-avant-rendu)
8. [PHASE 7 : Rendu Final 30 FPS, Inspection Visuelle & Clôture Registre](#phase-7--rendu-final-30-fps-inspection-visuelle--cl%C3%B4ture-registre)
9. [PHASE 8 : Distribution Ciblée (LinkedIn & Instagram) & Golden Hour](#phase-8--distribution-cibl%C3%A9e-linkedin--instagram--golden-hour)
10. [Catalogue Officiel des 8 Blueprints Universels & Multi-Tenant Studio](#catalogue-officiel-des-8-blueprints-universels--multi-tenant-studio)
11. [Matrice d'Audit Rapide (Checklist de Clôture)](#matrice-daudit-rapide-checklist-de-cl%C3%B4ture)

---

### Principes Directeurs & Effet Cliquet

1. **Loi du Cliquet ($N+1 > N$)** : Une vidéo nouvelle ne doit jamais régresser par rapport aux standards acquis sur les vidéos précédentes. Tout bug corrigé antérieurement (tailles de polices, retours orphelins, cartes inertes, dérives d'avatars) est définitivement interdit et bloqué à la source.
2. **Zero-Fluff / High-Density** : Format 1080x1920 (9:16 vertical), 30 FPS, centré sur la rétention mobile. Chaque frame doit apporter une information visuelle utile.
3. **Zéro Hardcoding & Thème Sémantique** : 100% des couleurs hors `:root` sont interdites. Utilisation stricte des variables CSS sémantiques.
4. **Bannissements Perpétuels** :
   - `#FF2A5F` (rose banni) : interdit sur 100% du projet.
   - `#agent-hud` : bandeau supérieur HUD définitivement banni.
   - Jargon technique d'ingénierie dans les scripts (Python, FFmpeg, Whisper, JavaScript, etc.).
   - Prix chiffrés et symboles monétaires dans les scripts et sous-titres publics (150 €, 200 €, 750 €, etc.).

---

### PHASE 1 : Ingestion Agnostique, Extraction de Joyau & Audit Éditorial

#### 1. Objectifs
Opérer en **Entrée Agnostique (Input Agnostic)** : recevoir n'importe quel matériau brut fourni par le client (note vocale WhatsApp de 2 min, post LinkedIn écrit, documentation technique, schéma Make/n8n, cas client, ou Loom trop long), en extraire la pépite / le joyau intellectuel, et le structurer en un script d'acting captivant au format étalon de ~60 secondes (amplitude 45s à 90s) avec flux de sous-titres épuré.

#### 2. Procédure Technique
1. **Ingestion & Extraction du narratif** : Identifier l'argument massue ou la douleur résolue dans le matériau brut et rédiger un script calibré (~60s) enrichi des balises comportementales ElevenLabs v3 (`[sighs]`, `[pause]`, `[confident]`, `[whispers]`, `[deep breath]`, etc.). Ces balises sont transmises au modèle vocal pour générer l'inflexion dramatique.
2. **Nettoyage des sous-titres** : Extraire une version débarrassée des balises entre crochets `[...]`. Les sous-titres affichés dans la Safe Zone haute (`#subtitles-box`) ne doivent afficher que les mots réellement articulés.
3. **Audit du jargon et des prix** :
   * Consulter `banned_global_jargon` dans `registry/video_memory.json` :
     ```json
     ["whisper", "faster-whisper", "ffmpeg", "playwright", "chromium", "codebase", "python", "javascript"]
     ```
   * Vérifier que ni le script parlé, ni les sous-titres, ni les overlays textuels ne contiennent ces termes.
   * Vérifier qu'aucun chiffre tarifaire (150, 200, 750, euro, €) ne figure dans le script (les tarifs sont strictement réservés aux DM et contrats).
4. **Définition du mot-clé CTA** : Confirmer le mot-clé unique pour l'appel à l'action final (ex. `"DEMO"`, `"CODE"`, `"TARIF"`, `"AUDIT"`). Il doit être unique et différer des vidéos précédentes.

---

### PHASE 2 : Récupération de l'Audio ElevenLabs & Alignement Millimétré

#### 1. Objectifs
Obtenir la piste audio master, mesurer sa durée exacte et générer la transcription mot à mot au centième de seconde (`0.01s`) pour synchroniser les animations sur la voix.

#### 2. Procédure Technique
1. **Fichier audio master** : Déposer le fichier généré dans le répertoire du projet sous le nom `voiceover.mp3` ou `voix.wav`.
2. **Mesure de précision via ffprobe** :
   ```bash
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <projet>/voiceover.mp3
   ```
   *Noter la durée exacte $T$ au millième (ex. `61.200s`). Toutes les scènes doivent s'enchaîner sans trou ni dépassement : $\sum \text{durations} = T$.*
3. **Transcription et alignement (0.01s)** :
   * Exécuter `faster-whisper` (modèle `base` ou `small`) pour générer `words.json`.
   * Chaque entrée doit avoir `{ "word": "mot", "start": 12.34, "end": 12.82 }`.
   * Injecter ces données dans `window.WORDS` de `timeline.js`.
4. **Horodatage chirurgical des énumérations** :
   * Pour chaque scène contenant une liste de $N$ cartes/étapes (ex. Scène 15 avec 3 canaux : LinkedIn, Email, Landing Page), relever dans `words.json` :
     * Instant d'énonciation du mot-clé de la Carte 1 ($t_1$)
     * Instant d'énonciation du mot-clé de la Carte 2 ($t_2$)
     * Instant d'énonciation du mot-clé de la Carte 3 ($t_3$)
   * Ces repères temporels commanderont l'allumage séquentiel individuel dans `video.js`.

---

### PHASE 3 : Direction d'Acteur & Poses d'Avatars (Arbitrage Strict)

#### 1. Objectifs
Donner une présence humaine et rythmée sans tomber dans la monotonie ni le recyclage paresseux des mêmes avatars.

#### 2. Règle d'Arbitrage des Poses
* **Interdiction d'utilisation mécanique** : Il est interdit de rejouer systématiquement la même séquence d'avatars sur toutes les vidéos.
* **Option A (Pose existante)** : Si une pose présente dans `assets/avatars/` (`stop.png`, `pointing.png`, `idea.png`, `shock.png`, `skeptic.png`, `mic.png`, etc.) correspond à 100% au ton littéral du propos, la réemployer.
* **Option B (Création d'une nouvelle pose dédiée)** : Si le propos exprime une attitude neuve (regarder sa montre face à la lenteur, hausser les épaules face au manque de transparence, tenir un contrat, croiser les bras, etc.) :
  1. Générer le visuel ou le sticker vectoriel cel-shaded.
  2. Supprimer tout fond (`background transparent`).
  3. Appliquer le **contour sticker blanc opaque de `8px`** caractéristique de la marque.
  4. Sauvegarder dans `assets/avatars/<nom_pose>.png`.
  5. Vérifier son hash SHA-256 pour garantir l'unicité binaire (`test_avatars_binary_uniqueness`).

---

### PHASE 4 : Conception du Storyboard & Illustrations 100% Inédites

#### 1. Objectifs
Garantir un impact visuel mobile d'élite avec des composants sur-mesure au format 9:16, parfaitement animés et exempts de tout recyclage.

#### 2. Règles de Conception Impératives
1. **Unicité totale des illustrations** :
   * Ouvrir `registry/video_memory.json` et consulter `used_illustrations` :
   * Toute illustration déjà listée est **strictement bannie** de réutilisation dans ce projet.
2. **Cadrage & Safe Zone 9:16 (Liberté Scénographique Débridée)** :
   * **Interdiction formelle du template répétitif** : Ne jamais répéter le patron `<div class="card"><div class="header">TITRE + BADGE</div>...</div>` de scène en scène.
   * **Diversité des Compositions Autorisées** :
     * Textes chocs plein écran sans boîte (`ZÉRO VIDÉO`, `CE N'EST PAS / TON CONTENU`).
     * Carrés de numérotation géants (`[ÉTAPE 1]`, `[ÉTAPE 2]`, `[ÉTAPE 3]`) seuls au centre.
     * Post-its et tuiles flottantes indépendantes volant en diagonale (style lymphe).
     * Schémas à flèches animées (`[BLOC A] ━━▶ [BLOC B]`) posés directement sur le fond sans boîte englobante.
   * Tous les éléments doivent respecter la safe-area 1080×1920 (zéro débordement hors écran).
3. **Hiérarchie Typographique à 2 Niveaux** :
   * **Titre principal de chaque scène d'illustration** : $\ge 28\text{px}$ (recommandé : `32px` à `36px`).
   * **Textes descriptifs, badges, sous-titres, étapes** : $\ge 20\text{px}$ (recommandé : `22px` à `24px`).
   * **Micro-tags techniques secondaires uniquement** : $\ge 18\text{px}$ (strictement limité à `.webcam-mute-badge`, `.wf-bar`, `.editor-lang-tag`, `.thumb-mini-tag`, `.window-title`).
4. **Anti-Orphelin (Axe 3)** :
   * Tous les badges néo-brutalistes entre crochets `[ ... ]`, les KPIs et les résolutions (ex. `1080 × 1920 PX`) doivent porter :
     ```css
     white-space: nowrap;
     ```
   * La hauteur utile doit respecter `rect.height <= 1.45 * lineHeight`. Aucun saut de ligne orphelin n'est toléré.
5. **Dynamique Multi-Étapes (Axe 4)** :
   * Pour toute scène multi-cartes de durée $> 3.5\text{s}$ ($N \ge 2$) :
   * Dans `video.js`, programmer l'activation successive :
     ```javascript
     // Exemple d'activation séquentielle exclusive
     const isCard0 = (t >= t_start_0 && t < t_start_1);
     const isCard1 = (t >= t_start_1 && t < t_start_2);
     const isCard2 = (t >= t_start_2 && t <= t_end);

     row0.classList.toggle("active", isCard0);
     row1.classList.toggle("active", isCard1);
     row2.classList.toggle("active", isCard2);
     ```
   * **Chacune des $N$ cartes** doit s'allumer à son tour. Aucune carte ne doit rester inerte pendant que les autres bougent.

---

### PHASE 5 : Scaffolding CLI & Implémentation CSS/JS Propre

#### 1. Objectifs
Générer l'arborescence standardisée du projet sans erreur manuelle et avec héritage automatique du design system.

#### 2. Procédure Technique
1. **Exécution du générateur** :
   ```bash
   python3 init_video.py --target studio_perso/video_03 --cta "TARIF" --title "Maître des Prix B2B"
   ```
2. **Fichiers générés automatiquement (Architecture Multi-Tenant)** :
   * Les projets ne contiennent que leurs données (`project.json`, `brand.json`, `scenes.json`, `timeline.js`, assets). Le moteur racine sert toutes les vidéos.
   * `project.json` : métadonnées (`format: "9:16"`, `fps: 30`, `load_project: true`), mot-clé CTA et tableau de scènes `bp_*`.
   * `brand.json` : charte de marque (palette Obsidian Flame, typographies, poses d'avatar).
   * `scenes.json` : définition déclarative des scènes du projet.
   * `timeline.js` : repères temporels et scènes au format `window.SCENES`.
   * `assets/` : dossier local pour les visuels spécifiques au projet.
3. **Règles d'écriture du code** :
   * Les fichiers moteur racine (`index.html`, `style.css`, `video.js`) ne sont jamais dupliqués dans le projet.
   * N'utiliser que des variables CSS sémantiques issues de `:root` (`var(--nom-variable)`).
   * Ne jamais coder de couleurs en dur dans `style.css` ni dans `video.js`.

---

### PHASE 6 : Validation Pre-Flight Bloquante (< 3s) AVANT Rendu

#### 1. Objectifs
Vérifier automatiquement et instantanément l'absence totale de défauts visuels, géométriques, typographiques ou dynamiques avant d'investir du temps GPU dans l'encodage vidéo.

#### 2. Procédure Technique
1. **Lancement du Gatekeeper** :
   ```bash
   python3 preflight_check.py --projet studio_perso/video_03
   ```
2. **Audit des 5 Axes** :
   * **Axe 1 (Géométrie)** : Illustrations $\ge 840 \times 520\text{px}$, cadrage 1080x1920 sans débordement.
   * **Axe 2 (Typographie)** : Double plancher validé ($\ge 20\text{px}$ général, $\ge 28\text{px}$ titre principal, $18\text{px}$ micro-tags).
   * **Axe 3 (Anti-Orphelin)** : Badges `[ ... ]` et KPIs courts sur 1 seule ligne sans débordement (`scrollWidth <= clientWidth + 2`).
   * **Axe 4 (Dynamique Multi-Étapes)** : Balayage à `0.3s` vérifiant que chaque carte d'une liste change d'état et s'active au bon moment.
   * **Axe 5 (Gouvernance & Unicité)** : Zéro HUD, zéro `#FF2A5F`, zéro réutilisation d'illustrations passées de `video_memory.json`, zéro jargon banni.
3. **Règle Fail-Fast Inflexible** :
   * Si `preflight_check.py` signale la moindre anomalie : **interdiction formelle de lancer le rendu FFmpeg**.
   * Corriger immédiatement le CSS ou le JS, puis relancer `preflight_check.py` jusqu'à obtenir `5/5 axes au vert`.

---

### PHASE 7 : Rendu Final 30 FPS, Inspection Visuelle & Clôture Registre

#### 1. Objectifs
Produire le master vidéo MP4 (H.264 / AAC 30 FPS), vérifier la conformité visuelle frame par frame et sceller le registre d'unicité.

#### 2. Procédure Technique
1. **Lancement du pipeline de rendu** :
   ```bash
   python3 render.py --projet studio_perso/video_03
   ```
   *`render.py` exécute automatiquement le preflight check en pré-étape bloquante en < 3 secondes.*
2. **Inspection visuelle des frames clés** :
   * Vérifier l'intro, le hook des 3 premières secondes.
   * Vérifier que **chaque carte** d'une liste séquentielle est capturée à son état allumé/actif.
   * Vérifier la netteté du CTA final (mot-clé monumental centré, typographie sans flou).
3. **Mise à jour de `registry/video_memory.json`** :
   * Ajouter la nouvelle entrée dans la liste `"videos"` :
     ```json
     {
       "video_id": "video_03",
       "target": "studio_perso",
       "title": "Titre validé",
       "topic": "Sujet traité",
       "cta_keyword": "TARIF",
       "used_illustrations": [
         "pricing_matrix_shock",
         "hidden_costs_breakdown",
         "roi_calculator_instant",
         "direct_tier_comparison"
       ],
       "avatar_sequence": [
         "stop",
         "watch_impatient",
         "shrug_pricing",
         "pointing"
       ]
     }
     ```
4. **Validation de non-régression globale** :
   ```bash
   python3 -m unittest discover -s tests -v
   graphify update .
   ```

---

### PHASE 8 : Distribution Ciblée (LinkedIn & Instagram) & Golden Hour

#### 1. Objectifs
Transformer le master vidéo en vues qualifiées et en leads B2B en publiant exclusivement sur les deux canaux rentables (**LinkedIn** en priorité de vente et **Instagram Reels** avec recommandation Facebook en vitrine), tout en éliminant la dispersion sur les réseaux secondaires.

#### 2. Procédure Technique
1. **Génération automatique du Kit de Distribution** :
   ```bash
   python3 generate_social_pack.py --projet <chemin_projet>
   ```
   *Ce script génère `DISTRIBUTION_KIT.md` directement dans le dossier du projet avec post LinkedIn calibré, légende Instagram, premier commentaire et teaser story.*
2. **Vérification Pre-Upload Smartphone** :
   - Instagram : Option `Importer avec la meilleure qualité` active + Recadrage couverture dans l'onglet `Grille du profil` (centré dans la zone 1:1 `Y: 420-1500px`) + Option `Recommander sur Facebook` active.
   - LinkedIn : Texte avec accroche visible en moins de 140 caractères + Zéro lien externe dans le corps du post.
3. **Exécution de la Golden Hour (Minutes 0 à 60)** :
   - *Minute 01* : Poster le premier commentaire amorce et l'épingler (`Pin comment`).
   - *Minute 05* : Partager le Reel en Story Instagram avec sticker masquant le bas pour forcer le clic vers le post original.
   - *Minutes 05 à 45* : Répondre à 100% des commentaires reçus avec une phrase de plus de 5 mots et une question de relance.
   - *Interdictions absolues* : Ne jamais regarder la vidéo 50 fois en boucle depuis le même compte, ne jamais supprimer/re-publier dans les 24h, ne jamais éditer le texte dans les 20 premières minutes.

---

### Catalogue Officiel des 8 Blueprints Universels & Multi-Tenant Studio

Le studio AGENT404 dispose d'un moteur de production industrialisé "Video-as-Code" multi-tenant. Chaque vidéo client est isolée dans son propre répertoire sous `studio_clients/<client_id>/` et est pilotée **à 100% par `scene.params` dans `project.json`** (ZÉRO nouvelle ligne de JS nécessaire, temps de production divisé par 4 : $< 2\text{ h}$ par vidéo).

#### 1. Architecture Multi-Tenant & Fichier `brand.json`

Chaque dossier client (`studio_clients/<client_id>/`) possède un fichier `brand.json` qui personnalise instantanément la charte graphique sans toucher au cœur du moteur :

```json
{
  "brand_name": "ACME CORP",
  "theme": {
    "bg_canvas": "#F5F2EB",
    "surface_card": "#FFFFFF",
    "ink": "#111111",
    "accent_primary": "#FF4F18",
    "tile_1": "#FEF08A",
    "tile_2": "#BFDBFE",
    "tile_3": "#A7F3D0"
  },
  "typography": {
    "font_heading": "Montserrat",
    "font_body": "Inter",
    "font_mono": "JetBrains Mono"
  },
  "avatars": {
    "base_path": "assets/avatars/",
    "default": "idea.png",
    "poses": {
      "idea": "idea.png",
      "pointing": "pointing.png",
      "facepalm": "facepalm.png",
      "laptop": "laptop.png",
      "mic": "mic.png",
      "money": "money.png"
    }
  }
}
```

*Le moteur applique dynamiquement ces valeurs sur les variables `:root` (`--bg-canvas`, `--surface-card`, `--ink`, `--accent-primary`, etc.) et résout les poses d'avatars déclarées dans `brand.json` avec fallback transparent vers la base universelle.*

---

#### 2. Registre Vectoriel Universel `SVG_ICONS`

22 icônes vectorielles standardisées (`viewBox="0 0 24 24"`, traits épais de `2.5px`, fond transparent ou aplats sémantiques) sont disponibles et injectables dans n'importe quel blueprint via leur clé :

* **Symboles Sémantiques (18)** : `question`, `lock`, `camera`, `bulb`, `clapper`, `clock`, `scale`, `check`, `cross`, `robot`, `mic`, `code`, `bolt`, `file`, `chart`, `calendar`, `rocket`, `gear`.
* **Réseaux Sociaux Officiels (4)** : `linkedin`, `tiktok`, `reels`, `shorts`.

---

#### 3. Schémas JSON des 8 Blueprints Universels (`bp_*`)

##### 1. `bp_hook_question` (Accroche / Obsession / Rupture)
* **Usage** : Première scène de captation d'attention, question provocatrice ou énoncé d'un problème criant.
```json
{
  "id": "scene_01",
  "type": "bp_hook_question",
  "avatar_mode": "duo_lymphe",
  "params": {
    "top_badge": "LE PROBLÈME",
    "box_color": "var(--tile-yellow)",
    "icon": "question",
    "title": "POURQUOI 90% DES PROSPECTS IGNORENT VOS MESSAGES ?",
    "subtitle": "Le modèle traditionnel de prospection est mort.",
    "stamp_text": "BLOQUÉ"
  }
}
```

##### 2. `bp_friction_stack` (Liste de galères / Piliers / Arguments)
* **Usage** : Énumération de 2 à 4 frictions, empilement de points de douleur ou piliers d'une méthode.
```json
{
  "id": "scene_02",
  "type": "bp_friction_stack",
  "avatar_mode": "solo",
  "params": {
    "header_badge": "3 FRICTIONS CRITIQUES",
    "items": [
      {
        "icon": "clock",
        "box_color": "var(--tile-yellow)",
        "text": "15 heures perdues par semaine",
        "right_badge": "TEMPS",
        "status": "cross",
        "appear_at_offset": 0.0
      },
      {
        "icon": "cross",
        "box_color": "var(--surface-card)",
        "text": "Taux de réponse inférieur à 2%",
        "right_badge": "SILENCE",
        "status": "cross",
        "appear_at_offset": 0.6
      },
      {
        "icon": "bolt",
        "box_color": "var(--tile-blue)",
        "text": "Fatigue mentale et zéro pipeline",
        "right_badge": "IMPACT",
        "status": "cross",
        "appear_at_offset": 1.2
      }
    ],
    "connectors": "none"
  }
}
```

##### 3. `bp_stat_shock` (Chiffre choc / Compteur métrique / Preuve)
* **Usage** : Preuve d'autorité ou métrique saillante avec jauge animée et compteur dynamique.
```json
{
  "id": "scene_03",
  "type": "bp_stat_shock",
  "avatar_mode": "hidden",
  "params": {
    "top_badge": "RÉSULTAT CHIFFRÉ",
    "stat_from": 0,
    "stat_to": 78,
    "stat_suffix": "%",
    "label": "DE TEMPS GAGNÉ DÈS LA PREMIÈRE SEMAINE",
    "progress_bar": true,
    "footer_stamp": "MESURÉ"
  }
}
```

##### 4. `bp_versus_compare` (Avant / Après, Clones IA vs Humain, Problème vs Solution)
* **Usage** : Comparaison radicale entre une ancienne approche inefficace et la nouvelle solution.
```json
{
  "id": "scene_04",
  "type": "bp_versus_compare",
  "avatar_mode": "solo",
  "params": {
    "layout": "vertical",
    "left_or_top": {
      "badge": "MÉTHODE OBSOLÈTE",
      "title": "Copier-coller manuel & relances à l'aveugle",
      "icon": "cross",
      "color": "var(--surface-card)",
      "status": "cross"
    },
    "right_or_bottom": {
      "badge": "MOTEUR AUTOMATISÉ",
      "title": "Ingestion agnostique & personnalisation hyper-ciblée",
      "icon": "check",
      "color": "var(--tile-yellow)",
      "status": "check"
    },
    "footer_stamp": "SANS APPEL"
  }
}
```

##### 5. `bp_code_window` (Preuve technique / Terminal / Workflow)
* **Usage** : Fenêtre Mac/Linux Néo-Brutaliste montrant du code, une transcription dynamique ou un waveform audio.
```json
{
  "id": "scene_05",
  "type": "bp_code_window",
  "avatar_mode": "hidden",
  "params": {
    "window_title": "pipeline_execution.py",
    "theme": "dark",
    "mode": "code",
    "lines": [
      "def run_growth_engine(client):",
      "    target = analyze_prospect(client)",
      "    return generate_hyper_targeted_video(target)"
    ],
    "footer_stamp": "DÉTERMINISTE",
    "stamp_offset": 1.2
  }
}
```

##### 6. `bp_grid_2x2` (4 styles / 4 assets / Multi-cartes)
* **Usage** : Déploiement de 4 caractéristiques, 4 livrables ou 4 piliers d'offre sous forme de tuiles carrées.
```json
{
  "id": "scene_06",
  "type": "bp_grid_2x2",
  "avatar_mode": "hidden",
  "params": {
    "top_badge": "LE PACK COMPLET",
    "cards": [
      { "icon": "camera", "title": "Vidéo 9:16 Haute Densité", "color": "var(--tile-yellow)", "appear_at_offset": 0.0 },
      { "icon": "file", "title": "Post LinkedIn Clé en Main", "color": "var(--tile-blue)", "appear_at_offset": 0.3 },
      { "icon": "mic", "title": "Audio Studio & Sound Design", "color": "var(--tile-green)", "appear_at_offset": 0.6 },
      { "icon": "rocket", "title": "Distribution & Golden Hour", "color": "var(--surface-card)", "appear_at_offset": 0.9 }
    ],
    "bottom_meter": {
      "label": "Taux d'automatisation",
      "from": 0,
      "to": 100
    }
  }
}
```

##### 7. `bp_logo_carousel_rtl` (Carrousel 1 à 1 centré Droite $\rightarrow$ Gauche)
* **Usage** : Défilement centré et percutant de logos de réseaux sociaux ou de plateformes partenaires.
```json
{
  "id": "scene_07",
  "type": "bp_logo_carousel_rtl",
  "avatar_mode": "solo",
  "params": {
    "top_badge": "DIFFUSION MULTI-CANAL",
    "items": [
      { "logo": "linkedin", "label": "LINKEDIN", "badge": "B2B LEADS", "at_time": 0.0 },
      { "logo": "reels", "label": "INSTAGRAM", "badge": "VITRINE", "at_time": 1.2 },
      { "logo": "tiktok", "label": "TIKTOK", "badge": "VIRALITÉ", "at_time": 2.4 },
      { "logo": "shorts", "label": "SHORTS", "badge": "NOTORIÉTÉ", "at_time": 3.6 }
    ]
  }
}
```

##### 8. `bp_cta_conversion` (Conversion finale Simple ou Double Porte)
* **Usage** : Clôture avec saisie simulée du mot-clé en message privé, clic vectoriel et présentation des portes de conversion.
```json
{
  "id": "scene_08",
  "type": "bp_cta_conversion",
  "avatar_mode": "solo",
  "params": {
    "variant": "two_door",
    "keyword": "STUDIO",
    "button_label": "ENVOYER",
    "click_at_offset": 1.2,
    "doors": [
      {
        "badge": "PORTE 1 : GRATUIT",
        "title": "Guide Video-as-Code",
        "subtitle": "Le playbook complet offert en DM",
        "color": "var(--surface-card)",
        "appear_at_offset": 1.8
      },
      {
        "badge": "PORTE 2 : STUDIO",
        "title": "Production Sur-Mesure",
        "subtitle": "4 capsules prêtes à diffuser / mois",
        "color": "var(--tile-yellow)",
        "appear_at_offset": 2.4
      }
    ]
  }
}
```

---

#### 4. Workflow Client Standardisé (Zéro JS)

1. **Création du projet client** :
   ```bash
   cp -r studio_clients/_template_prospect/ studio_clients/<client_id>/
   ```
2. **Configuration de marque** :
   Adapter `studio_clients/<client_id>/brand.json` (palette, polices, avatars).
3. **Rédaction du scénario** :
   Remplir `project.json` avec les scènes `bp_*` adaptées au message.
4. **Génération de la timeline** :
   ```bash
   python3 build_master_timeline.py -p studio_clients/<client_id>
   ```
5. **Validation Pre-Flight (< 3s)** :
   ```bash
   python3 preflight_check.py -p studio_clients/<client_id>
   ```
6. **Rendu Master 30 FPS** :
   ```bash
   python3 render.py -p studio_clients/<client_id>
   ```
   *Le fichier final est automatiquement généré sous `studio_clients/<client_id>/output_final.mp4`.*

---

### Matrice d'Audit Rapide (Checklist de Clôture)

| Phase | Critère Validé | Statut Obligatoire |
| :--- | :--- | :---: |
| **P1** | Zéro tag ElevenLabs `[...]` dans les sous-titres + Zéro jargon banni | **REQUIS** |
| **P2** | Timestamps `0.01s` Whisper générés + Durée totale $T$ vérifiée au millième | **REQUIS** |
| **P3** | Arbitrage poses existantes vs création pose dédiée (fond transparent + sticker 8px) | **REQUIS** |
| **P4** | Zéro illustration recyclée + Tailles $\ge 20\text{px}$/$\ge 28\text{px}$ + Allumage individuel de chaque carte | **REQUIS** |
| **P5** | Scaffolding `init_video.py` + 100% variables `:root` + Zéro hex hors `:root` + Zéro `#FF2A5F` | **REQUIS** |
| **P6** | `preflight_check.py` exécuté et validé à 100% (5/5 axes au vert) | **REQUIS** |
| **P7** | Master MP4 30 FPS conforme (`H.264`, `yuv420p`, `-maxrate 15M`, `aac 44.1kHz`, `-movflags +faststart`) + `video_memory.json` scellé | **REQUIS** |
| **P8** | `DISTRIBUTION_KIT.md` généré + Checklist smartphone & Golden Hour prêtes pour LinkedIn & Instagram | **REQUIS** |

*Ce protocole garantit un niveau de qualité constant, prévisible et reproductible sans aucune retouche manuelle.*
