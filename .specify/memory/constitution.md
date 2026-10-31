# AGENT404 Engine Constitution

## Core Principles

### I. Rendu Déterministe Frame-par-Frame (NON-NÉGOCIABLE)
Le moteur vidéo fonctionne exclusivement sur un modèle frame-par-frame hors-ligne. Toute animation doit être une fonction mathématique pure de l'instant temporel $t$ (`window.setTime(t)`). Aucune horloge asynchrone (`requestAnimationFrame`, `Date.now()`, `setInterval`) ni transition CSS temps réel n'est autorisée lors des captures Playwright. Deux rendus successifs d'un même projet en mode déterministe doivent produire des flux d'images décodées strictement identiques (framemd5 identiques, PSNR infini).

### II. Protection Stricte des Fichiers de Référence et Gel
Les productions de référence validées (`studio_perso/video_01_decouverte` et `studio_perso/video_03`) sont protégées par le champ `"gele": true` dans `project.json`. Le pipeline (`make_video.py`) refuse catégoriquement d'écraser des fichiers existants dans le dossier du projet sans l'option explicite `--forcer` ou l'isolation via `--sortie <dossier>`. Le Golden Master et les manifestes d'intégrité ne sont jamais régénérés sans validation explicite du propriétaire.

### III. Sound Design Procédural et Reproductibilité Acoustique
Le mixage des bruitages procéduraux (`sfx.py` : whoosh feutré, pop organique, micro-clics) doit être 100 % reproductible lorsque `rendu_deterministe: true`. La graine aléatoire est dérivée de manière stable via `zlib.crc32` de l'identifiant du projet et injectée dans un générateur NumPy dédié. Deux mixages successifs d'un projet déterministe doivent produire des fichiers WAV identiques octet par octet (empreinte SHA-256 rigoureusement identique).

### IV. Progression Continue et Non-Régression de la Qualité Vidéo (Effet Cliquet)
Chaque nouvelle vidéo (personnelle ou client) doit égaler ou surpasser la précédente sur trois axes mesurables : écriture & rythme (copywriting de rétention), cinétique des animations (spring overshoot) et richesse visuelle. Dans une même vidéo, aucune illustration, composant ou animation ne doit être dupliqué deux fois. Les expressions et poses d'avatar doivent être utilisées avec pertinence selon le style retenu (Mascotte, Éditorial ou Démonstration).

### V. Standard Vertical 9:16 et Conformité Safe-Area
Toute vidéo est encodée au format vertical 1080x1920 à 30.0 FPS (vidéo H.264 / audio AAC). Les éléments graphiques critiques, textes, sous-titres et appels à l'action sont impérativement restreints à la zone centrale de sécurité ($900 \times 1400\text{ px}$), en préservant une marge basse de 280 px pour les éléments d'interface des plateformes (TikTok, Reels, Shorts) et une marge droite de 80 px pour les boutons d'interaction.

---

## Les 5 Principes Directeurs de Conception (Obligatoires & Transversaux)

Le projet AGENT404 applique rigoureusement à tous ses développements, scripts vidéo et choix d'architecture les cinq concepts fondamentaux suivants :

1. **Concept 1 : Définir le problème précis plutôt qu'une idée vague**  
   *« Tu ne décris plus une idée. Tu définis le problème à résoudre. »*  
   - *Application AGENT404* : Résoudre la douleur exacte des fondateurs d'agences B2B et consultants indépendants qui développent leur personal branding sur LinkedIn : ils publient à l'écrit et possèdent l'expertise, mais produisent peu de vidéos faute de temps pour tourner et monter. Le studio transforme leurs publications LinkedIn et notes vocales en vidéos animées professionnelles, sans tournage ni montage.

2. **Concept 2 : Décrire les gestes et le fonctionnement étape par étape**  
   *« Tu passes d'un concept à un fonctionnement que tu peux vérifier, étape par étape. »*  
   - *Application AGENT404* : Le pipeline est une chaîne séquentielle vérifiable sans effet boîte noire : ingestion agnostique -> sélection de l'idée et structuration du script -> alignement acoustique mot-à-mot Whisper -> mixage sonore procédural NumPy -> rendu DOM frame-par-frame Playwright -> encodage FFmpeg. Chaque scène déclarée dans `project.json` est mesurée et vérifiée à la milliseconde.

3. **Concept 3 : Définir explicitement ce qu'on refuse (Les non-objectifs)**  
   *« Dis aussi ce que tu ne veux pas. La clarté, c'est aussi décider ce qui peut attendre. »*  
   - *Application AGENT404* :
     - **Zéro jargon technique dans les vidéos** : proscription formelle des termes techniques (Python, JavaScript, FFmpeg, Whisper, Faster-Whisper, codebase).
     - **Zéro prix dans les vidéos** : aucun chiffre (150, 200, 450, 750) ni symbole tarifaire à l'oral comme à l'écrit dans les vidéos publiques.
     - **Zéro HUD** : suppression définitive et irrévocable de tout bandeau HUD (`#agent-hud`) du projet.
     - **Zéro promesse de performance commerciale non maîtrisée** : nous promettons la régularité, le gain de temps et la qualité de production, jamais un nombre garanti de vues ou de ventes.
     - **Exclusion commerciale stricte** : refus des prospects sans activité commerciale réelle, des freelances sans budget et des grandes entreprises disposant d'équipes vidéo internes.

4. **Concept 4 : Remplacer « ça ne marche pas » par un constat précis mesuré**  
   *« Identifie l'écart entre le résultat attendu et le résultat obtenu. »*  
   - *Application AGENT404* : Tout diagnostic technique s'appuie sur des métriques concrètes (framemd5, PSNR infini, durée ffprobe, luminance OpenCV > 32) et tout diagnostic commercial s'appuie sur le suivi réel (conversations, propositions, paiements, réachats).

5. **Concept 5 : Des décisions claires avec critères d'acceptation testables**  
   *« Je saurai que ça fonctionne si... Un brief précis ne garantit pas un code fiable : il faut encore le tester. »*  
   - *Application AGENT404* : Toute fonctionnalité ou vidéo est validée par des tests automatisés (`python3 -m unittest discover -s tests -v`) obligatoires : 100 % au vert avant livraison.

---

## Décisions Actives du Fondateur (Stratégie Verrouillée 30 Jours)

1. **Positionnement Officiel** :
   - Production de vidéos courtes pour le personal branding des experts B2B sur LinkedIn (fondateurs de petites agences B2B et consultants B2B indépendants).
   - Le personal branding est le bénéfice commercial ; la production vidéo est le service vendu ; AGENT404 reste l'infrastructure interne.
2. **Trois Styles de Production (1 seul service)** :
   - **Mascotte** : Contenu pédagogique, dynamique et accessible.
   - **Éditorial** : Personal branding sobre, expertise et autorité.
   - **Démonstration** : Workflows, logiciels, systèmes et études de cas.
3. **Grille Tarifaire Expérimentale** :
   - **Ancre de référence** : 200 € par vidéo hors abonnement.
   - **Pilote (Test Découverte)** : 150 € (1 vidéo, 48h à 72h ouvrées, 100 % déductible du 1er mois d'abonnement sous 7 jours).
   - **Starter** : 450 €/mois (4 vidéos par mois, 1 par semaine).
   - **Growth (Abonnement Studio)** : 750 €/mois (8 vidéos par mois, 2 par semaine).
4. **Montants Interdits en Vidéo Publique** :
   - 150, 200, 450, 750 (aucun prix ni délai dit ou affiché dans une vidéo publique).
5. **Pérennité des Actifs et Gel de Développement (30 Jours)** :
   - Aucun nouveau positionnement, aucun développement majeur du moteur, aucune nouvelle identité visuelle avant les premières ventes.
   - Conservation des deux vidéos `studio_perso/video_01_decouverte` et `studio_perso/video_03` comme démonstrations officielles.
6. **Thème Visuel Officiel** :
   - Thème Obsidian Flame : fond beige uni #F5F2EB, encre #111111, accent orange flamme #FF4F18, pastels jaune #FEF08A, bleu #BFDBFE et vert #A7F3D0. Aucun fond sombre, aucune grille, zéro `#FF2A5F`.

---

## Architecture & Stack Technique

- **Frontend Graphique** : HTML5 sémantique, Vanilla CSS (thème Obsidian Flame et thèmes clients dynamiques), JavaScript natif (zéro framework lourd, zéro node_modules). Moteur multi-tenant partagé à la racine (`index.html`, `style.css`, `video.js`).
- **Moteur de Capture** : Playwright Chromium Headless avec synchronisation totale des polices (`document.fonts.ready`), décodage préalable de toutes les images (`img.decode()`), et recyclage mémoire régulier anti-fuite.
- **Encodage & Assemblage** : FFmpeg natif via pipe image2pipe JPEG qualité 90, profil H.264 CRF 18, preset veryfast, audio AAC 192k.
- **Audio & Transcription** : Faster-Whisper (modèle small, quantifié int8 sur CPU) pour l'alignement acoustique forcé mot-à-mot sans interpolation.

## Governance & Contrôles Qualité

1. **Branche unique de travail** : Branche `feat/obsidian-flame` lors des développements d'harmonisation.
2. **Portails de test** : Tous les tests unitaires et d'intégrité (`python3 -m unittest discover -s tests -v`) doivent passer à 100 % avant toute mise en production.
3. **Propriété exclusive** : Projet détenu et gouverné par Kreesten AGBOTON.

**Version**: 1.5.0 | **Ratified**: 2026-10-17 | **Last Amended**: 2026-10-30 (Verrouillage Stratégique 30 Jours)
