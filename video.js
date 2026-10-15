/**
 * MOTEUR D'ANIMATION DÉTERMINISTE VANILLA JS
 * Expose window.setTime(t) pour le rendu frame-par-frame headless
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
   * Met à jour le fond dynamique du canvas en fonction de scene.data.bg
   * Valeurs supportées : 'grid' (défaut), 'red', 'diamonds', 'circles'
   */
  function updateBackground(bgType) {
    const targetBg = bgType || "grid";
    if (targetBg === currentBg) return;
    currentBg = targetBg;
    canvas.classList.remove("bg-grid", "bg-red", "bg-diamonds", "bg-circles");
    canvas.classList.add(`bg-${targetBg}`);
  }

  /**
   * Fonction globale de rendu instantané à l'instant t (en secondes)
   */
  window.setTime = function (t) {
    if (subtitleChunks.length === 0 && window.WORDS && window.WORDS.length > 0) {
      initData();
    }

    // 1. Sous-titres dynamiques (Top 20%)
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
      updateBackground("grid");
      return;
    }

    const scene = window.SCENES[sceneIdx];
    const duration = scene.end - scene.start;
    const progress = Math.min(1, Math.max(0, (t - scene.start) / duration));

    // Gestion du fond dynamique de la scène
    updateBackground(scene.data && scene.data.bg);

    // Initialisation du DOM du composant au changement de scène
    if (sceneIdx !== activeSceneIndex) {
      activeSceneIndex = sceneIdx;
      sceneContainer.innerHTML = renderComponent(scene.type, scene.data);
    }

    // Mise à jour continue déterministe (ressort, typing, list index)
    animateComponent(scene.type, scene.data, progress, t);
  }

  function renderComponent(type, data) {
    switch (type) {
      case "face":
        const isHeadOnly = data.avatar && (data.avatar.includes("skeptic") || data.avatar.includes("mini"));
        return `
          <div class="comp-face ${isHeadOnly ? 'face-headonly' : ''}" id="comp-face">
            <img src="${data.avatar}" alt="Avatar" class="avatar-sticker" id="avatar-img" />
            ${data.label ? `<div class="face-badge">${data.label}</div>` : ""}
          </div>
        `;
      case "big":
        return `
          <div class="comp-big">
            <div class="big-box">${data.text}</div>
            ${data.sub ? `<div class="big-sub">${data.sub}</div>` : ""}
          </div>
        `;
      case "list":
        return `
          <div class="comp-list">
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
          <div class="comp-window">
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
          <div class="comp-cards">
            ${data.cards.map(c => `
              <div class="card-item">
                <div class="card-icon">${c.icon}</div>
                <div class="card-title">${c.title}</div>
              </div>
            `).join("")}
          </div>
        `;
      case "rpg":
        return `
          <div class="comp-rpg">
            <div class="rpg-top-meta">
              <div class="rpg-tag">ZONE: ${data.zone || "WORLD"}</div>
              <div class="rpg-tag">QUÊTE: ${data.quest || "MAIN"}</div>
            </div>
            <div class="rpg-scene">${data.illustration || "⚔️"}</div>
            <div class="rpg-dialog-box">
              <img src="${data.mini_avatar}" class="rpg-avatar" />
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

  function animateComponent(type, data, progress, t) {
    if (type === "face") {
      const avatar = document.getElementById("avatar-img");
      if (avatar) {
        const isHeadOnly = data.avatar && (data.avatar.includes("skeptic") || data.avatar.includes("mini"));
        const spring = Math.sin(Math.min(1, progress * 4) * (Math.PI / 2));
        const scale = 0.75 + 0.25 * spring;
        if (isHeadOnly) {
          avatar.style.transform = `scale(${scale})`;
          avatar.style.transformOrigin = "center center";
        } else {
          avatar.style.transform = `translateX(-50%) scale(${scale})`;
          avatar.style.transformOrigin = "bottom center";
        }
      }
    } else if (type === "window") {
      const contentEl = document.getElementById("typewriter-content");
      if (contentEl && data.text) {
        const charCount = Math.floor(progress * data.text.length);
        contentEl.textContent = data.text.substring(0, charCount);
      }
    } else if (type === "list") {
      const total = data.items.length;
      const activeIdx = Math.min(total - 1, Math.floor(progress * total));
      for (let i = 0; i < total; i++) {
        const itemEl = document.getElementById(`list-item-${i}`);
        if (itemEl) {
          if (i === activeIdx) {
            itemEl.classList.add("active");
          } else {
            itemEl.classList.remove("active");
          }
        }
      }
    }
  }

  // Initialisation à l'évaluation du script
  initData();
})();
