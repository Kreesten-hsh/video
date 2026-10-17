# AGENT404 · PLAN DE PRODUCTION DE LA VITRINE SHOWCASE (3 STYLES)
**Objectif :** Disposer de 3 preuves visuelles irréfutables et différenciées avant tout démarchage commercial.  
**Règle d'or :** Ne jamais annoncer à un prospect qu'une démonstration existe tant qu'elle n'a pas été compilée en MP4 et contrôlée par `ffprobe`. Ne pas altérer la Golden Master existante (`tests/test_video01_golden_master.py`).

---

## 1. Diagnostic du moteur actuel & Capital technique existant

L'audit du dépôt confirme que le moteur AGENT404 dispose d'une base robuste et déterministe :
- **Pipeline d'encodage :** Python 3.12 + Playwright Headless + FFmpeg (`libx264`, `yuv420p`, crf 18, 30 FPS).
- **Architecture d'affichage :** HTML5, Vanilla CSS et JavaScript pur (zéro framework lourd, zéro dépendance Node).
- **Composants déjà implémentés dans `video.js` :**
  - `window` : Terminal développeur avec effet de frappe typewriter déterministe.
  - `cards` : Cartes d'interfaces et modules fonctionnels (1 à 3 cartes).
  - `big` : Chiffres clés et punchlines plein écran.
  - `list` : Listes numérotées cadencées.
  - `engine_arch` : Schémas d'architecture et de flux en continu.
  - `sync_timer` & `speed_counter` : Compteurs d'alignement temporel et barres comparatives.
  - `face` & `emotion_morph` : Sticker d'avatar avec états émotionnels et badges lower-third.
- **Règles de composition :** Safe areas 9:16 respectées (HUD à top: 28px, sous-titres dynamiques top: 96px, marge basse préservée).

---

## 2. Démonstration 1 · Style Produit SaaS & DevTool (Le cas "API to Data")

### Cadrage stratégique
- **Public cible :** Fondateurs de DevTools, Micro-SaaS B2B, éditeurs d'APIs (ex. cibles Typebot, Piloterr, Breakcold).
- **Problème résolu :** Les fonctionnalités techniques sont documentées en texte brut, cURL ou JSON statique. Les prospects non-développeurs décrochent instantanément.
- **Hook visuel (0–3s) :** Un curseur de terminal qui tape à vive allure une commande d'API, interrompu par une alerte rouge néon : *"Pourquoi votre doc fait fuir 80 % de vos prospects sales ?"*
- **Lien avec l'offre commerciale :** Prouve la capacité d'AGENT404 Studio à vulgariser des outils complexes pour en faire des armes d'acquisition sur LinkedIn et X.

### Découpage séquentiel (Format 25 secondes / 750 frames @ 30 FPS)

| Plage temps | Type composant | Visuel & Action à l'écran | Accompagnement audio & Typo |
| :--- | :--- | :--- | :--- |
| **0.0s – 3.2s** | `window` (Terminal) | Terminal sombre `#090D16`. Une commande `curl -X POST api.votre-saas.com/v1/extract` s'écrit en typewriter vert néon `#00F5A0`. Le retour affiche un bloc JSON rouge `#FF2A5F` austère. | Bruit de frappe mécanique + SFX d'erreur système. Typo : *JetBrains Mono*. |
| **3.2s – 9.0s** | `cards` (UI animée) | Transition spring fluide. Le JSON se déconstruit et se range dans deux cartes épurées : "Prospect qualifié" et "Coordonnées vérifiées" avec badges verts pulsants. | Musique lofi feutrée + SFX de validation fluide. Sous-titres dynamiques top: 96px. |
| **9.0s – 17.5s** | `speed_counter` | Deux barres comparatives : "Recherche manuelle : 15 minutes" (rouge) vs "Via API en direct : 2 secondes" (vert émeraude). Le compteur numérique s'incrémente en direct. | SFX de montée en fréquence (pitch shift positif). |
| **17.5s – 25.0s** | `big` + Lower-third | Punchline finale : *"Montrez la donnée, pas le code."* Badge lower-third AGENT404 Studio avec mention de la livraison en 48h. | SFX de cloche de fin feutrée. |

---

## 3. Démonstration 2 · Style Animation de Concept Technique (Le cas "Architecture IA")

### Cadrage stratégique
- **Public cible :** CTOs, agences Nocode, formateurs tech et éditeurs IA (ex. cibles Contournement, Alegria, Captain Data).
- **Problème résolu :** Expliquer le fonctionnement d'un agent IA ou d'un flux de webhooks sans endormir avec un diagramme statique Draw.io ou Notion.
- **Hook visuel (0–3s) :** Deux blocs en collision visuelle : un modèle de langage (LLM) et une base de données, reliés par un flux d'énergie pulsé.
- **Lien avec l'offre commerciale :** Démontre la valeur du Studio pour le content marketing éducatif et l'autorité technique.

### Découpage séquentiel (Format 28 secondes / 840 frames @ 30 FPS)

| Plage temps | Type composant | Visuel & Action à l'écran | Accompagnement audio & Typo |
| :--- | :--- | :--- | :--- |
| **0.0s – 3.5s** | `big` | Fond carbone texturé. Message d'impact : *"Un agent IA sans contexte n'est qu'un chatbot bavard."* Badge alerte rouge. | Son d'impact sourd. Typo : *Syne 900*. |
| **3.5s – 12.0s** | `engine_arch` | Double bloc animé : Bloc gauche "Données brutes client" relié par un canal lumineux à engrenage (`arch-gear`) vers le bloc droit "Agent décisionnel". Le flux s'anime de gauche à droite. | Son de flux électrique continu normalisé. Sous-titres mot-à-mot blancs sur fond noir. |
| **12.0s – 20.0s** | `list` | 3 étapes d'orchestration s'empilent avec un léger effet de ressort : 01. Ingestion sécurisée, 02. Filtrage déterministe, 03. Action métier directe. | SFX de click mécanique à chaque apparition d'item. |
| **20.0s – 28.0s** | `face` + Badge | L'avatar sticker réagit avec approbation (`assets/avatars/happy.png`), badge statut *"Système Opérationnel 100%"*. Appel à l'action sobre. | Accord musical de résolution. |

---

## 4. Démonstration 3 · Style Corporate Sobre & Institutionnel (Le cas "Gain Métier B2B")

### Cadrage stratégique
- **Public cible :** Dirigeants de PME, agences Webflow d'élite, outils RH et comptables (ex. cibles Digidop, Noqode, Missive).
- **Problème résolu :** Rassurer des clients qui rejettent l'esthétique "hacker/cyberpunk" et exigent un rendu sobre, élégant, typographiquement irréprochable et conforme aux standards suisses/nordiques.
- **Hook visuel (0–3s) :** Un chiffre minimaliste et grand format sur fond ardoise neutre : *"4 heures perdues chaque semaine sur vos devis."*
- **Lien avec l'offre commerciale :** Établit la polyvalence du moteur AGENT404 Studio pour s'adapter à des chartes graphiques d'entreprises traditionnelles sans néons superflus.

### Découpage séquentiel (Format 22 secondes / 660 frames @ 30 FPS)

| Plage temps | Type composant | Visuel & Action à l'écran | Accompagnement audio & Typo |
| :--- | :--- | :--- | :--- |
| **0.0s – 3.0s** | `big` épuré | Fond ardoise sombre `#0F172A`. Typographie blanche pure *Plus Jakarta Sans*. Chiffre blanc sur fond transparent, sans effets néons. | Voix off sobre, absence de synthétiseur lourd, silence maîtrisé. |
| **3.0s – 11.0s** | `cards` corporate | 2 cartes blanches épurées sur fond sombre : à gauche *"Processus manuel (3 outils fragmentés)"*, à droite *"Workflow centralisé (Validation en 1 clic)"*. | SFX de glissement de carte papier feutré. Sous-titres bicolores sobres. |
| **11.0s – 17.5s** | `sync_timer` | Compteur numérique précis : le temps de validation passe de 48 heures à 12 minutes. Animation fluide sans saccade. | SFX de tic-tac régulier très doux. |
| **17.5s – 22.0s** | Lower-third sobre | Carte finale avec logo client, typographie élégante, sans mention superflue. | Clôture douce. |

---

## 5. Protocole de production, d'isolation et de contrôle qualité

Pour respecter les consignes strictes du projet :
1. **Zéro régression sur la Golden Master :**
   - La suite de tests `tests/test_video01_golden_master.py` doit être exécutée et rester au vert.
   - Aucun fichier de la vidéo 01 (`tests/golden_master/`) ne doit être modifié ou déplacé.
2. **Isolation des scénarios dans `showcase/` :**
   - Chaque démo aura son fichier de données dédié : `showcase/demo_saas.json`, `showcase/demo_tech.json`, `showcase/demo_corporate.json`.
   - Le moteur `video.js` sera nourri dynamiquement sans forcer de modification structurelle du code de rendu.
3. **Contrôle d'acceptation avant publication commerciale :**
   - Vérification de la durée réelle avec `ffprobe`.
   - Vérification de la synchronisation audio/sous-titres (marge d'erreur < 50ms).
   - Contrôle du poids de fichier (cible < 15 Mo pour un MP4 de 30s en H.264).
