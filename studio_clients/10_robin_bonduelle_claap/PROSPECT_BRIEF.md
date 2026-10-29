# FICHE PROSPECT & STRATÉGIE OUTBOUND : Robin Bonduelle

- **ID Prospect** : #10
- **Titre** : Co-fondateur & CEO
- **Entreprise** : Claap (15-30 employés (B2B SaaS Seed/Series A))
- **LinkedIn** : https://fr.linkedin.com/in/robin-bonduelle-6812a626
- **Site Web** : https://claap.io
- **Email Pro** : `robin@claap.io`

---

## 🎯 Diagnostic Contenu
- **Contenu écrit** : Robin écrit sur l'épuisement causé par les réunions synchrones, la puissance du feedback asynchrone et l'analyse automatique des sales calls par IA pour fermer plus de deals.
- **Angle mort vidéo** : Paradoxe total : Claap est une plateforme de vidéo asynchrone, mais le profil personnel de Robin ne publie pratiquement que du texte pur. Il manque d'un pipeline de production de capsules courtes pour incarner sa marque personnelle sans empiéter sur son rôle de CEO.

---

## 🚀 Cheval de Troie Visuel (Teaser 15s)
- **Sujet** : La réunion de 30 minutes qui aurait pu être un mémo de 2 minutes
- **Blueprints mobilisés** :
  1. `0.0s - 5.14s` : `bp_hook_question` (ENCORE UNE RÉUNION DE 30 MIN DANS TON CALENDRIER ?)
  2. `5.14s - 11.06s` : `bp_friction_stack`
  3. `11.06s - 15.10s` : `bp_cta_conversion`

---

## 💬 Message Privé LinkedIn (DM < 400 car.)
> **Note d'invitation (184/200)** :  
> Tes retours sur la transition vers le travail asynchrone et la fin des réunions synchrones stériles sont brillants. Je développe un studio vidéo B2B sans caméra. Ravi de te suivre.  
>  
> **Message 1 (335 car.)** :  
> Hello Robin, ton post sur le coût caché des réunions de 30 minutes sans ordre du jour est une claque de bon sens. Pour évangéliser les managers pressés, une capsule vidéo incisive de 15s a un impact décuplé. J'ai prototypé ce message en vidéo motion aux couleurs de Claap. Tu veux jeter un œil au MP4 ici ?

---

## ✉️ Cold Email J+1
**Objet :** `ton post sur les réunions inutiles en vidéo`

Hello Robin,

Ton post chiffrant le coût astronomique des réunions synchrones de 30 minutes touche un point névralgique chez tous les CEO.
Ce format d'argumentaire s'adapte à merveille au format vidéo court vertical pour frapper les décideurs sur LinkedIn et Shorts.
On a modélisé ta réflexion en un teaser vidéo 15s néo-brutaliste sans tournage, prêt à être diffusé.
Notre Pack Découverte (150 €, 100% déduit du premier mois d'abonnement) permet de tester sur une capsule 60s sans engagement.
Je peux te glisser la démo MP4 en réponse à ce message ?

Kreesten - Agent404

---

## 🎬 Commandes de Rendu Vidéo
```bash
# 1. Vérification de la timeline
python3 build_master_timeline.py -p studio_clients/10_robin_bonduelle_claap

# 2. Rendu de la vidéo MP4
python3 render.py -p studio_clients/10_robin_bonduelle_claap -o studio_clients/10_robin_bonduelle_claap/output_demo_15s.mp4 --fast
```
