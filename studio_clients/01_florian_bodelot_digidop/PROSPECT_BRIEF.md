# FICHE PROSPECT & STRATÉGIE OUTBOUND : Florian Bodelot

- **ID Prospect** : #01
- **Titre** : Co-fondateur & CEO
- **Entreprise** : Digidop & Vydera (12-25 employés (Agence Webflow Enterprise & SEO B2B))
- **LinkedIn** : https://fr.linkedin.com/in/florian-bodelot-digidop
- **Site Web** : https://www.digidop.com
- **Email Pro** : `florian@digidop.com`

---

## 🎯 Diagnostic Contenu
- **Contenu écrit** : Florian publie 3 à 4 posts écrits par semaine sur LinkedIn, riches en études de cas techniques : migration de sites d'ETI de WordPress vers Webflow Enterprise, temps de chargement divisé par 4, scores Lighthouse à 99/100 et démantèlement de la dette technique.
- **Angle mort vidéo** : Ses études de cas restent figées dans de longs pavés de texte et des captures d'écran statiques. Il ne publie aucune vidéo courte car une agence de production web est déjà saturée de projets clients, et installer caméras, éclairage et 4h de montage hebdomadaire est un gouffre opérationnel.

---

## 🚀 Cheval de Troie Visuel (Teaser 15s)
- **Sujet** : Pourquoi 70% des refontes WordPress B2B échouent avant le mois 6
- **Blueprints mobilisés** :
  1. `0.0s - 5.14s` : `bp_hook_question` (VOTRE SITE B2B MET PLUS DE 4 SECONDES À CHARGER ?)
  2. `5.14s - 11.06s` : `bp_versus_compare`
  3. `11.06s - 15.10s` : `bp_cta_conversion`

---

## 💬 Message Privé LinkedIn (DM < 400 car.)
> **Note d'invitation (191/200)** :  
> Ton cas client sur la migration Webflow et le score Lighthouse à 98 m'a bluffé. Je pilote un studio de capsules vidéo B2B sans caméra. Curieux de suivre tes prochains retours d'expérience.  
>  
> **Message 1 (363 car.)** :  
> Hello Florian, j'ai vu passer ton post sur la dette technique des 28 plugins WordPress. L'argument est imparable, mais beaucoup de décideurs zappent les longs posts écrits. J'ai transformé ton raisonnement en une capsule vidéo 15s animée aux couleurs de Digidop (sans tournage). Je peux te déposer le MP4 ici si tu veux voir le rendu ?

---

## ✉️ Cold Email J+1
**Objet :** `ton post wordpress vs webflow en vidéo`

Hello Florian,

J'ai décortiqué ton post sur les sites B2B qui rament sous 28 plugins WordPress : le diagnostic est d'une clarté rare.
Le problème, c'est que 80% des CMOs sur mobile survolent le texte sans retenir tes chiffres clés.
On a converti ton post en une capsule vidéo de 15 secondes aux couleurs de Digidop, sans que tu aies à allumer une seule caméra.
Notre Pack Découverte (150 €, 100% remboursé sur l'abonnement) te permet de tester sur une capsule 60s sans aucun engagement.
Je te dépose le MP4 de démo en réponse à ce mail ?

Kreesten - Agent404

---

## 🎬 Commandes de Rendu Vidéo
```bash
# 1. Vérification de la timeline
python3 build_master_timeline.py -p studio_clients/01_florian_bodelot_digidop

# 2. Rendu de la vidéo MP4
python3 render.py -p studio_clients/01_florian_bodelot_digidop -o studio_clients/01_florian_bodelot_digidop/output_demo_15s.mp4 --fast
```
