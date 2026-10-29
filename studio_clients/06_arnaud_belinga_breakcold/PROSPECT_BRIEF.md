# FICHE PROSPECT & STRATÉGIE OUTBOUND : Arnaud Belinga

- **ID Prospect** : #06
- **Titre** : Co-fondateur
- **Entreprise** : Breakcold (2-5 employés (Bootstrapped AI-Native Social CRM))
- **LinkedIn** : https://fr.linkedin.com/in/arnaud-belinga-ai-native-crm
- **Site Web** : https://breakcold.com
- **Email Pro** : `arnaud@breakcold.com`

---

## 🎯 Diagnostic Contenu
- **Contenu écrit** : Arnaud publie plusieurs fois par semaine sur le social selling LinkedIn/Twitter, la fin de l'ère du cold outreach agressif et la lourdeur des CRM traditionnels comme Salesforce pour les indépendants et petites équipes.
- **Angle mort vidéo** : Breakcold est un produit très visuel et dynamique, mais Arnaud communique presque exclusivement par écrit. Il n'a pas le temps d'installer une régie vidéo pour produire des reels quotidiens sans sacrifier le dev produit.

---

## 🚀 Cheval de Troie Visuel (Teaser 15s)
- **Sujet** : Pourquoi les commerciaux détestent mettre à jour leur CRM
- **Blueprints mobilisés** :
  1. `0.0s - 5.14s` : `bp_hook_question` (TON CRM TE PREND PLUS DE TEMPS QUE VENDRE ?)
  2. `5.14s - 11.06s` : `bp_versus_compare`
  3. `11.06s - 15.10s` : `bp_cta_conversion`

---

## 💬 Message Privé LinkedIn (DM < 400 car.)
> **Note d'invitation (188/200)** :  
> Ton retour d'expérience sur la fin du cold calling pur et l'essor du social selling dans Breakcold m'a marqué. Je crée des vidéos B2B sans caméra pour SaaS. Ravi de te suivre ici.  
>  
> **Message 1 (342 car.)** :  
> Hello Arnaud, ton comparatif entre la lourdeur des vieux CRM et l'approche Breakcold résume parfaitement la douleur des SDRs. En vidéo verticale courte, ce message convertit énormément sur Twitter et LinkedIn. J'ai monté une démo 15s percutante reprenant ton argumentaire. Je peux te faire suivre le fichier vidéo ?

---

## ✉️ Cold Email J+1
**Objet :** `ton post sur les vieux crm en vidéo courte`

Hello Arnaud,

Ton post opposant l'enfer de saisie des anciens CRM à l'agilité sociale de Breakcold est redoutable d'efficacité.
Pour évangéliser les commerciaux sur mobile, une vidéo courte de 60s sans filtre frappe 10x plus fort que du texte.
On a mis en scène ton post dans un teaser 15s percutant sans caméra, entièrement stické à la marque Breakcold.
Tu peux tester notre production avec le Pack Découverte (150 €, intégralement déductible du premier mois).
Dis-moi si tu veux que je te glisse le MP4 en réponse à ce mail.

Kreesten - Agent404

---

## 🎬 Commandes de Rendu Vidéo
```bash
# 1. Vérification de la timeline
python3 build_master_timeline.py -p studio_clients/06_arnaud_belinga_breakcold

# 2. Rendu de la vidéo MP4
python3 render.py -p studio_clients/06_arnaud_belinga_breakcold -o studio_clients/06_arnaud_belinga_breakcold/output_demo_15s.mp4 --fast
```
