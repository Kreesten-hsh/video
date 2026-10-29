# FICHE PROSPECT & STRATÉGIE OUTBOUND : Bastien Paul

- **ID Prospect** : #09
- **Titre** : Co-fondateur & CEO
- **Entreprise** : Hublead (2-5 employés (Bootstrapped Sales Extension SaaS))
- **LinkedIn** : https://www.linkedin.com/in/bastien-paul-hublead
- **Site Web** : https://hublead.io
- **Email Pro** : `bastien@hublead.io`

---

## 🎯 Diagnostic Contenu
- **Contenu écrit** : Bastien poste sur l'hygiène CRM, la perte de temps des commerciaux à faire du copier-coller entre LinkedIn et HubSpot, et la productivité des équipes SDR.
- **Angle mort vidéo** : Il documente bien les frictions commerciales mais sous forme de listes à puces. L'impact de gagner 5 heures par semaine s'illustre de façon spectaculaire avec une comparaison avant/après animée, mais Bastien manque de temps de tournage.

---

## 🚀 Cheval de Troie Visuel (Teaser 15s)
- **Sujet** : Combien d'heures ton équipe commerciale perd à faire du copier-coller
- **Blueprints mobilisés** :
  1. `0.0s - 5.14s` : `bp_hook_question` (TES COMMERCIAUX PASSENT LEUR VIE SUR HUBSPOT ?)
  2. `5.14s - 11.06s` : `bp_versus_compare`
  3. `11.06s - 15.10s` : `bp_stat_shock`

---

## 💬 Message Privé LinkedIn (DM < 400 car.)
> **Note d'invitation (187/200)** :  
> Ton retour sur les 5h par semaine gaspillées par les sales en ressaisie LinkedIn-HubSpot est tellement vrai. Je crée des formats vidéo B2B percutants sans caméra. Ravi de connecter.  
>  
> **Message 1 (337 car.)** :  
> Hello Bastien, ton post sur le calvaire des commerciaux qui passent leur temps à recopier des profils LinkedIn dans HubSpot tape dans le mille. Pour convertir un Head of Sales, une vidéo avant/après de 15s est imbattable. J'ai généré une capsule démo animée pour Hublead. Je peux te la glisser ici en MP4 ?

---

## ✉️ Cold Email J+1
**Objet :** `ton comparatif hublead vs copier-coller en vidéo`

Hello Bastien,

Ton post sur les 5 heures hebdomadaires perdues par commercial en saisie manuelle CRM tape exactement là où ça fait mal.
Sur les réseaux, une démonstration en vidéo animée de 60s convainc 3x plus vite un Head of Sales qu'un post textuel.
On a décliné ton post en un teaser vidéo 15s percutant sans caméra, respectant scrupuleusement la charte Hublead.
Tu peux évaluer notre studio grâce au Pack Découverte à 150 € (entièrement déductible de l'abonnement mensuel).
Tu veux que je te transmette le fichier MP4 par retour de mail ?

Kreesten - Agent404

---

## 🎬 Commandes de Rendu Vidéo
```bash
# 1. Vérification de la timeline
python3 build_master_timeline.py -p studio_clients/09_bastien_paul_hublead

# 2. Rendu de la vidéo MP4
python3 render.py -p studio_clients/09_bastien_paul_hublead -o studio_clients/09_bastien_paul_hublead/output_demo_15s.mp4 --fast
```
