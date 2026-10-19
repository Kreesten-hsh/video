# RÈGLE ABSOLUE : PROGRESSION CONTINUE ET NON-RÉGRESSION DE LA QUALITÉ VIDÉO
# STANDARD DE CRAFT ET D'EXCELLENCE AGENT404

Date d'effet : Octobre 2026 (révisé le 19 octobre 2026)  
Portée : Tous les projets vidéo (vidéos personnelles studio_perso/ et vidéos clients studio_clients/)  
Gouvernance : Kreesten AGBOTON  
Positionnement : Clarté visuelle B2B qui remplace la caméra et fait signer des clients (Arrêter de vendre « du code Python »).  
Ciblage chirurgical : 70 % des efforts sur les fondateurs de SaaS B2B bootstrappés rentables ; 30 % sur les agences B2B expertes ; exclusion stricte des freelances débutants et des licornes internalisées.

---

## 1. LES 5 CONCEPTS DIRECTEURS DE PRODUCTION VIDÉO

Toute capsule vidéo créée pour AGENT404 ou pour un client applique obligatoirement les 5 concepts suivants :

1. **Concept 1 : Définir le problème précis plutôt qu'une idée vague**  
   *« Tu ne décris plus une idée. Tu définis le problème à résoudre. »*  
   - Le script ne part jamais d'une idée floue (« parlons de notre produit »), mais attaque frontalement la douleur aiguë du prospect : l'abandon des Looms de 10 minutes, la documentation que personne ne lit, ou la perte de leads qualifiés.
2. **Concept 2 : Décrire les gestes et le fonctionnement étape par étape (Show, Don't Tell)**  
   *« Tu passes d'un concept à un fonctionnement que tu peux vérifier, étape par étape. »*  
   - Chaque argument est séquencé en étapes visuelles vérifiables : 1 proposition = 1 scène avec une simulation concrète de l'objet métier (lecteur Loom qui décroche, interface SaaS vivante, grille de distribution 3 canaux).
   - Règle « 1 Mot Prononcé = 1 Action Visuelle » : Pour toute énumération ou liste, chaque élément s'affiche ou s'anime au centième de seconde exact où il est prononcé.
3. **Concept 3 : Définir explicitement ce qu'on refuse (Les non-objectifs & Zéro Recyclage)**  
   *« Dis aussi ce que tu ne veux pas. La clarté, c'est aussi décider ce qui peut attendre. »*  
   - **Refus absolu du jargon technique** : Proscription totale de mots comme Python, FFmpeg, Whisper, codebase dans les scripts et sous-titres vidéos.
   - **Refus absolu des prix** : Zéro montant (250 €, 500 €) ni symbole tarifaire dans les vidéos publiques.
   - **Refus absolu du HUD** : Le bandeau supérieur (#agent-hud) est banni définitivement de l'interface graphique.
   - **Refus absolu du rouge/rose (#FF2A5F)** : Zéro `bg: "alert"` et zéro `bg: "mint"`. Pour les états négatifs ou erreurs, utiliser l'ardoise `#161B22`, bordures `#30363D`, texte `#8B949E` et accents ambre `#F59E0B`.
   - **Refus absolu de l'inter-recyclage** : Interdiction totale de réutiliser dans une nouvelle vidéo un composant visuel, une carte, un texte d'écran ou un terminal provenant d'une vidéo précédente (ex. interdiction de reprendre la carte `00:21.466 ms`, le spectre `vocal1.m4a` ou la barre `COMPILATION FFmpeg` de la Vidéo 1 dans la Vidéo 2).
   - **Refus de la duplication interne** : Zéro composant ou animation identique dupliqué dans une même vidéo.
4. **Concept 4 : Remplacer « ça ne marche pas » par un constat précis mesuré**  
   *« Identifie l'écart entre le résultat attendu et le résultat obtenu. »*  
   - Tout écart est audité avec des valeurs mesurées : durée exacte de transition, écart de luminance de l'avatar (> 32 sur zone sticker via OpenCV), mesure de marge safe-area (> 280 px en bas, > 80 px à droite).
5. **Concept 5 : Des décisions claires avec critères d'acceptation testables**  
   *« Je saurai que ça fonctionne si... Un brief précis ne garantit pas un code fiable : il faut encore le tester. »*  
   - La vidéo est acceptée uniquement si la suite de tests automatisés dédiée (`tests/test_video0X_spec.py`) valide 100 % des critères : 0 trou temporel dans `timeline.js`, conformité audio/vidéo stricte `ffprobe`, présence vérifiée de chaque sticker, unicité SHA-256 de chaque avatar.

---

## 2. PRINCIPE CARDINAL : LA LOI D'EFFET CLIQUET & D'EXCELLENCE PROGRESSIVE (N+1 > N)

Chaque nouvelle vidéo produite sur le moteur AGENT404 (vidéo $N+1$) doit impérativement surpasser la vidéo précédente (vidéo $N$) sur l'ensemble des axes d'évaluation. Aucune régression n'est tolérée :

1. **Effet Cliquet Systémique & Tests Bloquants** :
   - Toute anomalie constatée et corrigée sur une vidéo $N$ (ex. retours à la ligne orphelins sur KPIs, listes multi-étapes figées, textes trop petits, éléments HUD parasites) devient immédiatement et irrévocablement une règle d'architecture et un test unitaire bloquant (`unittest` + `preflight_check.py`) pour toutes les vidéos $N+1$.
2. **Unicité Créative Absolue Inter-Vidéos & Intra-Vidéo** :
   - **Interdiction de recyclage inter-vidéos** : Une vidéo $N+1$ ne doit réutiliser aucun identifiant ni gabarit d'illustration d'une vidéo antérieure (validé automatiquement contre le registre `registry/video_memory.json`).
   - **Interdiction de duplication intra-vidéo** : Zéro composant visuel, carte ou animation réutilisé deux fois au sein du même clip (sauf intention narrative explicite).
3. **Sélection Sémantique des Avatars (Zéro Forçage Mécanique)** :
   - Le choix des poses et stickers d'avatars découle à 100 % du sens littéral et de l'émotion vocale de la réplique prononcée.
   - Il n'existe aucune obligation de réutiliser tout l'éventail des poses existantes d'une vidéo à l'autre : la pertinence sémantique prime sur la variété forcée.
4. **Synchronisation Millimétrée des Énumérations & Listes** :
   - Pour toute liste, carte multi-canaux ou énumération, la cinétique visuelle est strictement asservie au millième de seconde aux timestamps des mots audio prononcés. Chaque carte s'active ou s'illumine au moment précis où le mot clé correspondant est audible.
5. **Occupation Obligatoire de la Safe Zone 9:16 & Standards Typographiques** :
   - **Gabarit des cartes centrales** : Largeur minimale absolue de `840px` (plage cible `880px–940px`), hauteur minimale de `520px` (plage cible `620px–880px`) pour éliminer tout vide vertical excessif sur écran 1080×1920.
   - **Lisibilité mobile garantie** : Aucun texte visible dans `#scene-container` ne doit avoir une taille calculée inférieure à `18px` (seuil de conception recommandé : `22px` minimum pour le corps de texte, `34px-56px` pour les titres et KPIs).
   - **Anti-Orphelin & No-Wrap** : `white-space: nowrap` obligatoire sur tous les badges `[ ... ]`, KPIs, résolutions géantes et étiquettes courtes, avec vérification géométrique `scrollWidth <= clientWidth + 2`.
6. **Thématisation 100 % Variables CSS & Proscription des Couleurs Bannies** :
   - 100 % des couleurs proviennent des variables sémantiques déclarées dans `:root` (`--bg-canvas`, `--surface-card`, `--accent-primary`, `--accent-warning`, etc.) pour autoriser une thématisation instantanée sur les projets clients `studio_clients/`.
   - Bannissement absolu et perpétuel du rose/rouge `#FF2A5F` et du HUD supérieur (`#agent-hud`).

---

## 3. LES 4 PILIERS D'AMÉLIORATION CONTINUE

### A. Écriture & Rythme Narratif (Copywriting de Rétention)
- **Hook immédiat ($t \le 1{,}2\text{ s}$)** : Accroche textuelle percutante affichée dès l'image 0 sans fondu au noir, appuyée par une rupture visuelle franche à 1,2s (punch-in zoom ou pop sonore mat).
- **Zéro temps mort** : Suppression chirurgicale de toute hésitation, mot parasite ou silence résiduel ($> 0{,}2\text{ s}$).
- **Clarté cognitive** : Une seule idée majeure par vidéo, développée en arguments visuels distincts conduisant à un appel à l'action sans ambiguïté.

### B. Variété et Richesse Visuelle Intraclip (Règle de Non-Répétition)
- **Interdiction de duplication interne** : Au sein d'une même vidéo, il est formellement interdit d'utiliser deux fois la même illustration, icône, composant ou animation strictement identique, sauf intention narrative explicite.
- **Rupture visuelle cadencée** : Le spectateur doit faire face à un événement visuel renouvelé (changement de composant DOM, variation d'angle, zoom progressif, décor dynamique) toutes les 1,8 à 2,6 secondes.

### C. Singularité des Avatars et Bibliothèque d'Expressions
- **Proscription du clonage mécanique & intégrité SHA-256** : Chaque sticker dans `assets/avatars/` doit avoir une empreinte SHA-256 unique. Aucun faux doublon sous des noms différents n'est toléré.
- **Cadrage buste complet obligatoire** : Bannissement définitif des têtes coupées sans épaules ni buste flottant au milieu du cadre (ex. ancien `mini.png` ou `skeptic.png`). Tout avatar plein écran doit être cadré en buste complet avec épaules, veste et cravate.
- **Pertinence sémantique & émotionnelle** : L'avatar ne peut être affiché que si son expression et sa gestuelle collent à 100 % au sens de la réplique (ex. `stop` sur refus, `idea` sur solution, `mic` sur vocal, `pointing` sur appel à l'action). En cas d'inadéquation, privilégier une animation UI sur-mesure ou un médaillon PiP.
- **Enrichissement permanent** : Si une émotion nécessaire n'existe pas dans `assets/avatars/`, de nouvelles prises brutes doivent être générées/capturées sur fond neutre et intégrées au moteur via `build_stickers.py`.

### D. Cinétique Déterministe et Standards Graphiques
- **Mouvements physiques vivants** : Toute apparition d'élément doit exploiter une courbe d'amortissement dynamique (spring overshoot) plutôt qu'un déplacement linéaire rigide.
- **Typographie et Safe-Area 9:16** :
  - Respect strict de la zone de sécurité centrale ($900 \times 1400\text{ px}$).
  - Marge basse de 280 px exempte de tout texte critique ou bouton (réservée aux éléments d'interface des plateformes TikTok, Reels et Shorts).
  - Lisibilité absolue à l'écran : contrastes élevés (fond sombre `#0D1117`, texte blanc `#FFFFFF` ou vert menthe `#00F5A0`, bordures néo-brutalistes franches, zéro `#FF2A5F`).

---

## 4. SCÉNARIOS D'APPLICATION ET GESTION DES CAS LIMITES

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

## 5. GRILLE DE VALIDATION AVANT EXPORT DÉFINITIF

Avant d'approuver une vidéo pour diffusion ou livraison client, valider les 5 points de contrôle suivants :
1. [ ] **Supériorité relative** : Cette vidéo surpasse-t-elle la précédente en écriture, rythme ou finesse d'animation ?
2. [ ] **Non-répétition interne** : Chaque scène apporte-t-elle une composition ou un composant nouveau ?
3. [ ] **Spécificité des expressions** : Les poses d'avatar reflètent-elles fidèlement l'émotion exacte de chaque réplique ?
4. [ ] **Conformité Safe-Area** : Tous les titres, sous-titres et appels à l'action sont-ils protégés des masques d'interface des réseaux sociaux ?
5. [ ] **Validation technique** : Le rendu s'exécute-t-il sans frame vide, sans désynchronisation audio et avec conformité `ffprobe` (1080x1920, h264/aac, 30 fps) ?
