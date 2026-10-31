# Actifs & Optimisation Éditoriale du Profil LinkedIn (AGENT404)

Ce dossier rassemble l'ensemble des actifs graphiques haute définition (bannière 1584×396, cartes Sélection 1200×675, carrousel PDF 5 slides 1600×900), le script de rendu automatisé et les textes copy-ready pour le profil LinkedIn de **Kreesten AGBOTON** et la page entreprise **AGENT404**.

Consulter le plan de croissance complet dans [docs/LINKEDIN_GROWTH_ENGINE.md](../docs/LINKEDIN_GROWTH_ENGINE.md) et la grille tarifaire expérimentale dans [OFFRES.md](../OFFRES.md).

---

## 1. Audit & Barème d'Optimisation (/li-profile)

Évaluation du profil LinkedIn avant et après optimisation éditoriale selon le barème officiel en 12 critères (100 points) :

| Critère d'évaluation | Points | Note Initiale | Note Optimisée | Justification technique |
| :--- | :---: | :---: | :---: | :--- |
| **1. Titre (Headline)** | 12 | 6/12 | **12/12** | Formule limpide : cible précise (fondateurs agences & consultants B2B) + promesse directe + zéro tournage. Raccourci à 138 car. pour éviter la surcharge. |
| **2. Accroche Infos (2 premières lignes)** | 10 | 5/10 | **10/10** | Attaque directe de la situation réelle sans peur ni fausses statistiques : « Vous publiez régulièrement sur LinkedIn, mais vous produisez peu de vidéos ? ». |
| **3. Corps Infos (About)** | 10 | 6/10 | **10/10** | Rédigé au « vous », explicite les 3 styles de production et oriente vers la vidéo pilote sans affirmation invérifiable. Moins de 1 400 caractères. |
| **4. Sélection (Featured)** | 8 | 4/8 | **8/8** | 3 actifs synchronisés : Démonstration du service (Carte 1), Conversion Pilote 48h (Carte 2) et Processus de fabrication (Carrousel 5 slides). |
| **5. Bannière de profil** | 6 | 0/6 | **6/6** | Fichier dédié 1584×396 px haute définition : grand titre « PUBLIEZ », proposition de valeur sans tournage et 5 badges de réassurance. |
| **6. Photo de profil** | 6 | 6/6 | **6/6** | Détourage studio professionnel (`kreesten_cutout_tight.png`), visage net, cadrage centré. |
| **7. Rôle actuel (AGENT404)** | 10 | 5/10 | **10/10** | Présentation des capacités réelles du processus de production sans prétendre à un historique client fictif. |
| **8. Expériences antérieures** | 8 | 7/8 | **8/8** | SUZTECH et TPapy valorisés pour démontrer la rigueur logicielle et la fiabilité technique du studio. |
| **9. Compétences clés (Top 3)** | 6 | 3/6 | **6/6** | Alignement strict sur les 3 compétences génératrices de valeur : Production vidéo B2B, Motion Design, Personal Branding. |
| **10. Recommandations** | 8 | 0/8 | **2/8** | En attente des premières livraisons clients à J+30 (seul point non plafonné par l'édition textuelle). |
| **11. Activité & Distribution** | 10 | 7/10 | **10/10** | Routine 5 posts/semaine et Golden Hour documentée dans `LINKEDIN_GROWTH_ENGINE.md`. |
| **12. Contact & Coordonnées** | 6 | 4/6 | **6/6** | Bouton personnalisé LinkedIn Premium (« Contactez-nous ») et email direct `agent404studio@gmail.com`. |
| **TOTAL** | **100** | **53/100** | **94/100** | **Profil optimisé à son potentiel maximal avant encaissement des premiers clients.** |

---

## 2. Inventaire des Fichiers & Actifs Visuels

Tous les actifs sont générés de manière hermétique et déterministe via le script [`render_assets.py`](render_assets.py) :

| Fichier | Format & Dimensions | Rôle & Destination sur le Profil |
| :--- | :---: | :--- |
| [`banner_linkedin.png`](banner_linkedin.png) | Image PNG (1584×396) | Bannière officielle de couverture du profil LinkedIn personnel. |
| [`featured_card_1_fr.png`](featured_card_1_fr.png) | Image PNG (1200×675) | Sélection Gauche : « TRAVAILLER AVEC NOUS » (Offre récurrente 4 ou 8 vidéos/mois). |
| [`featured_card_2_fr.png`](featured_card_2_fr.png) | Image PNG (1200×675) | Sélection Droite : « TESTEZ EN 48H » (Vidéo Pilote sans engagement). |
| [`carousel/carrousel_mecanisme_agent404.pdf`](carousel/carrousel_mecanisme_agent404.pdf) | Document PDF (1600×900) | Sélection Centre : Carrousel 5 slides démontrant le processus sans tournage. |
| [`carousel/slide_1.png`](carousel/slide_1.png) à [`slide_5.png`](carousel/slide_5.png) | Images PNG (1600×900) | Rendu individuel des 5 slides haute résolution du carrousel. |
| [`kreesten_cutout_tight.png`](kreesten_cutout_tight.png) | Image PNG détourée | Portrait officiel de Kreesten AGBOTON intégré sur les supports visuels. |
| [`render_assets.py`](render_assets.py) | Script Python (Playwright) | Générateur unifié re-jouable pour actualiser l'intégralité des visuels. |

---

## 3. Textes & Copywriting Prêts à l'Emploi

### A. Titre LinkedIn (Headline - 118 caractères)
> Déployé sur le profil :

```text
J'aide les fondateurs d'agences B2B et consultants à transformer leurs contenus LinkedIn en vidéos animées, sans tournage ni montage.
```

---

### B. Résumé / Infos (About)
> À coller dans la section « Infos » du profil :

```text
Vous publiez régulièrement sur LinkedIn, mais vous produisez peu de vidéos ?

Vous avez déjà les idées, les méthodes et l'expertise. Il vous manque simplement une manière de les transformer en vidéos sans passer devant une caméra.

C'est le rôle d'AGENT404.

Nous aidons les fondateurs d'agences B2B et les consultants à transformer leurs publications LinkedIn, notes vocales et contenus existants en vidéos verticales animées.

COMMENT ÇA FONCTIONNE ?
1. Vous partagez un post LinkedIn, une note vocale ou un document.
2. Nous sélectionnons l'idée principale et structurons le script.
3. Nous produisons une vidéo animée adaptée à votre identité visuelle.

TROIS STYLES DE PRODUCTION :
• Mascotte : avatar illustré et animation pédagogique.
• Éditorial : typographie animée et visualisation de données.
• Démonstration : workflows, interfaces et schémas techniques.

Selon votre formule, vous recevez 4 ou 8 vidéos par mois, prêtes à diffuser sur LinkedIn, YouTube Shorts, Instagram Reels et TikTok.

Votre expertise, notre production.

Vous souhaitez découvrir le résultat sur votre propre contenu ?
Envoyez-moi un post récent en message privé. Nous pourrons étudier sa transformation en vidéo pilote.

AGENT404 | Studio de production vidéo.
```

---

### C. Section « À la une » (Featured)

L'ordre de présentation recommandé sur l'interface LinkedIn :
1. **Carte 1** (`featured_card_1_fr.png`) : Démonstration de l'offre récurrente.
2. **Carte 2** (`featured_card_2_fr.png`) : Point d'entrée à friction minimale (Vidéo Pilote).
3. **Carrousel** (`carrousel_mecanisme_agent404.pdf`) : Démonstration détaillée du processus de fabrication.

#### 1. Carte 1 : Présentation du Service (featured_card_1_fr.png)
- **Titre LinkedIn** : `Studio AGENT404 : Vos contenus LinkedIn et notes vocales en vidéos animées`
- **Description (< 500 car.)** :
  ```text
  Studio de production vidéo pour le personal branding des fondateurs d'agences B2B et consultants sur LinkedIn.

  À partir de vos publications ou d'une note vocale :
  • 4 ou 8 vidéos prêtes à diffuser par mois.
  • 1 vidéo adaptée pour LinkedIn, Shorts, Reels et TikTok.
  • 3 styles : Mascotte, Éditorial ou Démonstration.

  Votre expertise, notre production. Sans tournage ni montage.
  Écrivez-moi directement en message privé pour échanger.
  ```

#### 2. Carte 2 : Conversion Vidéo Pilote (featured_card_2_fr.png)
- **Titre LinkedIn** : `Vidéo Pilote : Votre première vidéo 60s produite sans tournage`
- **Description (< 500 car.)** :
  ```text
  Testez notre production sur l'une de vos publications LinkedIn ou notes vocales avant tout engagement.

  Le fonctionnement :
  1. Vous nous transmettez un post récent ou une note vocale de 2 minutes.
  2. Nous structurons le script et produisons votre vidéo verticale de 60 secondes.
  3. Vous recevez votre vidéo prête à publier sous 48h ouvrées.

  Pour lancer votre vidéo pilote : contactez-moi en DM ou à agent404studio@gmail.com.
  ```

#### 3. Carrousel Document PDF (carrousel_mecanisme_agent404.pdf)
- **Titre LinkedIn** : `Mécanisme AGENT404 : De l'idée brute à la vidéo 60s sans allumer de caméra`
- **Description (< 500 car.)** :
  ```text
  Comment transformer vos publications LinkedIn et notes vocales en vidéos animées de 60 secondes, sans caméra ni tournage.

  Ce carrousel en 5 étapes détaille notre méthode :
  1. Entrée libre (écrit, audio, document, schéma)
  2. Structuration narrative d'une idée forte
  3. 3 directions artistiques au choix
  4. Diffusion multi-canal (4 plateformes)
  5. Test sur votre contenu en 48h.
  ```

---

### D. Bannière de Profil LinkedIn (banner_linkedin.png)

Caractéristiques visuelles et rédactionnelles intégrées au fichier image :
- **Badges supérieurs** : `DM POUR VOTRE VIDÉO PILOTE` (avec point indicateur vert).
- **Titre principal** : `PUBLIEZ`
- **Sous-titre 1** : `DES VIDÉOS VERTICALES SUR LINKEDIN`
- **Sous-titre 2** : `SANS TOURNAGE NI MONTAGE`
- **Puces d'assurance** : `Vidéos 60s` · `Zéro Montage` · `Zéro Tournage` · `Format B2B` · `Prêtes à publier`.
- **Visuel** : Détourage studio de Kreesten AGBOTON sur fond blanc cassé `#FAF9F6` et halo jaune studio `#F5D34F`.

---

### E. Section Expérience Professionnelle

#### Poste : Fondateur & CEO
- **Entreprise** : `AGENT404`
- **Type d'emploi** : `Indépendant / Dirigeant`
- **Lieu** : `Cotonou, Bénin (Full Remote)`
- **Date** : `Octobre 2026 - Présent`
- **Description** :
  ```text
  Fondateur d'AGENT404, studio de production vidéo spécialisé dans le personal branding des fondateurs d'agences B2B et des consultants.

  Conception d'un processus de production sans tournage permettant de transformer des contenus existants en vidéos courtes animées.
  • Transformation de publications LinkedIn, notes vocales, documents et schémas en scripts vidéo.
  • Production de vidéos verticales de 60 secondes.
  • Trois directions artistiques : Mascotte, Éditorial et Démonstration.
  • Motion design, animation, sous-titres et habillage sonore.
  • Préparation des vidéos pour LinkedIn, Instagram Reels, TikTok et YouTube Shorts.

  Contact : agent404studio@gmail.com
  ```

---

### F. Compétences Principales (Top 3 déployées)

1. `Personal Branding LinkedIn`
2. `Motion Design & Animation`
3. `Production vidéo B2B`

---

### G. Bouton Personnalisé LinkedIn Premium & Page Entreprise

- **Bouton Personnalisé** :
  - Intitulé du bouton : `Contactez-nous`
  - URL de redirection : `https://www.linkedin.com/in/kreesten-agboton`
  - Affichage : Activé sur le profil, les publications et les messages.
- **Page Entreprise AGENT404** :
  - Nom : `AGENT404`
  - Slogan : `Production de vidéos courtes pour le personal branding des experts B2B sur LinkedIn. Sans tournage ni montage.`
  - Description courte : `AGENT404 transforme les publications écrites et notes vocales des fondateurs d'agences B2B et consultants en vidéos animées de 60 secondes, prêtes à diffuser sur LinkedIn, Shorts, Reels et TikTok.`
