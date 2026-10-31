# RÈGLE ABSOLUE : PROGRESSION CONTINUE ET NON-RÉGRESSION DE LA QUALITÉ VIDÉO
# STANDARD DE CRAFT ET D'EXCELLENCE AGENT404

Portée : Tous projets vidéo (`studio_perso/` et `studio_clients/`)  
Gouvernance : Kreesten AGBOTON  
Positionnement : Production de vidéos courtes pour le personal branding des experts B2B sur LinkedIn. Transformation des publications LinkedIn et notes vocales des fondateurs d'agences B2B et consultants en vidéos animées professionnelles, sans tournage ni montage (« 8 vidéos par mois. Votre expertise, notre production. »).  
Ciblage (Filtre Exigeant 5 Critères) : (1) Fondateurs de petites agences B2B (automatisation, développement web, CRM, no-code, marketing spécialisé) et (2) Consultants B2B indépendants. Critères cumulatifs : vendre réellement un service ou accompagnement, activité commerciale identifiable, contenu et expertise suffisants, utilisation active de LinkedIn (3 à 5 posts/semaine), absence de production vidéo régulière satisfaisante.  
Styles de Production (1 seul service) : Mascotte (pédagogique et accessible), Éditorial (personal branding sobre et autorité), Démonstration (workflows, systèmes et études de cas).

---

## 1. LES 5 CONCEPTS DIRECTEURS DE PRODUCTION VIDÉO

Toute capsule vidéo applique obligatoirement les 5 concepts suivants :

1. **Définir le problème précis plutôt qu'une idée vague**  
   Le script attaque frontalement la douleur aiguë du prospect (corvée du tournage, Looms abandonnés, saturation de l'écrit seul). Il extrait le joyau narratif de tout matériau brut (vocal 2 min, post LinkedIn, doc, schéma Make/n8n, cas client).
2. **Décrire les gestes et le fonctionnement étape par étape (Show, Don't Tell)**  
   Chaque argument est séquencé en étapes visuelles vérifiables : 1 proposition = 1 scène avec simulation concrète de l'objet métier. Règle « 1 Mot Prononcé = 1 Action Visuelle » : toute énumération s'anime au centième de seconde exact où le mot est prononcé.
3. **Définir explicitement ce qu'on refuse (Non-objectifs & Zéro Recyclage)**  
   - **Zéro jargon technique** : Proscription de Python, FFmpeg, Whisper, codebase dans les scripts et sous-titres.
   - **Zéro prix dans les vidéos** : Aucun montant (150 €, 200 €, 450 €, 750 €) ni symbole tarifaire dans les vidéos publiques.
   - **Zéro HUD** : Le bandeau supérieur (`#agent-hud`) est banni définitivement.
   - **Zéro rouge/rose (#FF2A5F)** : Zéro `bg: "alert"` et zéro `bg: "mint"`. Rendu exclusif sur la palette Obsidian Flame.
   - **Zéro inter-recyclage** : Interdiction totale de réutiliser un composant, une carte, un texte d'écran ou un terminal d'une vidéo antérieure (ex. carte `00:21.466 ms`, spectre `vocal1.m4a`, barre `COMPILATION FFmpeg` de la Vidéo 1 bannis des vidéos ultérieures).
   - **Zéro duplication interne** : Aucun composant ou animation identique dupliqué au sein d'un même clip.
4. **Remplacer « ça ne marche pas » par un constat précis mesuré**  
   Tout écart est audité avec des valeurs métriques précises : durée de transition, écart de luminance de l'avatar (> 32 sur zone sticker via OpenCV), marges safe-area (> 280px en bas, > 80px à droite).
5. **Décisions claires avec critères d'acceptation testables**  
   La vidéo est acceptée uniquement si la suite de tests automatisés dédiée valide 100 % des critères : 0 trou temporel dans `timeline.js`, conformité audio/vidéo stricte `ffprobe`, présence de chaque sticker, unicité binaire SHA-256 de chaque avatar.

---

## 2. PRINCIPE CARDINAL : EFFET CLIQUET & EXCELLENCE PROGRESSIVE (N+1 > N)

Chaque nouvelle vidéo ($N+1$) doit impérativement surpasser la précédente ($N$). Aucune régression n'est tolérée :

1. **Effet Cliquet & Tests Bloquants** :  
   Toute anomalie corrigée sur la vidéo $N$ (retours à la ligne orphelins sur KPIs, listes figées, textes trop petits, éléments HUD) devient immédiatement une règle d'architecture et un test bloquant (`unittest` + `preflight_check.py`) pour les vidéos $N+1$.
2. **Unicité Créative Absolue** :  
   - **Inter-vidéos** : $N+1$ n'utilise aucun identifiant ni gabarit d'illustration antérieur (validé contre `registry/video_memory.json`).
   - **Intra-vidéo** : Zéro composant visuel, carte ou animation réutilisé deux fois dans le même clip.
3. **Sélection Sémantique des Avatars** :  
   Le choix des poses découle à 100 % du sens littéral et de l'émotion vocale de la réplique. Aucune obligation mécanique d'utiliser toutes les poses : la pertinence prime sur la variété forcée.
4. **Synchronisation Millimétrée des Listes** :  
   Pour toute liste ou carte multi-canaux, chaque élément s'active ou s'illumine au moment précis où le mot clé correspondant est audible.
5. **Liberté Scénographique 9:16 & Interdiction du Conteneur Unique Répétitif** :  
   - **Interdiction formelle du gabarit unique répétitif** : BANNISSEMENT STRICT du template `<div class="card"><div class="header">TITRE + BADGE</div>...</div>` répété d'une scène à l'autre.
   - **Compositions Débridées et Variées** : Autorisation et exigence de compositions variées adaptées au rythme narratif :
     - *Textes Chocs Plein Écran* sans boîte englobante (ex: `ZÉRO VIDÉO`, `CE N'EST PAS / TON CONTENU`, `POURQUOI ?`).
     - *Carrés de Numérotation Géants* (`[ÉTAPE 1]`, `[ÉTAPE 2]`, `[ÉTAPE 3]`) seuls au centre.
     - *Post-its et Tuiles flottantes indépendantes* volant en diagonale en quinconce (style lymphe 0:01 et 0:05).
     - *Schémas à flèches animées* (`[BLOC A] ━━▶ [BLOC B]`) posés directement sur le fond sans boîte englobante (style @ledevultime 0:58, 1:17).
   - **Lisibilité mobile** : Aucun texte calculé sous `18px` dans `#scene-container` (recommandé : corps `22px à 28px`, titres/KPIs `34px à 56px`, textes chocs `72px à 120px`).
   - **Anti-Orphelin & No-Wrap** : `white-space: nowrap` obligatoire sur badges `[ ... ]`, KPIs, résolutions géantes et étiquettes courtes, vérifié géométriquement par `scrollWidth <= clientWidth + 2`.
6. **Thématisation 100 % Variables CSS** :  
   100 % des couleurs proviennent des variables de `:root` (`--bg-canvas`, `--surface-card`, `--accent-primary`, etc.) pour autoriser la thématisation instantanée sur les projets clients. 0 hex hardcodé hors `:root`.

---

## 3. LES 4 PILIERS D'AMÉLIORATION CONTINUE

### A. Écriture & Rythme Narratif (Copywriting de Rétention)
- **Hook immédiat ($t \le 1{,}2\text{ s}$)** : Accroche textuelle dès l'image 0 sans fondu au noir, appuyée par une rupture visuelle franche à 1,2s (punch-in zoom ou pop sonore mat).
- **Zéro temps mort** : Suppression de toute hésitation ou silence résiduel ($> 0{,}2\text{ s}$).
- **Clarté cognitive** : 1 seule idée majeure par vidéo, développée en arguments visuels distincts jusqu'au CTA final.

### B. Variété et Richesse Visuelle Intraclip
- **Règle de non-répétition** : Interdiction d'utiliser deux fois la même illustration ou animation identique dans une même vidéo.
- **Rupture visuelle cadencée** : Événement visuel renouvelé (composant DOM, angle, zoom, décor) toutes les 1,8 à 2,6 secondes.

### C. Singularité des Avatars et Bibliothèque d'Expressions
- **Unicité SHA-256** : Chaque sticker dans `assets/avatars/` possède un hash SHA-256 unique. Zéro faux doublon binaire.
- **Cadrage buste complet** : Proscription définitive des têtes flottantes sans épaules. Tout avatar plein écran est cadré en buste complet avec épaules, veste et cravate.
- **Pertinence sémantique** : L'avatar ne s'affiche que si son expression colle au sens de la réplique (`stop` sur refus, `idea` sur solution, `mic` sur vocal, `pointing` sur CTA).
- **Enrichissement permanent** : Si une émotion requise manque, générer de nouvelles prises sur fond neutre et les détourer via `build_stickers.py`.

### D. Cinétique Déterministe et Standards Graphiques
- **Mouvements physiques** : Exploiter des courbes dynamiques (spring overshoot) plutôt que des déplacements linéaires rigides.
- **Safe-Area 9:16** : Zone de sécurité centrale ($900 \times 1400\text{ px}$). Marge basse de 280px à 380px sans texte critique (réservée à l'UI TikTok/Reels/Shorts).
- **Contraste maximal** : Thème Obsidian Flame (fond beige uni #F5F2EB, encre #111111, accent orange flamme #FF4F18, pastels jaune/bleu/vert, bordures néo-brutalistes franches, zéro fond sombre ni grille, zéro `#FF2A5F`).

---

## 4. SCÉNARIOS D'APPLICATION ET DÉTERMINISME

### Vidéos Clients (`studio_clients/`)
Adaptation stricte à la charte et aux avatars du client : déclinaison de sa palette officielle en conservant le contraste néo-brutaliste. Interdiction de copier-coller un gabarit d'un autre client sans refonte scénographique.

### Vidéos Personnelles du Fondateur (`studio_perso/`)
Banc d'essai et vitrine technologique maximale : introduction régulière de nouveaux composants DOM (`video.js`) et expérimentations visuelles. Toute innovation validée devient un standard disponible pour les clients.

### Déterminisme Strict
Toute animation est une fonction pure de $t$ dans `window.setTime(t)`. Aucune transition CSS temps réel susceptible de désynchroniser la capture Playwright headless. Tous les tests de non-régression (`test_reproducibility.py`, `test_verify_avatars.py`) doivent être verts.

---

## 5. GRILLE DE VALIDATION AVANT EXPORT DÉFINITIF

Avant d'approuver une vidéo pour diffusion ou livraison client :
1. [ ] **Supériorité relative** : Cette vidéo surpasse-t-elle la précédente en écriture, rythme ou finesse d'animation ?
2. [ ] **Non-répétition interne** : Chaque scène apporte-t-elle une composition ou un composant nouveau ?
3. [ ] **Spécificité des expressions** : Les poses d'avatar reflètent-elles fidèlement l'émotion exacte de chaque réplique ?
4. [ ] **Conformité Safe-Area** : Tous les titres, sous-titres et CTA sont-ils protégés des masques d'interface (marge basse $\ge 280\text{px}$) ?
5. [ ] **Validation technique** : Rendu sans frame vide, sans désynchronisation audio et conforme `ffprobe` (1080x1920, h264/aac, 30 fps).
