# CATALOGUE DES FORMATS VIRAUX RÉFÉRENCÉS (AGENT404)
## Index Stratégique & Matrice des 4 Piliers « Devenir sa Propre Niche »

Ce catalogue recense et classe les formats vidéo viraux retro-ingéniérés depuis `references/inbox/`. Chaque format est rattaché à l'un des 4 Piliers Narratifs fondamentaux pour permettre à un créateur ou dirigeant B2B de devenir sa propre référence sans tourner face caméra.

---

### PILIER 1 — TRAJECTOIRE / SPLIT-SCREEN TEMPOREL
* **Thèse** : Visualiser l'effet cumulé de deux décisions divergentes sur 6 à 12 mois.
* **Blueprint Dédié** : `bp_split_timeline` (9e Blueprint Universel).
* **Levier Psychologique** : Biais de contraste & projection temporelle (Aversion à la stagnation vs Attrait de l'autorité pérenne).

| Réf ID | Créateur | Concept / Titre | Durée | Hook Détecté | Dossier Analysé |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01` | **Jun Yuh** | *Choosing the niche vs Becoming the niche* | 60.3s | Duel / Contraste direct (Day 1 $\rightarrow$ 1 year) | [`01_jun_yuh_split_screen/`](analyzed/01_jun_yuh_split_screen/AUTOPSIE_FORMAT.md) |

---

### PILIER 2 — AUTOPSIE / COULISSES BRUTES
* **Thèse** : Ouvrir le capot technique pour prouver que le résultat n'est pas de la magie, mais un système automatisé déterministe.
* **Blueprint Dédié** : `bp_code_window` & `bp_friction_stack`.
* **Levier Psychologique** : Effet de transparence & supériorité d'outillage (Montrer le terminal CLI et le code sans fioritures).

| Réf ID | Créateur | Concept / Titre | Durée | Hook Détecté | Dossier Analysé |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `02` | **Mindura Agency** | *Textes animés générés par Claude Code en CLI* | 87.7s | Rupture de croyance (« C'est pas Premiere Pro... ») | [`02_mindura_claude_code/`](analyzed/02_mindura_claude_code/AUTOPSIE_FORMAT.md) |

---

### PILIER 3 — PREUVE TECHNIQUE / ÉTUDE DE CAS CHIFFRÉE
* **Thèse** : Établir l'autorité par des métriques irréfutables articulées après l'histoire, et convertir avec un entonnoir à double entrée.
* **Blueprint Dédié** : `bp_stat_shock` & `bp_cta_conversion` (Double Porte).
* **Levier Psychologique** : Biais d'ancrage & segmentation spontanée (1 mot-clé pour filtrer leads tièdes et leads chauds).

| Réf ID | Créateur | Concept / Titre | Durée | Hook Détecté | Dossier Analysé |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `03` | **Sky Tan** | *The Ultimate Storytelling Caption Structure* | 55.9s | Promesse de conversion double (100 clients + 700 leads) | [`03_sky_tan_storytelling_caption/`](analyzed/03_sky_tan_storytelling_caption/AUTOPSIE_FORMAT.md) |

---

### PILIER 4 — MANIFESTE / DESTRUCTION DE MYTHE B2B
* **Thèse** : Lister exhaustivement les options pour noyer le doute et offrir un choix clair orienté vers notre solution.
* **Blueprint Dédié** : `bp_grid_2x2` & `bp_versus_compare`.
* **Levier Psychologique** : Effet de profusion (Swipe file mental) & soulagement par la sélection.

| Réf ID | Créateur | Concept / Titre | Durée | Hook Détecté | Dossier Analysé |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `04` | **ContentMap** | *20 Formats viraux de Reels à tester (Catalogue)* | 17.4s | Checklist interactive ultra-rapide (cut toutes les 0.8s) | [`04_contentmap_listicle/`](analyzed/04_contentmap_listicle/AUTOPSIE_FORMAT.md) |

---

### Protocole pour ajouter un nouveau format :
```bash
python3 analyze_reference.py --input references/inbox/<video_ou_url> --name <slug>
```
Cette commande exécute le pipeline d'inspection `watch`, découpe les scènes, score le hook via `hook.py`, calcule le pacing via `pacing.py`, génère `AUTOPSIE_FORMAT.md` et produit le squelette de scènes `blueprint_template.json`.
