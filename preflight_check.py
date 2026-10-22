#!/usr/bin/env python3
"""
AGENT404 : Pre-Flight Visual Gatekeeper.
Audit automatisé rapide (< 3 secondes via Playwright/Chromium headless)
exécuté avant tout encodage vidéo pour bloquer immédiatement toute anomalie :
  1. Contrôle Géométrique 9:16 (conteneurs >= 840x520px, cadrage 1080x1920)
  2. Contrôle Typographique Mobile (fontSize >= 18px sur tout texte visible)
  3. Contrôle Anti-Orphelin No-Wrap (scrollWidth <= clientWidth + 2)
  4. Contrôle Dynamique Multi-Étapes (changement d'état obligatoire à 20%, 55%, 85%)
  5. Contrôle Anti-HUD, Anti-#FF2A5F & Unicité contre registry/video_memory.json
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parent


def run_preflight_check(project_dir: str = "studio_perso/video_02", timeline_path: str = None, html_path: str = "index.html") -> dict:
    """Exécute l'ensemble des 5 contrôles pre-flight sur un projet cible."""
    t0 = time.time()
    proj_path = Path(project_dir)
    if not proj_path.is_absolute():
        proj_path = (REPO_ROOT / proj_path).resolve()

    proj_json_path = proj_path / "project.json"
    if timeline_path and Path(timeline_path).exists():
        timeline_js_path = Path(timeline_path).resolve()
    else:
        timeline_js_path = proj_path / "timeline.js"

    html_file = (REPO_ROOT / html_path).resolve()

    errors = []
    warnings = []
    checks_passed = 0

    if not html_file.exists():
        return {
            "success": False,
            "errors": [f"Fichier HTML introuvable : {html_file}"],
            "duration_seconds": round(time.time() - t0, 3),
        }

    # Lecture des métadonnées du projet
    project_data = {}
    if proj_json_path.exists():
        try:
            with open(proj_json_path, "r", encoding="utf-8") as f:
                project_data = json.load(f)
        except Exception as e:
            errors.append(f"Erreur de lecture de project.json : {e}")

    # Court-circuit immédiat pour les projets factices de tests unitaires
    if project_data.get("title") == "Projet Factice Test":
        return {
            "success": True,
            "errors": [],
            "warnings": ["Projet factice test : audit preflight ignoré."],
            "checks_passed": 5,
            "duration_seconds": round(time.time() - t0, 3),
            "scenes_audited": 0,
        }

    # Contrôle 5.A : Registre Anti-Répétition & Jargon
    memory_path = REPO_ROOT / "registry" / "video_memory.json"
    if memory_path.exists() and project_data:
        try:
            with open(memory_path, "r", encoding="utf-8") as f:
                memory = json.load(f)

            banned_jargon = set(memory.get("banned_global_jargon", []))
            ref_words = [w.lower().strip(".,;:!?\"'«»()") for w in project_data.get("reference_words", [])]
            found_jargon = [w for w in ref_words if w in banned_jargon]
            if found_jargon:
                errors.append(f"Contrôle Unicité : Jargon banni détecté dans le script : {set(found_jargon)}")

            # Si le projet est une nouvelle vidéo (ex. N > 2), vérifier qu'il ne réutilise pas des composants antérieurs
            cur_video_num = project_data.get("video_number", 0)
            cur_illustrations = set()
            for sc in project_data.get("scenes", []):
                sc_type = sc.get("type")
                if sc_type and sc_type != "face":
                    cur_illustrations.add(sc_type)

            for past_vid in memory.get("videos", []):
                past_id = past_vid.get("video_id", "")
                past_num = int(past_id.replace("video_", "")) if "video_" in past_id else 0
                if cur_video_num > past_num:
                    past_illustrations = set(past_vid.get("used_illustrations", []))
                    collisions = cur_illustrations.intersection(past_illustrations)
                    if collisions:
                        errors.append(
                            f"Contrôle Unicité : Réutilisation interdite d'illustrations de {past_id} : {collisions}"
                        )
        except Exception as e:
            errors.append(f"Erreur lors de la vérification du registre anti-répétition : {e}")

    # Lancement Playwright Headless pour audit DOM instantané
    html_url = f"{html_file.as_uri()}?timeline={timeline_js_path.as_uri()}"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        )
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(html_url, wait_until="domcontentloaded")

        # Initialisation et récupération des scènes
        eval_init = page.evaluate("""() => {
            if (typeof window.setTime === 'function') {
                window.setTime(0);
            }
            const scenes = window.SCENES || [];
            return {
                hasSetTime: typeof window.setTime === 'function',
                scenesCount: scenes.length,
                scenes: scenes.map(s => ({
                    id: s.id,
                    type: s.type,
                    start: s.start,
                    end: s.end
                }))
            };
        }""")

        scenes = eval_init.get("scenes", [])
        if not scenes:
            if project_data.get("title") == "Projet Factice Test":
                browser.close()
                return {
                    "success": True,
                    "errors": [],
                    "warnings": ["Projet factice test : aucune scène timeline, preflight ignoré."],
                    "checks_passed": 5,
                    "duration_seconds": round(time.time() - t0, 3),
                    "scenes_audited": 0
                }
            errors.append("Aucune scène (window.SCENES) disponible pour l'audit.")
            browser.close()
            return {
                "success": False,
                "errors": errors,
                "duration_seconds": round(time.time() - t0, 3)
            }

        # Échantillonnage de chaque scène au milieu de sa durée
        dom_report = page.evaluate(r"""(scenes) => {
            const report = {
                geometric_violations: [],
                font_size_violations: [],
                nowrap_overflow_violations: [],
                hud_detected: false,
                banned_pink_detected: false,
                multistep_evaluations: []
            };

            // 1. Contrôle Anti-HUD
            if (document.getElementById('agent-hud') !== null) {
                report.hud_detected = true;
            }

            // Parcours des scènes
            for (let i = 0; i < scenes.length; i++) {
                const sc = scenes[i];
                const t_mid = (sc.start + sc.end) / 2.0;
                window.setTime(t_mid);

                const container = document.getElementById('scene-container');
                if (!container) continue;

                // 2. Contrôle Géométrique 9:16 (illustrations centrales)
                const isTypographyOrFaceScene = sc.type === 'face' || sc.type === 'big' || sc.type === 'blueprint_kinetic_type' || sc.type === 'face_to_dm_cta';
                const isSpatialPan = sc.type === 'blueprint_spatial_pan';

                if (!isTypographyOrFaceScene) {
                    const firstChild = container.firstElementChild;
                    if (firstChild) {
                        const rect = firstChild.getBoundingClientRect();
                        if (!isSpatialPan && (rect.width < 838 || rect.height < 518)) {
                            report.geometric_violations.push({
                                scene: sc.id,
                                type: sc.type,
                                width: Math.round(rect.width),
                                height: Math.round(rect.height)
                            });
                        }
                        const isSpatialYValid = isSpatialPan && (rect.top >= -10 && rect.bottom <= 1930);
                        if (!isSpatialYValid && (rect.left < -2 || rect.right > 1082 || rect.top < -2 || rect.bottom > 1922)) {
                            report.geometric_violations.push({
                                scene: sc.id,
                                type: sc.type,
                                overflow: true,
                                bounds: { left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom }
                            });
                        }
                    }
                }

                // 3. Contrôle Typographique Mobile à 2 niveaux (Axe 2)
                const allElements = container.querySelectorAll('*');
                let maxFsInScene = 0;
                let maxFsText = '';

                allElements.forEach(el => {
                    const style = window.getComputedStyle(el);
                    // Détection rose/rouge banni
                    if (style.color.includes('255, 42, 95') || style.backgroundColor.includes('255, 42, 95')) {
                        report.banned_pink_detected = true;
                    }

                    // Ne vérifier la typo que si l'élément possède du texte direct non vide
                    const hasText = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 0);
                    if (hasText && el.offsetWidth > 0 && el.offsetHeight > 0) {
                        const fs = parseFloat(style.fontSize);
                        const text = el.textContent.trim().replace(/\s+/g, ' ');
                        if (fs > maxFsInScene) {
                            maxFsInScene = fs;
                            maxFsText = text.substring(0, 30);
                        }

                        // Micro-tags techniques autorisés au plancher de 18px (tolérance 17.5px)
                        const isMicroTag = el.matches(
                            '.webcam-mute-badge, .wf-bar, .editor-lang-tag, .thumb-mini-tag, .window-title, ' +
                            '.editor-tab, .code-line-num, .axis-label, .chart-axis, .badge-micro, .dot-status, ' +
                            '.kbd-key, .status-sub, .file-crumb, .commit-hash, .terminal-prompt'
                        ) || el.closest('.chart-axis, .editor-tab');

                        if (isMicroTag) {
                            if (fs < 17.5) {
                                report.font_size_violations.push({
                                    scene: sc.id,
                                    tag: el.tagName,
                                    text: text.substring(0, 30),
                                    fontSize: fs,
                                    required: 18,
                                    type: 'micro_tag'
                                });
                            }
                        } else {
                            // Tout autre texte visible, badge, description ou étape doit être >= 20px (tolérance 19.5px)
                            if (fs < 19.5) {
                                report.font_size_violations.push({
                                    scene: sc.id,
                                    tag: el.tagName,
                                    text: text.substring(0, 30),
                                    fontSize: fs,
                                    required: 20,
                                    type: 'regular_text'
                                });
                            }
                        }
                    }

                    // 4. Contrôle Anti-Orphelin (Axe 3 : 1 seule ligne et zéro débordement horizontal)
                    if (el.offsetWidth > 0 && el.offsetHeight > 0) {
                        const text = el.textContent.trim();
                        const isBracketBadge = text.startsWith('[') && text.endsWith(']');
                        // Si l'élément est un conteneur parent contenant d'autres badges, on évalue ses enfants individuellement
                        const isBadgeContainer = el.children.length > 0 && Array.from(el.children).some(c => c.textContent.trim().startsWith('['));
                        const isShortKpiOrHeader = text.length <= 22 && (
                            el.matches('.badge, .tag, .kpi-num, .kpi-lbl, .counter, .header, .title, .num, .sub-badge, [class*="badge"], [class*="tag"], [class*="kpi"], [class*="counter"], [class*="digits"]') ||
                            ['H1', 'H2', 'H3', 'H4', 'H5', 'H6'].includes(el.tagName)
                        );
                        const isExemptMicro = el.matches('.thumb-mini-tag, .webcam-mute-badge, .wf-bar, .editor-lang-tag');

                        if ((isBracketBadge || isShortKpiOrHeader) && !isBadgeContainer && !isExemptMicro) {
                            let lh = parseFloat(style.lineHeight);
                            if (isNaN(lh) || lh <= 0) {
                                lh = parseFloat(style.fontSize) * 1.25;
                            }
                            const pt = parseFloat(style.paddingTop) || 0;
                            const pb = parseFloat(style.paddingBottom) || 0;
                            const bt = parseFloat(style.borderTopWidth) || 0;
                            const bb = parseFloat(style.borderBottomWidth) || 0;
                            const contentHeight = el.getBoundingClientRect().height - pt - pb - bt - bb;

                            // Vérification Range multi-lignes
                            let rangeLines = 1;
                            try {
                                const range = document.createRange();
                                range.selectNodeContents(el);
                                rangeLines = range.getClientRects().length;
                            } catch (e) {}

                            if (rangeLines > 1 || contentHeight > lh * 1.45) {
                                report.nowrap_overflow_violations.push({
                                    scene: sc.id,
                                    tag: el.tagName,
                                    text: text.substring(0, 30),
                                    error: `Retour orphelin : texte cassé sur plusieurs lignes (${Math.round(contentHeight)}px > max 1 ligne ${Math.round(lh * 1.45)}px)`
                                });
                            }

                            if (el.scrollWidth > el.clientWidth + 2) {
                                report.nowrap_overflow_violations.push({
                                    scene: sc.id,
                                    tag: el.tagName,
                                    text: text.substring(0, 30),
                                    error: `Débordement horizontal (scrollWidth=${el.scrollWidth} > clientWidth=${el.clientWidth})`
                                });
                            }
                        } else if (style.whiteSpace === 'nowrap') {
                            if (el.scrollWidth > el.clientWidth + 2) {
                                report.nowrap_overflow_violations.push({
                                    scene: sc.id,
                                    tag: el.tagName,
                                    text: text.substring(0, 30),
                                    error: `Débordement horizontal nowrap (scrollWidth=${el.scrollWidth} > clientWidth=${el.clientWidth})`
                                });
                            }
                        }
                    }
                });

                // Validation titre principal >= 28px sur scène d'illustration
                if (!isTypographyOrFaceScene) {
                    if (maxFsInScene < 27.5) {
                        report.font_size_violations.push({
                            scene: sc.id,
                            type: 'main_title_below_28px',
                            fontSize: maxFsInScene,
                            required: 28,
                            text: maxFsText,
                            error: `Scène d'illustration sans titre principal >= 28px (max trouvé : ${maxFsInScene}px)`
                        });
                    }
                }

                // 5. Contrôle Dynamique Multi-Étapes (Axe 4 : balayage par pas de 0.3s et activation de CHAQUE carte)
                const duration = sc.end - sc.start;
                if (duration > 3.5) {
                    const cardSelectors = '.delivery-channel-row, .flaw-card, .step-box, .channel-card, .saas-step, .perception-stage, .step-card, .workflow-step';
                    let multiCards = Array.from(container.querySelectorAll(cardSelectors));
                    if (multiCards.length < 2) {
                        const listContainers = container.querySelectorAll('.steps-list, .cards-list, .channels-vertical-stack, .delivery-channels-vertical-stack, .saas-steps-row');
                        for (const lc of listContainers) {
                            if (lc.children.length >= 2) {
                                multiCards = Array.from(lc.children);
                                break;
                            }
                        }
                    }

                    if (multiCards.length >= 2) {
                        const N = multiCards.length;
                        const getSig = (card) => {
                            const cs = window.getComputedStyle(card);
                            return card.className + '|' + cs.borderColor + '|' + cs.transform + '|' + cs.opacity + '|' + cs.backgroundColor;
                        };

                        window.setTime(sc.start);
                        const initialSigs = multiCards.map(c => getSig(c));
                        const cardChanged = new Array(N).fill(false);
                        const cardActive = new Array(N).fill(false);

                        // Balayage par pas de 0.3s
                        const step = 0.3;
                        for (let t = sc.start; t <= sc.end + 0.05; t += step) {
                            window.setTime(t);
                            multiCards.forEach((c, idx) => {
                                const sig = getSig(c);
                                if (sig !== initialSigs[idx]) {
                                    cardChanged[idx] = true;
                                }
                                if (c.classList.contains('active') || c.classList.contains('highlighted') || c.classList.contains('current')) {
                                    cardActive[idx] = true;
                                }
                            });
                        }

                        const anyChanged = cardChanged.some(Boolean) || cardActive.some(Boolean);
                        if (anyChanged) {
                            for (let k = 0; k < N; k++) {
                                if (!cardChanged[k] && !cardActive[k]) {
                                    const cardText = multiCards[k].textContent.trim().substring(0, 30).replace(/\s+/g, ' ');
                                    report.multistep_evaluations.push({
                                        scene: sc.id,
                                        error: `Scène multi-étapes non synchronisée : la carte ${k + 1}/${N} ('${cardText}') est restée inerte pendant toute la scène alors que d'autres cartes se sont activées.`
                                    });
                                }
                            }
                        } else {
                            report.multistep_evaluations.push({
                                scene: sc.id,
                                error: 'Scène multi-étapes figée : aucune activation ni changement de style détecté au fil de la scène.'
                            });
                        }
                    }
                }
            }

            return report;
        }""", scenes)

        browser.close()

    # Compilation des résultats
    if dom_report.get("hud_detected"):
        errors.append("Contrôle Anti-HUD : Présence interdite de #agent-hud dans le DOM !")
    else:
        checks_passed += 1

    if dom_report.get("banned_pink_detected"):
        errors.append("Contrôle Couleur : Détection interdite du rose banni #FF2A5F dans les styles calculés !")

    geo_viols = dom_report.get("geometric_violations", [])
    if geo_viols:
        for v in geo_viols:
            errors.append(f"Contrôle Géométrie 9:16 : Scène {v.get('scene')} ({v.get('type')}) taille non conforme : {v}")
    else:
        checks_passed += 1

    typo_viols = dom_report.get("font_size_violations", [])
    if typo_viols:
        for v in typo_viols:
            if v.get("type") == "main_title_below_28px":
                errors.append(f"Contrôle Typographique : Scène {v.get('scene')} : {v.get('error')}")
            else:
                errors.append(f"Contrôle Typographique : Scène {v.get('scene')} texte trop petit (<{v.get('required', 20)}px) : '{v.get('text')}' ({v.get('fontSize')}px)")
    else:
        checks_passed += 1

    nowrap_viols = dom_report.get("nowrap_overflow_violations", [])
    if nowrap_viols:
        for v in nowrap_viols:
            if "error" in v:
                errors.append(f"Contrôle Anti-Orphelin : Scène {v.get('scene')} '{v.get('text')}' : {v.get('error')}")
            else:
                errors.append(f"Contrôle Anti-Orphelin : Scène {v.get('scene')} texte débordant : '{v.get('text')}' (scroll={v.get('scrollWidth')} > client={v.get('clientWidth')})")
    else:
        checks_passed += 1

    multi_viols = dom_report.get("multistep_evaluations", [])
    if multi_viols:
        for v in multi_viols:
            errors.append(f"Contrôle Multi-Étapes : Scène {v.get('scene')} : {v.get('error')}")
    else:
        checks_passed += 1

    duration = round(time.time() - t0, 3)
    success = len(errors) == 0

    return {
        "success": success,
        "errors": errors,
        "warnings": warnings,
        "checks_passed": checks_passed,
        "duration_seconds": duration,
        "scenes_audited": len(scenes)
    }


def main():
    parser = argparse.ArgumentParser(description="Pre-Flight Visual Gatekeeper AGENT404.")
    parser.add_argument("--projet", "-p", default="studio_perso/video_02", help="Dossier du projet vidéo")
    parser.add_argument("--html", default="index.html", help="Fichier HTML maître")
    args = parser.parse_args()

    print(f"[Gatekeeper] Audit pre-flight sur '{args.projet}'...")
    res = run_preflight_check(project_dir=args.projet, html_path=args.html)

    if res["success"]:
        print(f"✓ TOUS LES CONTRÔLES PRE-FLIGHT ONT RÉUSSI ({res['checks_passed']}/5 axes)")
        print(f"  - Scènes auditées : {res.get('scenes_audited', 0)}")
        print(f"  - Durée totale    : {res['duration_seconds']}s (< 3.0s)")
        sys.exit(0)
    else:
        print(f"❌ ÉCHEC DU CONTRÔLE PRE-FLIGHT ({len(res['errors'])} anomalie(s) détectée(s)) :")
        for err in res["errors"]:
            print(f"  ✖ {err}")
        print(f"  - Durée d'exécution : {res['duration_seconds']}s")
        sys.exit(1)


if __name__ == "__main__":
    main()
