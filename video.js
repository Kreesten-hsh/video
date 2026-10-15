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
    const targetBg = bgType || "grid";
    if (targetBg !== currentBg) {
      currentBg = targetBg;
      canvas.classList.remove("bg-grid", "bg-red", "bg-diamonds", "bg-circles");
      canvas.classList.add(`bg-${targetBg}`);
    }

    if (targetBg === "grid") {
      const pos = (t * 20) % 60;
      canvas.style.backgroundPosition = `${pos}px ${pos}px`;
      canvas.style.backgroundSize = "60px 60px";
    } else if (targetBg === "red") {
      canvas.style.backgroundPosition = "0px 0px";
      canvas.style.backgroundSize = "60px 60px";
    } else if (targetBg === "circles") {
      const posY = (t * 600) % 120;
      canvas.style.backgroundPosition = `0px ${posY}px`;
      canvas.style.backgroundSize = "100px 120px";
    } else if (targetBg === "diamonds") {
      const scale = 1.0 + 0.12 * Math.sin(progress * Math.PI);
      const size = Math.round(90 * scale);
      const pos = (t * 25) % size;
      canvas.style.backgroundPosition = `${pos}px ${pos}px`;
      canvas.style.backgroundSize = `${size}px ${size}px`;
    }
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
        .map((w, idx) => `<span class="sub-word" id="sw-${idx}">${w.word}</span>`)
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
        const isHeadOnly = data.avatar && (data.avatar.includes("skeptic") || data.avatar.includes("mini"));
        return `
          <div class="comp-face ${isHeadOnly ? 'face-headonly' : ''}" id="comp-face">
            <img src="${data.avatar}" alt="Avatar" class="avatar-sticker" id="avatar-img" />
            ${data.label ? `<div class="face-badge" id="face-badge">${data.label}</div>` : ""}
          </div>
        `;
      case "big":
        return `
          <div class="comp-big" id="comp-big">
            <div class="big-box">${data.text}</div>
            ${data.sub ? `<div class="big-sub">${data.sub}</div>` : ""}
          </div>
        `;
      case "list":
        return `
          <div class="comp-list" id="comp-list">
            ${data.items.map((item, i) => `
              <div class="list-item" id="list-item-${i}">
                <div class="item-num">${String(i + 1).padStart(2, '0')}</div>
                <div class="item-text">${item}</div>
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
              <div class="window-title">${data.title || "terminal"}</div>
              <div style="width: 70px;"></div>
            </div>
            <div class="window-body"><span id="typewriter-content"></span><span class="cursor">▋</span></div>
          </div>
        `;
      case "cards":
        return `
          <div class="comp-cards" id="comp-cards">
            ${data.cards.map((c, i) => `
              <div class="card-item" id="card-item-${i}">
                <div class="card-icon">${c.icon}</div>
                <div class="card-title">${c.title}</div>
              </div>
            `).join("")}
          </div>
        `;
      case "split":
        return `
          <div class="comp-split" id="comp-split">
            <div class="split-col" id="split-col-left">
              <div class="split-badge badge-red">${data.left_badge || "AVANT ❌"}</div>
              <div class="split-card">
                <div class="split-title">${data.left_title || "MONTAGE MANUEL"}</div>
                <ul class="split-items">
                  ${(data.left_items || []).map(it => `<li>❌ ${it}</li>`).join("")}
                </ul>
              </div>
            </div>
            <div class="split-col" id="split-col-right">
              <div class="split-badge badge-green">${data.right_badge || "CODE ✅"}</div>
              <div class="split-card highlight">
                <div class="split-title">${data.right_title || "100% PROGRAMMÉ"}</div>
                <ul class="split-items">
                  ${(data.right_items || []).map(it => `<li>⚡ ${it}</li>`).join("")}
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
          <div class="comp-audio-wave" id="comp-audio-wave">
            <div class="wave-header">
              <div class="wave-tag">PIPELINE AUDIO v2.0</div>
              <div class="wave-status" id="wave-status">ANALYSE DU SPECTRE</div>
            </div>
            <div class="wave-bars-container" id="wave-bars-container">
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
      const isHeadOnly = data.avatar && (data.avatar.includes("skeptic") || data.avatar.includes("mini"));
      if (avatar) {
        if (isHeadOnly) {
          avatar.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
          avatar.style.transformOrigin = "center center";
        } else {
          avatar.style.transform = `translateX(-50%) translateY(${spring.ty}px) scale(${spring.scale})`;
          avatar.style.transformOrigin = "bottom center";
        }
      }
      if (badge && elapsed < 0.35) {
        const badgeP = Math.min(1, elapsed / 0.35);
        const bScale = 0.7 + 0.3 * badgeP + 0.1 * Math.sin(badgeP * Math.PI);
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
          statusEl.style.background = "#2BD980";
        }
        if (silenceBadge) {
          silenceBadge.textContent = "RYTHME 100% ACTIF";
          silenceBadge.style.background = "#FFE600";
        }
        if (btn) {
          btn.classList.add("pressed");
          btn.textContent = "✓ SILENCES PURGÉS";
        }
      } else {
        if (statusEl) {
          statusEl.textContent = "ANALYSE DU SPECTRE";
          statusEl.style.background = "var(--yellow)";
        }
        if (silenceBadge) {
          silenceBadge.textContent = "SILENCE DÉTECTÉ : 0.38s";
          silenceBadge.style.background = "var(--bg-beige)";
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
      if (contentEl && data.text) {
        const charCount = Math.floor(progress * data.text.length);
        contentEl.textContent = data.text.substring(0, charCount);
      }
    } else if (type === "rpg") {
      const el = document.getElementById("comp-rpg");
      if (el) {
        el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      }
    }
  }

  // Initialisation à l'évaluation du script
  initData();
})();
