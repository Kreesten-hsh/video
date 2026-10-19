/**
 * MOTEUR D'ANIMATION DÉTERMINISTE VANILLA JS
 * Rendu frame-par-frame 100% déterministe via window.setTime(t)
 */

(function () {
  const canvas = document.getElementById("video-canvas");
  const subtitlesBox = document.getElementById("subtitles-box");
  const sceneContainer = document.getElementById("scene-container");

  let subtitleChunks = [];
  let currentChunkIndex = -1;
  let activeSceneIndex = -1;
  let currentBg = "";

  /**
   * Découpe la liste linéaire de mots en paquets continus de 3 à 5 mots (défaut 4).
   */
  function buildSubtitleChunks(words) {
    if (!words || words.length === 0) return [];
    const chunks = [];
    const chunkSize = 4;

    for (let i = 0; i < words.length; i += chunkSize) {
      const slice = words.slice(i, i + chunkSize);
      chunks.push({
        start: slice[0].start,
        end: slice[slice.length - 1].end,
        words: slice
      });
    }
    return chunks;
  }

  function initData() {
    subtitleChunks = buildSubtitleChunks(window.WORDS || []);
    if (window.PROJECT_CONFIG && window.PROJECT_CONFIG.theme) {
      const root = document.documentElement;
      for (const [key, val] of Object.entries(window.PROJECT_CONFIG.theme)) {
        root.style.setProperty(`--${key}`, val);
      }
    }
  }

  /**
   * Pilote le décor dynamique de fond sur #video-canvas selon scene.data.bg et t
   */
  function updateBackground(bgType, t, progress) {
    const desired = (bgType === "diamonds" || bgType === "circles") ? `bg-${bgType}` : "bg-grid";
    if (currentBg !== desired) {
      currentBg = desired;
      canvas.className = desired;
    }
    canvas.style.backgroundColor = "";
    canvas.style.backgroundImage = "";
    canvas.style.backgroundSize = "";
    canvas.style.backgroundPosition = "";
  }

  /**
   * Fonction globale de rendu instantané à l'instant t (en secondes)
   */
  window.setTime = function (t) {
    if (subtitleChunks.length === 0 && window.WORDS && window.WORDS.length > 0) {
      initData();
    }

    // 1. Sous-titres dynamiques (Top)
    updateSubtitles(t);

    // 2. Scène centrale & inférieure
    updateScenes(t);
  };

  function updateSubtitles(t) {
    if (subtitleChunks.length === 0) return;

    let chunkIdx = subtitleChunks.findIndex(c => t >= c.start && t <= c.end);
    if (chunkIdx === -1) {
      for (let i = 0; i < subtitleChunks.length; i++) {
        if (t < subtitleChunks[i].start) {
          chunkIdx = Math.max(0, i - 1);
          break;
        }
      }
      if (chunkIdx === -1) chunkIdx = subtitleChunks.length - 1;
    }

    const chunk = subtitleChunks[chunkIdx];
    if (!chunk) return;

    if (chunkIdx !== currentChunkIndex) {
      currentChunkIndex = chunkIdx;
      subtitlesBox.innerHTML = chunk.words
        .map((w, idx) => `<span class="sub-word word" id="sw-${idx}">${w.word}</span>`)
        .join(" ");
    }

    chunk.words.forEach((w, idx) => {
      const el = document.getElementById(`sw-${idx}`);
      if (!el) return;
      if (t >= w.start && t <= w.end) {
        el.classList.add("active");
      } else {
        el.classList.remove("active");
      }
    });
  }

  function updateScenes(t) {
    if (!window.SCENES || window.SCENES.length === 0) return;

    const sceneIdx = window.SCENES.findIndex(s => t >= s.start && t < s.end);
    if (sceneIdx === -1) {
      sceneContainer.innerHTML = "";
      activeSceneIndex = -1;
      updateBackground("grid", t, 0);
      return;
    }

    const scene = window.SCENES[sceneIdx];
    const duration = scene.end - scene.start;
    const progress = Math.min(1, Math.max(0, (t - scene.start) / Math.max(0.001, duration)));
    const elapsed = t - scene.start;

    // Décor dynamique piloté par t et progress
    updateBackground(scene.data && scene.data.bg, t, progress);

    // Injection DOM au changement de scène
    if (sceneIdx !== activeSceneIndex) {
      activeSceneIndex = sceneIdx;
      sceneContainer.innerHTML = renderComponent(scene.type, scene.data);
    }

    // Animation continue déterministe avec physique d'overshoot
    animateComponent(scene.type, scene.data, progress, elapsed, t);
  }

  function renderComponent(type, data) {
    switch (type) {
      case "face":
        const isHeadOnly = data.avatar && data.avatar.includes("mini");
        const badgeText = data.badge || data.label || "";
        let heroTitleHtml = "";
        if (data.hero_title) {
          let formattedTitle = data.hero_title;
          if (data.highlight_word && formattedTitle.includes(data.highlight_word)) {
            formattedTitle = formattedTitle.replace(
              data.highlight_word,
              `<span class="highlight">${data.highlight_word}</span>`
            );
          }
          heroTitleHtml = `<div class="face-hero-title" id="face-hero-title">${formattedTitle}</div>`;
        }
        return `
          ${heroTitleHtml}
          <div class="comp-face ${isHeadOnly ? 'face-headonly' : ''}" id="comp-face">
            <img src="${data.avatar}" alt="Avatar" class="avatar-sticker" id="avatar-img" />
            ${badgeText ? `<div class="face-badge" id="face-badge">${badgeText}</div>` : ""}
          </div>
        `;
      case "big":
        const isLong = (data.text || "").length > 13;
        const fontSize = isLong ? "56px" : "68px";
        return `
          <div class="comp-big" id="comp-big">
            <div class="big-box" style="font-size: ${fontSize};">${data.text}</div>
            ${data.sub ? `<div class="big-sub">${data.sub}</div>` : ""}
          </div>
        `;
      case "list":
        return `
          <div class="comp-list" id="comp-list">
            ${data.header ? `<div class="list-header">${data.header}</div>` : ""}
            ${(data.items || []).map((item, i) => `
              <div class="list-item list-row" id="list-item-${i}">
                <div class="item-num list-num">${String(i + 1).padStart(2, '0')}</div>
                <div class="item-text list-text">${item}</div>
              </div>
            `).join("")}
          </div>
        `;
      case "window":
        return `
          <div class="comp-window" id="comp-window">
            <div class="window-header">
              <div class="window-dots">
                <div class="dot red"></div>
                <div class="dot yellow"></div>
                <div class="dot green"></div>
              </div>
              <div class="window-title">${data.title || "agent404_terminal.sh"}</div>
              <div style="width: 70px;"></div>
            </div>
            <div class="window-body"><span id="typewriter-content"></span><span class="cursor">▋</span></div>
          </div>
        `;
      case "cards":
        const cardsList = data.cards || [];
        const isSingle = cardsList.length === 1;
        return `
          <div class="comp-cards ${isSingle ? 'single-card' : ''}" id="comp-cards">
            ${cardsList.map((c, i) => `
              <div class="card-item" id="card-item-${i}">
                <div class="card-icon">${c.icon}</div>
                <div class="card-content">
                  <div class="card-title">${c.title}</div>
                  ${c.sub ? `<div class="card-sub">${c.sub}</div>` : ""}
                </div>
              </div>
            `).join("")}
          </div>
        `;
      case "engine_arch":
        return `
          <div class="comp-engine-arch comp-engine" id="comp-engine-arch">
            <div class="arch-block python">
              <div class="arch-icon">🐍</div>
              <div class="arch-info">
                <div class="arch-title">PYTHON 3.12</div>
                <div class="arch-desc">Audio • Faster-Whisper • FFmpeg</div>
              </div>
            </div>
            <div class="arch-middle">
              <div class="arch-gear" id="arch-gear">⚙️</div>
              <div class="arch-flow-tag">⚡ FLUX RAM STREAM ⚡</div>
            </div>
            <div class="arch-block js">
              <div class="arch-icon">⚡</div>
              <div class="arch-info">
                <div class="arch-title">JAVASCRIPT DOM</div>
                <div class="arch-desc">CSS Motion • 30 FPS Déterministe</div>
              </div>
            </div>
          </div>
        `;
      case "sync_timer":
        return `
          <div class="comp-sync-timer timer-card comp-timer" id="comp-sync-timer">
            <div class="sync-header timer-label">⏱️ ALIGNEMENT TEMPOREL ABSOLU</div>
            <div class="sync-display">
              <div class="sync-digits timer-digits" id="sync-digits">00:21.000 ms</div>
            </div>
            <div class="sync-pills">
              <div class="sync-pill timer-tag" id="sync-pill-0">[CHAQUE]</div>
              <div class="sync-pill timer-tag" id="sync-pill-1">[MOT]</div>
              <div class="sync-pill timer-tag" id="sync-pill-2">[PRÉCIS]</div>
            </div>
          </div>
        `;
      case "emotion_morph":
        return `
          <div class="comp-emotion comp-emotion-morph" id="comp-emotion-morph">
            <div class="emotion-stage">
              <img src="assets/avatars/happy.png" alt="Avatar" class="emotion-img active morph-avatar" id="morph-avatar" />
            </div>
            <div class="emotion-label morph-badge" id="morph-badge">😄 ÉMOTION : ENTHOUSIASTE</div>
          </div>
        `;
      case "ffmpeg_render":
        return `
          <div class="comp-ffmpeg-render comp-ffmpeg ffmpeg-card" id="comp-ffmpeg-render">
            <div class="ffmpeg-header">
              <div class="ffmpeg-title-box ffmpeg-head">🎬 COMPILATION FFmpeg</div>
              <div class="ffmpeg-frame-counter" id="ffmpeg-counter">FRAME 0 / 2200</div>
            </div>
            <div class="ffmpeg-progress-track ffmpeg-bar-bg">
              <div class="ffmpeg-progress-fill ffmpeg-bar-fill" id="ffmpeg-fill"></div>
              <div class="ffmpeg-progress-pct" id="ffmpeg-pct">0%</div>
            </div>
            <div class="ffmpeg-footer-badge">✓ ENCODAGE H.264 ULTRA RAPIDE (30 FPS)</div>
          </div>
        `;
      case "speed_counter":
        return `
          <div class="comp-speed-counter comp-speed speed-card" id="comp-speed-counter">
            <div class="speed-main-box">
              <div class="speed-time speed-title">⏱️ 02:00 MIN</div>
              <div class="speed-sub">DU MÉMO VOCAL AU MP4 FINAL</div>
            </div>
            <div class="speed-compare-zone">
              <div class="speed-row">
                <div class="speed-label speed-row-label">
                  <span>⚡ CODE PYTHON (MOTEUR)</span>
                  <span style="color: #047857; font-weight: 900;">100% PRÊT</span>
                </div>
                <div class="speed-bar-track">
                  <div class="speed-bar-fill code"></div>
                </div>
              </div>
              <div class="speed-row">
                <div class="speed-label speed-row-label">
                  <span>⏳ MONTEUR HUMAIN</span>
                  <span style="color: #090D16; font-weight: 900;">5% EN ATTENTE</span>
                </div>
                <div class="speed-bar-track">
                  <div class="speed-bar-fill human"></div>
                </div>
              </div>
            </div>
          </div>
        `;
      case "split":
        const lTitle = data.leftTitle || data.left_title || "AVANT ❌";
        const rTitle = data.rightTitle || data.right_title || "APRÈS ✅";
        const lItems = data.leftItems || data.left_items || [];
        const rItems = data.rightItems || data.right_items || [];
        return `
          <div class="comp-split" id="comp-split">
            <div class="split-col bad" id="split-col-left">
              <div class="split-badge">${data.left_badge || "IA / MONTEUR ❌"}</div>
              <div class="split-card">
                <div class="split-title">${lTitle}</div>
                <ul class="split-items">
                  ${lItems.map(it => `<li class="split-point">${it}</li>`).join("")}
                </ul>
              </div>
            </div>
            <div class="split-col good" id="split-col-right">
              <div class="split-badge">${data.right_badge || "CODE ✅"}</div>
              <div class="split-card highlight">
                <div class="split-title">${rTitle}</div>
                <ul class="split-items">
                  ${rItems.map(it => `<li class="split-point">${it}</li>`).join("")}
                </ul>
              </div>
            </div>
          </div>
        `;
      case "audio_wave":
        const barsCount = 28;
        const barsHtml = Array.from({ length: barsCount }, (_, i) => 
          `<div class="wave-bar" id="wbar-${i}"></div>`
        ).join("");
        return `
          <div class="comp-audio-wave wave-card comp-wave" id="comp-audio-wave">
            <div class="wave-header">
              <div class="wave-tag wave-title">${data.title || "vocal1.m4a — NETTOYAGE STUDIO"}</div>
              <div class="wave-status" id="wave-status">${data.sub || "ANALYSE DU SPECTRE"}</div>
            </div>
            <div class="wave-bars-container wave-box" id="wave-bars-container">
              ${barsHtml}
            </div>
            <div class="wave-footer">
              <div class="wave-silence-badge" id="wave-silence-badge">SILENCE DÉTECTÉ : 0.38s</div>
              <button class="wave-btn" id="wave-btn">⚡ COUPER LES SILENCES</button>
            </div>
          </div>
        `;
      case "rpg":
        return `
          <div class="comp-rpg" id="comp-rpg">
            <div class="rpg-top-meta">
              <div class="rpg-tag">ZONE: ${data.zone || "WORLD"}</div>
              <div class="rpg-tag">QUÊTE: ${data.quest || "MAIN"}</div>
            </div>
            <div class="rpg-scene">${data.illustration || "⚔️"}</div>
            <div class="rpg-dialog-box">
              <img src="${data.mini_avatar || 'assets/avatars/mini.png'}" class="rpg-avatar" />
              <div class="rpg-text-zone">
                <div class="rpg-speaker">${data.speaker || "HERO"}</div>
                <div class="rpg-text">${data.text || ""}</div>
              </div>
            </div>
          </div>
        `;
      case "loom_player_fail":
        return `
          <div class="comp-loom-fail" id="comp-loom-fail">
            <div class="loom-window-bar">
              <div class="loom-dots">
                <span class="dot red"></span>
                <span class="dot yellow"></span>
                <span class="dot green"></span>
              </div>
              <div class="loom-file-title">${data.title || "demo_produit_v4.mp4"}</div>
              <div class="loom-status-tag">LECTEUR BLOQUÉ</div>
            </div>
            <div class="loom-screen">
              <div class="loom-video-inner">
                <div class="loom-avatar-freeze">🥱</div>
                <div class="loom-pause-circle">⏸</div>
              </div>
              <div class="loom-alert-card" id="loom-alert-card">
                <div class="loom-alert-icon">📉</div>
                <div class="loom-alert-content">
                  <div class="loom-alert-title">${data.dropRate || "-88%"} D'AUDIENCE</div>
                  <div class="loom-alert-sub">${data.label || "DÉCROCHAGE APRÈS 28 SECONDES"}</div>
                </div>
              </div>
            </div>
            <div class="loom-bottom-bar">
              <div class="loom-time-track">
                <div class="loom-time-fill" id="loom-time-fill"></div>
              </div>
              <div class="loom-timestamps">
                <span class="time-cur">${data.stoppedAt || "00:28"}</span>
                <span class="time-sep">/</span>
                <span class="time-end">${data.duration || "11:45"}</span>
                <span class="time-note">❌ ONGLET FERMÉ</span>
              </div>
            </div>
          </div>
        `;
      case "phone_mockup_duo":
        const leftData = data.left || { title: "LOOM 12 MIN ❌", badge: "0 RDV BOOKÉ", items: ["12 min d'écran partagé", "Hésitations & silences", "Zéro structure visuelle"] };
        const rightData = data.right || { title: "PITCH 60S ✅", badge: "DÉCIDEUR CAPTIVÉ", items: ["60 secondes chrono", "Bénéfices visibles d'emblée", "Zooms & sous-titres dynamiques"] };
        return `
          <div class="comp-phone-duo" id="comp-phone-duo">
            <div class="phone-card fail-card" id="phone-left">
              <div class="phone-badge fail">${leftData.title}</div>
              <div class="phone-result-tag fail">${leftData.badge}</div>
              <div class="phone-items">
                ${(leftData.items || []).map(it => `<div class="phone-row fail">❌ ${it}</div>`).join("")}
              </div>
            </div>
            <div class="phone-card win-card" id="phone-right">
              <div class="phone-badge win">${rightData.title}</div>
              <div class="phone-result-tag win">${rightData.badge}</div>
              <div class="phone-items">
                ${(rightData.items || []).map(it => `<div class="phone-row win">⚡ ${it}</div>`).join("")}
              </div>
            </div>
          </div>
        `;
      case "workflow_nodes":
        const wfSteps = data.steps || [
          { num: "01", title: "PROBLÈME CLIENT", desc: "Douleur identifiée" },
          { num: "02", title: "TON PRODUIT", desc: "Solution visible en 1 clic" },
          { num: "03", title: "RÉSULTAT", desc: "Adoption & conversion" }
        ];
        return `
          <div class="comp-workflow-nodes" id="comp-workflow-nodes">
            ${data.header ? `<div class="wf-header">${data.header}</div>` : ""}
            <div class="wf-track">
              ${wfSteps.map((s, idx) => `
                <div class="wf-node ${idx === 1 ? 'wf-active' : ''}" id="wf-node-${idx}">
                  <div class="wf-num">${s.num}</div>
                  <div class="wf-info">
                    <div class="wf-title">${s.title}</div>
                    <div class="wf-desc">${s.desc}</div>
                  </div>
                </div>
                ${idx < wfSteps.length - 1 ? `<div class="wf-arrow" id="wf-arrow-${idx}">➔</div>` : ""}
              `).join("")}
            </div>
          </div>
        `;
      case "tier_table":
        const tiers = data.tiers || [
          { num: "01", name: "Vidéo Hook & Problème", desc: "Capte l'attention dans le feed sans le son" },
          { num: "02", name: "Vidéo Démo Produit 60s", desc: "Prouve la valeur et le gain de temps direct" },
          { num: "03", name: "Vidéo Preuve & Action", desc: "Convertit le prospect en rendez-vous" }
        ];
        return `
          <div class="comp-tier-table" id="comp-tier-table">
            <div class="tier-head">${data.header || "PACK 3 VIDÉOS DÉDIÉES"}</div>
            <div class="tier-rows">
              ${tiers.map((tItem, idx) => `
                <div class="tier-card" id="tier-card-${idx}">
                  <div class="tier-pill">FORMAT ${tItem.num}</div>
                  <div class="tier-body">
                    <div class="tier-name">${tItem.name}</div>
                    <div class="tier-desc">${tItem.desc}</div>
                  </div>
                  <div class="tier-status">✓ INCLUS</div>
                </div>
              `).join("")}
            </div>
          </div>
        `;
      case "cursor_action":
        return `
          <div class="comp-cursor-action" id="comp-cursor-action">
            <div class="cursor-window">
              <div class="cursor-window-bar">
                <div class="cursor-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
                <div class="cursor-window-title">${data.windowTitle || "PAGE DE VENTE SAAS"}</div>
              </div>
              <div class="cursor-window-body">
                <div class="cursor-target-btn" id="cursor-target-btn">
                  <span class="btn-sparkle">⚡</span>
                  <span class="btn-caption">${data.buttonText || "RÉSERVER UNE DÉMO"}</span>
                </div>
                <div class="cursor-feedback-badge" id="cursor-feedback-badge">
                  ${data.feedback || "✓ RENDEZ-VOUS CONFIRMÉ"}
                </div>
              </div>
            </div>
            <div class="virtual-cursor" id="virtual-cursor">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none">
                <path d="M4 3L11 21L14 13L22 10L4 3Z" fill="#00F5A0" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        `;
      case "dm_cta_sim":
        return `
          <div class="comp-dm-cta" id="comp-dm-cta">
            <div class="dm-head">
              <div class="dm-avatar-circle">🤖</div>
              <div class="dm-meta">
                <div class="dm-recipient">${data.targetUser || "@AGENT404"}</div>
                <div class="dm-online-badge">● EN LIGNE</div>
              </div>
            </div>
            <div class="dm-chat-zone">
              <div class="dm-bubble user-msg" id="dm-user-bubble">
                <span class="bubble-tag">TOI</span>
                <span class="bubble-content" id="dm-typewriter">${data.keyword || "DEMO"}</span>
              </div>
              <div class="dm-bubble bot-msg" id="dm-bot-bubble">
                <span class="bubble-tag">AGENT404</span>
                <span class="bubble-content">${data.responseText || "✓ Message reçu. Démo envoyée en 2 min."}</span>
              </div>
            </div>
            <div class="dm-bar">
              <div class="dm-text-field">Message privé...</div>
              <div class="dm-action-send" id="dm-action-send">➔</div>
            </div>
          </div>
        `;
      case "loom_player_drop":
        return `
          <div class="comp-loom-drop" id="comp-loom-drop">
            <div class="loom-drop-header">
              <div class="loom-drop-dots">
                <span class="dot red"></span>
                <span class="dot yellow"></span>
                <span class="dot green"></span>
              </div>
              <div class="loom-drop-title">${data.title || "loom_demo_prospect.mp4"}</div>
              <div class="loom-drop-badge">${data.label || "DÉCROCHAGE"}</div>
            </div>
            <div class="loom-drop-body">
              <div class="loom-retention-chart">
                <svg class="loom-retention-svg" viewBox="0 0 800 180" preserveAspectRatio="none">
                  <path d="M 0 30 Q 150 40 220 130 T 400 165 L 800 170" fill="none" stroke="#F59E0B" stroke-width="6" stroke-linecap="round" />
                  <line x1="220" y1="20" x2="220" y2="170" stroke="#F59E0B" stroke-width="2" stroke-dasharray="6,6" />
                </svg>
                <div class="retention-marker" id="retention-marker">📉 ${data.stoppedAt || "00:28"} : -88% AUDIENCE</div>
              </div>
              <div class="loom-drop-footer">
                <div class="loom-drop-stat">
                  <span class="loom-drop-val">${data.retention || "12%"}</span>
                  <span class="loom-drop-label">DE RÉTENTION FINALE</span>
                </div>
                <div class="loom-drop-stat">
                  <span class="loom-drop-val" style="color: #8B949E;">${data.duration || "10:00"}</span>
                  <span class="loom-drop-label">DURÉE TOTALE (TROP LONG)</span>
                </div>
              </div>
            </div>
          </div>
        `;
      case "browser_tab_overload":
        return `
          <div class="comp-browser-overload" id="comp-browser-overload">
            <div class="browser-tab-bar">
              <div class="browser-tab active">${data.tabTitle || "Screen Share — Meeting_Recording_12m.mp4"}</div>
              <div class="browser-tab">+ Nouvel onglet</div>
            </div>
            <div class="browser-clutter-body">
              <div class="clutter-grid">
                <div class="clutter-tile">📁 Bureau encombré</div>
                <div class="clutter-tile">📊 48 onglets ouverts</div>
                <div class="clutter-tile">💬 Notifications Slack</div>
                <div class="clutter-tile">⏳ Chargement infini...</div>
                <div class="clutter-tile">🔇 Micro mal réglé</div>
                <div class="clutter-tile">🔄 Défilement erratique</div>
                <div class="clutter-tile">📝 Notes désordonnées</div>
                <div class="clutter-tile">💤 Fatigue visuelle</div>
              </div>
              <div class="overload-warning-bar" id="overload-warning-bar">
                <div class="overload-timer">⏱️ ${data.timer || "12:00"}</div>
                <div class="overload-text">${data.tag || "12 MINUTES D'ÉCRAN PARTAGÉ ⏳"}</div>
              </div>
            </div>
          </div>
        `;
      case "loom_3_flaws_timeline":
        return `
          <div class="comp-flaws-timeline" id="comp-flaws-timeline">
            <div class="flaws-head">${data.header || "DÉCROCHAGE PROSPECT"}</div>
            ${(data.flaws || []).map((f, i) => `
              <div class="flaw-card" id="flaw-card-${i}">
                <div class="flaw-num">${f.num}</div>
                <div class="flaw-content">
                  <div class="flaw-title">${f.title}</div>
                  <div class="flaw-detail">${f.detail}</div>
                </div>
                <div class="flaw-icon">${f.icon}</div>
              </div>
            `).join("")}
          </div>
        `;
      case "tab_close_cursor":
        return `
          <div class="comp-tab-close" id="comp-tab-close">
            <div class="tab-close-bar">
              <div class="tab-close-tab">
                <span>🌐 ${data.tabName || "Loom — Démo Produit B2B"}</span>
                <span class="tab-cross-btn" id="tab-cross-btn">✕</span>
              </div>
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 16px; color: #8B949E;">Fermeture éclair</div>
            </div>
            <div class="tab-close-badge-box" id="tab-close-badge-box">
              <div class="tab-close-big">${data.badge || "ONGLET FERMÉ EN 30S"}</div>
              <div class="tab-close-sub">${data.sub || "PERDU AVANT LE MOINDRE BÉNÉFICE"}</div>
            </div>
            <div class="virtual-cursor" id="tab-cursor" style="position: absolute; pointer-events: none; z-index: 50;">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none">
                <path d="M4 3L11 21L14 13L22 10L4 3Z" fill="#F59E0B" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        `;
      case "product_vs_perception":
        if (data.phase === "perception") {
          return `
            <div class="comp-product-perception" id="comp-product-perception">
              <div class="perception-drop-card">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: 800; color: #8B949E; text-align: center;">
                  ${data.title || "VALEUR PERÇUE PAR LE PROSPECT"}
                </div>
                <div class="drop-gauge-box">
                  <div class="drop-val-side real">
                    <div class="lbl">VALEUR RÉELLE DU PRODUIT</div>
                    <div class="num">${data.dropFrom || "100%"}</div>
                  </div>
                  <div class="drop-arrow">➔ 📉</div>
                  <div class="drop-val-side perceived">
                    <div class="lbl">PERÇUE APRÈS LE LOOM</div>
                    <div class="num">${data.dropTo || "18%"}</div>
                  </div>
                </div>
                <div class="drop-warning-badge">${data.badge || "0 APPEL BOOKÉ"}</div>
                <div style="text-align: center; font-size: 20px; font-weight: 700; color: #8B949E;">
                  ${data.sub || "DÉMO AMATEUR = CONTRATS PERDUS"}
                </div>
              </div>
            </div>
          `;
        }
        return `
          <div class="comp-product-perception" id="comp-product-perception">
            <div class="product-card-solid">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="prod-title">${data.title || "TON PRODUIT SAAS"}</div>
                <div class="prod-rating">${data.rating || "★★★★★"}</div>
              </div>
              <div class="prod-sub">${data.subtitle || "ARCHITECTURE SOLIDE • VALEUR RÉELLE"}</div>
              <div class="prod-bullets">
                ${(data.points || []).map(p => `
                  <div class="bullet-item">
                    <span style="color: #00F5A0; font-size: 24px;">✓</span>
                    <span>${p}</span>
                  </div>
                `).join("")}
              </div>
            </div>
            ${data.avatar_pip ? `
              <div class="avatar-pip" id="avatar-pip">
                <img src="${data.avatar_pip}" alt="Avatar PiP" />
              </div>
            ` : ""}
          </div>
        `;
      case "interface_labyrinth_cut":
        return `
          <div class="comp-labyrinth-cut" id="comp-labyrinth-cut">
            <div class="labyrinth-head">${data.header || "VISITE DE L'INTERFACE SAAS"}</div>
            <div class="labyrinth-grid">
              ${(data.menus || []).map((m, i) => `
                <div class="menu-card" id="menu-card-${i}">${m}</div>
              `).join("")}
            </div>
            <div class="strike-line" id="strike-line"></div>
            <div class="labyrinth-cut-badge" id="labyrinth-cut-badge">${data.badge || "VISITE GUIDÉE DE 12 MENUS : IGNORÉE ✕"}</div>
          </div>
        `;
      case "sixty_sec_value_bridge":
        return `
          <div class="comp-sixty-bridge" id="comp-sixty-bridge">
            <div class="bridge-flow">
              <div class="bridge-box">
                <div class="title">${data.leftBox || "PROBLÈME DÉCIDEUR"}</div>
                <div class="desc">Douleur identifiée & blocage business</div>
              </div>
              <div class="bridge-chrono" id="bridge-chrono">
                <div class="num">${data.chrono || "60s"}</div>
                <div class="unit">CHRONO</div>
              </div>
              <div class="bridge-box sol">
                <div class="title">${data.rightBox || "SOLUTION + ROI IMMÉDIAT"}</div>
                <div class="desc" style="color: #00F5A0;">Bénéfice prouvé sans friction</div>
              </div>
            </div>
            <div class="bridge-tag-bar">${data.tag || "COMPRÉHENSION EN 60 SECONDES"}</div>
          </div>
        `;
      case "code_to_ui_live":
        return `
          <div class="comp-code-live" id="comp-code-live">
            <div class="code-window-col">
              <div class="code-window-bar">
                <div class="window-dots">
                  <span class="dot red"></span>
                  <span class="dot yellow"></span>
                  <span class="dot green"></span>
                </div>
                <span>${data.filename || "pipeline_render.js"}</span>
              </div>
              <div class="code-window-body" id="code-live-body"><span id="code-live-text"></span><span class="cursor">▋</span></div>
            </div>
            <div class="code-badges-col">
              <div class="code-pop-badge" id="code-badge-1">${data.badge1 || "📷 ZÉRO CAMÉRA"}</div>
              <div class="code-pop-badge" id="code-badge-2">${data.badge2 || "🎯 ZÉRO PRISE RATÉE"}</div>
            </div>
          </div>
        `;
      case "voice_to_word_grid":
        return `
          <div class="comp-word-grid" id="comp-word-grid">
            <div class="wave-clean-box">
              <div class="wave-clean-title">🎙️ ${data.audioFile || "memo_vocal_fondateur.m4a"} — DÉCOUPE DES SILENCES</div>
              <div class="wave-clean-bars" id="wave-clean-bars">
                ${Array.from({ length: 32 }, (_, i) => `<div class="wbar-clean" id="cwbar-${i}"></div>`).join("")}
              </div>
            </div>
            <div class="grid-sync-box">
              <div class="grid-sync-title">⚡ SYNCHRONISATION MOT-À-MOT DÉTERMINISTE (30 FPS)</div>
              <div class="grid-sync-cells">
                <div class="sync-cell"><div class="ts">00:00.01</div><div class="wd">[COUPE HÉSITATIONS]</div></div>
                <div class="sync-cell"><div class="ts">00:00.02</div><div class="wd">[ALIGNEMENT WHISPER]</div></div>
                <div class="sync-cell"><div class="ts">00:00.03</div><div class="wd">[CALIBRAGE FPS]</div></div>
              </div>
            </div>
          </div>
        `;
      case "saas_showcase_3steps":
        return `
          <div class="comp-saas-showcase" id="comp-saas-showcase">
            <div class="saas-app-bar">
              <div class="saas-app-logo">⚡ ${data.appName || "CloudMetrics — Intelligence B2B"}</div>
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 15px; color: #8B949E;">ENV: PRODUCTION</div>
            </div>
            <div class="saas-metrics-row">
              <div class="saas-metric-tile highlighted" id="saas-tile-1">
                <div class="lbl">KPI PRINCIPAL</div>
                <div class="val">+312% ROI</div>
              </div>
              <div class="saas-metric-tile" id="saas-tile-2">
                <div class="lbl">TEMPS GAGNÉ</div>
                <div class="val">14h / sem</div>
              </div>
              <div class="saas-metric-tile" id="saas-tile-3">
                <div class="lbl">CONVERSION</div>
                <div class="val">4.8x</div>
              </div>
            </div>
            <div class="saas-stage-tag" id="saas-stage-tag">${data.steps && data.steps[0] ? data.steps[0].label : "FONCTIONNALITÉ CLÉ ISOLÉE"}</div>
          </div>
        `;
      case "delivery_48h_3channels":
        return `
          <div class="comp-delivery-channels" id="comp-delivery-channels">
            <div class="delivery-head-badge">${data.header || "⚡ LIVRAISON CLÉ EN MAIN EN 48H"}</div>
            <div class="delivery-cards-grid">
              ${(data.cards || []).map((c, i) => `
                <div class="delivery-card-v" id="delivery-card-${i}">
                  <div class="chan-icon">${c.icon}</div>
                  <div class="chan-name">${c.channel}</div>
                  <div class="chan-tag">${c.tag}</div>
                  <div class="chan-desc">${c.desc}</div>
                </div>
              `).join("")}
            </div>
          </div>
        `;
      case "face_to_dm_cta":
        return `
          <div class="comp-face-dm" id="comp-face-dm">
            <div class="face-dm-avatar-stage" id="face-dm-avatar-stage">
              <div class="face-hero-title" style="top: 220px;">
                <span>TRANSFORME TES DÉMOS EN </span><span class="highlight">RDV</span>
              </div>
              <div class="comp-face">
                <img src="${data.avatar || 'assets/avatars/pointing.png'}" alt="Avatar" class="avatar-sticker" id="avatar-img" />
              </div>
            </div>
            <div class="face-dm-chat-stage" id="face-dm-chat-stage">
              <div class="comp-dm-cta" style="margin: 0 auto;">
                <div class="dm-head">
                  <div class="dm-avatar-circle">🤖</div>
                  <div class="dm-meta">
                    <div class="dm-recipient">${data.targetUser || "@AGENT404"}</div>
                    <div class="dm-online-badge">● EN LIGNE</div>
                  </div>
                </div>
                <div class="dm-chat-zone">
                  <div class="dm-bubble user-msg" id="dm-user-bubble">
                    <span class="bubble-tag">TOI</span>
                    <span class="bubble-content" id="dm-typewriter">${data.keyword || "DEMO"}</span>
                  </div>
                  <div class="dm-bubble bot-msg" id="dm-bot-bubble">
                    <span class="bubble-tag">AGENT404</span>
                    <span class="bubble-content">${data.responseText || "✓ Message reçu. Démo envoyée en 2 min."}</span>
                  </div>
                </div>
                <div class="dm-bar">
                  <div class="dm-text-field">Message privé...</div>
                  <div class="dm-action-send">➔</div>
                </div>
              </div>
            </div>
          </div>
        `;
      default:
        return `<div>Scène non définie</div>`;
    }
  }

  /**
   * Courbe spring overshoot : monte à 1.08 puis stabilise à 1.0 en 0.25s
   * avec léger translateY de 60px -> 0px
   */
  function calcSpringOvershoot(elapsed) {
    const tEnter = 0.25;
    if (elapsed >= tEnter) {
      return { scale: 1.0, ty: 0.0 };
    }
    const p = Math.max(0, elapsed / tEnter);
    const scale = 0.85 + 0.15 * p + 0.08 * Math.sin(p * Math.PI);
    const ty = 60 * (1.0 - p);
    return { scale, ty };
  }

  function animateComponent(type, data, progress, elapsed, t) {
    const spring = calcSpringOvershoot(elapsed);

    if (type === "face") {
      const avatar = document.getElementById("avatar-img");
      const badge = document.getElementById("face-badge");
      const heroTitle = document.getElementById("face-hero-title");
      const isHeadOnly = data.avatar && data.avatar.includes("mini");

      if (heroTitle) {
        heroTitle.style.transform = `translateX(-50%) translateY(${spring.ty}px) scale(${spring.scale})`;
      }

      // Dynamisme continu : flottement, inclinaison et zoom caméra progressif
      const floatY = Math.sin(t * 5) * 10;
      const tiltDeg = Math.sin(t * 2.5) * 1.5;
      const camZoom = 1.0 + progress * 0.05;

      if (avatar) {
        if (isHeadOnly) {
          avatar.style.transform = `translateY(${spring.ty + floatY}px) rotate(${tiltDeg}deg) scale(${spring.scale * camZoom})`;
          avatar.style.transformOrigin = "center center";
        } else {
          avatar.style.transform = `translateX(-50%) translateY(${spring.ty + floatY}px) rotate(${tiltDeg}deg) scale(${spring.scale * camZoom})`;
          avatar.style.transformOrigin = "bottom center";
        }
      }
      if (badge) {
        const badgeP = Math.min(1, elapsed / 0.35);
        const bScale = badgeP < 1 ? (0.7 + 0.3 * badgeP + 0.1 * Math.sin(badgeP * Math.PI)) : 1.0;
        badge.style.transform = `translateX(-50%) rotate(-2deg) scale(${bScale})`;
      }
    } else if (type === "big") {
      const el = document.getElementById("comp-big");
      if (el) {
        el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      }
    } else if (type === "cards") {
      const el = document.getElementById("comp-cards");
      if (el) {
        const total = (data.cards || []).length;
        for (let i = 0; i < total; i++) {
          const cardEl = document.getElementById(`card-item-${i}`);
          if (!cardEl) continue;
          const cardDelay = i * 0.15;
          const cardElapsed = Math.max(0, elapsed - cardDelay);
          if (cardElapsed === 0) {
            cardEl.style.opacity = "0";
            cardEl.style.transform = "translateY(50px) scale(0.7)";
          } else {
            const cardP = Math.min(1, cardElapsed / 0.22);
            const cardScale = 0.7 + 0.3 * cardP + (cardP < 1 ? 0.12 * Math.sin(cardP * Math.PI) : 0);
            const cardTy = 50 * (1 - cardP);
            cardEl.style.opacity = "1";
            cardEl.style.transform = `translateY(${cardTy}px) scale(${cardScale})`;
          }
        }
      }
    } else if (type === "list") {
      const total = (data.items || []).length;
      const activeIdx = Math.min(total - 1, Math.floor(progress * total));
      for (let i = 0; i < total; i++) {
        const itemEl = document.getElementById(`list-item-${i}`);
        if (!itemEl) continue;
        const itemDelay = i * 0.15;
        const itemElapsed = Math.max(0, elapsed - itemDelay);
        if (itemElapsed === 0) {
          itemEl.style.opacity = "0";
          itemEl.style.transform = "translateY(40px) scale(0.8)";
        } else {
          const itemP = Math.min(1, itemElapsed / 0.2);
          const itemScale = 0.8 + 0.2 * itemP + (itemP < 1 ? 0.1 * Math.sin(itemP * Math.PI) : 0);
          const itemTy = 40 * (1 - itemP);
          itemEl.style.opacity = "1";
          if (i === activeIdx) {
            itemEl.classList.add("active");
            itemEl.style.transform = `translateY(${itemTy}px) scale(${itemScale * 1.03}) translateX(20px)`;
          } else {
            itemEl.classList.remove("active");
            itemEl.style.transform = `translateY(${itemTy}px) scale(${itemScale})`;
          }
        }
      }
    } else if (type === "split") {
      const leftCol = document.getElementById("split-col-left");
      const rightCol = document.getElementById("split-col-right");
      if (leftCol) {
        const p1 = Math.min(1, elapsed / 0.25);
        const s1 = p1 < 1 ? (0.8 + 0.2 * p1 + 0.1 * Math.sin(p1 * Math.PI)) : 1.0;
        leftCol.style.transform = `translateY(${50 * (1 - p1)}px) scale(${s1})`;
      }
      if (rightCol) {
        const p2 = Math.min(1, Math.max(0, (elapsed - 0.15) / 0.25));
        if (elapsed < 0.15) {
          rightCol.style.opacity = "0";
          rightCol.style.transform = "translateY(50px) scale(0.8)";
        } else {
          rightCol.style.opacity = "1";
          const s2 = p2 < 1 ? (0.8 + 0.2 * p2 + 0.12 * Math.sin(p2 * Math.PI)) : 1.0;
          rightCol.style.transform = `translateY(${50 * (1 - p2)}px) scale(${s2})`;
        }
      }
    } else if (type === "audio_wave") {
      const el = document.getElementById("comp-audio-wave");
      if (el) {
        el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      }
      const barsCount = 28;
      const isCut = progress >= 0.42;
      const statusEl = document.getElementById("wave-status");
      const silenceBadge = document.getElementById("wave-silence-badge");
      const btn = document.getElementById("wave-btn");

      for (let i = 0; i < barsCount; i++) {
        const bar = document.getElementById(`wbar-${i}`);
        if (!bar) continue;
        const waveOsc = Math.sin(t * 14 + i * 0.45) * Math.cos(t * 7 - i * 0.2);
        const distFromCenter = Math.abs(i - barsCount / 2) / (barsCount / 2);
        const baseH = (1 - distFromCenter * 0.6) * 160;
        const h = Math.max(16, baseH * Math.abs(waveOsc) + 20);

        if (!isCut && i >= 11 && i <= 16) {
          bar.classList.add("silent");
          bar.style.height = "14px";
        } else {
          bar.classList.remove("silent");
          bar.style.height = `${Math.round(h)}px`;
        }
      }

      if (isCut) {
        if (statusEl) {
          statusEl.textContent = "SILENCES ÉLIMINÉS (-100%)";
          statusEl.style.background = "#00F5A0";
          statusEl.style.color = "#090D16";
        }
        if (silenceBadge) {
          silenceBadge.textContent = "RYTHME 100% ACTIF";
          silenceBadge.style.background = "#090D16";
          silenceBadge.style.color = "#00F5A0";
        }
        if (btn) {
          btn.classList.add("pressed");
          btn.textContent = "✓ SILENCES PURGÉS";
        }
      } else {
        if (statusEl) {
          statusEl.textContent = "ANALYSE DU SPECTRE";
          statusEl.style.background = "#00F5A0";
          statusEl.style.color = "#090D16";
        }
        if (silenceBadge) {
          silenceBadge.textContent = "SILENCE DÉTECTÉ : 0.38s";
          silenceBadge.style.background = "#090D16";
          silenceBadge.style.color = "#FFFFFF";
        }
        if (btn) {
          btn.classList.remove("pressed");
          btn.textContent = "⚡ COUPER LES SILENCES";
        }
      }
    } else if (type === "window") {
      const el = document.getElementById("comp-window");
      if (el) {
        el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      }
      const contentEl = document.getElementById("typewriter-content");
      if (contentEl) {
        const fullText = (data.lines && Array.isArray(data.lines)) ? data.lines.join("\n") : (data.text || "");
        const charCount = Math.floor(progress * fullText.length);
        contentEl.textContent = fullText.substring(0, charCount);
      }
    } else if (type === "rpg") {
      const el = document.getElementById("comp-rpg");
      if (el) {
        el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      }
    } else if (type === "engine_arch") {
      const el = document.getElementById("comp-engine-arch");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const gear = document.getElementById("arch-gear");
      if (gear) gear.style.transform = `rotate(${t * 120}deg)`;
    } else if (type === "sync_timer") {
      const el = document.getElementById("comp-sync-timer");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const digits = document.getElementById("sync-digits");
      if (digits) {
        const ms = Math.floor((t * 1000) % 1000).toString().padStart(3, '0');
        digits.textContent = `00:21.${ms} ms`;
      }
      const p0 = document.getElementById("sync-pill-0");
      const p1 = document.getElementById("sync-pill-1");
      const p2 = document.getElementById("sync-pill-2");
      if (p0) {
        if (progress >= 0.20) p0.classList.add("locked");
        else p0.classList.remove("locked");
      }
      if (p1) {
        if (progress >= 0.50) p1.classList.add("locked");
        else p1.classList.remove("locked");
      }
      if (p2) {
        if (progress >= 0.75) p2.classList.add("locked");
        else p2.classList.remove("locked");
      }
    } else if (type === "emotion_morph") {
      const avatar = document.getElementById("morph-avatar");
      const badge = document.getElementById("morph-badge");
      let src = "assets/avatars/happy.png";
      let text = "😄 ÉMOTION : ENTHOUSIASTE";
      let badgeBg = "#00F5A0";
      let badgeColor = "#090D16";

      if (progress >= 0.66) {
        src = "assets/avatars/skeptic.png";
        text = "🤨 ÉMOTION : SCEPTIQUE";
        badgeBg = "#FFFFFF";
        badgeColor = "#090D16";
      } else if (progress >= 0.33) {
        src = "assets/avatars/shock.png";
        text = "😱 ÉMOTION : CHOQUÉ";
        badgeBg = "#00F5A0";
        badgeColor = "#090D16";
      }

      if (avatar && !avatar.src.endsWith(src)) {
        avatar.src = src;
      }
      if (badge && badge.textContent !== text) {
        badge.textContent = text;
        badge.style.background = badgeBg;
        badge.style.color = badgeColor;
      }
      const floatY = Math.sin(t * 5) * 8;
      const camZoom = 1.0 + progress * 0.04;
      if (avatar) {
        avatar.style.transform = `translateY(${spring.ty + floatY}px) scale(${spring.scale * camZoom})`;
      }
    } else if (type === "ffmpeg_render") {
      const el = document.getElementById("comp-ffmpeg-render");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const counter = document.getElementById("ffmpeg-counter");
      const fill = document.getElementById("ffmpeg-fill");
      const pct = document.getElementById("ffmpeg-pct");
      const totalFrames = 2200;
      const curFrame = Math.min(totalFrames, Math.floor(progress * totalFrames));
      const pctVal = Math.min(100, Math.floor(progress * 100));
      if (counter) counter.textContent = `FRAME ${curFrame} / ${totalFrames}`;
      if (fill) fill.style.width = `${pctVal}%`;
      if (pct) pct.textContent = `${pctVal}%`;
    } else if (type === "speed_counter") {
      const el = document.getElementById("comp-speed-counter");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
    } else if (type === "loom_player_fail") {
      const el = document.getElementById("comp-loom-fail");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const fill = document.getElementById("loom-time-fill");
      if (fill) {
        const fillP = Math.min(1, elapsed / 0.35);
        fill.style.width = `${fillP * 18}%`;
      }
      const badge = document.getElementById("loom-alert-card");
      if (badge) {
        const bp = Math.min(1, elapsed / 0.3);
        const bscale = bp < 1 ? (0.6 + 0.4 * bp + 0.1 * Math.sin(bp * Math.PI)) : 1.0;
        badge.style.transform = `scale(${bscale})`;
      }
    } else if (type === "phone_mockup_duo") {
      const left = document.getElementById("phone-left");
      const right = document.getElementById("phone-right");
      if (left) {
        const lp = Math.min(1, elapsed / 0.22);
        const lScale = lp < 1 ? (0.8 + 0.2 * lp) : 1.0;
        left.style.transform = `translateX(${(1 - lp) * -40}px) scale(${lScale})`;
        left.style.opacity = `${lp}`;
      }
      if (right) {
        const rightElapsed = Math.max(0, elapsed - 0.12);
        const rp = Math.min(1, rightElapsed / 0.22);
        const rScale = rp < 1 ? (0.8 + 0.2 * rp + 0.08 * Math.sin(rp * Math.PI)) : 1.0;
        right.style.transform = `translateX(${(1 - rp) * 40}px) scale(${rScale})`;
        right.style.opacity = `${rp}`;
      }
    } else if (type === "workflow_nodes") {
      const el = document.getElementById("comp-workflow-nodes");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      for (let i = 0; i < 3; i++) {
        const node = document.getElementById(`wf-node-${i}`);
        if (!node) continue;
        const nElapsed = Math.max(0, elapsed - i * 0.12);
        const np = Math.min(1, nElapsed / 0.2);
        const nScale = np < 1 ? (0.7 + 0.3 * np + 0.1 * Math.sin(np * Math.PI)) : 1.0;
        node.style.transform = `scale(${nScale})`;
        node.style.opacity = `${np}`;
      }
    } else if (type === "tier_table") {
      const el = document.getElementById("comp-tier-table");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      for (let i = 0; i < 3; i++) {
        const row = document.getElementById(`tier-card-${i}`);
        if (!row) continue;
        const rElapsed = Math.max(0, elapsed - i * 0.12);
        const rp = Math.min(1, rElapsed / 0.2);
        const rScale = rp < 1 ? (0.8 + 0.2 * rp) : 1.0;
        row.style.transform = `translateX(${(1 - rp) * 30}px) scale(${rScale})`;
        row.style.opacity = `${rp}`;
      }
    } else if (type === "cursor_action") {
      const el = document.getElementById("comp-cursor-action");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const cur = document.getElementById("virtual-cursor");
      const btn = document.getElementById("cursor-target-btn");
      const feedback = document.getElementById("cursor-feedback-badge");
      const moveP = Math.min(1, elapsed / 0.45);
      const startX = 260, startY = 220;
      const targetX = 0, targetY = 0;
      const curX = startX + (targetX - startX) * moveP;
      const curY = startY + (targetY - startY) * moveP;
      const isClicked = elapsed >= 0.45;
      if (cur) {
        cur.style.transform = `translate(${curX}px, ${curY}px) scale(${isClicked ? 0.9 : 1.0})`;
      }
      if (btn) {
        btn.style.transform = `scale(${isClicked ? 0.96 : 1.0})`;
        if (isClicked) {
          btn.style.boxShadow = "0 2px 0 #000000";
          btn.style.background = "#047857";
        }
      }
      if (feedback) {
        const fp = Math.max(0, Math.min(1, (elapsed - 0.48) / 0.2));
        feedback.style.opacity = `${fp}`;
        feedback.style.transform = `scale(${0.8 + 0.2 * fp})`;
      }
    } else if (type === "dm_cta_sim") {
      const el = document.getElementById("comp-dm-cta");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const userBubble = document.getElementById("dm-user-bubble");
      const botBubble = document.getElementById("dm-bot-bubble");
      const up = Math.min(1, elapsed / 0.25);
      if (userBubble) {
        userBubble.style.opacity = `${up}`;
        userBubble.style.transform = `scale(${0.8 + 0.2 * up})`;
      }
      if (botBubble) {
        const bp = Math.max(0, Math.min(1, (elapsed - 0.4) / 0.25));
        botBubble.style.opacity = `${bp}`;
        botBubble.style.transform = `scale(${0.8 + 0.2 * bp})`;
      }
    } else if (type === "loom_player_drop") {
      const el = document.getElementById("comp-loom-drop");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const marker = document.getElementById("retention-marker");
      if (marker) {
        const mp = Math.min(1, Math.max(0, (elapsed - 0.15) / 0.25));
        const mscale = mp < 1 ? (0.6 + 0.4 * mp + 0.12 * Math.sin(mp * Math.PI)) : 1.0;
        marker.style.transform = `scale(${mscale})`;
        marker.style.opacity = `${mp}`;
      }
    } else if (type === "browser_tab_overload") {
      const el = document.getElementById("comp-browser-overload");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const warning = document.getElementById("overload-warning-bar");
      if (warning) {
        const wp = Math.min(1, Math.max(0, (elapsed - 0.2) / 0.25));
        warning.style.opacity = `${wp}`;
        warning.style.transform = `scale(${0.85 + 0.15 * wp})`;
      }
    } else if (type === "loom_3_flaws_timeline") {
      const el = document.getElementById("comp-flaws-timeline");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      for (let i = 0; i < 3; i++) {
        const card = document.getElementById(`flaw-card-${i}`);
        if (!card) continue;
        const delay = i * 0.25;
        const cElapsed = Math.max(0, elapsed - delay);
        if (cElapsed === 0) {
          card.style.opacity = "0";
          card.style.transform = "translateY(30px) scale(0.9)";
        } else {
          const cp = Math.min(1, cElapsed / 0.22);
          const cscale = cp < 1 ? (0.85 + 0.15 * cp + 0.08 * Math.sin(cp * Math.PI)) : 1.0;
          card.style.opacity = "1";
          card.style.transform = `translateY(${30 * (1 - cp)}px) scale(${cscale})`;
        }
      }
    } else if (type === "tab_close_cursor") {
      const el = document.getElementById("comp-tab-close");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const cur = document.getElementById("tab-cursor");
      const btn = document.getElementById("tab-cross-btn");
      const badge = document.getElementById("tab-close-badge-box");

      const moveP = Math.min(1, elapsed / 0.4);
      const startX = 260, startY = 180;
      const targetX = 0, targetY = 0;
      const curX = startX + (targetX - startX) * moveP;
      const curY = startY + (targetY - startY) * moveP;
      const isClicked = elapsed >= 0.4;

      if (cur) {
        cur.style.transform = `translate(${curX}px, ${curY}px) scale(${isClicked ? 0.88 : 1.0})`;
      }
      if (btn) {
        if (isClicked) {
          btn.style.background = "#F59E0B";
          btn.style.color = "#090D16";
          btn.style.transform = "scale(0.92)";
        } else {
          btn.style.background = "#30363D";
          btn.style.color = "#F59E0B";
          btn.style.transform = "scale(1.0)";
        }
      }
      if (badge) {
        const bp = Math.max(0, Math.min(1, (elapsed - 0.35) / 0.25));
        badge.style.opacity = `${bp}`;
        badge.style.transform = `rotate(-2deg) scale(${0.8 + 0.2 * bp})`;
      }
    } else if (type === "product_vs_perception") {
      const el = document.getElementById("comp-product-perception");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const pip = document.getElementById("avatar-pip");
      if (pip) {
        const floatY = Math.sin(t * 4) * 6;
        pip.style.transform = `translateY(${floatY}px)`;
      }
    } else if (type === "interface_labyrinth_cut") {
      const el = document.getElementById("comp-labyrinth-cut");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const strike = document.getElementById("strike-line");
      const badge = document.getElementById("labyrinth-cut-badge");
      const isCut = progress >= 0.4;
      if (strike) {
        if (isCut) {
          const cutP = Math.min(1, (progress - 0.4) / 0.15);
          strike.style.opacity = `${cutP}`;
          strike.style.transform = `rotate(-12deg) scaleX(${cutP})`;
        } else {
          strike.style.opacity = "0";
          strike.style.transform = "rotate(-12deg) scaleX(0)";
        }
      }
      if (badge) {
        if (isCut) {
          const bp = Math.min(1, (progress - 0.45) / 0.15);
          badge.style.opacity = `${bp}`;
          badge.style.transform = `translate(-50%, -50%) rotate(-4deg) scale(${0.7 + 0.3 * bp})`;
        } else {
          badge.style.opacity = "0";
          badge.style.transform = `translate(-50%, -50%) rotate(-4deg) scale(0.7)`;
        }
      }
    } else if (type === "sixty_sec_value_bridge") {
      const el = document.getElementById("comp-sixty-bridge");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const chrono = document.getElementById("bridge-chrono");
      if (chrono) {
        const beat = 1.0 + Math.sin(t * 8) * 0.05;
        chrono.style.transform = `scale(${beat})`;
      }
    } else if (type === "code_to_ui_live") {
      const el = document.getElementById("comp-code-live");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const textEl = document.getElementById("code-live-text");
      if (textEl) {
        const fullCode = data.code || "";
        const charCount = Math.floor(Math.min(1, elapsed / 0.8) * fullCode.length);
        textEl.textContent = fullCode.substring(0, charCount);
      }
      const b1 = document.getElementById("code-badge-1");
      const b2 = document.getElementById("code-badge-2");
      if (b1) {
        const p1 = Math.max(0, Math.min(1, (elapsed - 0.25) / 0.22));
        b1.style.opacity = `${p1}`;
        b1.style.transform = `translateX(${40 * (1 - p1)}px) scale(${0.85 + 0.15 * p1})`;
      }
      if (b2) {
        const p2 = Math.max(0, Math.min(1, (elapsed - 0.55) / 0.22));
        b2.style.opacity = `${p2}`;
        b2.style.transform = `translateX(${40 * (1 - p2)}px) scale(${0.85 + 0.15 * p2})`;
      }
    } else if (type === "voice_to_word_grid") {
      const el = document.getElementById("comp-word-grid");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const barsCount = 32;
      for (let i = 0; i < barsCount; i++) {
        const bar = document.getElementById(`cwbar-${i}`);
        if (!bar) continue;
        const waveOsc = Math.sin(t * 12 + i * 0.4) * Math.cos(t * 6 - i * 0.25);
        const distFromCenter = Math.abs(i - barsCount / 2) / (barsCount / 2);
        const baseH = (1 - distFromCenter * 0.5) * 80;
        const h = Math.max(12, baseH * Math.abs(waveOsc) + 16);
        bar.style.height = `${Math.round(h)}px`;
      }
    } else if (type === "saas_showcase_3steps") {
      const el = document.getElementById("comp-saas-showcase");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const tag = document.getElementById("saas-stage-tag");
      const tile1 = document.getElementById("saas-tile-1");
      const tile2 = document.getElementById("saas-tile-2");
      const tile3 = document.getElementById("saas-tile-3");
      const steps = data.steps || [];

      if (progress < 0.33) {
        if (tag && steps[0]) tag.textContent = `${steps[0].num} ${steps[0].label}`;
        if (tile1) tile1.classList.add("highlighted");
        if (tile2) tile2.classList.remove("highlighted");
        if (tile3) tile3.classList.remove("highlighted");
      } else if (progress < 0.66) {
        if (tag && steps[1]) tag.textContent = `${steps[1].num} ${steps[1].label}`;
        if (tile1) tile1.classList.remove("highlighted");
        if (tile2) tile2.classList.add("highlighted");
        if (tile3) tile3.classList.remove("highlighted");
      } else {
        if (tag && steps[2]) tag.textContent = `${steps[2].num} ${steps[2].label}`;
        if (tile1) tile1.classList.remove("highlighted");
        if (tile2) tile2.classList.remove("highlighted");
        if (tile3) tile3.classList.add("highlighted");
      }
    } else if (type === "delivery_48h_3channels") {
      const el = document.getElementById("comp-delivery-channels");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const cards = data.cards || [];
      const activeIdx = Math.min(cards.length - 1, Math.floor(progress * cards.length));
      for (let i = 0; i < cards.length; i++) {
        const cEl = document.getElementById(`delivery-card-${i}`);
        if (!cEl) continue;
        if (i === activeIdx) {
          cEl.classList.add("active");
        } else {
          cEl.classList.remove("active");
        }
      }
    } else if (type === "face_to_dm_cta") {
      const avatarStage = document.getElementById("face-dm-avatar-stage");
      const chatStage = document.getElementById("face-dm-chat-stage");
      const userBubble = document.getElementById("dm-user-bubble");
      const botBubble = document.getElementById("dm-bot-bubble");
      const avatar = document.getElementById("avatar-img");

      const switchTime = 0.42;
      if (progress < switchTime) {
        if (avatarStage) {
          avatarStage.style.opacity = "1";
          avatarStage.style.pointerEvents = "auto";
        }
        if (chatStage) {
          chatStage.style.opacity = "0";
          chatStage.style.pointerEvents = "none";
        }
        if (avatar) {
          const floatY = Math.sin(t * 5) * 10;
          const tiltDeg = Math.sin(t * 2.5) * 1.5;
          avatar.style.transform = `translateX(-50%) translateY(${spring.ty + floatY}px) rotate(${tiltDeg}deg) scale(${spring.scale})`;
        }
      } else {
        const chatProgress = (progress - switchTime) / (1 - switchTime);
        if (avatarStage) {
          avatarStage.style.opacity = "0";
          avatarStage.style.pointerEvents = "none";
        }
        if (chatStage) {
          const cp = Math.min(1, chatProgress / 0.3);
          chatStage.style.opacity = `${cp}`;
          chatStage.style.pointerEvents = "auto";
          chatStage.style.transform = `translate(-50%, -50%) scale(${0.85 + 0.15 * cp})`;
        }
        if (userBubble) {
          const up = Math.min(1, chatProgress / 0.4);
          userBubble.style.opacity = `${up}`;
          userBubble.style.transform = `scale(${0.8 + 0.2 * up})`;
        }
        if (botBubble) {
          const bp = Math.max(0, Math.min(1, (chatProgress - 0.4) / 0.4));
          botBubble.style.opacity = `${bp}`;
          botBubble.style.transform = `scale(${0.8 + 0.2 * bp})`;
        }
      }
    }
  }

  // Initialisation à l'évaluation du script
  initData();
})();
