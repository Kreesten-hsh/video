# PLAYBOOK OFFICIEL DE PRODUCTION VIDÉO AGENT404
## Guide d'Ingénierie & Protocole Standardisé en 7 Phases (Loi d'Effet Cliquet $N+1 > N$)

Ce document constitue la **référence absolue** pour la création de toute vidéo au sein du studio (capsules personnelles dans `studio_perso/` ou capsules sur-mesure pour clients dans `studio_clients/`).
Tout agent ou développeur intervenant sur la chaîne de production **doit exécuter les 7 phases séquentiellement sans en sauter aucune**.

---

### SOMMAIRE
1. [Principes Directeurs & Effet Cliquet](#principes-directeurs--effet-cliquet)
2. [PHASE 1 — Lecture du Script Tagué & Audit Éditorial](#phase-1--lecture-du-script-tagu%C3%A9--audit-%C3%A9ditorial)
3. [PHASE 2 — Récupération de l'Audio ElevenLabs & Alignement Millimétré](#phase-2--r%C3%A9cup%C3%A9ration-de-laudio-elevenlabs--alignement-millim%C3%A9tr%C3%A9)
4. [PHASE 3 — Direction d'Acteur & Poses d'Avatars (Arbitrage Strict)](#phase-3--direction-dacteur--poses-davatars-arbitrage-strict)
5. [PHASE 4 — Conception du Storyboard & Illustrations 100% Inédites](#phase-4--conception-du-storyboard--illustrations-100-in%C3%A9dites)
6. [PHASE 5 — Scaffolding CLI & Implémentation CSS/JS Propre](#phase-5--scaffolding-cli--impl%C3%A9mentation-cssjs-propre)
7. [PHASE 6 — Validation Pre-Flight Bloquante (< 3s) AVANT Rendu](#phase-6--validation-pre-flight-bloquante--3s-avant-rendu)
8. [PHASE 7 — Rendu Final 30 FPS, Inspection Visuelle & Clôture Registre](#phase-7--rendu-final-30-fps-inspection-visuelle--cl%C3%B4ture-registre)
9. [Matrice d'Audit Rapide (Checklist de Clôture)](#matrice-daudit-rapide-checklist-de-cl%C3%B4ture)

---

### Principes Directeurs & Effet Cliquet

1. **Loi du Cliquet ($N+1 > N$)** : Une vidéo nouvelle ne doit jamais régresser par rapport aux standards acquis sur les vidéos précédentes. Tout bug corrigé antérieurement (tailles de polices, retours orphelins, cartes inertes, dérives d'avatars) est définitivement interdit et bloqué à la source.
2. **Zero-Fluff / High-Density** : Format 1080x1920 (9:16 vertical), 30 FPS, centré sur la rétention mobile. Chaque frame doit apporter une information visuelle utile.
3. **Zéro Hardcoding & Thème Sémantique** : 100% des couleurs hors `:root` sont interdites. Utilisation stricte des variables CSS sémantiques.
4. **Bannissements Perpétuels** :
   - `#FF2A5F` (rose banni) : interdit sur 100% du projet.
   - `#agent-hud` : bandeau supérieur HUD définitivement banni.
   - Jargon technique d'ingénierie dans les scripts (Python, FFmpeg, Whisper, JavaScript, etc.).

---

### PHASE 1 — Lecture du Script Tagué & Audit Éditorial

#### 1. Objectifs
Transformer le script brut fourni par l'utilisateur en un texte d'acting précis et un flux de sous-titres épuré, tout en vérifiant l'absence totale de jargon banni.

#### 2. Procédure Technique
1. **Extraction du texte d'acting** : Le script fourni contient des balises comportementales ElevenLabs v3 (`[sighs]`, `[pause]`, `[confident]`, `[whispers]`, `[deep breath]`, etc.). Ces balises sont transmises au modèle vocal pour générer l'inflexion dramatique.
2. **Nettoyage des sous-titres** : Extraire une version débarrassée des balises entre crochets `[...]`. Les sous-titres affichés dans la Safe Zone haute (`#subtitles-box`) ne doivent afficher que les mots réellement articulés.
3. **Audit du jargon** :
   * Consulter `banned_global_jargon` dans `registry/video_memory.json` :
     ```json
     ["whisper", "faster-whisper", "ffmpeg", "playwright", "chromium", "codebase", "python", "javascript"]
     ```
   * Vérifier que ni le script parlé, ni les sous-titres, ni les overlays textuels ne contiennent ces termes.
4. **Définition du mot-clé CTA** : Confirmer le mot-clé unique pour l'appel à l'action final (ex. `"DEMO"`, `"CODE"`, `"TARIF"`, `"AUDIT"`). Il doit être unique et différer des vidéos précédentes.

---

### PHASE 2 — Récupération de l'Audio ElevenLabs & Alignement Millimétré

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

### PHASE 3 — Direction d'Acteur & Poses d'Avatars (Arbitrage Strict)

#### 1. Objectifs
Donner une présence humaine et rythmée sans tomber dans la monotonie ni le recyclage paresseux des mêmes avatars.

#### 2. Règle d'Arbitrage des Poses
* **Interdiction d'utilisation mécanique** : Il est interdit de rejouer systématiquement la même séquence d'avatars sur toutes les vidéos.
* **Option A — Pose existante** : Si une pose présente dans `assets/avatars/` (`stop.png`, `pointing.png`, `idea.png`, `shock.png`, `skeptic.png`, `mic.png`, etc.) correspond à 100% au ton littéral du propos, la réemployer.
* **Option B — Création d'une nouvelle pose dédiée** : Si le propos exprime une attitude neuve (regarder sa montre face à la lenteur, hausser les épaules face au manque de transparence, tenir un contrat, croiser les bras, etc.) :
  1. Générer le visuel ou le sticker vectoriel cel-shaded.
  2. Supprimer tout fond (`background transparent`).
  3. Appliquer le **contour sticker blanc opaque de `8px`** caractéristique de la marque.
  4. Sauvegarder dans `assets/avatars/<nom_pose>.png`.
  5. Vérifier son hash SHA-256 pour garantir l'unicité binaire (`test_avatars_binary_uniqueness`).

---

### PHASE 4 — Conception du Storyboard & Illustrations 100% Inédites

#### 1. Objectifs
Garantir un impact visuel mobile d'élite avec des composants sur-mesure au format 9:16, parfaitement animés et exempts de tout recyclage.

#### 2. Règles de Conception Impératives
1. **Unicité totale des illustrations** :
   * Ouvrir `registry/video_memory.json` et consulter `used_illustrations` :
   * Toute illustration déjà listée est **strictement bannie** de réutilisation dans ce projet.
2. **Cadrage & Safe Zone 9:16** :
   * Les conteneurs d'illustrations centraux doivent occuper :
     * Largeur : **`880px` à `940px`** (centré sur 1080px).
     * Hauteur : **`620px` à `880px`** (centré verticalement dans la zone `scene-zone` de `top: 260px` à `bottom: 240px`).
   * Tout conteneur $< 840 \times 520\text{px}$ est immédiatement rejeté par le Gatekeeper.
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

### PHASE 5 — Scaffolding CLI & Implémentation CSS/JS Propre

#### 1. Objectifs
Générer l'arborescence standardisée du projet sans erreur manuelle et avec héritage automatique du design system.

#### 2. Procédure Technique
1. **Exécution du générateur** :
   ```bash
   python3 init_video.py --target studio_perso/video_03 --cta "TARIF" --title "Maître des Prix B2B"
   ```
2. **Fichiers générés automatiquement** :
   * `index.html` : structuré pour le canvas 9:16, 100% exempt de `#agent-hud`.
   * `style.css` : bloc `:root` complet de variables CSS sémantiques, zéro code `#hex` hors `:root`, zéro `#FF2A5F`.
   * `timeline.js` : squelette de scènes et mots alignés.
   * `video.js` : squelette du moteur d'animation rappelant en commentaire d'en-tête les illustrations passées et le jargon interdit.
   * `project_config.json` et `project.json` : métadonnées et scènes synchronisées.
3. **Règles d'écriture du code** :
   * N'utiliser que `var(--nom-variable)` pour toute couleur ou nuance.
   * Ne jamais coder de couleurs en dur dans `style.css` ni dans `video.js`.

---

### PHASE 6 — Validation Pre-Flight Bloquante (< 3s) AVANT Rendu

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

### PHASE 7 — Rendu Final 30 FPS, Inspection Visuelle & Clôture Registre

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

### Matrice d'Audit Rapide (Checklist de Clôture)

| Phase | Critère Validé | Statut Obligatoire |
| :--- | :--- | :---: |
| **P1** | Zéro tag ElevenLabs `[...]` dans les sous-titres + Zéro jargon banni | **REQUIS** |
| **P2** | Timestamps `0.01s` Whisper générés + Durée totale $T$ vérifiée au millième | **REQUIS** |
| **P3** | Arbitrage poses existantes vs création pose dédiée (fond transparent + sticker 8px) | **REQUIS** |
| **P4** | Zéro illustration recyclée + Tailles $\ge 20\text{px}$/$\ge 28\text{px}$ + Allumage individuel de chaque carte | **REQUIS** |
| **P5** | Scaffolding `init_video.py` + 100% variables `:root` + Zéro hex hors `:root` + Zéro `#FF2A5F` | **REQUIS** |
| **P6** | `preflight_check.py` exécuté et validé à 100% (5/5 axes au vert) | **REQUIS** |
| **P7** | Master MP4 30 FPS conforme + `video_memory.json` mis à jour + 100% tests unitaires au vert | **REQUIS** |

*Ce protocole garantit un niveau de qualité constant, prévisible et reproductible sans aucune retouche manuelle.*
