# AGENT404 · AUDIT DE MATURITÉ & ÉTUDE DE SÉCURITÉ DE HARVEY
**Dépôt audité :** [https://github.com/ethanplusai/harvey](https://github.com/ethanplusai/harvey) (Version 0.3.0)  
**Date d'audit :** 17 octobre 2026  
**Statut d'exécution :** Audit statique et architectural isolé · **AUCUNE ACTIVATION, AUCUN ENVOI RÉALISÉ**

---

## 1. Environnement technique & Dépendances système

| Critère | Spécification Harvey | Environnement Local Actuel | Statut & Diagnostic |
| :--- | :--- | :--- | :--- |
| **Version Python** | `requires-python = ">=3.11"` (`pyproject.toml:10`) | `Python 3.12.3` | **COMPATIBLE** |
| **Frameworks CLI** | FastAPI, Uvicorn, Pydantic v2, Aiosqlite | Présents dans l'écosystème Python local | **COMPATIBLE** |
| **Moteur Web / Crawler** | Playwright >= 1.40, BeautifulSoup4 | Playwright déjà installé pour le moteur vidéo | **COMPATIBLE** |
| **Base de données** | SQLite asynchrone (`aiosqlite`, fichier `harvey.db`) | Système de fichiers local | **COMPATIBLE** |
| **Isolation recommandée** | Répertoire et virtualenv isolés | Obligation stricte de ne pas polluer le dépôt vidéo | **À CONFINER HORS DU REPO** |

> [!WARNING]
> **Règle d'or d'isolation des dépendances** :  
> Le dépôt vidéo d'AGENT404 fonctionne selon une architecture déterministe minimale sans `node_modules` et avec un environnement Python axé sur la compilation FFmpeg/Playwright. Harvey ne doit **JAMAIS** être installé ou cloné dans la racine du dépôt `video/`. Son installation future devra résider dans un répertoire dédié hors du dépôt (ex. `~/tools/harvey/`) avec son propre environnement virtuel (`.venv`).

---

## 2. Incompatibilité Critique du Fournisseur IA (Codex CLI vs Claude)

Harvey repose sur un moteur d'IA appelé **Brain** (`harvey/brain.py`), qui délègue l'analyse, la rédaction et le traitement des réponses soit à **Claude Code CLI** (par défaut), soit à **Codex CLI**.

### Diagnostic de compatibilité Codex :
1. **Version requise par Harvey :**  
   Le fichier `harvey/codex.py` (lignes 91-96 et 402) impose un verrouillage strict :
   ```python
   SUPPORTED_CODEX_VERSIONS = ("0.159.3",)
   
   if version not in SUPPORTED_CODEX_VERSIONS:
       raise _setup_error(f"Unsupported Codex CLI version {version}. Supported: {', '.join(SUPPORTED_CODEX_VERSIONS)}. Install one with: npm install -g @openai/codex@{SUPPORTED_CODEX_VERSIONS[-1]}")
   ```
2. **Version actuellement installée sur la machine :**  
   L'exécution de `codex --version` renvoie :
   ```text
   codex-cli 0.154.0-alpha.6.2
   ```
3. **Verdict technique :**  
   **INCOMPATIBILITÉ BLOQUANTE**. Harvey refusera catégoriquement de s'exécuter avec le Codex CLI présent sur la machine. Toute tentative d'appel lèvera immédiatement une exception `CodexError(kind="setup")`.

### Diagnostic de compatibilité Claude Code :
1. **Exécutable recherché :** `shutil.which("claude")` (`harvey/setup.py:72`).
2. **Statut sur la machine :** `which claude` ne renvoie aucun binaire installé.
3. **Verdict technique :**  
   Aucun des deux moteurs d'IA attendus par Harvey n'est opérationnel à cet instant.

### Actions de déblocage requises (avant toute utilisation) :
- Soit mettre à jour Codex CLI vers la version exacte requise :  
  `npm install -g @openai/codex@0.159.3`
- Soit installer Claude Code CLI et s'authentifier :  
  `npm install -g @anthropic-ai/claude-code && claude login`

---

## 3. Analyse des Canaux, des Coûts et des Risques Opérationnels

### A. Canaux d'envoi d'emails
1. **Fournisseur recommandé :** Gmail / Google Workspace via OAuth2 (pas de mot de passe stocké).
2. **Sécurité du nom de domaine (Point critique) :**  
   Il est strictement interdit d'utiliser l'adresse email principale du fondateur ou le domaine principal du projet pour de la prospection à froid. Tout envoi doit être réalisé depuis un **domaine secondaire dédié** (ex. `agent404studio.com` ou `getagent404.com`), avec configuration DNS complète :
   - **SPF** (Sender Policy Framework)
   - **DKIM** (DomainKeys Identified Mail)
   - **DMARC** (avec politique de surveillance progressive)
   - Préchauffage (*warmup*) d'au moins 14 jours avant d'atteindre 30 envois/jour.

### B. Outils de découverte (Scouting) & Tarification réelle
- **OpenStreetMap** : Gratuit (0 $), configuré par défaut, mais totalement inadapté à AGENT404 (répertoire d'adresses physiques de commerces locaux, pas de SaaS tech).
- **Serper.dev (Google Search API)** : 2 500 requêtes gratuites sans carte bancaire, puis 50 $ par pack prépayé. Recommandé pour la recherche de signaux d'actualité.
- **DataForSEO** : 0,372 $ par millier d'entreprises, mais impose un rechargement minimal de **50 $** à l'ouverture du compte.

### C. Vérification d'adresses (Protection contre le blacklisting)
- **ZeroBounce** : 100 vérifications gratuites par mois (recommandé pour les adresses Google Workspace / Microsoft 365).
- **Reoon Email Verifier** : 600 vérifications gratuites par mois (excellent filtre anti-catchall).
- *Règle AGENT404 :* Sans clé de vérification active, Harvey classe toute adresse devinée en statut *"guess"* et bloque l'envoi.

---

## 4. Mode Brouillon Uniquement & Garde-Fous Humains

Pour garantir qu'aucun email ne parte automatiquement sans relecture attentive :

### A. Configuration dans `harvey.yaml`
```yaml
channels:
  email:
    enabled: true
    provider: "gmail"
    require_approval: true    # OBLIGATOIRE : place chaque email généré dans la file d'attente
    max_daily_sends: 0        # Verrouille l'envoi automatisé
    send_to_risky: false      # Refus des domaines fourre-tout (catch-all)
    max_bounce_rate: 0.03     # Suspension immédiate si plus de 3% de rejets

  linkedin:
    enabled: false            # DÉSACTIVATION STRICTE DU SCRAPING PLAYWRIGHT
```

### B. Commandes de contrôle opérationnel
- **Mettre en pause tout flux d'envoi sortant :**
  ```bash
  harvey sending --pause
  ```
- **Inspecter les messages en attente de validation :**
  ```bash
  harvey outbox
  ```
- **Approuver unitairement un message après relecture humaine :**
  ```bash
  harvey outbox --approve <ID_MESSAGE>
  ```
- **Rejeter un message inadapté :**
  ```bash
  harvey outbox --reject <ID_MESSAGE>
  ```

---

## 5. Gestion des Rejets, Bounces et Désabonnements

Le code source d'Harvey intègre des mécanismes de conformité légale (RGPD / CAN-SPAM) :
1. **Gestion des bounces (`is_bounce: True`) :**  
   Détection automatique des messages d'erreur de distribution (Mail Delivery Subsystem). Le contact est immédiatement marqué `bounced`, retiré de toute relance et le taux de bounce de la campagne est recalculé. Si le taux dépasse 5 %, la campagne est automatiquement mise en pause.
2. **Traitement des désabonnements (`harvey/agents/handler.py:509`) :**  
   L'agent d'analyse classe toute réponse négative explicite (*"Arrêtez de m'écrire"*, *"Désabonnez-moi"*, *"Pas intéressé"*) sous l'intention `unsubscribe`. Le contact est basculé en statut `opt_out` et toute tentative d'envoi future vers cette adresse est bloquée au niveau de la base de données.

---

## 6. Recommandation Stratégique pour AGENT404

1. **Ne pas activer Harvey aujourd'hui :**  
   La base qualifiée compte actuellement 13 dossiers hautement prioritaires (Catégorie A). À ce stade, envoyer des messages semi-automatisés par un bot est contre-productif. Les 5 à 10 premiers contacts doivent être réalisés **manuellement** par le fondateur via LinkedIn ou Twitter.
2. **Utiliser Harvey ultérieurement comme CRM local de brouillons :**  
   Une fois le modèle validé sur les 3 premiers clients payants, Harvey pourra être installé dans un dossier externe pour préparer des brouillons de relance, mais toujours avec `require_approval: true` et sans automatisation LinkedIn.
