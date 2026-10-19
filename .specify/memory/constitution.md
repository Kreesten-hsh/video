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

## Architecture & Stack Technique

- **Frontend Graphique** : HTML5 sémantique, Vanilla CSS (tokens Cyber-Mint), JavaScript natif (zéro framework lourd, zéro node_modules).
- **Moteur de Capture** : Playwright Chromium Headless avec synchronisation totale des polices (`document.fonts.ready`), décodage préalable de toutes les images (`img.decode()`), et recyclage mémoire régulier anti-fuite.
- **Encodage & Assemblage** : FFmpeg natif via pipe image2pipe JPEG qualité 90, profil H.264 CRF 18, preset veryfast, audio AAC 192k.
- **Audio & Transcription** : Faster-Whisper (modèle small, quantifié int8 sur CPU) pour l'alignement acoustique forcé mot-à-mot sans interpolation.

## Governance & Contrôles Qualité

1. **Branche unique** : Branche locale `main` synchronisée avec `origin/main`. Aucune branche parallèle. Poussée normale sans force-push.
2. **Portails de test** : Tous les tests unitaires et d'intégrité (`python3 -m unittest -v`) doivent passer à 100% avant toute mise en production.
3. **Propriété exclusive** : Projet détenu et gouverné par Kreesten AGBOTON.

**Version**: 1.1.0 | **Ratified**: 2026-10-17 | **Last Amended**: 2026-10-19
