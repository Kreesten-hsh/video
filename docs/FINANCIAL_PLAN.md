# AGENT404 : MODÈLE FINANCIER ET PLAN D'ENCAISSEMENT AU 31 DÉCEMBRE 2026

Statut de gouvernance : DOCUMENT FINANCIER MAÎTRE  
Date de référence : 17 octobre 2026  
Propriétaire : Kreesten AGBOTON (Abomey-Calavi, Bénin)  
Taux de conversion officiel de référence : 1 EUR = 655,957 FCFA (parité fixe zone Franc CFA)  
Horizon d'exécution : 75 jours (du 17 octobre 2026 au 31 décembre 2026)  

---

## 1. Cadrage de l'Objectif Financier Directeur (North Star)

L'unique objectif du projet AGENT404 est d'encaisser du cash réel avant la fin de l'exercice 2026.

| Indicateur | Valeur en FCFA | Valeur en Euros (€) | Statut méthodologique |
| :--- | :---: | :---: | :--- |
| **OBJECTIF MAÎTRE (North Star)** | **2 000 000 FCFA** | **≈ 3 049 €** | [OBJECTIF] Cible impérative au 31/12/2026 |
| **Plancher de repli réaliste** | **1 639 892 FCFA** | **2 500 €** | [OBJECTIF] Seuil de validation commerciale forte (82 %) |
| **Plancher de survie minimal** | **819 946 FCFA** | **1 250 €** | [OBJECTIF] Filet de sécurité en cas de friction sévère (41 %) |

Règle de gestion stricte : seul le cash effectivement crédité sur le compte bancaire est comptabilisé. Les promesses orales, intentions d'achat et factures émises non réglées valent 0 FCFA.

---

## 2. Situation Comptable Réelle au 17 Octobre 2026

| Poste comptable | Montant constaté | Statut d'audit |
| :--- | :---: | :--- |
| **Encaissements réels à date** | **0 € / 0 FCFA** | [INCONNU] À confirmer formellement par le propriétaire |
| **Factures émises non encaissées** | **0 € / 0 FCFA** | [FAIT VÉRIFIÉ] Aucune créance client en cours |
| **Nombre de prospects contactés** | **0** | [FAIT VÉRIFIÉ] Prospection non démarrée |
| **Preuve de marché réelle** | **Aucune** | [FAIT VÉRIFIÉ] Les personas du panel étaient simulées |
| **Montant restant à encaisser** | **2 000 000 FCFA** | [OBJECTIF] Soit environ 3 049 € à trouver en 75 jours |

---

## 3. Structure des Coûts et Incertitudes Opérationnelles

L'affirmation antérieure selon laquelle les coûts seraient inférieurs à 15 € et la rentabilité supérieure à 90 % n'a jamais été démontrée par des pièces comptables. Voici la réalité disséquée poste par poste :

### A. Coûts variables de production
- **Génération vidéo locale (AGENT404)** : 0 € d'API vidéo par génération. Le pipeline tourne en local avec Playwright Chromium, Faster-Whisper et FFmpeg [FAIT VÉRIFIÉ].
- **Synthèse vocale (ElevenLabs ou équivalent)** :
  - Tarifs publics constatés : Formule Starter à 5 $ / mois (environ 3 000 FCFA pour 30 000 caractères avec droits commerciaux), Formule Creator à 22 $ / mois (environ 14 000 FCFA pour 100 000 caractères) [FAIT VÉRIFIÉ].
  - Abonnement actif réel du propriétaire : [INCONNU] (à renseigner par le propriétaire). Si le client fournit son propre mémo vocal, le coût d'API vocale est de 0 €.
- **Électricité et connectivité locale (Abomey-Calavi)** : Coût marginal estimé à 5 000 FCFA par mois de calcul machine [HYPOTHÈSE].

### B. Frais d'encaissement et commissions de paiement
- **Réception des fonds en devises (SEPA / International)** :
  - Option Moneco (compte avec IBAN européen pour la diaspora) : Frais de virement SEPA entrant, frais de conversion et commission de rapatriement vers portefeuille local ou banque locale : [INCONNU] (à mesurer via un virement test réel).
  - Option Ecobank Bénin : Frais de virement international SWIFT entrant, commissions de change et délais de compensation interbancaire : [INCONNU] (variables selon banque émettrice, généralement forfait de 10 € à 25 € par virement + marge de change).
  - [DÉCISION] : Réaliser immédiatement un virement test de 10 € pour calibrer exactement les frais de friction bancaire réels.

### C. Temps de travail humain (temps de production)
- Le moteur impose actuellement d'écrire en dur les scènes et les mots dans le code Python (`build_master_timeline.py`) pour chaque nouvelle vidéo.
- Temps passé par vidéo client : entre 1h30 et 3h par vidéo (ajustement du texte, validation acoustique, relecture visuelle) [HYPOTHÈSE].
- Temps non mesuré à date sur une vraie commande client : [INCONNU].

### D. Rentabilité et marge nette
- [FAIT VÉRIFIÉ] : Aucune marge nette ne peut être garantie ni annoncée comme prouvée tant que les frais bancaires et le temps de travail par vidéo n'ont pas été mesurés sur les 3 premières livraisons.

---

## 4. Calendrier d'Encaissement du Forfait Studio (Effet Mois Pleins)

L'Offre Studio (500 € par mois pour 8 vidéos) est payée d'avance chaque mois.  
Dans l'intervalle restant du 17 octobre au 31 décembre 2026, un client Studio ne peut rapporter que les mois entamés avant le 31 décembre :

| Période de signature du contrat | Mois encaissables en 2026 | Cash collecté par client (€) | Cash collecté en FCFA |
| :--- | :---: | :---: | :---: |
| Signature avant le 31 octobre | 3 mois (Octobre, Novembre, Décembre) | 1 500 € | 983 936 FCFA |
| Signature entre le 1er et le 15 novembre | 2 mois (Novembre, Décembre) | 1 000 € | 655 957 FCFA |
| Signature entre le 16 et le 30 novembre | 1,5 mois (acompte 50 % nov + déc) | 750 € | 491 968 FCFA |
| Signature après le 1er décembre | 1 mois (Décembre uniquement) | 500 € | 327 979 FCFA |

Constat mathématique : Dès que le 31 octobre sera passé sans signature Studio, le potentiel maximal d'un nouveau client Studio tombera mécaniquement de 1 500 € à 1 000 € pour l'année 2026.

---

## 5. Trois Scénarios d'Exécution Chiffrés

Les calculs reposent exclusivement sur les deux seules offres actives :
- **Offre Pilote** : 250 € (163 989 FCFA) pour 3 vidéos verticales.
- **Offre Studio** : 500 € / mois (327 979 FCFA) pour 8 vidéos verticales.

Toutes les hypothèses de conversion ci-dessous sont marquées [HYPOTHÈSE] car aucune prospection réelle n'a encore été menée.

### Scénario 1 : Prudent (Friction marché et retards)
- *Hypothèses* : Démarrage de la prospection début novembre. 25 prospects contactés, 3 réponses, 2 démos. Objections fortes sur la jeunesse de l'agence.
- *Ventes réalisées* :
  - 3 Pilotes vendus (2 en novembre, 1 en décembre) : $3 \times 250\text{ €} = 750\text{ €}$
  - 1 client Pilote converti en Studio pour décembre uniquement : $1 \times 500\text{ €} = 500\text{ €}$
- *Encaissement total* : **1 250 €** (environ **819 946 FCFA**).
- *Taux d'atteinte de la cible* : **41,0 %**.
- *Bilan* : L'objectif des 2 000 000 FCFA n'est pas atteint, mais 17 vidéos sont livrées et le modèle est validé par de vrais acheteurs.

### Scénario 2 : Réaliste (Exécution commerciale rigoureuse)
- *Hypothèses* : Démarrage immédiat fin octobre sur les 10 prospects les mieux vérifiés. 5 démonstrations personnalisées sans clone non consenti.
- *Ventes réalisées* :
  - 4 Pilotes vendus en novembre : $4 \times 250\text{ €} = 1\,000\text{ €}$
  - 1 client Pilote transformé en Studio sur 2 mois (mi-novembre et décembre) : $1 \times 1\,000\text{ €} = 1\,000\text{ €}$
  - 1 client Studio direct signé début décembre : $1 \times 500\text{ €} = 500\text{ €}$
- *Encaissement total* : **2 500 €** (environ **1 639 892 FCFA**).
- *Taux d'atteinte de la cible* : **82,0 %**.
- *Bilan* : Encaissement solide de plus de 1,6 million FCFA. Base récurrente établie pour janvier 2027.

### Scénario 3 : Ambitieux (Atteinte et dépassement des 2 000 000 FCFA)
- *Hypothèses* : Prospection active, retours rapides, 7 démos présentées, conversion forte grâce à la qualité visuelle du moteur.
- *Ventes réalisées* :
  - 5 Pilotes vendus : $5 \times 250\text{ €} = 1\,250\text{ €}$ (819 946 FCFA)
  - 2 clients Studio convertis dès novembre (chacun 2 mois : novembre + décembre) : $2 \times 2 \times 500\text{ €} = 2\,000\text{ €}$ (1 311 914 FCFA)
- *Encaissement total* : **3 250 €** (environ **2 131 860 FCFA**).
- *Taux d'atteinte de la cible* : **106,6 %**.
- *Bilan* : **Objectif de 2 000 000 FCFA franchi avant le 31 décembre 2026.**

---

## 6. Ce Qu'il Faut Réellement Vendre Pour Faire 2 000 000 FCFA

Pour encaisser exactement ou plus de 2 000 000 FCFA (soit 3 049 €) avant le 31 décembre 2026 avec les seules offres actives, Kreesten AGBOTON doit impérativement concrétiser l'une des combinaisons suivantes :

1. **Option A (Mix équilibré recommandé)** : Vendre **5 Pilotes** (1 250 €) et signer **2 abonnements Studio sur 2 mois** (2 000 €). Total : **3 250 €** (2 131 860 FCFA).
2. **Option B (Forte récurrence Studio)** : Signer **1 client Studio fin octobre** (3 mois = 1 500 €) + **1 client Studio mi-novembre** (2 mois = 1 000 €) + **1 client Studio en décembre** (1 mois = 500 €) + **1 Pilote** (250 €). Total : **3 250 €** (2 131 860 FCFA).
3. **Option C (Pur Pilote sans récurrence)** : Vendre **13 Pilotes payants** à 250 € chacun. Total : **3 250 €** (2 131 860 FCFA). Exige de trouver 13 clients distincts en 75 jours (charge de prospection très élevée).

---

## 7. Répartition Chirurgicale des Efforts & Application des 5 Concepts

### A. Ciblage des segments rentables (70 / 30)
- **70 % des efforts commerciaux** : Cible n° 1 — **Fondateurs de SaaS B2B bootstrappés rentables** (Typebot, Piloterr, Breakcold, Pharow, Tally). Painkiller : leurs fonctionnalités sont techniques, les prospects ne regardent pas les Looms de 10 min. Conversion naturelle : Pilote 250 € (3 vidéos) vers Studio 500 €/m.
- **30 % des efforts commerciaux** : Cible n° 2 — **Agences B2B expertes & Organismes Tech** (Digidop, Noqode, Contournement, Ottho). Painkiller : publient à l'écrit mais pas le temps de tourner en vidéo face caméra. Conversion naturelle : Studio 500 €/m (8 vidéos) pour du MRR prévisible.
- **Exclusion stricte** : Freelances débutants (pas de budget 250 €) et grandes licornes (Pennylane, Gorgias avec studios internes) -> Zéro temps alloué.

### B. Application des 5 concepts directeurs à l'objectif financier
1. **Concept 1 (Problème précis)** : Ne plus vendre une idée vague ou du code Python, mais vendre la clarté visuelle qui remplace la caméra et convertit les prospects B2B.
2. **Concept 2 (Fonctionnement étape par étape)** : Cycle de vente standardisé : message d'accroche ultra-ciblé → proposition d'un pilote 250 € sous 48h → encaissement d'avance → livraison MP4 1080x1920.
3. **Concept 3 (Non-objectifs clairs)** : Refus d'accorder des remises, refus de faire des démos gratuites non sollicitées, refus de prospecter hors du Top 10 qualifié.
4. **Concept 4 (Constat précis mesuré)** : Suivi rigoureux du tableau de conversion : nombre de décideurs contactés, taux de réponse, nombre de paiements reçus (rapprochement bancaire).
5. **Concept 5 (Critères d'acceptation testables)** : L'objectif 2 000 000 FCFA est validé uniquement lorsque les relevés bancaires attestent 2 000 000 FCFA crédités.

### Condition critique de succès
Arrêter immédiatement tout développement technique superflu et démarrer les premiers contacts directs auprès des décideurs cibles avant la fin du mois d'octobre 2026.
