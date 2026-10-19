---
name: produce-video
description: Protocole officiel en 7 phases pour concevoir, aligner, animer et rendre une vidéo AGENT404 sans régression
---

# Workflow : Production Vidéo AGENT404 (Protocole Standardisé en 7 Phases)

Ce workflow régit la création de toute nouvelle capsule vidéo (`studio_perso/video_XX` ou `studio_clients/<client>/video_XX`).
Il applique la Loi de l'Effet Cliquet ($N+1 > N$) : aucune vidéo ne peut être rendue si elle n'a pas validé l'intégralité des 5 axes du Gatekeeper.

Consulter le guide complet dans [`VIDEO_PRODUCTION_PLAYBOOK.md`](file:///home/hasashi/Bureau/video/VIDEO_PRODUCTION_PLAYBOOK.md).

---

## Les 7 Phases Obligatoires

### PHASE 1 — Lecture du Script Tagué & Audit Éditorial
1. **Script source** : Lire le texte fourni avec ses balises d'acting ElevenLabs v3 (`[sighs]`, `[pause]`, `[confident]`, `[whispers]`, etc.).
2. **Nettoyage sous-titres** : Extraire une version épurée sans balises entre crochets `[...]` pour l'affichage textuel à l'écran (uniquement les mots prononcés).
3. **Audit Jargon** : Vérifier dans `registry/video_memory.json` qu'aucun terme de `banned_global_jargon` (`python`, `javascript`, `ffmpeg`, `whisper`, etc.) n'apparaît dans le script parlé ou les sous-titres.
4. **Mot-clé CTA** : Confirmer le mot-clé d'appel à l'action unique en message privé (ex. `"DEMO"`, `"CODE"`, `"TARIF"`, `"AUDIT"`).

### PHASE 2 — Récupération de l'Audio ElevenLabs & Alignement Millimétré
1. **Fichier audio** : Déposer le fichier master dans le dossier projet (`voiceover.mp3` ou `voix.wav`).
2. **Mesure de durée exacte** :
   ```bash
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <projet>/voiceover.mp3
   ```
3. **Transcription mot à mot (0.01s)** : Exécuter `faster-whisper` (ou le script d'alignement du studio) pour obtenir `words.json` et peupler `window.WORDS` dans `timeline.js`.
4. **Horodatage des listes** : Noter précisément les timestamps de début et de fin de chaque élément d'une énumération ou liste de cartes (ex. Carte 1 à `t1`, Carte 2 à `t2`, Carte 3 à `t3`).

### PHASE 3 — Direction d'Acteur & Poses d'Avatars (Arbitrage Strict)
1. **Analyse émotionnelle** : Pour chaque scène incarnée (`type: "face"` ou PiP), identifier l'action littérale et l'attitude requise.
2. **Règle d'arbitrage** :
   - *Interdiction* de recycler aveuglément l'intégralité des poses des vidéos passées.
   - Si une pose existante dans `assets/avatars/` correspond parfaitement à l'émotion du passage (ex. `stop.png`, `pointing.png`), l'utiliser.
   - Si le script exprime une attitude inédite (regarder sa montre, hausser les épaules, tenir un document, croiser les bras, etc.), **générer une nouvelle pose dédiée** :
     - Fond transparent (PNG).
     - Contour sticker blanc net de `8px`.
     - Style vectoriel cel-shaded cohérent avec l'identité de marque.
     - Unicité binaire SHA-256 validée contre les poses existantes.

### PHASE 4 — Conception du Storyboard & Illustrations 100% Inédites
1. **Consultation du registre** : Lire `registry/video_memory.json` (`used_illustrations`) pour lister les composants déjà utilisés. **Interdiction formelle de les réutiliser**.
2. **Géométrie 9:16** : Concevoir des composants occupant pleinement l'espace utile central :
   - Largeur : `880px` à `940px`.
   - Hauteur minimale : `620px` à `880px`.
3. **Hiérarchie typographique** :
   - Titre principal de chaque scène d'illustration $\ge 28\text{px}$.
   - Textes descriptifs, listes, étapes et badges $\ge 20\text{px}$.
   - Micro-tags techniques secondaires tolérés à $\ge 18\text{px}$ (`.thumb-mini-tag`, `.wf-bar`, `.editor-lang-tag`, `.webcam-mute-badge`).
   - `white-space: nowrap` obligatoire sur tous les badges `[ ... ]`, KPIs, nombres et résolutions pour interdire les retours orphelins sur 2 lignes.
4. **Dynamique multi-étapes** : Dans toute scène contenant $N$ cartes/étapes ($N \ge 2$), programmer dans `video.js` l'activation séquentielle individuelle de **chacune des $N$ cartes** aux timestamps identifiés en Phase 2 (zéro carte inerte).

### PHASE 5 — Scaffolding & Implémentation CSS/JS
1. **Initialisation automatique** :
   ```bash
   python3 init_video.py --target <dossier> --cta "<MOT_CLE>" --title "<Titre>"
   ```
2. **Discipline CSS** :
   - 100% de variables CSS sémantiques issues de `:root` (`var(--accent-primary)`, `var(--surface-card)`, etc.).
   - Zéro code couleur hexadécimal `#hex` en dur hors `:root`.
   - Bannissement perpétuel et absolu de `#FF2A5F` et du HUD (`#agent-hud`).

### PHASE 6 — Validation Pre-Flight Bloquante (< 3s) AVANT Rendu
1. **Exécution du Gatekeeper** :
   ```bash
   python3 preflight_check.py --projet <dossier>
   ```
2. **Règle d'arrêt absolu** :
   - Si un seul des 5 axes échoue (géométrie, typo $< 20\text{px}$, retour orphelin, carte inerte, collision registre ou HUD), corriger immédiatement.
   - **Il est formellement interdit de démarrer `render.py` avant d'avoir obtenu `5/5 axes au vert`.**

### PHASE 7 — Rendu Final 30 FPS, Inspection & Clôture Registre
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
