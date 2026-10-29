# FICHE PROSPECT & STRATÉGIE OUTBOUND : Ruben Taïeb

- **ID Prospect** : #19
- **Titre** : Ghostwriter de Dirigeants & CEO
- **Entreprise** : Ruben Taieb Consulting (1-3 employés (Ghostwriting & Personal Branding Exécutif))
- **LinkedIn** : https://www.linkedin.com/in/rubentaieb/
- **Site Web** : https://rubentaieb.com
- **Email Pro** : `ruben@rubentaieb.com`

---

## 🎯 Diagnostic Contenu
- **Contenu écrit** : Ruben aide des dirigeants à prendre la parole sans filtre sur LinkedIn, raconte les coulisses du ghostwriting et dénonce la banalité des contenus générés par IA.
- **Angle mort vidéo** : Ses clients CEO lui demandent fréquemment de les aider à produire de la vidéo, mais ils refusent les contraintes de tournage. Ruben lui-même communique uniquement par texte. S'associer à un format zéro caméra lui permettrait de doubler la valeur apportée à ses clients sans effort de production.

---

## 🚀 Cheval de Troie Visuel (Teaser 15s)
- **Sujet** : Pourquoi un dirigeant ne devrait jamais déléguer sa voix à une IA
- **Blueprints mobilisés** :
  1. `0.0s - 5.14s` : `bp_hook_question` (TES POSTS LINKEDIN RESSEMBLENT À CEUX DE TOUT LE MONDE ?)
  2. `5.14s - 11.06s` : `bp_versus_compare`
  3. `11.06s - 15.10s` : `bp_cta_conversion`

---

## 💬 Message Privé LinkedIn (DM < 400 car.)
> **Note d'invitation (184/200)** :  
> Tes conseils sur la façon d'extraire la voix authentique d'un CEO plutôt que de régurgiter des banalités sont tops. Je produis des vidéos B2B sans caméra. Hâte de te suivre.  
>  
> **Message 1 (344 car.)** :  
> Hello Ruben, ton post sur la différence entre un contenu jetable écrit par ChatGPT et une vraie voix de dirigeant tape dans le mille. Tes clients CEOs cherchent souvent à faire de la vidéo sans y passer 3h de tournage. J'ai prototypé ton post en vidéo motion 15s sans caméra. Tu veux que je te dépose le MP4 ici ?

---

## ✉️ Cold Email J+1
**Objet :** `tes textes de ghostwriting incarnés en vidéo`

Hello Ruben,

Ton post sur l'importance de préserver la singularité d'un dirigeant face au déferlement de posts IA génériques est exemplaire.
Aujourd'hui, les CEOs veulent rayonner en vidéo mais refusent les tournages lourds et les avatars robotiques.
On a matérialisé ton argument dans une capsule vidéo animée de 15s sans caméra, prête à être diffusée.
Notre Pack Découverte (150 €, 100% déductible du premier mois) est idéal pour tester ce levier sur tes propres contenus.
Dis-moi si tu veux recevoir le teaser MP4 par retour de mail.

Kreesten - Agent404

---

## 🎬 Commandes de Rendu Vidéo
```bash
# 1. Vérification de la timeline
python3 build_master_timeline.py -p studio_clients/19_ruben_taieb_ghostwriting

# 2. Rendu de la vidéo MP4
python3 render.py -p studio_clients/19_ruben_taieb_ghostwriting -o studio_clients/19_ruben_taieb_ghostwriting/output_demo_15s.mp4 --fast
```
