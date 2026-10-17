# Graph Report - video  (2026-10-17)

## Corpus Check
- 137 files · ~612,653 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .csv 2, .css 1)

## Summary
- 922 nodes · 1036 edges · 103 communities (76 shown, 27 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f602efc1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- json
- build_master_timeline.py
- AGENT404 · Business plan
- common.sh
- video.js
- panel.py
- Tasks: [FEATURE NAME]
- speckit-analyze/SKILL.md
- AGENT404 // PLAN D'EXÉCUTION FINANCIER (OBJECTIF 31 DÉCEMBRE 2026)
- AGENT404 // Moteur de Vidéo Programmatique & Studio B2B
- AGENT404 // GRILLE DES OFFRES COMMERCIALES & SERVICES
- Execution Steps
- Caption Animation
- Short-Form Video
- 2. DÉTAIL DES MODULES LOGICIELS ET SCRIPTS
- Word-Timed Captions — End-to-End Build
- Lower Thirds
- AGENT404 // VUE D'ENSEMBLE DU PROJET & ALIGNEMENT STRATÉGIQUE
- Feature Specification: [FEATURE NAME]
- Countdown Video
- AGENT404 · RAPPORT DE TRAÇABILITÉ & SOURCING AUDIT
- speckit-plan/SKILL.md
- speckit-specify/SKILL.md
- speckit-tasks/SKILL.md
- 3. TABLEAU DÉTAILLÉ DES CHANTIERS ET TÂCHES
- Core Principles
- Core Principles
- founder-board
- founder-ops
- AGENT404 // TABLEAU DE BORD DE L'ÉTAT DU PROJET (PROJECT STATUS)
- AGENT404 — Stratégie Marketing & Plan de Lancement
- founder-consumer
- founder-marketing
- founder-offer
- Lower-Third Component — runnable code
- Retention Pacing — Short-Form Video Reference
- #10 · Missive (Philippe Lehoux — CEO & Co-fondateur)
- #1 · Typebot (Baptiste Arnaud — Fondateur & Créateur)
- #4 · Noqode (Amaury de Luca — Fondateur & CEO)
- #5 · Breakcold (Arnaud Belinga — CEO & Co-fondateur)
- #6 · Tally (Marie Martens — Co-fondatrice & Head of Growth)
- #7 · Contournement (Alexis Kovalenko — Co-fondateur)
- #8 · Axonaut (Nicolas Lemonnier — CEO & Co-fondateur)
- #9 · Dust.tt (Gabriel Hubert — CEO & Co-fondateur)
- #2 · Piloterr (Josselin Liebe — Fondateur & CEO)
- #3 · Pharow (Bruno Laporte — CEO & Co-fondateur)
- Implementation Plan: [FEATURE]
- founder-brand
- founder-competitors
- founder-plan
- founder-pricing
- speckit-checklist/SKILL.md
- Buyer panel: AGENT404 (Moteur & Studio de Vidéos Verticales Programmatiques B2B)
- Countdown Cookbook
- founder-cfo
- founder-launch
- speckit-clarify/SKILL.md
- speckit-implement/SKILL.md
- Synthèse Exécutive : AGENT404
- Digit Flip & Roll Transitions
- speckit-constitution/SKILL.md
- speckit-taskstoissues/SKILL.md
- Monopoly lens
- Offers lens
- Product lens
- Unit economics: AGENT404 (Programmatic Video Engine & Studio)
- AGENT404 — Stratégie Tarifaire & Grille de Prix
- Project Profile: video (Agent404 // Cyber-Mint)
- Caption Animation
- Countdown Video
- The three lenses
- Lower Thirds
- Short-Form Video
- AGENT404 — Board of Directors Verdict
- AGENT404 — Board Brief
- [CHECKLIST TYPE] Checklist: [FEATURE NAME]
- Sélection resserrée pour conversion rapide vers l'objectif 2 000 000 FCFA
- SKILLS_INDEX.md
- idea.md
- pricing-curve.md

## God Nodes (most connected - your core abstractions)
1. `Caption Animation` - 14 edges
2. `Short-Form Video` - 13 edges
3. `Tasks: [FEATURE NAME]` - 13 edges
4. `Word-Timed Captions — End-to-End Build` - 12 edges
5. `Lower Thirds` - 12 edges
6. `save()` - 11 edges
7. `tally()` - 11 edges
8. `main()` - 11 edges
9. `create-new-feature.sh script` - 11 edges
10. `Countdown Video` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Step 3: deal and run` --references--> `init()`  [INFERRED]
  .agents/skills/founder-consumer/SKILL.md → .agents/skills/founder-consumer/panel.py
- `Step 3: deal and run` --references--> `save()`  [INFERRED]
  .agents/skills/founder-consumer/SKILL.md → .agents/skills/founder-consumer/panel.py
- `9. Gestion des Risques & Mesures d'Atténuation` --references--> `validate_timeline()`  [INFERRED]
  PRD.md → build_master_timeline.py
- `check-prerequisites.sh script` --calls--> `check_dir()`  [EXTRACTED]
  .specify/scripts/bash/check-prerequisites.sh → .specify/scripts/bash/common.sh
- `check-prerequisites.sh script` --calls--> `check_file()`  [EXTRACTED]
  .specify/scripts/bash/check-prerequisites.sh → .specify/scripts/bash/common.sh

## Import Cycles
- None detected.

## Communities (103 total, 27 thin omitted)

### Community 0 - "json"
Cohesion: 0.10
Nodes (23): analyse(), load(), main(), _money(), NumbersError, report(), sensitivity(), _sum() (+15 more)

### Community 1 - "build_master_timeline.py"
Cohesion: 0.09
Nodes (19): align_reference_audio(), norm(), strip_accents(), main(), step3_build_timeline(), validate_timeline(), apply_sticker_effect(), fit_in_canvas() (+11 more)

### Community 2 - "AGENT404 · Business plan"
Cohesion: 0.05
Nodes (39): 1. Ce que fait l'entreprise et pour qui, 1. Données du Panel & Sensibilité Prix (Van Westendorp), 1. Données Probantes & Enseignements du Panel Acheteurs, 1. Risques critiques partagés (soulevés par plusieurs membres), 2. Checklist des conditions suspensives du Board, 2. Comparatif Concurrentiel Direct & Substituts, 2. Déclaration de Positionnement, 2. Le verdict et les chiffres clés (+31 more)

### Community 3 - "common.sh"
Cohesion: 0.11
Nodes (30): check-prerequisites.sh script, check_dir(), check_file(), find_specify_root(), format_speckit_command(), get_current_branch(), get_feature_paths(), get_invoke_separator() (+22 more)

### Community 4 - "video.js"
Cohesion: 0.36
Nodes (7): animateComponent(), buildSubtitleChunks(), calcSpringOvershoot(), initData(), renderComponent(), updateBackground(), updateScenes()

### Community 5 - "panel.py"
Cohesion: 0.16
Nodes (20): _answer_ok(), check(), deal(), init(), load_state(), main(), _num(), PanelError (+12 more)

### Community 6 - "Tasks: [FEATURE NAME]"
Cohesion: 0.07
Nodes (26): Dependencies & Execution Order, Format: `[ID] [P?] [Story] Description`, Implementation for User Story 1, Implementation for User Story 2, Implementation for User Story 3, Implementation Strategy, Incremental Delivery, MVP First (User Story 1 Only) (+18 more)

### Community 7 - "speckit-analyze/SKILL.md"
Cohesion: 0.08
Nodes (25): 1. Initialize Analysis Context, 2. Load Artifacts (Progressive Disclosure), 3. Build Semantic Models, 4. Detection Passes (Token-Efficient Analysis), 5. Severity Assignment, 6. Produce Compact Analysis Report, 7. Provide Next Actions, 8. Offer Remediation (+17 more)

### Community 8 - "AGENT404 // PLAN D'EXÉCUTION FINANCIER (OBJECTIF 31 DÉCEMBRE 2026)"
Cohesion: 0.09
Nodes (22): 1. CADRAGE DE LA NORTH STAR FINANCIÈRE, 2. TABLEAU DE BORD DES FLUX FINANCIERS, 3. IMPACT CRITIQUE DU TEMPS RESTANT ET DE LA DURÉE D'ENGAGEMENT, 4. SCÉNARIOS CHIFFRÉS D'ENCAISSEMENT, 5. POSTES DE COÛTS RÉELS & SEUILS DE RENTABILITÉ, 6. FUNNEL DE PROSPECTION COMMERCIALE & RATIOS ESTIMATIFS, 7. RÈGLES DE DÉCISION ET D'ARBITRAGE STRATÉGIQUE, 8. ROUTINE DE REVUE HEBDOMADAIRE (CADENCE DES 75 JOURS) (+14 more)

### Community 10 - "AGENT404 // Moteur de Vidéo Programmatique & Studio B2B"
Cohesion: 0.09
Nodes (22): 1. Document Control & Executive Summary, 2.1 Les Douleurs du Marché (Pain Points), 2.2 La Solution AGENT404, 2. Problématique & Opportunité de Marché, 3.1 Cibles Prioritaires, 3.2 Parcours Utilisateur (Client Journey), 3. Personas Cibles & Parcours Utilisateur, 4.1 Module 1 : Ingestion Audio & Alignement Forcé (`build_master_timeline.py`) (+14 more)

### Community 11 - "AGENT404 // GRILLE DES OFFRES COMMERCIALES & SERVICES"
Cohesion: 0.12
Nodes (16): 1. Les Deux Offres Principales AGENT404, 2. Stratégie de Tarification Progressive (750 € ➔ 1 500 € – 2 000 €), 3. Offre de Formations (Phase 2 — Post-Validation), AGENT404 // GRILLE DES OFFRES COMMERCIALES & SERVICES, Cadre contractuel, Propriété Intellectuelle et Licences, Catalogue de Formations Envisagé, Formation 1 · Créer des vidéos animées avec l'IA, Formation 2 · Automatiser sa production vidéo (+8 more)

### Community 12 - "Execution Steps"
Cohesion: 0.12
Nodes (15): 1. Initialize Convergence Context, 2. Load Artifacts (Progressive Disclosure), 3. Build the Intent Inventory, 4. Assess the Codebase and Classify Findings, 5. Assign Severity, 6. Present the In-Session Findings Summary, 7. Append Convergence Tasks (or report converged), 8. Provide Next Actions (Handoff) (+7 more)

### Community 13 - "Caption Animation"
Cohesion: 0.13
Nodes (14): Burn-in vs sidecar SRT/VTT, Caption Animation, Deliver & verify (rendered stills → MP4), Output checklist, Pages, not walls of text, Per-word pop-in (Remotion), Readable type and safe-area placement (9:16, 1080×1920), Reference files (+6 more)

### Community 14 - "Short-Form Video"
Cohesion: 0.14
Nodes (13): 9:16 safe areas, Captions, Deliver & verify (rendered stills → MP4), Hook grammar (first ~1s), Loops & re-watch, Output checklist, Pattern interrupts & cut rhythm, Reference files (+5 more)

### Community 15 - "2. DÉTAIL DES MODULES LOGICIELS ET SCRIPTS"
Cohesion: 0.14
Nodes (13): 1. VUE D'ENSEMBLE DU PIPELINE DE PRODUCTION, 2. DÉTAIL DES MODULES LOGICIELS ET SCRIPTS, 3. DÉPENDANCES ET ENVIRONNEMENT TECHNIQUE, 4. LIMITES D'ARCHITECTURE, RIGIDITÉS ET PORTABILITÉ, 5. CAPACITÉS EXISTANTES VS FONCTIONNALITÉS ABSENTES, A. Dépendances Python réelles, A. Ingestion et Alignement Forcé : [build_master_timeline.py](file:///home/hasashi/Bureau/video/build_master_timeline.py), AGENT404 // SPÉCIFICATIONS TECHNIQUES DE L'ARCHITECTURE DU MOTEUR (+5 more)

### Community 16 - "Word-Timed Captions — End-to-End Build"
Cohesion: 0.15
Nodes (12): 10. Render, 1. The one data shape, 2. Transcribe to word-level timing (Whisper), 3. Parse an existing SRT into tokens, 4. Page the tokens (1–4 words at a time), 5. Remotion component: word-timed with active highlight, 6. Web/CSS path (live DOM player), 7. Emit a sidecar SRT / VTT from the same tokens (+4 more)

### Community 17 - "Lower Thirds"
Cohesion: 0.15
Nodes (12): Anatomy, Deliver & verify (rendered stills → MP4), Enter & exit animations, In/out timing & dwell, Lower Thirds, Output checklist, Reference files, Safe area & broadcast conventions (+4 more)

### Community 18 - "AGENT404 // VUE D'ENSEMBLE DU PROJET & ALIGNEMENT STRATÉGIQUE"
Cohesion: 0.15
Nodes (12): 1. L'OBJECTIF FINANCIER PRIORITAIRE (NORTH STAR), 2. POURQUOI AGENT404 EXISTE, 3. COMMENT LE CONTENU ET LA TECHNIQUE SERVENT L'OBJECTIF FINANCIER, 4. LES DEUX MODÈLES COMMERCIAUX ACTUELS, 5. EXTENSIONS FUTURES (APRÈS LE 31 DÉCEMBRE 2026), 6. LIMITES ACTUELLES DU PROTOTYPE (LUCIDITÉ COMMERCIALE), A. Définition stricte de la cible, A. Le constat du marché (+4 more)

### Community 19 - "Feature Specification: [FEATURE NAME]"
Cohesion: 0.15
Nodes (12): Assumptions, Edge Cases, Feature Specification: [FEATURE NAME], Functional Requirements, Key Entities *(include if feature involves data)*, Measurable Outcomes, Requirements *(mandatory)*, Success Criteria *(mandatory)* (+4 more)

### Community 20 - "Countdown Video"
Cohesion: 0.17
Nodes (11): Countdown Video, Deliver & verify (rendered stills → MP4), Digit roll / flip transitions, Frame-accurate countdown (Remotion → MP4), Looping background, Output checklist, Reference files, The one rule: drive the number from the clock, never a tick (+3 more)

### Community 21 - "AGENT404 · RAPPORT DE TRAÇABILITÉ & SOURCING AUDIT"
Cohesion: 0.17
Nodes (11): 1. Environnement technique & Outils réellement mobilisés, 2. Synthèse quantitative du pipeline de sourcing, 3. Analyse des motifs d'exclusion (18 dossiers archivés), 4. Répartition du lot retenu (30 prospects qualifiés), 5. Limites méthodologiques & Transparence sur les données, A. Par Score, AGENT404 · RAPPORT DE TRAÇABILITÉ & SOURCING AUDIT, B. Par Priorité Commerciale (+3 more)

### Community 22 - "speckit-plan/SKILL.md"
Cohesion: 0.18
Nodes (10): Completion Report, Done When, Key rules, Mandatory Post-Execution Hooks, Outline, Phase 0: Outline & Research, Phase 1: Design & Contracts, Phases (+2 more)

### Community 23 - "speckit-specify/SKILL.md"
Cohesion: 0.18
Nodes (10): Completion Report, Done When, For AI Generation, Mandatory Post-Execution Hooks, Outline, Pre-Execution Checks, Quick Guidelines, Section Requirements (+2 more)

### Community 24 - "speckit-tasks/SKILL.md"
Cohesion: 0.18
Nodes (10): Checklist Format (REQUIRED), Completion Report, Done When, Mandatory Post-Execution Hooks, Outline, Phase Structure, Pre-Execution Checks, Task Generation Rules (+2 more)

### Community 25 - "3. TABLEAU DÉTAILLÉ DES CHANTIERS ET TÂCHES"
Cohesion: 0.18
Nodes (10): 1. HIÉRARCHIE DES PRIORITÉS, 2. DÉCOUPAGE EN PHASES CHRONOLOGIQUES (75 JOURS RESTANTS), 3. TABLEAU DÉTAILLÉ DES CHANTIERS ET TÂCHES, 4. CE QUE NOUS REFUSONS FORMELLEMENT DE FAIRE AVANT LE 31 DÉCEMBRE, AGENT404 // ROADMAP STRATÉGIQUE ET PLAN DE DÉVELOPPEMENT PRIORISÉ, Phase 1 : Sécurisation de la Référence Technique (Golden Master), Phase 2 : Documentation Stratégique, Financière et Technique, Phase 3 : Amorçage Commercial & Première Signature Client (Semaines 42 à 44 — 18 au 31 octobre 2026) (+2 more)

### Community 26 - "Core Principles"
Cohesion: 0.18
Nodes (10): Core Principles, Governance, [PRINCIPLE_1_NAME], [PRINCIPLE_2_NAME], [PRINCIPLE_3_NAME], [PRINCIPLE_4_NAME], [PRINCIPLE_5_NAME], [PROJECT_NAME] Constitution (+2 more)

### Community 27 - "Core Principles"
Cohesion: 0.18
Nodes (10): Core Principles, Governance, [PRINCIPLE_1_NAME], [PRINCIPLE_2_NAME], [PRINCIPLE_3_NAME], [PRINCIPLE_4_NAME], [PRINCIPLE_5_NAME], [PROJECT_NAME] Constitution (+2 more)

### Community 28 - "founder-board"
Cohesion: 0.20
Nodes (9): founder-board, Output, Rules, Step 0: the idea file, Step 1: brief the board, Step 2: convene, Step 3: the chair's summary, The rule about the three names (+1 more)

### Community 29 - "founder-ops"
Cohesion: 0.20
Nodes (9): founder-ops, Output, Step 1: what the business has to do every day, Step 2: suppliers, Step 3: people, Step 4: routines (SOPs), Step 5: tools, Step 6: licences, permits and insurance (+1 more)

### Community 30 - "AGENT404 // TABLEAU DE BORD DE L'ÉTAT DU PROJET (PROJECT STATUS)"
Cohesion: 0.20
Nodes (9): 1. TABLEAU DE BORD EXÉCUTIF, 2. SITUATION FINANCIÈRE RÉELLE (FAITS VS OBJECTIFS), 3. ÉTAT D'AVANCEMENT TECHNIQUE DU MOTEUR, 4. ÉTAT RÉEL DES DEUX OFFRES COMMERCIALES, 5. BLOCAGES PRINCIPAUX, 6. PROCHAINE ACTION PRIORITAIRE UNIQUE, A. Réalisations confirmées [FAIT VÉRIFIÉ], AGENT404 // TABLEAU DE BORD DE L'ÉTAT DU PROJET (PROJECT STATUS) (+1 more)

### Community 31 - "AGENT404 — Stratégie Marketing & Plan de Lancement"
Cohesion: 0.20
Nodes (9): 1. Données Probantes & Enseignements du Panel Acheteurs, 2. Déclaration de Positionnement, 3. Canaux de Distribution Ciblés, 4. Les 10 Hooks d'Acquisition (Calibrés pour stopper le scroll en 3s), 5. Calendrier de Campagne sur 30 Jours, AGENT404 — Stratégie Marketing & Plan de Lancement, Version A (Orientée Gain de Temps & Délégation), Version B (Orientée Identité & Rejet des Avatars IA — RECOMMANDÉE) (+1 more)

### Community 32 - "founder-consumer"
Cohesion: 0.22
Nodes (8): founder-consumer, Honest limits, say them once, Output, Step 1: the target customer, Step 2: the pitch, Step 4: read it to the user, The brief every buyer gets, The tool

### Community 33 - "founder-marketing"
Cohesion: 0.22
Nodes (8): founder-marketing, Output, Rules, Step 1: read the evidence, Step 2: positioning, Step 3: channels, Step 4: the 30-day campaign, Step 5: budget and numbers

### Community 34 - "founder-offer"
Cohesion: 0.22
Nodes (8): founder-offer, Output, Rules, Step 1: read what is already known, Step 2: the problem list, Step 3: solutions, trimmed and stacked, Step 4: score it, Step 5: re-test it

### Community 35 - "Lower-Third Component — runnable code"
Cohesion: 0.22
Nodes (8): 1. Remotion component (props-driven, frame-deterministic), 2. CSS / HTML version (no dependencies), Batch: one branded clip per person, Built by the team behind iart.ai, Lower-Third Component — runnable code, Quick reference, Roster → many instances (one design, a whole panel), Wipe-bar variant (broadcast feel)

### Community 36 - "Retention Pacing — Short-Form Video Reference"
Cohesion: 0.22
Nodes (8): 1. A complete `<Short>` composition, 2. The 9:16 safe-area overlay (dev-only), 3. Hook pattern library, 4. Retention-curve debugging, 5. Per-platform safe zones, 6. Template × topic — batch output, Built by the team behind iart.ai, Retention Pacing — Short-Form Video Reference

### Community 37 - "#10 · Missive (Philippe Lehoux — CEO & Co-fondateur)"
Cohesion: 0.22
Nodes (9): #10 · Missive (Philippe Lehoux — CEO & Co-fondateur), 1. Raison de son classement dans le Top 10, 2. Preuves commerciales & Éléments factuels, 3. Diagnostic du besoin vidéo, 4. Offre recommandée & Modèle économique, 5. Angle d'approche personnalisé (Anti-slop), 6. Message d'approche prêt à l'envoi (LinkedIn / Réseau Pro), 7. Concept de micro-démo personnalisée (15 secondes) (+1 more)

### Community 38 - "#1 · Typebot (Baptiste Arnaud — Fondateur & Créateur)"
Cohesion: 0.22
Nodes (9): 1. Raison de son classement dans le Top 10, #1 · Typebot (Baptiste Arnaud — Fondateur & Créateur), 2. Preuves commerciales & Éléments factuels, 3. Diagnostic du besoin vidéo, 4. Offre recommandée & Modèle économique, 5. Angle d'approche personnalisé (Anti-slop), 6. Message d'approche prêt à l'envoi (LinkedIn / Réseau Pro), 7. Concept de micro-démo personnalisée (15 secondes) (+1 more)

### Community 39 - "#4 · Noqode (Amaury de Luca — Fondateur & CEO)"
Cohesion: 0.22
Nodes (9): 1. Raison de son classement dans le Top 10, 2. Preuves commerciales & Éléments factuels, 3. Diagnostic du besoin vidéo, #4 · Noqode (Amaury de Luca — Fondateur & CEO), 4. Offre recommandée & Modèle économique, 5. Angle d'approche personnalisé (Anti-slop), 6. Message d'approche prêt à l'envoi (LinkedIn / Réseau Pro), 7. Concept de micro-démo personnalisée (15 secondes) (+1 more)

### Community 40 - "#5 · Breakcold (Arnaud Belinga — CEO & Co-fondateur)"
Cohesion: 0.22
Nodes (9): 1. Raison de son classement dans le Top 10, 2. Preuves commerciales & Éléments factuels, 3. Diagnostic du besoin vidéo, 4. Offre recommandée & Modèle économique, 5. Angle d'approche personnalisé (Anti-slop), #5 · Breakcold (Arnaud Belinga — CEO & Co-fondateur), 6. Message d'approche prêt à l'envoi (LinkedIn / Réseau Pro), 7. Concept de micro-démo personnalisée (15 secondes) (+1 more)

### Community 41 - "#6 · Tally (Marie Martens — Co-fondatrice & Head of Growth)"
Cohesion: 0.22
Nodes (9): 1. Raison de son classement dans le Top 10, 2. Preuves commerciales & Éléments factuels, 3. Diagnostic du besoin vidéo, 4. Offre recommandée & Modèle économique, 5. Angle d'approche personnalisé (Anti-slop), 6. Message d'approche prêt à l'envoi (LinkedIn / Réseau Pro), #6 · Tally (Marie Martens — Co-fondatrice & Head of Growth), 7. Concept de micro-démo personnalisée (15 secondes) (+1 more)

### Community 42 - "#7 · Contournement (Alexis Kovalenko — Co-fondateur)"
Cohesion: 0.22
Nodes (9): 1. Raison de son classement dans le Top 10, 2. Preuves commerciales & Éléments factuels, 3. Diagnostic du besoin vidéo, 4. Offre recommandée & Modèle économique, 5. Angle d'approche personnalisé (Anti-slop), 6. Message d'approche prêt à l'envoi (LinkedIn / Réseau Pro), 7. Concept de micro-démo personnalisée (15 secondes), #7 · Contournement (Alexis Kovalenko — Co-fondateur) (+1 more)

### Community 43 - "#8 · Axonaut (Nicolas Lemonnier — CEO & Co-fondateur)"
Cohesion: 0.22
Nodes (9): 1. Raison de son classement dans le Top 10, 2. Preuves commerciales & Éléments factuels, 3. Diagnostic du besoin vidéo, 4. Offre recommandée & Modèle économique, 5. Angle d'approche personnalisé (Anti-slop), 6. Message d'approche prêt à l'envoi (LinkedIn / Réseau Pro), 7. Concept de micro-démo personnalisée (15 secondes), #8 · Axonaut (Nicolas Lemonnier — CEO & Co-fondateur) (+1 more)

### Community 44 - "#9 · Dust.tt (Gabriel Hubert — CEO & Co-fondateur)"
Cohesion: 0.22
Nodes (9): 1. Raison de son classement dans le Top 10, 2. Preuves commerciales & Éléments factuels, 3. Diagnostic du besoin vidéo, 4. Offre recommandée & Modèle économique, 5. Angle d'approche personnalisé (Anti-slop), 6. Message d'approche prêt à l'envoi (LinkedIn / Réseau Pro), 7. Concept de micro-démo personnalisée (15 secondes), 8. Objection probable & Traitement commercial (+1 more)

### Community 45 - "#2 · Piloterr (Josselin Liebe — Fondateur & CEO)"
Cohesion: 0.22
Nodes (9): 1. Raison de son classement dans le Top 10, #2 · Piloterr (Josselin Liebe — Fondateur & CEO), 2. Preuves commerciales & Éléments factuels, 3. Diagnostic du besoin vidéo, 4. Offre recommandée & Modèle économique, 5. Angle d'approche personnalisé (Anti-slop), 6. Message d'approche prêt à l'envoi (LinkedIn / Réseau Pro), 7. Concept de micro-démo personnalisée (15 secondes) (+1 more)

### Community 46 - "#3 · Pharow (Bruno Laporte — CEO & Co-fondateur)"
Cohesion: 0.22
Nodes (9): 1. Raison de son classement dans le Top 10, 2. Preuves commerciales & Éléments factuels, 3. Diagnostic du besoin vidéo, #3 · Pharow (Bruno Laporte — CEO & Co-fondateur), 4. Offre recommandée & Modèle économique, 5. Angle d'approche personnalisé (Anti-slop), 6. Message d'approche prêt à l'envoi (LinkedIn / Réseau Pro), 7. Concept de micro-démo personnalisée (15 secondes) (+1 more)

### Community 47 - "Implementation Plan: [FEATURE]"
Cohesion: 0.22
Nodes (8): Complexity Tracking, Constitution Check, Documentation (this feature), Implementation Plan: [FEATURE], Project Structure, Source Code (repository root), Summary, Technical Context

### Community 48 - "founder-brand"
Cohesion: 0.25
Nodes (7): founder-brand, Output, Rules, Step 1: read the brief, Step 2: name candidates, Step 3: voice and promise, Step 4: the look, as a brief

### Community 49 - "founder-competitors"
Cohesion: 0.25
Nodes (7): founder-competitors, Output, Step 1: who is there, Step 2: the facts, Step 3: what their customers say, Step 4: the map and the gap, The rules

### Community 50 - "founder-plan"
Cohesion: 0.25
Nodes (7): founder-plan, Output, Rules, Step 1: see what is there, Step 2: the summary, Step 3: compile, Step 4: the one-pager

### Community 51 - "founder-pricing"
Cohesion: 0.25
Nodes (7): founder-pricing, Output, Rules, Step 1: what buyers said, Step 2: what competitors charge, Step 3: what the business needs, Step 4: decide

### Community 52 - "speckit-checklist/SKILL.md"
Cohesion: 0.25
Nodes (7): Anti-Examples: What NOT To Do, Checklist Purpose: "Unit Tests for English", Example Checklist Types & Sample Items, Execution Steps, Post-Execution Checks, Pre-Execution Checks, User Input

### Community 53 - "Buyer panel: AGENT404 (Moteur & Studio de Vidéos Verticales Programmatiques B2B)"
Cohesion: 0.25
Nodes (7): Buyer panel: AGENT404 (Moteur & Studio de Vidéos Verticales Programmatiques B2B), By buying behaviour, By income, By segment, What would flip a no, Why they buy, Why they pass

### Community 54 - "Countdown Cookbook"
Cohesion: 0.29
Nodes (6): 1. Configurable Remotion countdown (mm:ss + dd:hh:mm:ss), 2. Count down to a fixed date (live web component), 3. "Starting soon" stream screen, 4. Seamless looping background, Built by the team behind iart.ai, Countdown Cookbook

### Community 55 - "founder-cfo"
Cohesion: 0.29
Nodes (6): founder-cfo, Output, Rules, Step 1: gather the inputs, Step 2: run it, Step 3: the CFO's note

### Community 56 - "founder-launch"
Cohesion: 0.29
Nodes (6): founder-launch, Output, Step 1: test before you spend, Step 2: the countdown, Step 3: launch day, Step 4: the first 30 days

### Community 57 - "speckit-clarify/SKILL.md"
Cohesion: 0.29
Nodes (6): Completion Report, Done When, Mandatory Post-Execution Hooks, Outline, Pre-Execution Checks, User Input

### Community 58 - "speckit-implement/SKILL.md"
Cohesion: 0.29
Nodes (6): Completion Report, Done When, Mandatory Post-Execution Hooks, Outline, Pre-Execution Checks, User Input

### Community 59 - "Synthèse Exécutive : AGENT404"
Cohesion: 0.29
Nodes (6): 1. Ce que fait l'entreprise et pour qui, 2. Le verdict et les chiffres clés, 3. Consensus et divergences entre le Conseil (Board) et le Panel Acheteurs, 4. Le risque majeur et sa parade, 5. Ce dont le fondateur a besoin pour démarrer, Synthèse Exécutive : AGENT404

### Community 60 - "Digit Flip & Roll Transitions"
Cohesion: 0.33
Nodes (5): Choosing, Digit Flip & Roll Transitions, Flip card (split-flap), Odometer reel (Remotion, frame-driven), Shared idea

### Community 61 - "speckit-constitution/SKILL.md"
Cohesion: 0.33
Nodes (5): Outline, Post-Execution Checks, Pre-Execution Checks, Scope Guard, User Input

### Community 62 - "speckit-taskstoissues/SKILL.md"
Cohesion: 0.33
Nodes (5): Deprecation Notice, Outline, Post-Execution Checks, Pre-Execution Checks, User Input

### Community 63 - "Monopoly lens"
Cohesion: 0.33
Nodes (5): If FUND IF: the conditions, Monopoly lens, The questions I would ask the founder, What is strong, What would kill it (the top 3, most dangerous first)

### Community 64 - "Offers lens"
Cohesion: 0.33
Nodes (5): If FUND IF: the conditions, Offers lens, The questions I would ask the founder, What is strong, What would kill it (the top 3, most dangerous first)

### Community 65 - "Product lens"
Cohesion: 0.33
Nodes (5): If FUND IF: the conditions, Product lens, The questions I would ask the founder, What is strong, What would kill it (the top 3, most dangerous first)

### Community 66 - "Unit economics: AGENT404 (Programmatic Video Engine & Studio)"
Cohesion: 0.33
Nodes (5): One video, The margin that matters, Unit economics: AGENT404 (Programmatic Video Engine & Studio), What if, Year 1, month by month

### Community 67 - "AGENT404 — Stratégie Tarifaire & Grille de Prix"
Cohesion: 0.33
Nodes (5): 1. Données du Panel & Sensibilité Prix (Van Westendorp), 2. Comparatif Concurrentiel Direct & Substituts, 3. L'Échelle de Valeur (Price Ladder), 4. Offre d'Amorçage & Dérisquage (Launch Offer), AGENT404 — Stratégie Tarifaire & Grille de Prix

### Community 68 - "Project Profile: video (Agent404 // Cyber-Mint)"
Cohesion: 0.40
Nodes (4): 1. Stack & Architecture, 2. Resource Affinity (Auto-Routed), 3. Local Constraints & Conventions, Project Profile: video (Agent404 // Cyber-Mint)

### Community 69 - "Caption Animation"
Cohesion: 0.40
Nodes (4): Caption Animation, Example prompts, What's inside, When it activates

### Community 70 - "Countdown Video"
Cohesion: 0.40
Nodes (4): Countdown Video, Example prompts, What's inside, When it activates

### Community 71 - "The three lenses"
Cohesion: 0.40
Nodes (4): The Monopoly lens, The Offers lens, The Product lens, The three lenses

### Community 72 - "Lower Thirds"
Cohesion: 0.40
Nodes (4): Example prompts, Lower Thirds, What's inside, When it activates

### Community 73 - "Short-Form Video"
Cohesion: 0.40
Nodes (4): Example prompts, Short-Form Video, What's inside, When it activates

### Community 74 - "AGENT404 — Board of Directors Verdict"
Cohesion: 0.40
Nodes (4): 1. Risques critiques partagés (soulevés par plusieurs membres), 2. Checklist des conditions suspensives du Board, 3. La version la plus forte de ce business (Vision du Conseil), AGENT404 — Board of Directors Verdict

### Community 75 - "AGENT404 — Board Brief"
Cohesion: 0.40
Nodes (4): AGENT404 — Board Brief, L'Idée & L'Offre, La Cible, Les Chiffres & Contraintes

### Community 76 - "[CHECKLIST TYPE] Checklist: [FEATURE NAME]"
Cohesion: 0.40
Nodes (4): [Category 1], [Category 2], [CHECKLIST TYPE] Checklist: [FEATURE NAME], Notes

## Knowledge Gaps
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Sélection resserrée pour conversion rapide vers l'objectif 2 000 000 FCFA` connect `Sélection resserrée pour conversion rapide vers l'objectif 2 000 000 FCFA` to `#10 · Missive (Philippe Lehoux — CEO & Co-fondateur)`, `#1 · Typebot (Baptiste Arnaud — Fondateur & Créateur)`, `#4 · Noqode (Amaury de Luca — Fondateur & CEO)`, `#5 · Breakcold (Arnaud Belinga — CEO & Co-fondateur)`, `#6 · Tally (Marie Martens — Co-fondatrice & Head of Growth)`, `#7 · Contournement (Alexis Kovalenko — Co-fondateur)`, `#8 · Axonaut (Nicolas Lemonnier — CEO & Co-fondateur)`, `#9 · Dust.tt (Gabriel Hubert — CEO & Co-fondateur)`, `#2 · Piloterr (Josselin Liebe — Fondateur & CEO)`, `#3 · Pharow (Bruno Laporte — CEO & Co-fondateur)`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.09988385598141696 - nodes in this community are weakly interconnected._
- **Why does `AGENT404 // Moteur de Vidéo Programmatique & Studio B2B` connect `AGENT404 // Moteur de Vidéo Programmatique & Studio B2B` to `build_master_timeline.py`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Should `build_master_timeline.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08585858585858586 - nodes in this community are weakly interconnected._
- **Should `AGENT404 · Business plan` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._
- **Should `common.sh` be split into smaller, more focused modules?**
  _Cohesion score 0.11470985155195682 - nodes in this community are weakly interconnected._
- **Should `Tasks: [FEATURE NAME]` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._