# AGENT404 Engine Constitution

## Core Principles

### I. Rendu Déterministe Frame-par-Frame (NON-NÉGOCIABLE)
Le moteur vidéo fonctionne exclusivement sur un modèle frame-par-frame hors-ligne. Toute animation doit être une fonction mathématique pure de l'instant temporel $t$ (`window.setTime(t)`). Aucune horloge asynchrone (`requestAnimationFrame`, `Date.now()`, `setInterval`) ni transition CSS temps réel n'est autorisée lors des captures Playwright. Deux rendus successifs d'un même projet en mode déterministe doivent produire des flux d'images décodées strictement identiques (framemd5 identiques, PSNR infini).

### II. Protection Stricte des Fichiers de Référence et Gel
Les productions de référence validées (telles que `studio_perso/video_01`) sont protégées par le champ `"gele": true` dans `project.json`. Le pipeline (`make_video.py`) refuse catégoriquement d'écraser des fichiers existants dans le dossier du projet sans l'option explicite `--forcer` ou l'isolation via `--sortie <dossier>`. Le Golden Master et les manifestes d'intégrité ne sont jamais régénérés sans validation explicite du propriétaire.

### III. Sound Design Procédural et Reproductibilité Acoustique
Le mixage des bruitages procéduraux (`sfx.py` : whoosh feutré, pop organique, micro-clics) doit être 100% reproductible lorsque `rendu_deterministe: true`. La graine aléatoire est dérivée de manière stable via `zlib.crc32` de l'identifiant du projet et injectée dans un générateur NumPy dédié. Deux mixages successifs d'un projet déterministe doivent produire des fichiers WAV identiques octet par octet (empreinte SHA-256 rigoureusement identique).

### IV. Progression Continue et Non-Régression de la Qualité Vidéo (Effet Cliquet)
Chaque nouvelle vidéo (personnelle ou client) doit égaler ou surpasser la précédente sur trois axes mesurables : écriture & rythme (copywriting de rétention), cinétique des animations (spring overshoot) et richesse visuelle. Dans une même vidéo, aucune illustration, composant ou animation ne doit être dupliqué deux fois. Les expressions et poses d'avatar doivent être renouvelées et enrichies pour chaque script, sans recyclage mécanique des poses historiques.

### V. Standard Vertical 9:16 et Conformité Safe-Area
Toute vidéo est encodée au format vertical 1080x1920 à 30.0 FPS (vidéo H.264 / audio AAC). Les éléments graphiques critiques, textes, sous-titres et appels à l'action sont impérativement restreints à la zone centrale de sécurité ($900 \times 1400\text{ px}$), en préservant une marge basse de 280 px pour les éléments d'interface des plateformes (TikTok, Reels, Shorts) et une marge droite de 80 px pour les boutons d'interaction.

## Les 5 Principes Directeurs de Conception (Obligatoires & Transversaux)

Le projet AGENT404 applique rigoureusement à tous ses développements, scripts vidéo et choix d'architecture les cinq concepts fondamentaux suivants :

1. **Concept 1 : Définir le problème précis plutôt qu'une idée vague**  
   *« Tu ne décris plus une idée. Tu définis le problème à résoudre. »*  
   - *Application AGENT404* : Résoudre la douleur exacte (painkiller) des fondateurs de SaaS B2B : leurs fonctionnalités sont puissantes mais techniques, leurs prospects ne lisent pas la documentation et ne regardent pas leurs Looms de 10 minutes. La vidéo programmatique remplace l'écran partagé amateur par une démonstration chirurgicale de 45 à 60 secondes.

2. **Concept 2 : Décrire les gestes et le fonctionnement étape par étape**  
   *« Tu passes d'un concept à un fonctionnement que tu peux vérifier, étape par étape. »*  
   - *Application AGENT404* : Le pipeline est une chaîne séquentielle vérifiable sans effet boîte noire : ingestion audio -> alignement acoustique mot-à-mot Whisper -> mixage sonore procédural NumPy -> rendu DOM frame-par-frame Playwright -> encodage FFmpeg. Chaque scène déclarée dans `project.json` est mesurée et vérifiée à la milliseconde.

3. **Concept 3 : Définir explicitement ce qu'on refuse (Les non-objectifs)**  
   *« Dis aussi ce que tu ne veux pas. La clarté, c'est aussi décider ce qui peut attendre. »*  
   - *Application AGENT404* :
     - **Zéro jargon technique dans les vidéos** : proscription formelle des termes techniques (Python, JavaScript, FFmpeg, Whisper, Faster-Whisper, codebase). La technologie s'exprime uniquement par le résultat (clarté, netteté, rapidité).
     - **Zéro prix dans les vidéos** : aucun chiffre (250 €, 500 €) ni symbole tarifaire à l'oral comme à l'écrit dans les vidéos. Le prix est un levier de clôture réservé aux échanges privés (DM).
     - **Zéro HUD** : suppression définitive et irrévocable de tout bandeau HUD (`#agent-hud`) du projet.
     - **Exclusion commerciale stricte** : refus de prospecter les freelances sans budget, les créateurs IA sans produit et les grosses licornes (Pennylane, Gorgias, Strapi) disposant d'équipes internes.

4. **Concept 4 : Remplacer « ça ne marche pas » par un constat précis mesuré**  
   *« Identifie l'écart entre le résultat attendu et le résultat obtenu. »*  
   - *Application AGENT404* : Tout diagnostic s'appuie sur des métriques concrètes : calcul d'écarts de hash (framemd5), PSNR infini, durée audio exacte (au millième de seconde via ffprobe), luminance OpenCV (> 32 sur zone avatar) et absence stricte de frames vides.

5. **Concept 5 : Des décisions claires avec critères d'acceptation testables**  
   *« Je saurai que ça fonctionne si... Un brief précis ne garantit pas un code fiable : il faut encore le tester. »*  
   - *Application AGENT404* : Toute fonctionnalité ou vidéo est validée par des tests automatisés (`pytest tests/`) obligatoires : 100% au vert avant livraison. Critères techniques d'acceptation : conformité ffprobe (1080x1920, 30 FPS, H.264/AAC), zéro trou ni chevauchement de scène dans `timeline.js`, et zéro doublon d'illustration.

---

## Ciblage Commercial & Positionnement Stratégique Réajusté

Le positionnement d'AGENT404 est clarifié : **Ne pas vendre « du code Python », mais vendre de la clarté visuelle B2B qui remplace la caméra et fait signer des clients.**

| Segment | Qui exactement ? (Exemples qualifiés) | Leur VRAI problème douloureux (Painkiller) | Offre naturelle | Verdict opérationnel |
| :--- | :--- | :--- | :--- | :--- |
| **Cible n° 1 (70 % des efforts)** | **Fondateurs de SaaS B2B & Outils Tech bootstrappés rentables** (Typebot, Piloterr, Breakcold, Pharow, Tally) | Leurs fonctionnalités sont puissantes mais techniques. Leurs prospects ne lisent pas la doc et ne regardent pas leurs Looms de 10 min. Besoin de démos produit de 45s ultra-claires pour convertir sur leur site et sur LinkedIn. | **Pilote 250 €** (3 vidéos) → puis **Studio 500 €/mois** pour chaque nouvelle feature. | **EXCELLENTE CIBLE** (Solvables, comprennent la valeur du design système, décision rapide en direct avec le fondateur). |
| **Cible n° 2 (30 % des efforts)** | **Agences B2B expertes & Organismes Tech** (Digidop, Noqode, Contournement, Ottho) | Ils publient beaucoup à l'écrit (études de cas, méthodes) mais n'ont pas le temps de tourner des vidéos face caméra chaque semaine. | **Studio 500 €/mois** (8 vidéos) à partir de leurs posts écrits ou vocaux WhatsApp. | **TRÈS BONNE CIBLE** pour le revenu récurrent (MRR). |
| **À ÉCARTER (Exclusion stricte)** | **Freelances débutants, créateurs IA sans produit, grosses licornes** (Pennylane, Gorgias, Strapi) | Les petits n'ont pas 250 € ; les licornes ont déjà une équipe motion design interne. | Aucune offre | **PERTE DE TEMPS.** |

---

## Architecture & Stack Technique

- **Frontend Graphique** : HTML5 sémantique, Vanilla CSS (tokens Cyber-Mint et thèmes clients dynamiques), JavaScript natif (zéro framework lourd, zéro node_modules).
- **Moteur de Capture** : Playwright Chromium Headless avec synchronisation totale des polices (`document.fonts.ready`), décodage préalable de toutes les images (`img.decode()`), et recyclage mémoire régulier anti-fuite.
- **Encodage & Assemblage** : FFmpeg natif via pipe image2pipe JPEG qualité 90, profil H.264 CRF 18, preset veryfast, audio AAC 192k.
- **Audio & Transcription** : Faster-Whisper (modèle small, quantifié int8 sur CPU) pour l'alignement acoustique forcé mot-à-mot sans interpolation.

## Governance & Contrôles Qualité

1. **Branche unique** : Branche locale `main` synchronisée avec `origin/main`. Aucune branche parallèle. Poussée normale sans force-push.
2. **Portails de test** : Tous les tests unitaires et d'intégrité (`pytest tests/`) doivent passer à 100% avant toute mise en production.
3. **Propriété exclusive** : Projet détenu et gouverné par Kreesten AGBOTON.

**Version**: 1.2.0 | **Ratified**: 2026-10-17 | **Last Amended**: 2026-10-19
