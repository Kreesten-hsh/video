# AGENT404 // TABLEAU DE BORD DE L'ÉTAT DU PROJET (PROJECT STATUS)

> **Statut de gouvernance** : PHOTOGRAPHIE OPÉRATIONNELLE ACTUALISABLE  
> **Date de référence** : 17 octobre 2026  
> **Jours restants avant l'échéance financière** : 75 jours (31 décembre 2026)  

---

## 1. TABLEAU DE BORD EXÉCUTIF

| Domaine | Statut Global | Niveau de préparation | Risque / Bloquant majeur |
| :--- | :---: | :---: | :--- |
| **Encaissement Financier** | **IN PROGRESS** | **0 % de l'objectif atteint** | 0 € encaissés confirmés à date. 75 jours pour faire 2M FCFA. |
| **Prototype Moteur Vidéo** | **DONE** | **Opérationnel (Vidéo n° 1 validée)** | Illustrations basiques, texte en dur dans le code Python. |
| **Golden Master & Tests** | **DONE** | **Sécurisé & Immuable** | Aucun risque de régression sur la vidéo n° 1. |
| **Offre 1 : Studio (500 €/m)** | **DONE** | **Prête à la vente immédiate** | Nécessite un effort manuel de mise en scène par vidéo. |
| **Offre 2 : Déploiement (750 €)** | **BLOCKED** | **Non vendable en autonomie** | Bloqué par les 35 scènes en dur et les binaires Linux x86_64. |
| **Prospection Commerciale** | **PLANNED** | **Non démarrée** | Aucun prospect contacté à ce jour. Priorité n°1 absolue. |

---

## 2. SITUATION FINANCIÈRE RÉELLE (FAITS VS OBJECTIFS)

- **Cible financière au 31/12/2026 [OBJECTIF]** : **2 000 000 FCFA** (≈ **3 049 €**).
- **Plancher de repli [OBJECTIF]** : **1 023 000 FCFA** (1 560 €) à **1 312 000 FCFA** (2 000 €).
- **Cash réellement encaissé à date [INCERTITUDE]** : **0 € / 0 FCFA** *(en attente de confirmation du propriétaire)*.
- **Chiffre d'affaires facturé en attente [FAIT VÉRIFIÉ]** : **0 € / 0 FCFA**.
- **Dépenses professionnelles engagées [FAIT VÉRIFIÉ]** : **< 15 €** (coûts API vocale négligeables).
- **Résultat net réel [INCERTITUDE]** : **0 € / 0 FCFA**.
- **Montant restant à encaisser** : **2 000 000 FCFA** (≈ **3 049 €**).

---

## 3. ÉTAT D'AVANCEMENT TECHNIQUE DU MOTEUR

### A. Réalisations confirmées [FAIT VÉRIFIÉ]
- **Vidéo n° 1 de référence existante** : [output.mp4](file:///home/hasashi/Bureau/video/output.mp4) (1080×1920 @ 30 FPS, 63,16 s, H.264 / AAC).
- **Sauvegarde externe immuable** : Stockée hors Git sous `/home/hasashi/Bureau/agent404_backup_video01/output_reference_video01.mp4` (SHA-256 : `40ad86de522df58874e25c126fac5f6521e635afb8093fb4bacf97a972911a08`).
- **Branche de test Golden Master** : `test/video01-golden-master` contenant les 220 mots de référence ([words.reference.json](file:///home/hasashi/Bureau/video/tests/golden_master/video_01/words.reference.json)), les 35 scènes ([scenes.reference.json](file:///home/hasashi/Bureau/video/tests/golden_master/video_01/scenes.reference.json)), le manifeste et 5 captures visuelles témoins.
- **Suite de tests automatisée** : [tests/test_video01_golden_master.py](file:///home/hasashi/Bureau/video/tests/test_video01_golden_master.py) (6 tests unitaires réussis à 100% en lecture seule stricte).

### B. Limites techniques et points de blocage actuels [FAIT VÉRIFIÉ]
- **Script rigide** : [build_master_timeline.py](file:///home/hasashi/Bureau/video/build_master_timeline.py) exige exactement 220 mots et 35 scènes écrites en dur dans le code.
- **Portabilité limitée** : Dossier [bin/](file:///home/hasashi/Bureau/video/bin/) contenant des binaires FFmpeg/FFprobe compilés uniquement pour Linux x86_64.
- **Dépendance réseau** : Téléchargement dynamique des polices Google Fonts à chaque rendu Playwright.

---

## 4. ÉTAT RÉEL DES DEUX OFFRES COMMERCIALES

```
┌────────────────────────────────────────┬────────────────────────────────────────┐
│ OFFRE 1 : SHORT-FORM STUDIO            │ OFFRE 2 : ENGINE DEPLOYMENT            │
│ (Abonnement récurrent 500 € / mois)    │ (Installation clé en main 750 €)       │
├────────────────────────────────────────┼────────────────────────────────────────┤
│ STATUT : PRÊT À LA VENTE IMMÉDIATE     │ STATUT : BLOQUÉ EN VENTE AUTONOME      │
│                                        │                                        │
│ Raison : Le client achète les fichiers │ Raison : Le moteur ne permet pas       │
│ MP4 livrés. Même si nous devons ajuster│ encore à un tiers sans compétences dev │
│ le script Python à la main pour chaque │ d'éditer un simple JSON et de lancer   │
│ client, nous sommes capables de livrer │ sa propre vidéo sans assistance.       │
│ 8 vidéos par mois dès aujourd'hui.     │                                        │
└────────────────────────────────────────┴────────────────────────────────────────┘
```

---

## 5. BLOCAGES PRINCIPAUX

1. **Blocage commercial n°1 [ALERTE]** :
   Le moteur technique existe, mais **personne sur le marché ne sait qu'AGENT404 existe**. Aucune vidéo de démonstration n'a été publiée publiquement sur les comptes sociaux, et aucun prospect n'a été contacté.
2. **Blocage temporel n°2 [URGENCE]** :
   Il ne reste que 14 jours en octobre. Si aucun client Studio n'est signé avant le 31 octobre, le potentiel de cashflow 2026 sur ce client est amputé de 500 € (328 000 FCFA).

---

## 6. PROCHAINE ACTION PRIORITAIRE UNIQUE

> [!IMPORTANT]
> **ACTION N°1 IMMÉDIATE DU PROPRIÉTAIRE** :  
> **Publier la vidéo n° 1 sur LinkedIn et X avec l'accroche :**  
> *« Arrête de payer des monteurs ou des IA hors de prix. Cette vidéo est 100% générée par du code Python. Envoie "CODE" en message privé si tu veux déléguer tes vidéos sans allumer ta caméra. »*  
> **Puis engager la prospection directe de 20 fondateurs SaaS en messages privés.**
