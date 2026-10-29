# FICHE PROSPECT & STRATÉGIE OUTBOUND : Roland Vekemans

- **ID Prospect** : #04
- **Titre** : Co-fondateur & Dirigeant
- **Entreprise** : BeBranded (3-8 employés (Agence No-Code Webflow pour SaaS))
- **LinkedIn** : https://fr.linkedin.com/in/rolandvekemans
- **Site Web** : https://bebranded.xyz
- **Email Pro** : `roland@bebranded.xyz`

---

## 🎯 Diagnostic Contenu
- **Contenu écrit** : Roland partage des conseils Client-First sur Webflow, l'optimisation des taux de rebond des landing pages SaaS et des astuces d'intégration CSS propres.
- **Angle mort vidéo** : Ses carrousels de screenshots statiques sont soignés, mais le design web s'exprime avant tout dans le mouvement et les micro-animations. Il n'a pas le temps d'enregistrer et monter des vidéos facecam.

---

## 🚀 Cheval de Troie Visuel (Teaser 15s)
- **Sujet** : Les 3 erreurs qui tuent la conversion d'une landing page B2B
- **Blueprints mobilisés** :
  1. `0.0s - 5.14s` : `bp_hook_question` (TON SITE CONVERTIT À MOINS DE 1.5% ?)
  2. `5.14s - 11.06s` : `bp_friction_stack`
  3. `11.06s - 15.10s` : `bp_cta_conversion`

---

## 💬 Message Privé LinkedIn (DM < 400 car.)
> **Note d'invitation (184/200)** :  
> Tes explications sur la structure Client-First et la hiérarchie visuelle sont limpides. Je dirige un studio de vidéo B2B néo-brutaliste zéro caméra. Au plaisir de te suivre ici.  
>  
> **Message 1 (350 car.)** :  
> Hello Roland, ton post sur l'optimisation du Hero au-dessus de la ligne de flottaison est ultra concret. Vu la qualité visuelle de tes réalisations Webflow, tes posts méritent d'être animés en vidéo verticale. J'ai généré un extrait 15s avec tes codes graphiques BeBranded. Dis-moi si tu veux que je te glisse le MP4 ici ?

---

## ✉️ Cold Email J+1
**Objet :** `ton audit de landing page b2b en vidéo`

Hello Roland,

Ton post sur les 3 erreurs de hiérarchie visuelle dans le Hero des sites SaaS est d'une grande justesse.
Sur mobile, ce type d'audit cartonne en vidéo verticale dynamique, mais tourner du facecam est chronophage.
On a monté ton conseil en une capsule vidéo 15s néo-brutaliste sans caméra aux couleurs de BeBranded.
Avec notre Pack Découverte à 150 € (100% déductible du premier mois d'abonnement), tu peux tester sans friction.
Je te dépose le MP4 de démonstration en pièce jointe ?

Kreesten - Agent404

---

## 🎬 Commandes de Rendu Vidéo
```bash
# 1. Vérification de la timeline
python3 build_master_timeline.py -p studio_clients/04_roland_vekemans_bebranded

# 2. Rendu de la vidéo MP4
python3 render.py -p studio_clients/04_roland_vekemans_bebranded -o studio_clients/04_roland_vekemans_bebranded/output_demo_15s.mp4 --fast
```
