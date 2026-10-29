---
name: produce-video
description: Protocole officiel en 8 phases pour concevoir, aligner, animer et rendre une vidéo AGENT404 sans régression
---

# Workflow : Production Vidéo AGENT404 (Protocole Standardisé en 8 Phases)

Ce workflow régit la création de toute nouvelle capsule vidéo (`studio_perso/video_XX` ou `studio_clients/<client>/video_XX`).
Il applique la Loi de l'Effet Cliquet ($N+1 > N$) : aucune vidéo ne peut être rendue si elle n'a pas validé l'intégralité des 5 axes du Gatekeeper.

Consulter le guide complet dans [`VIDEO_PRODUCTION_PLAYBOOK.md`](../../VIDEO_PRODUCTION_PLAYBOOK.md).

---

## Les 8 Phases Obligatoires

### PHASE 1 : Ingestion Agnostique, Extraction de Joyau & Audit Éditorial
1. **Entrée Agnostique (Input Agnostic)** : Ingestion de n'importe quel matériau brut (note vocale WhatsApp 2 min, post LinkedIn écrit, documentation technique, schéma Make/n8n, cas client, ou Loom trop long).
2. **Extraction de Joyau & Scripting** : Extraire la pépite et formuler un script d'acting captivant au format étalon de ~60s (amplitude 45s à 90s) avec balises d'acting ElevenLabs v3 (`[sighs]`, `[pause]`, `[confident]`, `[whispers]`, etc.).
3. **Nettoyage sous-titres** : Extraire une version épurée sans balises entre crochets `[...]` pour l'affichage textuel à l'écran (uniquement les mots prononcés).
4. **Audit Jargon & Prix** :
   - Vérifier dans `registry/video_memory.json` qu'aucun terme de `banned_global_jargon` (`python`, `javascript`, `ffmpeg`, `whisper`, etc.) n'apparaît dans le script parlé ou les sous-titres.
   - Vérifier qu'aucun chiffre tarifaire (150, 200, 750, euro, €) ne figure dans le script (tarifs strictement réservés aux DM et contrats).
5. **Mot-clé CTA** : Confirmer le mot-clé d'appel à l'action unique en message privé (ex. `"DEMO"`, `"CODE"`, `"TARIF"`, `"AUDIT"`).

### PHASE 2 : Récupération de l'Audio ElevenLabs & Alignement Millimétré
1. **Fichier audio** : Déposer le fichier master dans le dossier projet (`voiceover.mp3` ou `voix.wav`).
2. **Mesure de durée exacte** :
   ```bash
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <projet>/voiceover.mp3
   ```
3. **Transcription mot à mot (0.01s)** : Exécuter `faster-whisper` (ou le script d'alignement du studio) pour obtenir `words.json` et peupler `window.WORDS` dans `timeline.js`.
4. **Horodatage des listes** : Noter précisément les timestamps de début et de fin de chaque élément d'une énumération ou liste de cartes (ex. Carte 1 à `t1`, Carte 2 à `t2`, Carte 3 à `t3`).

### PHASE 3 : Direction d'Acteur & Poses d'Avatars (Arbitrage Strict)
1. **Analyse émotionnelle** : Pour chaque scène incarnée (`type: "face"` ou PiP), identifier l'action littérale et l'attitude requise.
2. **Règle d'arbitrage** :
   - *Interdiction* de recycler aveuglément l'intégralité des poses des vidéos passées.
   - Si une pose existante dans `assets/avatars/` correspond parfaitement à l'émotion du passage (ex. `stop.png`, `pointing.png`), l'utiliser.
   - Si le script exprime une attitude inédite (regarder sa montre, hausser les épaules, tenir un document, croiser les bras, etc.), **générer une nouvelle pose dédiée** :
     - Fond transparent (PNG).
     - Contour sticker blanc net de `8px`.
     - Style vectoriel cel-shaded cohérent avec l'identité de marque.
     - Unicité binaire SHA-256 validée contre les poses existantes.

### PHASE 4 : Conception du Storyboard & Illustrations Néo-Brutalistes (Règles d'Or)
1. **Consultation du registre** : Lire `registry/video_memory.json` (`used_illustrations`) pour lister les composants déjà utilisés. **Interdiction formelle de les réutiliser**.
2. **Liberté Scénographique & Interdiction du Gabarit Unique Répétitif** :
   - **Interdiction formelle du template répétitif** : Bannissement strict du patron `<div class="card"><div class="header">TITRE + BADGE</div>...</div>` répété de scène en scène.
   - **Compositions variées libres** : Textes chocs plein écran sans boîte (`ZÉRO VIDÉO`, `CE N'EST PAS / TON CONTENU`), carrés de numérotation géants (`[ÉTAPE 1]`, etc.), post-its et tuiles flottantes indépendantes en diagonale (style lymphe), schémas à flèches animées (`[BLOC A] ━━▶ [BLOC B]`) posés directement sur le fond sans boîte englobante.
   - Zéro halo diffus, zéro flou (`filter: blur(...)` interdit), zéro effet "néon cyber".
3. **Zéro Pavé de Texte & Hiérarchie Typographique Lisible** :
   - **Zéro pavé de texte à l'écran** : tout texte explicatif ou descriptif de plus de 4-5 mots est banni.
   - Titre principal de chaque scène / carte : $\ge 28\text{px}$ en gras majuscules ultra-concis ($\le 4$ mots).
   - Aucun texte à l'écran inférieur à $26\text{px}$ (lisibilité immédiate sur smartphone à 1.5 mètre).
   - Micro-tags résiduels tolérés à $\ge 20\text{px}$ avec `white-space: nowrap` obligatoire.
4. **1 Idée = 1 Preuve Visuelle Physique** :
   - Remplacer les longs posts par des squelettes UI géométriques barrés d'un tampon `.neo-stamp` orange flamme (`background: var(--flame)`, texte blanc, bordure 4 px encre `var(--ink)`, ombre dure 8 px, rotation -6°, Montserrat 900 38 px majuscules, ex. `"PAVÉ DE 150 LIGNES = IGNORÉ !"`).
   - Utiliser des schémas physiques : cartes pastel physiques, tampons d'alerte, indicateurs de chronomètre grand format.
5. **Rythme & Dynamisme Temporel** :
   - Durée idéale par scène : **2.0s à 3.5s** (grand maximum 4.0s). Au-delà, le décrochage de rétention est garanti.
   - Dans toute scène multi-étapes ($N \ge 2$), activation séquentielle individuelle de **chacune des $N$ cartes** aux timestamps identifiés en Phase 2 (zéro carte inerte).
6. **Avatars Purs & Sous-titres Épurés** :
   - Avatars : zéro badge parasite (`.face-badge` strictement masqué), pur sticker avec ombre dure `drop-shadow(8px 8px 0px #111111)`.
   - Sous-titres : affichage direct sur fond beige uni mat sans cartouche blanc / pilule (aucune grille, zéro effet karaoké bloquant), un seul mot-clé sémantique en accent orange flamme (`color: var(--flame)` via `.keyword-accent` ou `.highlight`).

### PHASE 5 : Scaffolding & Implémentation CSS/JS
1. **Initialisation automatique** :
   ```bash
   python3 init_video.py --target <dossier> --cta "<MOT_CLE>" --title "<Titre>"
   ```
2. **Discipline CSS** :
   - 100% de variables CSS sémantiques issues de `:root` (`var(--accent-primary)`, `var(--surface-card)`, etc.).
   - Zéro code couleur hexadécimal `#hex` en dur hors `:root`.
   - Bannissement perpétuel et absolu de `#FF2A5F` et du HUD (`#agent-hud`).

### PHASE 6 : Validation Pre-Flight Bloquante (< 3s) AVANT Rendu
1. **Exécution du Gatekeeper** :
   ```bash
   python3 preflight_check.py --projet <dossier>
   ```
2. **Règle d'arrêt absolu** :
   - Si un seul des 5 axes échoue (géométrie, typo $< 20\text{px}$, retour orphelin, carte inerte, collision registre ou HUD), corriger immédiatement.
   - **Il est formellement interdit de démarrer `render.py` avant d'avoir obtenu `5/5 axes au vert`.**

### PHASE 7 : Rendu Final 30 FPS, Inspection & Clôture Registre
1. **Rendu FFmpeg** :
   ```bash
   python3 render.py --projet <dossier>
   ```
2. **Inspection visuelle** : Extraire et vérifier les frames clés (notamment l'état actif de chaque carte des scènes multi-étapes et le CTA monumental final).
3. **Mise à jour du registre** : Ajouter la nouvelle vidéo dans `registry/video_memory.json` :
   - `video_id`, `target`, `title`, `topic`, `cta_keyword`.
   - `used_illustrations` : identifiants de toutes les nouvelles illustrations introduites.
   - `avatar_sequence` : séquence ordonnée des poses incarnées.
4. **Vérification globale & graphe** :
   ```bash
   python3 -m unittest discover -s tests -v
   graphify update .
   ```

### PHASE 8 : Distribution Multi-Canaux & Golden Hour
1. Se référer au playbook complet [`docs/DISTRIBUTION_PLAYBOOK.md`](../../docs/DISTRIBUTION_PLAYBOOK.md).
2. Générer le pack de distribution complet :
   ```bash
   python3 generate_social_pack.py --projet <dossier>
   ```
3. Publication prioritaire LinkedIn (80 % du volume), relais Instagram Reels (20 %), TikTok en pause.
4. Présence active pendant la Golden Hour (premières 60 minutes après publication) pour répondre aux commentaires et engager les prospects.
