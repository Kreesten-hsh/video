# AGENT404 // ROADMAP STRATÉGIQUE ET PLAN DE DÉVELOPPEMENT PRIORISÉ

> **Statut de gouvernance** : FEUILLE DE ROUTE OPÉRATIONNELLE  
> **Dernière mise à jour** : 17 octobre 2026  
> **Horizon d'exécution** : 17 octobre 2026 ➔ 31 décembre 2026 (75 jours)  
> **Principe directeur** : *L'effort technique doit être strictement proportionné à l'encaissement financier.*  

---

## 1. HIÉRARCHIE DES PRIORITÉS

Chaque tâche planifiée est classée selon son impact direct sur l'encaissement de **2 000 000 FCFA** (≈ **3 049 €**) avant la date limite du 31 décembre 2026 :

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       HIÉRARCHIE D'INVESTISSEMENT DU TEMPS                  │
├────────────┬──────────────────────────────────┬─────────────────────────────┤
│ RANG       │ DOMAINE D'ACTIVITÉ               │ JUSTIFICATION ÉCONOMIQUE    │
├────────────┼──────────────────────────────────┼─────────────────────────────┤
│ Priorité 1 │ Acquisition & Conversion B2B     │ Aucun revenu n'existe sans  │
│            │ (Prospection, DMs, Démos)        │ contrat signé et encaissé.  │
├────────────┼──────────────────────────────────┼─────────────────────────────┤
│ Priorité 2 │ Capacité Effective de Livraison  │ Livrer les vidéos vendues   │
│            │ (Fiabilité, Rendu client)        │ pour valider les paiements. │
├────────────┼──────────────────────────────────┼─────────────────────────────┤
│ Priorité 3 │ Production de Contenu Éducatif   │ Créer la preuve par l'exemple│
│            │ (Publication TikTok/Reels/Shorts)│ pour attirer les prospects. │
├────────────┼──────────────────────────────────┼─────────────────────────────┤
│ Priorité 4 │ Industrialisation du Moteur      │ Découpler JSON et CLI quand │
│            │ (project.json, run.py, brand)    │ le volume de vente l'exige. │
├────────────┼──────────────────────────────────┼─────────────────────────────┤
│ Priorité 5 │ Extensions & Formations          │ STRICTEMENT AJOURNÉ après   │
│            │ (Cours vidéo, SaaS cloud)        │ le 31 décembre 2026.        │
└────────────┴──────────────────────────────────┴─────────────────────────────┘
```

---

## 2. DÉCOUPAGE EN PHASES CHRONOLOGIQUES (75 JOURS RESTANTS)

```
S42 (17-25 Oct)    S43-S44 (Fin Oct)       S45-S48 (Novembre)           S49-S52 (Décembre)
───────┬───────────────────┬───────────────────────┬───────────────────────────┬─────────────►
Phase 1 & 2 :       Phase 3 :               Phase 4 :                   Phase 5 :
Audit, Tests &      Amorçage Commercial     Livraison 1er Client &      Accélération, Ventes
Documentation       & Démos Personnalisées  Industrialisation JSON      Studio & Déploiements
[ACHEVÉ]            [IMMÉDIAT]              [EN PARALLÈLE]              [OBJECTIF 2M FCFA]
```

---

## 3. TABLEAU DÉTAILLÉ DES CHANTIERS ET TÂCHES

### Phase 1 : Sécurisation de la Référence Technique (Golden Master)
| ID | Tâche & Objectif | Statut | Effort | Dépendances | Critère d'acceptation |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **T1.1** | Création de la sauvegarde externe du MP4 original. | **DONE** | 1h | Aucune | Copie externe identique au bit près (SHA-256 vérifié). |
| **T1.2** | Extraction des données immuables (`words.reference.json`, `scenes.reference.json`, `manifest.json`). | **DONE** | 2h | T1.1 | 220 mots et 35 scènes figés dans `tests/golden_master/`. |
| **T1.3** | Capture des 5 frames visuelles témoins de référence ($t=1\text{s}, 10.5\text{s}, 22\text{s}, 47\text{s}, 62\text{s}$). | **DONE** | 1h | Playwright | 5 PNG haute fidélité enregistrés dans le manifest. |
| **T1.4** | Suite de tests automatisée de non-régression (`test_video01_golden_master.py`). | **DONE** | 2h | T1.2, T1.3 | 6 tests unitaires exécutés avec succès (`OK` en 0.14s). |

---

### Phase 2 : Documentation Stratégique, Financière et Technique
| ID | Tâche & Objectif | Statut | Effort | Dépendances | Critère d'acceptation |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **T2.1** | Rédaction de [PROJECT_OVERVIEW.md](file:///home/hasashi/Bureau/video/docs/PROJECT_OVERVIEW.md) (Vision, Cible 2M FCFA, Modèle). | **DONE** | 2h | Aucune | Objectif financier explicite en première section. |
| **T2.2** | Rédaction de [FINANCIAL_PLAN.md](file:///home/hasashi/Bureau/video/docs/FINANCIAL_PLAN.md) (Matrice 4 colonnes, scénarios, délais). | **DONE** | 3h | T2.1 | Ratios arithmétiques cohérents, suivi des 75 jours. |
| **T2.3** | Rédaction de [ARCHITECTURE.md](file:///home/hasashi/Bureau/video/docs/ARCHITECTURE.md) (Schéma Mermaid, pipeline, limites). | **DONE** | 3h | T2.1 | Pipeline réel décrit sans fard, limites actées. |
| **T2.4** | Rédaction de [ROADMAP.md](file:///home/hasashi/Bureau/video/docs/ROADMAP.md) (Priorités commerciales, planification S42-S52). | **DONE** | 2h | T2.2 | Tâches classées par contribution financière. |
| **T2.5** | Rédaction de [PROJECT_STATUS.md](file:///home/hasashi/Bureau/video/docs/PROJECT_STATUS.md) (Photographie instantanée, dashboard). | **DONE** | 1h | T2.1-T2.4 | Tableau de bord synthétique actualisable. |

---

### Phase 3 : Amorçage Commercial & Première Signature Client (Semaines 42 à 44 — 18 au 31 octobre 2026)
*Objectif : Signer le premier client Studio ou Pilote avant le 31 octobre pour encaisser la mensualité d'octobre.*

| ID | Tâche & Objectif | Statut | Effort | Dépendances | Critère d'acceptation |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **T3.1** | **Constitution de la liste de 60 prospects ultra-ciblés** (fondateurs SaaS B2B, consultants tech, formateurs publiant sur LinkedIn/X). | **PLANNED** | 4h | Aucune | Tableau de 60 contacts qualifiés avec profil, sujet de prédilection et angle d'approche. |
| **T3.2** | **Publication de la vidéo n° 1 de démonstration** sur LinkedIn, TikTok, Shorts et X avec le CTA « Envoie CODE en DM ». | **PLANNED** | 2h | Aucune | Vidéo publiée sur au moins 2 réseaux professionnels avec accroche orientée résolution de problème. |
| **T3.3** | **Prise de contact directe et proposition de 10 démos gratuites de 15s** personnalisées sur le sujet des prospects chauds. | **PLANNED** | 8h | T3.1 | Extraits personnalisés générés manuellement avec le moteur existant et envoyés par message privé. |
| **T3.4** | **Closing du 1er client payant** : Vendre l'Offre Pilote (250 €) ou l'Abonnement Studio (500 € / mois). | **PLANNED** | 4h | T3.3 | **Au moins 250 € à 500 € encaissés avant le 31 octobre 2026.** |

---

### Phase 4 : Industrialisation Légère du Moteur & Livraison Client (Semaines 45 à 47 — Novembre 2026)
*Objectif : Rendre la production des vidéos clients rapide et sans risque pour assurer la livraison sans fatigue.*

| ID | Tâche & Objectif | Statut | Effort | Dépendances | Critère d'acceptation |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **T4.1** | **Création du schéma de projet déclaratif `project.json`** : Découpler les textes et scènes de `build_master_timeline.py`. | **PLANNED** | 6h | Phase 1 (Golden Master) | Le moteur lit n'importe quel `project.json` et le test Golden Master de la vidéo n° 1 continue de passer à 100%. |
| **T4.2** | **Création du point d'entrée unifié `run.py`** avec support des drapeaux `--project`, `--dry-run`, `--skip-align`. | **PLANNED** | 4h | T4.1 | Une seule commande génère la vidéo de bout en bout en moins de 3 minutes. |
| **T4.3** | **Enrichissement visuel ciblé (2 à 3 nouveaux composants à fort impact)** : Améliorer les cartes et graphiques pour satisfaire les retours du premier client. | **PLANNED** | 8h | Retours client T3.4 | Nouveaux composants intégrés sans régression sur les scènes existantes. |
| **T4.4** | **Livraison des vidéos du Client 1 et signature du Client 2** (Atteindre 1 500 € encaissés cumulés). | **PLANNED** | 10h | T4.2 | Deuxième mensualité encaissée + nouveau client signé. |

---

### Phase 5 : Accélération Commerciale & Déploiements Moteur (Semaines 48 à 52 — Décembre 2026)
*Objectif : Encaisser les 1 500 € restants pour franchir les 2 000 000 FCFA (3 049 €) avant le 31 décembre.*

| ID | Tâche & Objectif | Statut | Effort | Dépendances | Critère d'acceptation |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **T5.1** | **Vente de l'Offre 2 (Déploiement Moteur clé en main à 750 €)** à 1 ou 2 clients disposant de compétences techniques. | **PLANNED** | 12h | T4.2 | 750 € à 1 500 € encaissés comptant + installation validée chez le client. |
| **T5.2** | **Encaissement des mensualités de décembre des clients Studio existants**. | **PLANNED** | 2h | T4.4 | Paiements récurrents validés sur le compte bancaire. |
| **T5.3** | **Bilan financier final de clôture d'exercice au 31 décembre 2026**. | **PLANNED** | 3h | T5.1, T5.2 | Rapprochement bancaire : vérification des 2 000 000 FCFA encaissés. |

---

## 4. CE QUE NOUS REFUSONS FORMELLEMENT DE FAIRE AVANT LE 31 DÉCEMBRE

Pour sanctuariser le temps de travail sur les tâches génératrices de cash, les chantiers suivants sont **interdits d'exécution [DÉCISION]** :
- Créer une interface web (frontend Next.js / React / SaaS) pour le moteur.
- Développer un système d'authentification utilisateur ou de base de données SQL.
- Tenter d'intégrer des modèles d'IA vidéo lourds (Kling, Runway, Wan) qui réintroduiraient des coûts et des artefacts.
- Tourner des vidéos de formation ou créer une plateforme de cours en ligne.
- Refactoriser le CSS ou réécrire le code JavaScript tant que le pipeline actuel compile les MP4 attendus par les clients.
