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

    // 0. HUD AGENT404
    const totalDuration = (window.SCENES && window.SCENES.length > 0) ? window.SCENES[window.SCENES.length - 1].end : 71.51;
    const hudFill = document.getElementById("hud-progress-fill");
    const hudTimer = document.getElementById("hud-timer");
    if (hudFill && totalDuration > 0) {
      const pct = Math.min(100, Math.max(0, (t / totalDuration) * 100));
      hudFill.style.width = `${pct}%`;
    }
    if (hudTimer) {
      const mins = Math.floor(t / 60).toString().padStart(2, "0");
      const secs = Math.floor(t % 60).toString().padStart(2, "0");
      hudTimer.textContent = `${mins}:${secs} // 30FPS`;
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
        return `
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
      const isHeadOnly = data.avatar && data.avatar.includes("mini");

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
    }
  }

  // Initialisation à l'évaluation du script
  initData();
})();
