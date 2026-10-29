# Playbook Officiel de Distribution Sociale AGENT404
## Protocole Multi-Canaux, Kit de Diffusion et Règle de la Golden Hour

Ce document formalise la phase 8 du workflow de production AGENT404 (`produce-video`). Il régit la diffusion stratégique de chaque capsule vidéo verticale produite par le studio, que ce soit pour nos propres canaux (`studio_perso/`) ou pour nos clients (`studio_clients/`).

Pour la conception des scripts et des formats viraux, consulter [VIRAL_CONTENT_ENGINE.md](VIRAL_CONTENT_ENGINE.md).  
Pour la stratégie de croissance et l'optimisation de profil sur LinkedIn, consulter [LINKEDIN_GROWTH_ENGINE.md](LINKEDIN_GROWTH_ENGINE.md).

---

## 1. Répartition Stratégique des Canaux (1 Master = 4 Canaux)

Chaque vidéo AGENT404 est rendue en un master unique 9:16 (1080x1920 @ 30 FPS). La diffusion du studio applique la répartition suivante :

| Canal | Part de Diffusion | Rôle Stratégique | Format de Publication |
| :--- | :--- | :--- | :--- |
| **LinkedIn** | **80 % (Priorité absolue)** | Acquisition B2B directe, autorité auprès des fondateurs et agences, conversion en messagerie privée. | Vidéo native + post texte court (< 140 car. avant le fold) + premier commentaire épinglé. |
| **Instagram Reels** | **20 % (Relais d'autorité)** | Preuve visuelle du moteur, vitrine design et conversion via DM automatisés sur mot-clé. | Reel natif + cover 9:16 issue de la première frame + légende courte (< 60 car. avant le cut). |
| **YouTube Shorts** | Archivage passif | Référencement longue traîne et requêtes de recherche B2B. | Short avec titre axé sur la douleur client. |
| **TikTok** | En pause | Canal actuellement gelé au profit de l'écosystème B2B LinkedIn. | Reprise asynchrone des masters. |

---

## 2. Génération Automatique du Social Pack

Avant toute publication, le community manager ou l'opérateur génère le kit de distribution via le script dédié :

```bash
python3 generate_social_pack.py --projet studio_perso/video_01_decouverte
```

Cette commande génère le fichier `DISTRIBUTION_KIT.md` directement dans le dossier du projet avec :
1. **Le post LinkedIn complet** : calibré sous la barre des 140 caractères avant le repli « ...voir plus », avec appel à l'action mot-clé.
2. **La légende Instagram Reels** : optimisée pour l'accroche visuelle sous les 60 caractères.
3. **Le premier commentaire d'amorce (Self-Pinned Comment)** : question ouverte ou relance immédiate pour déclencher des réponses sous le post.
4. **Le concept de Story Instagram Teaser** : mini-séquence en 3 slides pour renvoyer le trafic vers le Reel.
5. **La checklist smartphone** : vérification du volume audio, de la première frame de couverture et du format vertical.

---

## 3. Le Protocole de la Golden Hour (H+0 à H+1)

L'algorithme de distribution (LinkedIn et Instagram) évalue la pertinence d'un contenu durant ses **60 premières minutes** de vie :

1. **Publication à heure fixe** :
   - Mardi ou Jeudi entre 07h30 et 08h30 (créneau mobile pré-bureau des décideurs B2B).
2. **Premier commentaire immédiat** :
   - Épingler le commentaire d'amorce généré dans `DISTRIBUTION_KIT.md` dans les 60 secondes suivant la mise en ligne.
3. **Réactivité chirurgicale sous les commentaires** :
   - Répondre à 100 % des interactions reçues pendant la première heure en posant une question de relance.
   - Dès qu'un prospect commente le mot-clé d'appel à l'action (ex. « CLARTÉ »), lui répondre publiquement pour valider l'envoi puis basculer en messagerie privée.
4. **Relais Story immédiat** :
   - Repartager la publication dans la Story Instagram avec un sticker sondage ou question pour orienter vers le Reel.

---

## 4. Inbound DM et Transformation en Client

La vidéo n'a pas vocation à faire du clic vain : elle sert d'amorce conversationnelle.

1. **Livraison de valeur brute** :
   - Transmettre le document promis (ex. carrousel de décomposition technique, étude de cas ou audit).
2. **Déclenchement du diagnostic** :
   - Demander quel élément du workflow résonne le plus avec son organisation actuelle.
3. **Proposition de l'offre d'entrée** :
   - Proposer notre Sprint Test (150 € pour 1 capsule livrée sous 48h sur la base d'une note vocale) pour lever toute friction technique avant le forfait mensuel (750 €/mois pour 8 vidéos) ou la formule à l'unité (200 €).
