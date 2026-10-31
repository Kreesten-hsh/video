# Playbook Officiel de Distribution Sociale AGENT404
## Protocole Multi-Canaux, Kit de Diffusion et Règle de la Golden Hour

Ce document formalise la phase 8 du workflow de production AGENT404 (`produce-video`). Il régit la diffusion stratégique de chaque capsule vidéo verticale produite par le studio, que ce soit pour nos propres canaux (`studio_perso/`) ou pour le personal branding de nos clients B2B (`studio_clients/`).

Pour la conception des scripts et des formats viraux, consulter [VIRAL_CONTENT_ENGINE.md](VIRAL_CONTENT_ENGINE.md).  
Pour la stratégie de positionnement et de prospection sur LinkedIn, consulter [LINKEDIN_GROWTH_ENGINE.md](LINKEDIN_GROWTH_ENGINE.md).

---

## 1. Répartition Stratégique des Canaux (1 Master = 4 Canaux)

Chaque vidéo AGENT404 est rendue en un master unique 9:16 (1080x1920 @ 30 FPS). La diffusion applique la répartition suivante :

| Canal | Part de Diffusion | Rôle Stratégique | Format de Publication |
| :--- | :---: | :--- | :--- |
| **LinkedIn** | **80 % (Priorité absolue)** | Canal principal de personal branding des fondateurs d'agences B2B et consultants, conversion en messagerie privée. | Vidéo native + post texte court (< 140 car. avant le repli) + premier commentaire épinglé. |
| **Instagram Reels** | **20 % (Relais visuel)** | Vitrine de la direction artistique (Mascotte, Éditorial, Démonstration) et présence multicanale. | Reel natif + cover 9:16 issue de la première frame + légende courte (< 60 car. avant le cut). |
| **YouTube Shorts** | Relais multicanal | Référencement longue traîne de l'expertise B2B. | Short avec titre axé sur le problème métier résolu. |
| **TikTok** | En pause (Studio) / Actif (Client) | Réutilisation sans effort du même fichier master 9:16. | Reprise asynchrone des masters. |

---

## 2. Génération Automatique du Social Pack

Avant toute publication, l'opérateur génère le kit de distribution via le script dédié :

```bash
python3 generate_social_pack.py --projet studio_perso/video_01_decouverte
```

Cette commande génère le fichier `DISTRIBUTION_KIT.md` directement dans le dossier du projet avec :
1. **Le post LinkedIn complet** : calibré sous la barre des 140 caractères avant le repli « ...voir plus », avec appel à l'action sobre.
2. **La légende Instagram Reels** : optimisée pour l'accroche visuelle sous les 60 caractères.
3. **Le premier commentaire d'amorce (Self-Pinned Comment)** : question ouverte ou précision méthodologique pour engager la discussion sous le post.
4. **Le concept de Story Instagram Teaser** : mini-séquence en 3 slides pour renvoyer le trafic vers le Reel.
5. **La checklist smartphone** : vérification du volume audio, de la première frame de couverture et du format vertical.

---

## 3. Le Protocole de la Golden Hour (H+0 à H+1)

L'algorithme de distribution (LinkedIn et Instagram) évalue la pertinence d'un contenu durant ses **60 premières minutes** de vie :

1. **Publication à heure fixe** :
   - Mardi, Mercredi ou Vendredi entre 07h30 et 08h30 (créneau mobile pré-bureau des décideurs B2B).
2. **Premier commentaire immédiat** :
   - Épingler le commentaire d'amorce généré dans `DISTRIBUTION_KIT.md` dans les 60 secondes suivant la mise en ligne.
3. **Réactivité sous les commentaires** :
   - Répondre à 100 % des interactions reçues pendant la première heure en posant une question de relance pertinente.
   - Dès qu'un prospect manifeste un intérêt ou commente le mot-clé (ex. « CLARTÉ »), lui répondre publiquement puis poursuivre l'échange en messagerie privée.

---

## 4. Transformation des Conversations en Clients Payants

La vidéo sert à démontrer notre capacité à transformer une expertise écrite ou vocale en contenu vidéo clair :

1. **Qualification du besoin (Filtre des 5 critères)** :
   - Vérifier que l'interlocuteur est un fondateur d'agence B2B ou un consultant indépendant ayant une vraie activité commerciale et publiant déjà sur LinkedIn.
2. **Choix du style adapté** :
   - Identifier lequel des 3 styles (**Mascotte**, **Éditorial**, **Démonstration**) correspond le mieux à son positionnement.
3. **Proposition de l'offre d'entrée** :
   - Proposer la **Vidéo Pilote à 150 €** (1 vidéo de 45 à 60 secondes produite à partir d'un de ses posts LinkedIn ou d'une note vocale, 100 % déductible sous 7 jours), avant d'envisager les formules récurrentes **Starter (450 €/mois pour 4 vidéos)** ou **Growth (750 €/mois pour 8 vidéos)**.
