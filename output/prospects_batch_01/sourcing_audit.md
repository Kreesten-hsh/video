# AGENT404 · RAPPORT DE TRAÇABILITÉ & SOURCING AUDIT
## Mission : Constitution du lot n° 1 de 30 prospects B2B qualifiés (Score ≥ 4/5)
**Date d'exécution :** Samedi 17 octobre 2026  
**Auteur :** Responsable Growth Intelligence & Outbound B2B, AGENT404  
**Répertoire de livraison :** `output/prospects_batch_01/`  
**Objectif financier sous-jacent :** Atteindre 2 000 000 FCFA (~3 049 €) de chiffre d'affaires encaissé avant le 31 décembre 2026 via AGENT404 Studio (500 €/mois) et Pilote (250 €).

---

## 1. Environnement technique & Outils réellement mobilisés

Conformément à la règle d'or **AVAILABLE ≠ REQUIRED** et au diagnostic initial de l'environnement, seuls les outils indispensables et opérationnels ont été exploités :

| Outil / Ressource | Statut | Usage effectif lors de la mission |
| :--- | :--- | :--- |
| **search_web** (Native) | Fonctionnel | Exécution de requêtes booléennes ciblées pour identifier les pages tarifaires, levées de fonds, acquisitions, rôles exécutifs et actualités récentes. |
| **read_url_content** (Native) | Fonctionnel | Extraction textuelle et vérification directe des pages de tarification (`/pricing`, `/tarifs`) et des conditions générales. |
| **github-mcp-server** | Fonctionnel | Audit des commits récents, des releases et des changelogs sur les projets DevTools (ex. validation du commit du 15 octobre 2026 sur Typebot). |
| **agent-reach** | Partiel (Web reader actif) | Inspection des pages web via moteur Markdown sans dépendance aux APIs tierces payantes. |
| **Python & openpyxl** | Fonctionnel | Création programmatique du classeur Excel stylisé (`prospects_batch_01.xlsx`), des exports CSV et des contrôles de cohérence. |
| **Skills antislop-copywriting & humanizer** | Actifs | Rédaction sans complaisance des messages d'approche : suppression du jargon IA, des fausses familiarités et des flatteries creuses. |

*Note de conformité : Aucun outil Notion ni API externe non autorisée n'a été appelé. Toutes les données sont consolidées localement sur le système de fichiers.*

---

## 2. Synthèse quantitative du pipeline de sourcing

Le processus de découverte a été conduit par lots successifs pour garantir une sélectivité maximale :

- **Candidats bruts identifiés :** 114 entreprises et outils explorés.
- **Candidats audités en profondeur (Recherche OSINT & vérification tarifaire) :** 48 dossiers complets examinés.
- **Doublons et variantes de domaines éliminés :** 9 cas (redirections de domaines, filiales de mêmes groupes ou cofondateurs multiples).
- **Candidats formellement rejetés :** 18 entreprises documentées dans [`prospects_rejected.csv`](file:///home/hasashi/Bureau/video/output/prospects_batch_01/prospects_rejected.csv).
- **Prospects finaux retenus :** **30 prospects** atteignant tous le score parfait vérifié de **5/5** (soit 100% de conformité au seuil minimal de 4/5).

---

## 3. Analyse des motifs d'exclusion (18 dossiers archivés)

L'application stricte de la grille d'admissibilité a conduit à rejeter 18 entreprises pourtant populaires :

1. **Rachat par des grands groupes et perte d'autonomie commerciale (5 cas) :**
   - *Flusk* : racheté par Bubble.io, fonctionnalités intégrées dans Bubble, pas d'offre B2B autonome.
   - *Cycle.app* : racheté par Atlassian fin 2025 pour intégration dans Jira Product Discovery.
   - *Octolis* : racheté par Brevo, fondateur devenu VP Growth de Brevo.
   - *Snipcart* : racheté par Duda, direction historique réorientée.
   - *DashThis* : racheté par le holding de consolidation saas.group.

2. **Opacité tarifaire et absence de prix public (4 cas) :**
   - *Scalezia*, *Zetoolbox*, *Ouiflow*, *Synqro* : ces agences ou cabinets imposent un appel de découverte ou un devis personnalisé sans afficher de grille tarifaire ou de seuil plancher vérifiable en ligne. Échec du Critère 1 (Solvabilité démontrée).

3. **Modèles purement commissionnels ou pay-as-you-go sous le seuil de 29 €/mois (5 cas) :**
   - *Plunk* (0.001 $/email sans forfait fixe), *Gladia* (0.16 €/h d'audio en pay-as-you-go), *Swikly* (1.99% par caution), *CinetPay* et *Julaya* (frais transactionnels de 1 à 3.5% sans abonnement SaaS fixe vérifiable).

4. **Absence de décideur vérifiable ou prix masqué (4 cas) :**
   - *Applitech CI* : dirigeant / fondateur non identifié avec certitude sur les surfaces publiques (échec Critère 4).
   - *GoMyCode* : tarifs masqués derrière un formulaire de demande de brochure.
   - *June.so* : abandon de la grille fixe au profit d'un devis privé par chat basé sur les MAU.
   - *Datablist* : offre payante de départ à 20-25 $/mois, strictement sous le seuil obligatoire de 29 €/mois.

---

## 4. Répartition du lot retenu (30 prospects qualifiés)

### A. Par Score
- **Score 5/5 :** 30 prospects (100 %)
- **Score 4/5 :** 0 prospect
- **Score ≤ 3/5 :** 0 (Exclus)

### B. Par Priorité Commerciale
- **Priorité A (Forte adéquation & signal commercial récent < 14 jours) :** 28 prospects (93,3 %)
- **Priorité B (Bonne adéquation, conversion à moyen terme) :** 2 prospects (6,7 % : Agendrix, Bexio)

### C. Par Zone Géographique
- **France :** 24 prospects (80,0 %)
- **Belgique :** 2 prospects (6,7 % : Overloop, Tally)
- **Canada francophone (Québec) :** 3 prospects (10,0 % : Missive, Leadfox, Agendrix)
- **Suisse (Suisse romande) :** 1 prospect (3,3 % : Bexio)

### D. Par Typologie de Marché
- **SaaS B2B & DevTools :** 18 entreprises (60,0 %)
- **Agences Web, Nocode & Growth :** 4 entreprises (13,3 %)
- **Organismes de Formation Tech / IA / NoCode :** 3 entreprises (10,0 %)
- **Fintech & Gestion B2B :** 5 entreprises (16,7 %)

---

## 5. Limites méthodologiques & Transparence sur les données

1. **Adresses email :** Conformément à la consigne stricte de ne jamais fabriquer d'adresse email ni d'extrapoler des syntaxes non confirmées, seules les adresses explicitement publiées sur des surfaces officielles (ex. commits Git signés pour Baptiste Arnaud, mentions légales pour Amaury de Luca) ont été renseignées. Pour les autres, la mention *"Non publié publiquement - Prise de contact directe recommandée via LinkedIn / X"* est inscrite.
2. **Fenêtre d'activité récente :** Les signaux récents ont été vérifiés entre le 7 et le 15 octobre 2026 (< 14 jours par rapport au 17 octobre 2026), avec mention du sujet précis et du lien direct.
3. **Surfaces vidéo auditées :** Pour chaque prospect, la homepage, la page tarifaire, le compte LinkedIn du dirigeant et, le cas échéant, la chaîne YouTube ou le compte X ont été audités pour constater l'absence de vidéo verticale animée courte de 30 secondes.

---
*Ce rapport certifie que l'intégralité des données figurant dans le classeur Excel et le fichier CSV est appuyée par des faits vérifiés et des liens consultables.*