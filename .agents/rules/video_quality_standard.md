# RÈGLE ABSOLUE : PROGRESSION CONTINUE ET NON-RÉGRESSION DE LA QUALITÉ VIDÉO
# STANDARD DE CRAFT ET D'EXCELLENCE AGENT404

Date d'effet : Octobre 2026  
Portée : Tous les projets vidéo (vidéos personnelles studio_perso/ et vidéos clients studio_clients/)  
Gouvernance : Kreesten AGBOTON  

---

## 1. PRINCIPE CARDINAL : L'EFFET CLIQUET (ZERO REGRESSION)

Chaque nouvelle vidéo produite sur le moteur AGENT404 (vidéo $N+1$) doit impérativement être supérieure ou égale à la vidéo précédente (vidéo $N$) sur l'ensemble des axes d'évaluation. Aucune régression n'est autorisée :
- Ni dans la qualité de l'écriture narrative et du sound design.
- Ni dans l'impact visuel, la cinétique et la fluidité des animations DOM.
- Ni dans la stabilité, le déterminisme et la couverture de tests du code source.

Tout ajout ou modification de vidéo doit hisser le niveau global du studio sans jamais abaisser les exigences de rendu acquises.

---

## 2. LES 4 PILIERS D'AMÉLIORATION CONTINUE

### A. Écriture & Rythme Narratif (Copywriting de Rétention)
- **Hook immédiat ($t \le 1{,}2\text{ s}$)** : Accroche textuelle percutante affichée dès l'image 0 sans fondu au noir, appuyée par une rupture visuelle franche à 1,2s (punch-in zoom ou pop sonore mat).
- **Zéro temps mort** : Suppression chirurgicale de toute hésitation, mot parasite ou silence résiduel ($> 0{,}2\text{ s}$).
- **Clarté cognitive** : Une seule idée majeure par vidéo, développée en arguments visuels distincts conduisant à un appel à l'action sans ambiguïté.

### B. Variété et Richesse Visuelle Intraclip (Règle de Non-Répétition)
- **Interdiction de duplication interne** : Au sein d'une même vidéo, il est formellement interdit d'utiliser deux fois la même illustration, icône, composant ou animation strictement identique, sauf intention narrative explicite (ex: fermeture de boucle finale / *sentence loop*).
- **Rupture visuelle cadencée** : Le spectateur doit faire face à un événement visuel renouvelé (changement de composant DOM, variation d'angle, zoom progressif, décor dynamique) toutes les 1,8 à 2,6 secondes.

### C. Singularité des Avatars et Bibliothèque d'Expressions
- **Proscription du clonage mécanique** : Une vidéo ne doit pas se contenter de réutiliser indéfiniment les 3 mêmes poses historiques (`stop`, `pointing`, `happy`) au risque d'uniformiser toutes les productions du studio.
- **Incarnation sur-mesure** : Chaque script requiert un casting d'expressions faciales et de postures corporelles spécifiquement adaptées à ses émotions (doute, ironie, démonstration technique, rejet, satisfaction, complicité).
- **Enrichissement permanent** : Si une émotion nécessaire n'existe pas dans `assets/avatars/`, de nouvelles prises brutes doivent être capturées sur fond neutre et intégrées au moteur via `build_stickers.py`.

### D. Cinétique Déterministe et Standards Graphiques
- **Mouvements physiques vivants** : Toute apparition d'élément doit exploiter une courbe d'amortissement dynamique (spring overshoot) plutôt qu'un déplacement linéaire rigide.
- **Typographie et Safe-Area 9:16** :
  - Respect strict de la zone de sécurité centrale ($900 \times 1400\text{ px}$).
  - Marge basse de 280 px exempte de tout texte critique ou bouton (réservée aux éléments d'interface des plateformes TikTok, Reels et Shorts).
  - Lisibilité absolue à l'écran : contrastes élevés (fond sombre `#0D1117`, texte blanc `#FFFFFF` ou vert menthe `#00F5A0`, bordures néo-brutalistes franches).

---

## 3. SCÉNARIOS D'APPLICATION ET GESTION DES CAS LIMITES

### Scénario 1 : Vidéos Clients (`studio_clients/`)
- La règle s'applique avec adaptation stricte à la charte et à la personnalité du client :
  - Utilisation des avatars et photos détourées du client ou de ses intervenants.
  - Déclinaison de sa palette de couleurs officielle tout en maintenant le niveau de contraste et de dynamisme néo-brutaliste.
  - Interdiction de copier-coller un gabarit d'un autre client sans personnalisation poussée de la scénographie.

### Scénario 2 : Vidéos Personnelles du Fondateur (`studio_perso/`)
- Servent de banc d'essai et de vitrine technologique maximale :
  - Doivent introduire régulièrement de nouveaux composants DOM (`video.js`) et de nouvelles expérimentations visuelles (morphing, graphiques d'architecture, intégrations de code terminal).
  - Toute innovation visuelle validée sur une vidéo personnelle devient un standard disponible pour les offres clients.

### Scénario 3 : Contraintes Techniques et Déterminisme
- L'ambition visuelle ne doit jamais compromettre l'intégrité technique :
  - Toute animation doit rester 100% déterministe (pilotée analytiquement par $t$ dans `window.setTime(t)`).
  - Aucune transition CSS temps réel susceptible de créer des désynchronisations en capture Playwright headless.
  - Tous les tests de non-régression (`tests/test_reproducibility.py`, `tests/test_verify_avatars.py`, golden master) doivent rester strictement au vert.

---

## 4. GRILLE DE VALIDATION AVANT EXPORT DÉFINITIF

Avant d'approuver une vidéo pour diffusion ou livraison client, valider les 5 points de contrôle suivants :
1. [ ] **Supériorité relative** : Cette vidéo surpasse-t-elle la précédente en écriture, rythme ou finesse d'animation ?
2. [ ] **Non-répétition interne** : Chaque scène apporte-t-elle une composition ou un composant nouveau ?
3. [ ] **Spécificité des expressions** : Les poses d'avatar reflètent-elles fidèlement l'émotion exacte de chaque réplique ?
4. [ ] **Conformité Safe-Area** : Tous les titres, sous-titres et appels à l'action sont-ils protégés des masques d'interface des réseaux sociaux ?
5. [ ] **Validation technique** : Le rendu s'exécute-t-il sans frame vide, sans désynchronisation audio et avec conformité `ffprobe` (1080x1920, h264/aac, 30 fps) ?
