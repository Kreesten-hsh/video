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

  function easeOutExpo(x) {
    return x === 1 ? 1 : 1 - Math.pow(2, -10 * x);
  }

  function easeInOutCubic(x) {
    return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  }

  function easeOutBack(x) {
    const c1 = 1.70158;
    const c3 = c1 + 1;
    return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
  }

  /**
   * Découpe la liste de mots Whisper en paquets dynamiques mot par mot :
   * - center_slam (88px) : 2 à 3 mots max pour ne jamais déborder
   * - dynamic_band (52px) : 3 mots
   * - single_line_top (38px) / legacy : 4 mots max
   * Fermeture immédiate du paquet si :
   * 1. Changement de scène (findSceneIdx(w[j+1]) !== findSceneIdx(w[j]))
   * 2. Ponctuation forte (., ?, !, :, ou , en center_slam)
   * 3. Pause respiratoire >= 0.22s
   */
  function buildSubtitleChunks(words) {
    if (!words || words.length === 0) return [];

    function findSceneIdx(time) {
      return (window.SCENES || []).findIndex(s => time >= s.start && time < s.end);
    }

    const chunks = [];
    let currentSlice = [];
    let currentMode = "legacy";

    for (let j = 0; j < words.length; j++) {
      const w = words[j];
      const scIdx = findSceneIdx(w.start);
      const sc = scIdx !== -1 ? window.SCENES[scIdx] : null;
      const mode = (sc && sc.caption_mode) || "legacy";

      if (currentSlice.length === 0) {
        currentMode = mode;
      }

      // Nettoyage de la ponctuation : suppression des ., ,, ;, : à la fin (conservation de ? et !)
      const cleanedWord = (w.word || "").replace(/[.,;:]+$/, "");
      currentSlice.push({
        ...w,
        word: cleanedWord,
        rawWord: w.word
      });

      let chunkSize = 4;
      if (mode === "center_slam") {
        const firstLen = currentSlice[0].word.length;
        const secondLen = words[j + 1] ? words[j + 1].word.length : 0;
        chunkSize = (firstLen + secondLen > 13) ? 2 : 3;
      } else if (mode === "dynamic_band") {
        chunkSize = 3;
      } else if (mode === "single_line_top") {
        chunkSize = 4;
      }

      let shouldClose = false;

      // Taille max atteinte
      if (currentSlice.length >= chunkSize) {
        shouldClose = true;
      }

      // Dernier mot
      if (j === words.length - 1) {
        shouldClose = true;
      } else {
        const nextW = words[j + 1];
        const nextScIdx = findSceneIdx(nextW.start);

        // Condition 1 : Changement de scène
        if (nextScIdx !== scIdx) {
          shouldClose = true;
        }

        // Condition 2 : Ponctuation forte
        const wordText = (w.word || "").trim();
        const hasPunctuation = (mode === "center_slam")
          ? /[.,!?:;]$/.test(wordText)
          : /[.!?:]$/.test(wordText);

        if (hasPunctuation) {
          shouldClose = true;
        }

        // Condition 3 : Pause respiratoire >= 0.22s
        if ((nextW.start - w.end) >= 0.22) {
          shouldClose = true;
        }
      }

      if (shouldClose && currentSlice.length > 0) {
        chunks.push({
          start: currentSlice[0].start,
          end: currentSlice[currentSlice.length - 1].end,
          words: currentSlice,
          mode: currentMode
        });
        currentSlice = [];
      }
    }

    if (currentSlice.length > 0) {
      chunks.push({
        start: currentSlice[0].start,
        end: currentSlice[currentSlice.length - 1].end,
        words: currentSlice,
        mode: currentMode
      });
    }

    // Anti-mot orphelin obligatoire : fusionne les chunks isolés de 1 seul mot
    for (let i = chunks.length - 1; i >= 1; i--) {
      const c = chunks[i];
      const prev = chunks[i - 1];
      if (c.words.length === 1) {
        const scIdxCurrent = findSceneIdx(c.start);
        const scIdxPrev = findSceneIdx(prev.start);
        if (scIdxCurrent === scIdxPrev || prev.words.length <= 3) {
          prev.words.push(...c.words);
          prev.end = c.end;
          chunks.splice(i, 1);
        }
      }
    }
    if (chunks.length > 1 && chunks[0].words.length === 1) {
      chunks[1].words.unshift(...chunks[0].words);
      chunks[1].start = chunks[0].start;
      chunks.splice(0, 1);
    }

    // Coloration sémantique fixe (Style @ledevultime) : 1 mot-clé porteur de sens
    const FRENCH_STOP_WORDS = new Set([
      "le", "la", "les", "un", "une", "des", "de", "du", "d", "l",
      "tu", "il", "on", "mais", "ou", "et", "donc",
      "dans", "sur", "pour", "par", "avec", "sans",
      "qui", "que", "ne", "pas", "plus",
      "as", "est", "sont", "a", "en", "au"
    ]);

    chunks.forEach(chunk => {
      let bestIdx = -1;
      let maxLen = -1;
      chunk.words.forEach((cw, idx) => {
        const cleanNorm = (cw.word || "").toLowerCase().replace(/[^a-zà-ÿ0-9]/g, "");
        if (!FRENCH_STOP_WORDS.has(cleanNorm)) {
          if (cleanNorm.length > maxLen) {
            maxLen = cleanNorm.length;
            bestIdx = idx;
          }
        }
      });
      if (bestIdx === -1 && chunk.words.length > 0) {
        chunk.words.forEach((cw, idx) => {
          const cleanNorm = (cw.word || "").toLowerCase().replace(/[^a-zà-ÿ0-9]/g, "");
          if (cleanNorm.length > maxLen) {
            maxLen = cleanNorm.length;
            bestIdx = idx;
          }
        });
      }
      chunk.keywordIndex = bestIdx >= 0 ? bestIdx : 0;
    });

    return chunks;
  }

  function initData() {
    // 1. Initialisation des Thèmes (Preset ou Variables personnalisées)
    if (window.PROJECT_CONFIG) {
      if (window.PROJECT_CONFIG.theme_preset) {
        document.documentElement.setAttribute("data-theme", window.PROJECT_CONFIG.theme_preset);
        if (canvas) canvas.setAttribute("data-theme", window.PROJECT_CONFIG.theme_preset);
      }
      if (window.PROJECT_CONFIG.theme) {
        const root = document.documentElement;
        for (const [key, val] of Object.entries(window.PROJECT_CONFIG.theme)) {
          root.style.setProperty(`--${key}`, val);
        }
      }
    }

    subtitleChunks = buildSubtitleChunks(window.WORDS || []);

    try {
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get("safe_zones") === "1" || urlParams.get("safezones") === "1") {
        let overlay = document.getElementById("safe-zones-overlay");
        if (!overlay && canvas) {
          overlay = document.createElement("div");
          overlay.id = "safe-zones-overlay";
          overlay.innerHTML = `
            <div class="sz-zone-top">UI APPS DANGER (0 - 220px)</div>
            <div class="sz-crop-insta-4-5"></div>
            <div class="sz-crop-insta-1-1"></div>
            <div class="sz-zone-right">UI BOUTONS (950 - 1080px)</div>
            <div class="sz-zone-bottom">UI NOM & TICKER DANGER (1540 - 1920px)</div>
          `;
          canvas.appendChild(overlay);
        }
      }
    } catch (e) {}
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
   * Pilote la Caméra Virtuelle Non-Linéaire, les Keyframes et la Parallaxe à 30% sur #bg-layer
   */
  function updateCamera(t, scene, progress) {
    const rig = document.getElementById("camera-rig");
    if (!rig) return;

    let currentZoom = 1.0;
    let currentPanX = 0;
    let currentPanY = 0;
    const drift = 0.03 * progress;

    if (scene && scene.camera && Array.isArray(scene.camera.keyframes) && scene.camera.keyframes.length > 0) {
      const kfs = scene.camera.keyframes;
      let k1 = kfs[0];
      let k2 = kfs[kfs.length - 1];
      for (let i = 0; i < kfs.length - 1; i++) {
        if (t >= kfs[i].at && t <= kfs[i + 1].at) {
          k1 = kfs[i];
          k2 = kfs[i + 1];
          break;
        }
      }
      const dt = Math.max(0.001, k2.at - k1.at);
      const rawP = Math.min(1, Math.max(0, (t - k1.at) / dt));
      const pEased = dt <= 0.6 ? easeOutBack(rawP) : (dt <= 0.8 ? easeOutExpo(rawP) : easeInOutCubic(rawP));
      currentZoom = (k1.zoom || 1.0) + ((k2.zoom || 1.0) - (k1.zoom || 1.0)) * pEased + drift;
      currentPanX = (k1.panX || 0) + ((k2.panX || 0) - (k1.panX || 0)) * pEased;
      currentPanY = (k1.panY || 0) + ((k2.panY || 0) - (k1.panY || 0)) * pEased;
    } else if (scene && scene.camera) {
      const cam = scene.camera;
      const pEased = easeInOutCubic(progress);
      const zFrom = cam.zoomFrom || 1.0;
      const zTo = cam.zoomTo || (zFrom + 0.04);
      currentZoom = zFrom + (zTo - zFrom) * pEased + drift;
      currentPanX = (cam.panX || 0) * pEased;
      currentPanY = (cam.panY || 0) * pEased;
    } else {
      currentZoom = 1.0;
      currentPanX = 0;
      currentPanY = 0;
    }

    // Punch-in dynamique à chaque début de scène sur les 0.30 premières secondes
    if (scene) {
      const sceneElapsed = Math.max(0, t - scene.start);
      if (sceneElapsed < 0.30) {
        const pScene = sceneElapsed / 0.30;
        const entryPunch = (1 - easeOutBack(pScene)) * 0.06;
        currentZoom += entryPunch;
      }
    }

    // En mode center_slam, zoom-kick (scale 1.06 -> 1.0) à chaque nouveau paquet de mots
    const isCenterSlam = scene && (scene.caption_mode === "center_slam");
    if (isCenterSlam && subtitleChunks.length > 0) {
      const curChunk = subtitleChunks.find(c => t >= c.start && t <= c.end);
      if (curChunk) {
        const chunkElapsed = Math.max(0, t - curChunk.start);
        if (chunkElapsed < 0.25) {
          const pKick = chunkElapsed / 0.25;
          const kick = (1 - easeOutExpo(pKick)) * 0.06;
          currentZoom += kick;
        }
      }
    }

    rig.style.transform = `scale(${currentZoom}) translate(${currentPanX}px, ${currentPanY}px)`;

    // Parallaxe 30% sur le fond et dérive vivante du filigrane
    const bgLayer = document.getElementById("bg-layer");
    if (bgLayer) {
      const bgZoom = 1 + (currentZoom - 1) * 0.3;
      const bgPanX = currentPanX * 0.3;
      const bgPanY = currentPanY * 0.3;
      bgLayer.style.transform = `scale(${bgZoom}) translate(${bgPanX}px, ${bgPanY}px)`;
    }
    const watermark = document.getElementById("watermark-text");
    if (watermark) {
      const driftX = (t * 10) % 400 - 200;
      const driftY = Math.sin(t * 0.35) * 12;
      watermark.style.transform = `translate(${driftX}px, ${driftY}px)`;
      if (scene && scene.watermark && watermark.textContent !== scene.watermark) {
        watermark.textContent = scene.watermark;
      }
    }
  }

  /**
   * Chorégraphie de l'Avatar Global selon scene.avatar_mode ("hero", "inset", "hidden")
   */
  function updateAvatar(t, scene, progress) {
    const wrapper = document.getElementById("global-avatar-wrapper");
    const img = document.getElementById("global-avatar-img");
    if (!wrapper || !img) return;

    // L'avatar n'apparaît que s'il est explicitement 'hero' (ou face sans masquage)
    const isSelfContainedAvatar = (scene.type === "blueprint_overwhelm" || scene.type === "face_to_dm_cta" || scene.type === "face");
    const mode = isSelfContainedAvatar ? "hidden" : (
      scene.avatar_mode === "hero" ? "hero" : "hidden"
    );

    wrapper.className = "avatar-" + mode;

    if (scene.data && scene.data.avatar && !isSelfContainedAvatar) {
      if (img.getAttribute("src") !== scene.data.avatar) {
        img.setAttribute("src", scene.data.avatar);
      }
    }

    if (mode === "hero") {
      const floatY = Math.sin(t * 4.5) * 8;
      const tilt = Math.sin(t * 2.2) * 1.2;
      img.style.transform = `translateY(${floatY}px) rotate(${tilt}deg)`;
    } else if (mode === "inset") {
      const pulse = 1.0 + Math.sin(t * 3) * 0.03;
      wrapper.style.transform = `scale(${pulse})`;
    }
  }

  /**
   * Fonction globale de rendu instantané à l'instant t (en secondes)
   */
  window.setTime = function (t) {
    if (subtitleChunks.length === 0 && window.WORDS && window.WORDS.length > 0) {
      initData();
    }

    const sceneIdx = (window.SCENES || []).findIndex(s => t >= s.start && t < s.end);
    const activeScene = sceneIdx !== -1 ? window.SCENES[sceneIdx] : null;

    // 1. Sous-titres dynamiques multi-zones avec anti-collision
    updateSubtitles(t, activeScene);

    // 2. Scène centrale & inférieure
    updateScenes(t);
  };

  function updateSubtitles(t, activeScene) {
    const subtitlesZone = document.getElementById("subtitles-zone");
    if (!subtitlesZone) return;

    // Suppression de collision sur scènes Avatar avec hero_title
    if (activeScene && activeScene.type === "face" && activeScene.data && activeScene.data.hero_title) {
      subtitlesZone.className = "mode-hidden";
      return;
    }

    let mode = (activeScene && activeScene.caption_mode) || "legacy";
    if (activeScene && activeScene.type === "blueprint_kinetic_type" && mode !== "center_slam" && mode !== "hidden") {
      mode = "single_line_top";
    }

    if (mode === "center_slam") {
      subtitlesZone.className = "mode-center-slam";
      if (activeScene && activeScene.avatar_mode === "hero") {
        subtitlesZone.classList.add("has-avatar-hero");
      }
    } else if (mode === "dynamic_band") {
      subtitlesZone.className = "mode-dynamic-band";
    } else if (mode === "single_line_top") {
      subtitlesZone.className = "mode-single-line-top";
    } else if (mode === "hidden" || mode === "ui_embedded") {
      subtitlesZone.className = "mode-hidden";
    } else {
      subtitlesZone.className = ""; // legacy mode
    }

    // Anti-collision : si center_slam et que la scène n'est pas kinetic_type,
    // on masque ou abaisse la carte centrale de #scene-container
    if (sceneContainer) {
      if (mode === "center_slam" && activeScene && activeScene.type !== "blueprint_kinetic_type") {
        sceneContainer.style.opacity = "0.15";
        sceneContainer.style.transform = "scale(0.88)";
      } else {
        sceneContainer.style.opacity = "";
        sceneContainer.style.transform = "";
      }
    }

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
        .map((w, idx) => {
          const isKeyword = idx === chunk.keywordIndex;
          const cls = `sub-word word${isKeyword ? ' keyword-accent' : ''}`;
          return `<span class="${cls}" id="sw-${idx}">${w.word}</span>`;
        })
        .join(" ");
    }

    // Karaoké actif uniquement en mode center_slam ou dynamic_band (désactivé en single_line_top pour un affichage stable)
    if (mode === "center_slam" || mode === "dynamic_band") {
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

    if (mode === "center_slam") {
      const chunkElapsed = Math.max(0, t - chunk.start);
      const slamSpring = calcSpringOvershoot(chunkElapsed);
      subtitlesBox.style.transform = `scale(${slamSpring.scale})`;
    } else {
      subtitlesBox.style.transform = "";
    }
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

    // Caméra virtuelle non-linéaire & parallaxe
    updateCamera(t, scene, progress);

    // Chorégraphie de l'avatar
    updateAvatar(t, scene, progress);

    // Décor dynamique piloté par t et progress
    updateBackground(scene.data && scene.data.bg, t, progress);

    // Changement dynamique de thème à la volée (effet caméléon)
    if (scene.switch_theme) {
      document.documentElement.setAttribute("data-theme", scene.switch_theme);
      if (canvas) canvas.setAttribute("data-theme", scene.switch_theme);
    }

    // Injection DOM au changement de scène (support des 6 blueprints ou des scènes legacy)
    if (sceneIdx !== activeSceneIndex) {
      activeSceneIndex = sceneIdx;
      if (scene.type && scene.type.startsWith("blueprint_")) {
        sceneContainer.innerHTML = renderBlueprint(scene.type, scene.data || {}, scene);
      } else {
        sceneContainer.innerHTML = renderComponent(scene.type, scene.data);
      }
    }

    // Animation continue déterministe avec physique d'overshoot et beats sémantiques
    if (scene.type && scene.type.startsWith("blueprint_")) {
      animateBlueprint(scene.type, scene.data || {}, progress, elapsed, t, scene);
    } else {
      animateComponent(scene.type, scene.data, progress, elapsed, t, scene);
    }
  }

  /**
   * ==========================================================================
   * LES 6 BLUEPRINTS SIGNATURES DU STUDIO AGENT404
   * ==========================================================================
   */
  const SVG_LINKEDIN = `<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><rect width="48" height="48" rx="10" fill="#0A66C2"/><path d="M14.5 19H19.5V35H14.5V19ZM17 12C15.4 12 14 13.4 14 15C14 16.6 15.4 18 17 18C18.6 18 20 16.6 20 15C20 13.4 18.6 12 17 12Z" fill="white"/><path d="M22.5 19H27.3V21.2H27.4C28.1 19.9 29.8 18.5 32.3 18.5C37.5 18.5 38.5 21.9 38.5 26.4V35H33.5V27.1C33.5 25.2 33.5 22.8 30.8 22.8C28.1 22.8 27.7 24.9 27.7 26.9V35H22.5V19Z" fill="white"/></svg>`;

  const SVG_TIKTOK = `<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><rect width="48" height="48" rx="10" fill="#000000"/><path d="M33.5 17.5C31.5 17.5 29.8 16.6 28.5 15.2V27.8C28.5 33.2 24.1 37.5 18.8 37.5C13.4 37.5 9 33.1 9 27.8C9 22.4 13.4 18 18.8 18C19.3 18 19.8 18.05 20.3 18.15V22.9C19.8 22.75 19.3 22.65 18.8 22.65C16 22.65 13.7 24.95 13.7 27.75C13.7 30.55 16 32.85 18.8 32.85C21.6 32.85 23.8 30.55 23.8 27.75V9.5H28.5C28.5 12.3 30.7 14.5 33.5 14.5V17.5Z" fill="#25F4EE"/><path d="M34.5 16.5C32.5 16.5 30.8 15.6 29.5 14.2V26.8C29.5 32.2 25.1 36.5 19.8 36.5C14.4 36.5 10 32.1 10 26.8C10 21.4 14.4 17 19.8 17C20.3 17 20.8 17.05 21.3 17.15V21.9C20.8 21.75 20.3 21.65 19.8 21.65C17 21.65 14.7 23.95 14.7 26.75C14.7 29.55 17 31.85 19.8 31.85C22.6 31.85 24.8 29.55 24.8 26.75V8.5H29.5C29.5 11.3 31.7 13.5 34.5 13.5V16.5Z" fill="#FE2C55"/><path d="M34 17C32 17 30.3 16.1 29 14.7V27.3C29 32.7 24.6 37 19.3 37C13.9 37 9.5 32.6 9.5 27.3C9.5 21.9 13.9 17.5 19.3 17.5C19.8 17.5 20.3 17.55 20.8 17.65V22.4C20.3 22.25 19.8 22.15 19.3 22.15C16.5 22.15 14.2 24.45 14.2 27.25C14.2 30.05 16.5 32.35 19.3 32.35C22.1 32.35 24.3 30.05 24.3 27.25V9H29C29 11.8 31.2 14 34 14V17Z" fill="white"/></svg>`;

  const SVG_REELS = `<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><defs><radialGradient id="ig-grad" cx="20%" cy="110%" r="130%"><stop offset="0%" stop-color="#FFDD55"/><stop offset="25%" stop-color="#FF5D3B"/><stop offset="50%" stop-color="#FF0069"/><stop offset="75%" stop-color="#D300C5"/><stop offset="100%" stop-color="#7638FA"/></radialGradient></defs><rect width="48" height="48" rx="12" fill="url(#ig-grad)"/><rect x="11" y="11" width="26" height="26" rx="7" stroke="white" stroke-width="3" fill="none"/><circle cx="24" cy="24" r="6" stroke="white" stroke-width="3" fill="none"/><circle cx="31.5" cy="16.5" r="1.5" fill="white"/></svg>`;

  const SVG_SHORTS = `<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><rect width="48" height="48" rx="10" fill="#FF0000"/><path d="M31.2 20.1C29.6 19.2 28.2 19.1 28.2 19.1L29.6 18.2C32.1 16.7 32.9 13.5 31.4 11C29.9 8.5 26.7 7.7 24.2 9.2L16.2 14C14.1 15.3 12.8 17.7 13 20.2C13.2 22.7 14.9 24.7 17.3 25.3L15.6 26.3C13.1 27.8 12.3 31 13.8 33.5C15.3 36 18.5 36.8 21 35.3L29 30.5C31.1 29.2 32.4 26.8 32.2 24.3C32 21.8 30.3 20.8 31.2 20.1Z" fill="#CC0000"/><path d="M29.5 17.5L24 14.2C21.8 12.9 19 13.6 17.7 15.8C16.4 18 17.1 20.8 19.3 22.1L20.8 23L16.5 25.5C14.3 26.8 13.6 29.6 14.9 31.8C16.2 34 19 34.7 21.2 33.4L26.7 30.1C28.9 28.8 29.6 26 28.3 23.8L26.8 22.9L31.1 20.4C33.3 19.1 34 16.3 32.7 14.1C31.7 12.4 29.5 17.5 29.5 17.5Z" fill="white"/><polygon points="21,19 21,29 29,24" fill="#FF0000"/></svg>`;

  function renderBlueprint(type, data, scene) {
    switch (type) {
      case "blueprint_kinetic_type":
        const highlight = data.highlight || "";
        let textHtml = data.text || "";
        if (highlight && textHtml.includes(highlight)) {
          textHtml = textHtml.replace(highlight, `<span class="highlight">${highlight}</span>`);
        }
        const isCenterSlam = (scene && scene.caption_mode === "center_slam");
        return `
          <div class="blueprint-kinetic-type ${isCenterSlam ? "has-center-slam" : ""}" id="blueprint-kinetic-type">
            ${data.tag ? `<div class="bkt-tag">${data.tag}</div>` : ""}
            ${!isCenterSlam ? `<div class="bkt-main-text">${textHtml}</div>` : ""}
            ${data.impact_number ? `<div class="bkt-impact-number">${data.impact_number}</div>` : ""}
          </div>
        `;

      case "blueprint_cursor_ui":
        const themes = data.themes || [
          { name: "01. Éditorial Chaud", id: "claude" },
          { name: "02. Tech Sombre", id: "cobalt-grid" },
          { name: "03. Conseil Financier", id: "editorial-forest" },
          { name: "04. Créateur Percutant", id: "bold-poster" }
        ];
        return `
          <div class="blueprint-cursor-ui" id="blueprint-cursor-ui">
            <div class="bcui-header">
              <div class="bcui-title">${data.title || "EFFET CAMÉLÉON : 4 CHARTES"}</div>
              <div class="bcui-status" id="bcui-status">${data.status_initial || "SUR-MESURE HAUTE PRÉCISION"}</div>
            </div>
            <div class="bcui-preview" id="bcui-preview">
              <div class="bcui-preview-badge">DIRECTION ARTISTIQUE ACTIVE</div>
              <div class="bcui-preview-title" id="bcui-preview-title">${data.preview_title || "CHARTE GRAPHIQUE : PRÊTE À ADAPTER"}</div>
            </div>
            <div class="bcui-actions-grid" id="bcui-actions-grid">
              ${themes.map((th, idx) => `
                <div class="bcui-btn" id="bcui-btn-${idx}">
                  ${th.name}
                </div>
              `).join("")}
            </div>
            <svg class="bcui-cursor" id="bcui-cursor" viewBox="0 0 24 24" fill="none">
              <path d="M5.5 3.2L18.8 12.4C19.7 13 19.3 14.5 18.2 14.6L12.5 15.1L9.6 20.3C9.1 21.2 7.7 21 7.5 19.9L5.5 3.2Z" fill="var(--mint)" stroke="var(--bg-carbon)" stroke-width="2"/>
            </svg>
            <div class="cursor-click-ripple" id="bcui-ripple"></div>
          </div>
        `;

      case "blueprint_terminal_scene":
        return `
          <div class="blueprint-terminal-scene" id="blueprint-terminal-scene">
            <div class="bts-titlebar">
              <div class="bts-dot bts-dot-close"></div>
              <div class="bts-dot bts-dot-min"></div>
              <div class="bts-dot bts-dot-max"></div>
              <div class="bts-title">${data.window_title || "agent404-terminal"}</div>
            </div>
            <div class="bts-body">
              <div><span class="bts-prompt">&gt;</span><span id="bts-command-text"></span><span class="bts-cursor-block" id="bts-cursor"></span></div>
              <div class="bts-output" id="bts-output" style="display: none;">${data.output_text || "✓ Traitement terminé avec succès."}</div>
            </div>
          </div>
        `;

      case "blueprint_compare_split":
        return `
          <div class="blueprint-compare-split" id="blueprint-compare-split">
            <div class="bcs-card bcs-card-avant" id="bcs-card-avant">
              <div class="bcs-badge bcs-badge-avant" id="bcs-badge-avant">${data.badge_avant || "✕ CLONE IA GÉNÉRIQUE"}</div>
              <div class="bcs-card-title">${data.title_avant || "Visage Robotique"}</div>
              <div class="bcs-card-desc">${data.desc_avant || "Même modèle cloné que tout le monde sur LinkedIn"}</div>
            </div>
            <div class="bcs-card bcs-card-apres bcs-card-warning" id="bcs-card-apres">
              <div class="bcs-badge bcs-badge-apres" id="bcs-badge-apres">${data.badge_apres || "⚠️ SANCTION CRÉDIBILITÉ"}</div>
              <div class="bcs-card-title" id="bcs-title-apres">${data.title_apres || "Crédibilité : 0%"}</div>
              <div class="bcs-card-desc" id="bcs-desc-apres">${data.desc_apres || "Confiance détruite en 3 secondes chrono"}</div>
              <div class="bcs-gauge-container" id="bcs-gauge-container">
                <div class="bcs-gauge-label">
                  <span>NIVEAU DE CONFIANCE</span>
                  <span class="bcs-gauge-val" id="bcs-gauge-val">100%</span>
                </div>
                <div class="bcs-gauge-track">
                  <div class="bcs-gauge-fill" id="bcs-gauge-fill" style="width: 100%;"></div>
                </div>
              </div>
            </div>
          </div>
        `;

      case "blueprint_spatial_pan":
        const stations = data.stations || [
          { title: "NOTE VOCALE OU POST", icon: "🎤" },
          { title: "DÉCOUPAGE RYTHMIQUE CHIRURGICAL", icon: "✂️" },
          { title: "PREUVE VISUELLE MOT-À-MOT", icon: "🎯" }
        ];
        const s1 = stations[0] || { title: "NOTE VOCALE OU POST", icon: "🎤" };
        const s2 = stations[1] || { title: "DÉCOUPAGE RYTHMIQUE CHIRURGICAL", icon: "✂️" };
        const s3 = stations[2] || { title: "PREUVE VISUELLE MOT-À-MOT", icon: "🎯" };
        return `
          <div class="blueprint-spatial-pan" id="blueprint-spatial-pan">
            <div class="bsp-station pastel-yellow" id="bsp-st-1" style="transform: rotate(-1.5deg);">
              <div class="bcs-badge bcs-badge-apres">01</div>
              <div class="bsp-content" style="display: flex; flex-direction: column; justify-content: center; gap: 6px; flex: 1; margin-left: 20px;">
                <div class="bcs-card-title" style="font-size: 32px; font-weight: 900; text-transform: uppercase;">${s1.title}</div>
                <div class="bsp-progress-track">
                  <div class="bsp-progress-fill" id="bsp-progress-1"></div>
                </div>
              </div>
              <div class="bsp-icon-box" id="bsp-icon-1">${s1.icon || "🎤"}</div>
            </div>
            <div class="bsp-connector" id="bsp-conn-1">↓</div>
            <div class="bsp-station pastel-blue" id="bsp-st-2" style="transform: rotate(1.5deg);">
              <div class="bcs-badge bcs-badge-apres">02</div>
              <div class="bsp-content" style="display: flex; flex-direction: column; justify-content: center; gap: 6px; flex: 1; margin-left: 20px;">
                <div class="bcs-card-title" style="font-size: 32px; font-weight: 900; text-transform: uppercase;">${s2.title}</div>
                <div class="bsp-progress-track">
                  <div class="bsp-progress-fill" id="bsp-progress-2"></div>
                </div>
              </div>
              <div class="bsp-icon-box" id="bsp-icon-2">${s2.icon || "✂️"}</div>
            </div>
            <div class="bsp-connector" id="bsp-conn-2">↓</div>
            <div class="bsp-station pastel-green" id="bsp-st-3" style="transform: rotate(-1.5deg);">
              <div class="bcs-badge bcs-badge-apres">03</div>
              <div class="bsp-content" style="display: flex; flex-direction: column; justify-content: center; gap: 6px; flex: 1; margin-left: 20px;">
                <div class="bcs-card-title" style="font-size: 32px; font-weight: 900; text-transform: uppercase;">${s3.title}</div>
                <div class="bsp-progress-track">
                  <div class="bsp-progress-fill" id="bsp-progress-3"></div>
                </div>
              </div>
              <div class="bsp-icon-box" id="bsp-icon-3">${s3.icon || "🎯"}</div>
            </div>
          </div>
        `;

      case "blueprint_overwhelm":
        const cards = data.cards || ["Allumer la Caméra", "Régler la Lumière", "4h de Montage", "Abandon du Post"];
        const avatarSrc = data.avatar || "assets/avatars/facepalm.png";
        return `
          <div class="blueprint-overwhelm" id="blueprint-overwhelm">
            ${data.title ? `<div class="bow-title">${data.title}</div>` : ""}
            <div class="bow-grid">
              ${cards.map((c, idx) => `
                <div class="bow-badge" id="bow-badge-${idx}">
                  ${c}
                </div>
              `).join("")}
            </div>
            <div class="bow-avatar-box">
              <img src="${avatarSrc}" alt="Avatar" class="bow-avatar" id="bow-avatar" />
            </div>
          </div>
        `;

      case "blueprint_delivery_grid":
        const channelList = [
          { name: "01. LINKEDIN", svg: SVG_LINKEDIN },
          { name: "02. TIKTOK", svg: SVG_TIKTOK },
          { name: "03. INSTAGRAM REELS", svg: SVG_REELS },
          { name: "04. YOUTUBE SHORTS", svg: SVG_SHORTS }
        ];
        return `
          <div class="blueprint-delivery-grid" id="blueprint-delivery-grid">
            <div class="bdg-header-box" id="bdg-header-box">
              <div class="bdg-header-title">⚡ LIVRAISON EN 48H CHRONO — EXPORT MULTI-FORMAT 9:16</div>
              <div class="bdg-progress-track">
                <div class="bdg-progress-bar" id="bdg-render-bar"></div>
              </div>
            </div>
            <div class="bdg-grid" id="bdg-grid">
              ${channelList.map((ch, idx) => `
                <div class="bdg-card channel-card" id="channel-card-${idx}">
                  <div class="bdg-icon">${ch.svg}</div>
                  <div class="bdg-card-title">${ch.name}</div>
                </div>
              `).join("")}
            </div>
          </div>
        `;

      default:
        return `<div class="comp-box">Blueprint ${type}</div>`;
    }
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
                  <span style="color: var(--mint-dark); font-weight: 900;">100% PRÊT</span>
                </div>
                <div class="speed-bar-track">
                  <div class="speed-bar-fill code"></div>
                </div>
              </div>
              <div class="speed-row">
                <div class="speed-label speed-row-label">
                  <span>⏳ MONTEUR HUMAIN</span>
                  <span style="color: var(--bg-carbon); font-weight: 900;">5% EN ATTENTE</span>
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
                <path d="M4 3L11 21L14 13L22 10L4 3Z" fill="var(--accent-primary)" stroke="var(--bg-carbon)" stroke-width="2.5" stroke-linejoin="round"/>
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
              <div class="loom-drop-url">loom.com/share/demo_produit_v4.mp4</div>
              <div class="loom-drop-badge">LECTEUR B2B BLOQUÉ</div>
            </div>
            <div class="loom-drop-screen">
              <div class="loom-drop-chart-zone">
                <svg class="loom-drop-chart-svg" viewBox="0 0 860 220" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="dropGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="var(--accent-warning)" stop-opacity="0.3" />
                      <stop offset="100%" stop-color="var(--accent-warning)" stop-opacity="0.0" />
                    </linearGradient>
                  </defs>
                  <path d="M 0 30 Q 180 35 240 180 L 860 195 L 860 220 L 0 220 Z" fill="url(#dropGrad)" />
                  <path d="M 0 30 Q 180 35 240 180 L 860 195" fill="none" stroke="var(--accent-warning)" stroke-width="6" stroke-linecap="round" />
                  <line x1="240" y1="20" x2="240" y2="200" stroke="var(--accent-warning)" stroke-width="3" stroke-dasharray="6,6" />
                </svg>
                <div class="retention-marker" id="retention-marker">📉 00:28 : CHUTE BRUTALE D'AUDIENCE</div>
              </div>
              <div class="loom-webcam-bubble">
                <div class="webcam-silhouette">👤</div>
                <div class="webcam-mute-badge">🔇</div>
              </div>
              <div class="loom-screen-player-bar">
                <div class="loom-pause-btn">⏸</div>
                <div class="loom-time-slider">
                  <div class="loom-time-fill-active"></div>
                  <div class="loom-time-cursor"></div>
                </div>
                <div class="loom-time-digits">00:28 / 10:00</div>
              </div>
            </div>
            <div class="loom-kpi-footer">
              <div class="loom-kpi-block amber">
                <div class="kpi-num">12%</div>
                <div class="kpi-lbl">RÉTENTION FINALE</div>
              </div>
              <div class="loom-kpi-block dark">
                <div class="kpi-num">88%</div>
                <div class="kpi-lbl">QUITTENT AVANT 1 MIN</div>
              </div>
            </div>
          </div>
        `;
      case "browser_tab_overload":
        return `
          <div class="comp-browser-overload" id="comp-browser-overload">
            <div class="browser-tab-bar">
              <div class="browser-tab active">
                <span>🌐 Loom — Meeting_Recording_12m.mp4</span>
                <span class="tab-close-x">✕</span>
              </div>
              <div class="browser-tab-add">+ Nouvel onglet</div>
            </div>
            <div class="browser-overload-screen">
              <div class="wireframe-chaos-bg">
                <div class="wf-window wf-win1">
                  <div class="wf-bar">📊 Dashboard Ventes Q3</div>
                  <div class="wf-body-chaos">
                    <div class="wf-line w70"></div><div class="wf-line w90"></div>
                  </div>
                </div>
                <div class="wf-window wf-win2">
                  <div class="wf-bar">💬 Slack (18 non lus)</div>
                  <div class="wf-body-chaos">
                    <div class="wf-line w50"></div><div class="wf-line w80"></div>
                  </div>
                </div>
                <div class="wf-window wf-win3">
                  <div class="wf-bar">⚙️ Paramètres / Logs</div>
                  <div class="wf-body-chaos">
                    <div class="wf-line w70"></div>
                  </div>
                </div>
              </div>
              <div class="overload-shock-alert" id="overload-shock-alert">
                <div class="shock-timer">⏳ 12:00 MINUTES</div>
                <div class="shock-title">ÉCRAN PARTAGÉ BRUT • ZÉRO MONTAGE</div>
              </div>
            </div>
            <div class="overload-footer-tags">
              <div class="overload-tag-item" id="otag-0">[ 15 ONGLETS OUVERTS ]</div>
              <div class="overload-tag-item" id="otag-1">[ MICRO MAL RÉGLÉ ]</div>
              <div class="overload-tag-item" id="otag-2">[ ZÉRO STRUCTURE ]</div>
            </div>
          </div>
        `;
      case "loom_3_flaws_timeline":
        return `
          <div class="comp-flaws-timeline" id="comp-flaws-timeline">
            <div class="flaw-card" id="flaw-card-0">
              <div class="flaw-left">
                <div class="flaw-badge-num">01</div>
                <div class="flaw-texts">
                  <div class="flaw-main-title">01. HÉSITATIONS</div>
                  <div class="flaw-sub-desc">Rythme haché & bafouillages</div>
                </div>
              </div>
              <div class="flaw-illustration-right">
                <div class="flaw-bubble-crossed">
                  <span class="strike-text">« Euh... attends... »</span>
                  <div class="mini-wave-hashed">
                    <span class="wave-chunk"></span><span class="wave-chunk"></span><span class="wave-chunk gap"></span><span class="wave-chunk"></span>
                  </div>
                </div>
              </div>
            </div>
            <div class="flaw-card" id="flaw-card-1">
              <div class="flaw-left">
                <div class="flaw-badge-num">02</div>
                <div class="flaw-texts">
                  <div class="flaw-main-title">02. SILENCES</div>
                  <div class="flaw-sub-desc">Temps morts interminables</div>
                </div>
              </div>
              <div class="flaw-illustration-right">
                <div class="flaw-ecg-flatline">
                  <div class="ecg-mic">🔇</div>
                  <div class="ecg-line-flat">────── 4.2s BLANC AUDIO ──────</div>
                </div>
              </div>
            </div>
            <div class="flaw-card" id="flaw-card-2">
              <div class="flaw-left">
                <div class="flaw-badge-num">03</div>
                <div class="flaw-texts">
                  <div class="flaw-main-title">03. VOIX FATIGUÉE</div>
                  <div class="flaw-sub-desc">Ton monotone & lassant</div>
                </div>
              </div>
              <div class="flaw-illustration-right">
                <div class="flaw-battery-gauge">
                  <div class="batt-shell">
                    <div class="batt-fill" style="width: 15%;"></div>
                  </div>
                  <div class="batt-label">15% ÉNERGIE</div>
                </div>
              </div>
            </div>
          </div>
        `;
      case "tab_close_cursor":
        return `
          <div class="comp-tab-close" id="comp-tab-close">
            <div class="tab-close-browser-top">
              <div class="tab-item-active">
                <span>🌐 Loom — Démo Produit B2B (12:00)</span>
                <div class="tab-btn-close-action" id="tab-btn-close-action">✕ FERMER L'ONGLET</div>
              </div>
            </div>
            <div class="tab-close-preview-body" id="tab-close-preview-body">
              <div class="preview-mini-loom" id="preview-mini-loom">
                <div class="mini-loom-screen">
                  <div class="mini-loom-freeze">🥱 Démo figée à 00:30</div>
                  <div class="mini-progress-bar"><div class="mini-fill" style="width: 4%;"></div></div>
                </div>
              </div>
              <div class="tab-close-stamp" id="tab-close-stamp">
                <div class="stamp-icon">✕</div>
                <div class="stamp-main-text">ONGLET FERMÉ EN 30S</div>
                <div class="stamp-sub-text">PROSPECT PERDU AVANT LE MOINDRE ARGUMENT</div>
              </div>
            </div>
            <div class="virtual-cursor" id="tab-cursor" style="position: absolute; pointer-events: none; z-index: 60;">
              <svg width="68" height="68" viewBox="0 0 24 24" fill="none">
                <path d="M4 3L11 21L14 13L22 10L4 3Z" fill="var(--accent-warning)" stroke="var(--bg-dark)" stroke-width="2.5" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>
        `;
      case "product_vs_perception":
        if (data.phase === "perception") {
          return `
            <div class="comp-product-perception perception-stage" id="comp-product-perception">
              <div class="perception-header-title">VALEUR PERÇUE PAR LE PROSPECT</div>
              <div class="bar-chart-giant-compare">
                <div class="compare-col left-real">
                  <div class="col-kpi" id="col-kpi-real">100%</div>
                  <div class="col-bar-track">
                    <div class="col-bar-fill real-fill"></div>
                  </div>
                  <div class="col-label">VALEUR RÉELLE DU PRODUIT</div>
                </div>
                <div class="compare-vs-badge">VS</div>
                <div class="compare-col right-perceived">
                  <div class="col-kpi amber" id="col-kpi-perceived">18%</div>
                  <div class="col-bar-track">
                    <div class="col-bar-fill perceived-fill" id="perceived-fill"></div>
                  </div>
                  <div class="col-label amber">VALEUR PERÇUE APRÈS TON LOOM</div>
                </div>
              </div>
              <div class="perception-banner-impact" id="perception-impact-banner">
                RÉSULTAT : 0 APPEL BOOKÉ
              </div>
            </div>
          `;
        }
        return `
          <div class="comp-product-perception product-stage" id="comp-product-perception">
            <div class="product-saas-excellence-card">
              <div class="saas-card-top-bar">
                <div class="saas-card-title-group">
                  <div class="saas-card-title">TON PRODUIT SAAS</div>
                  <div class="saas-badge-stars">★★★★★ EXCELLENT</div>
                </div>
              </div>
              <div class="saas-card-grid-widgets">
                <div class="saas-widget-box">
                  <div class="widget-metric-num">99.99%</div>
                  <div class="widget-metric-lbl">UPTIME & FIABILITÉ</div>
                  <div class="widget-status-dot">● SYSTÈME STABLE</div>
                </div>
                <div class="saas-widget-box">
                  <div class="widget-metric-num">+340%</div>
                  <div class="widget-metric-lbl">EFFICACITÉ API & CORE</div>
                  <svg class="widget-trend-svg" viewBox="0 0 160 40">
                    <path d="M 0 35 Q 40 30 80 18 T 160 5" fill="none" stroke="var(--accent-primary)" stroke-width="4" stroke-linecap="round"/>
                  </svg>
                </div>
                <div class="saas-widget-box full-span">
                  <div class="widget-row-feature">
                    <span class="feat-check">✓</span>
                    <span class="feat-text">ARCHITECTURE ROBUSTE, RAPIDE & SCALABLE</span>
                  </div>
                </div>
              </div>
            </div>
            ${data.avatar_pip ? `
              <div class="avatar-pip-medallion" id="avatar-pip">
                <img src="${data.avatar_pip}" alt="Avatar Sceptique" />
              </div>
            ` : ""}
          </div>
        `;
      case "interface_labyrinth_cut":
        const menusList = [
          "Dashboard", "Analytics", "Settings", "Billing",
          "Team Roles", "API Keys", "Webhooks", "Audit Logs",
          "Security", "Integrations", "Exports", "Config"
        ];
        return `
          <div class="comp-labyrinth-cut" id="comp-labyrinth-cut">
            <div class="labyrinth-top-header">VISITE GUIDÉE DE L'INTERFACE SAAS</div>
            <div class="labyrinth-menus-grid" id="labyrinth-grid">
              ${menusList.map((m, i) => `
                <div class="menu-pill-card" id="menu-pill-${i}">
                  <span class="menu-icon">📁</span>
                  <span class="menu-name">${m}</span>
                </div>
              `).join("")}
            </div>
            <div class="strike-cross-line line-1" id="strike-line-1"></div>
            <div class="strike-cross-line line-2" id="strike-line-2"></div>
            <div class="labyrinth-central-banner" id="labyrinth-central-banner">
              <div class="banner-big-reject">✕ VISITE GUIDÉE DE 12 MENUS : IGNORÉE</div>
              <div class="banner-sub-reject">L'ACHETEUR B2B N'A PAS 12 MINUTES</div>
            </div>
          </div>
        `;
      case "sixty_sec_value_bridge":
        return `
          <div class="comp-sixty-bridge" id="comp-sixty-bridge">
            <div class="bridge-top-circle-chrono">
              <svg class="chrono-svg-ring" viewBox="0 0 240 240">
                <circle cx="120" cy="120" r="102" fill="var(--bg-dark)" stroke="var(--border-subtle)" stroke-width="12" />
                <circle cx="120" cy="120" r="102" fill="none" stroke="var(--accent-primary)" stroke-width="12"
                  stroke-dasharray="640" stroke-dashoffset="0" stroke-linecap="round" id="chrono-progress-ring"
                  transform="rotate(-90 120 120)" />
              </svg>
              <div class="chrono-inner-content">
                <div class="chrono-digits" id="chrono-digits">60s</div>
                <div class="chrono-unit">CHRONO</div>
              </div>
            </div>
            <div class="bridge-two-cards-row">
              <div class="bridge-card problem">
                <div class="bcard-num">1.</div>
                <div class="bcard-title">SON PROBLÈME</div>
                <div class="bcard-desc">Identifié dès la 1re seconde</div>
              </div>
              <div class="bridge-arrow-animated">━━━▶</div>
              <div class="bridge-card solution">
                <div class="bcard-num green">2.</div>
                <div class="bcard-title green">TA SOLUTION</div>
                <div class="bcard-desc">ROI prouvé sans friction</div>
              </div>
            </div>
            <div class="bridge-bottom-pill">
              ✓ COMPRÉHENSION IMMÉDIATE DU DÉCIDEUR
            </div>
          </div>
        `;
      case "code_to_ui_live":
        return `
          <div class="comp-code-live" id="comp-code-live">
            <div class="code-editor-top-half">
              <div class="code-editor-bar">
                <div class="editor-dots">
                  <span class="dot red"></span>
                  <span class="dot yellow"></span>
                  <span class="dot green"></span>
                </div>
                <div class="editor-tab-title">demo_generator.js</div>
                <div class="editor-lang-tag">JAVASCRIPT</div>
              </div>
              <div class="code-editor-content">
                <pre id="code-live-code" class="code-pre"><span class="c-kw">const</span> <span class="c-var">demo</span> = <span class="c-obj">Agent404</span>.<span class="c-fn">create</span>({
  <span class="c-prop">format</span>: <span class="c-str">"1080x1920"</span>,
  <span class="c-prop">camera</span>: <span class="c-bool">false</span>,
  <span class="c-prop">retakes</span>: <span class="c-num">0</span>
});
<span class="c-var">demo</span>.<span class="c-fn">renderPerfectCut</span>();</pre>
              </div>
            </div>
            <div class="code-bottom-cards-row">
              <div class="code-proof-card left" id="code-card-camera">
                <div class="proof-icon">🚫📷</div>
                <div class="proof-texts">
                  <div class="proof-title">ZÉRO CAMÉRA</div>
                  <div class="proof-sub">Aucun tournage requis</div>
                </div>
              </div>
              <div class="code-proof-card right" id="code-card-retakes">
                <div class="proof-icon green">🎯</div>
                <div class="proof-texts">
                  <div class="proof-title green">ZÉRO PRISE RATÉE</div>
                  <div class="proof-sub">100% déterministe du 1er coup</div>
                </div>
              </div>
            </div>
          </div>
        `;
      case "voice_to_word_grid":
        return `
          <div class="comp-word-grid" id="comp-word-grid">
            <div class="audio-clean-tier">
              <div class="tier-top-label">
                <span>🎙️ NOTE VOCALE : PURGE AUTOMATIQUE</span>
                <span class="tier-tag-clean" id="tier-tag-clean">✂️ HÉSITATIONS PURGÉES</span>
              </div>
              <div class="audio-track-simulation">
                <div class="audio-silence-block s1" id="silence-block-1">
                  <div class="silence-label">« Euh... »</div>
                </div>
                <div class="audio-wave-bars-active" id="audio-wave-active">
                  ${Array.from({ length: 28 }, (_, i) => `<div class="awave-bar" id="awbar-${i}"></div>`).join("")}
                </div>
                <div class="audio-silence-block s2" id="silence-block-2">
                  <div class="silence-label">[ Silence 3.8s ]</div>
                </div>
              </div>
            </div>
            <div class="word-sync-tier">
              <div class="word-sync-header">✓ SYNCHRONISATION AU CENTIÈME DE SECONDE (0.01s)</div>
              <div class="word-magnetic-cards">
                <div class="word-mag-card" id="word-card-0">
                  <div class="word-timer">00.12s</div>
                  <div class="word-box">[ TON ]</div>
                </div>
                <div class="word-mag-card" id="word-card-1">
                  <div class="word-timer">00.48s</div>
                  <div class="word-box">[ OUTIL ]</div>
                </div>
                <div class="word-mag-card" id="word-card-2">
                  <div class="word-timer">00.85s</div>
                  <div class="word-box">[ B2B ]</div>
                </div>
              </div>
            </div>
          </div>
        `;
      case "saas_showcase_3steps":
        return `
          <div class="comp-saas-showcase" id="comp-saas-showcase">
            <div class="saas-theater-header">
              <div class="saas-theater-logo">⚡ CloudMetrics B2B</div>
              <div class="saas-step-progress">
                <span class="step-pill-indicator active" id="st-pill-1">① ISOLEMENT CLÉ</span>
                <span class="step-pill-indicator" id="st-pill-2">② PARCOURS UTILISATEUR</span>
                <span class="step-pill-indicator" id="st-pill-3">③ HAUTE DÉFINITION</span>
              </div>
            </div>
            <div class="saas-theater-stage">
              <!-- Phase 1: Isolation de la fonctionnalité clé -->
              <div class="theater-phase phase-1" id="theater-phase-1">
                <div class="dashboard-grid-mini">
                  <div class="mini-widget blur" id="d-wid-1">📁 Imports Leads</div>
                  <div class="mini-widget hero-focus" id="d-wid-hero">
                    <div class="wid-kpi-badge">① FONCTIONNALITÉ CLÉ ISOLÉE</div>
                    <div class="wid-hero-num">+312% CONVERSION B2B</div>
                    <div class="wid-hero-sub">Pipeline généré en 1 clic</div>
                    <svg class="wid-chart-svg" viewBox="0 0 280 60">
                      <path d="M 0 50 Q 70 45 140 25 T 280 8" fill="none" stroke="var(--accent-primary)" stroke-width="5" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <div class="mini-widget blur" id="d-wid-2">⚙️ Webhooks</div>
                  <div class="mini-widget blur" id="d-wid-3">📊 Logs</div>
                </div>
              </div>
              <!-- Phase 2: Parcours utilisateur simulé -->
              <div class="theater-phase phase-2" id="theater-phase-2" style="display: none;">
                <div class="user-journey-path">
                  <div class="journey-badge-top">② PARCOURS UTILISATEUR SIMULÉ</div>
                  <div class="journey-steps-row">
                    <div class="journey-step-box" id="j-step-1">
                      <div class="j-step-num">1</div>
                      <div class="j-step-name">Import Leads</div>
                      <div class="j-step-check">✓</div>
                    </div>
                    <div class="j-step-arrow">━━━▶</div>
                    <div class="journey-step-box" id="j-step-2">
                      <div class="j-step-num">2</div>
                      <div class="j-step-name">Qualification Auto</div>
                      <div class="j-step-check">✓</div>
                    </div>
                    <div class="j-step-arrow">━━━▶</div>
                    <div class="journey-step-box" id="j-step-3">
                      <div class="j-step-num">3</div>
                      <div class="j-step-name">RDV Booké</div>
                      <div class="j-step-check">✓</div>
                    </div>
                  </div>
                  <div class="journey-cta-btn" id="journey-cta-btn">
                    [ GÉNÉRER LE PIPELINE AUTOMATIQUE ]
                  </div>
                </div>
                <div class="virtual-cursor" id="journey-cursor" style="position: absolute; pointer-events: none; z-index: 50;">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none">
                    <path d="M4 3L11 21L14 13L22 10L4 3Z" fill="var(--accent-primary)" stroke="var(--bg-dark)" stroke-width="2.5" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
              <!-- Phase 3: Rendu HD au pixel près -->
              <div class="theater-phase phase-3" id="theater-phase-3" style="display: none;">
                <div class="hd-master-frame">
                  <div class="hd-corner top-left"></div>
                  <div class="hd-corner top-right"></div>
                  <div class="hd-corner bottom-left"></div>
                  <div class="hd-corner bottom-right"></div>
                  <div class="hd-giant-res">1080 × 1920 PX</div>
                  <div class="hd-sub-badge">HAUTE DÉFINITION • AU PIXEL PRÈS ✓</div>
                  <div class="hd-tags-row">
                    <span class="hd-tag">[ NETTETÉ 100% ]</span>
                    <span class="hd-tag">[ 60 SECONDES ]</span>
                    <span class="hd-tag">[ PRÊT À PUBLIER ]</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
      case "delivery_48h_3channels":
        return `
          <div class="comp-delivery-channels" id="comp-delivery-channels">
            <div class="delivery-master-header">
              ⚡ LIVRAISON EN 48H : PACK 3 VIDÉOS VERTICALES
            </div>
            <div class="delivery-channels-vertical-stack">
              <div class="delivery-channel-row" id="channel-row-0">
                <div class="chan-thumb linkedin">
                  <div class="thumb-mini-tag">LINKEDIN FEED</div>
                  <div class="thumb-play">▶</div>
                </div>
                <div class="chan-info-side">
                  <div class="chan-title-line">
                    <span class="chan-num">01.</span>
                    <span class="chan-name">SUR LINKEDIN</span>
                    <span class="chan-badge">✓ FORMAT HOOK 9:16</span>
                  </div>
                  <div class="chan-pitch">Capte l'attention dans le feed sans le son</div>
                </div>
              </div>
              <div class="delivery-channel-row" id="channel-row-1">
                <div class="chan-thumb outreach">
                  <div class="thumb-mini-tag">EMAIL / DM</div>
                  <div class="thumb-play">▶</div>
                </div>
                <div class="chan-info-side">
                  <div class="chan-title-line">
                    <span class="chan-num">02.</span>
                    <span class="chan-name">EN PROSPECTION B2B</span>
                    <span class="chan-badge">✓ 60S CHRONO</span>
                  </div>
                  <div class="chan-pitch">Remplace tes pavés de texte et Loom de 10 min</div>
                </div>
              </div>
              <div class="delivery-channel-row" id="channel-row-2">
                <div class="chan-thumb landing">
                  <div class="thumb-mini-tag">HERO BANNER</div>
                  <div class="thumb-play">▶</div>
                </div>
                <div class="chan-info-side">
                  <div class="chan-title-line">
                    <span class="chan-num">03.</span>
                    <span class="chan-name">EN HAUT DE TA LANDING PAGE</span>
                    <span class="chan-badge">✓ CONVERSION</span>
                  </div>
                  <div class="chan-pitch">Explique ton produit en 60s et convertit</div>
                </div>
              </div>
            </div>
          </div>
        `;
      case "face_to_dm_cta":
        const keyword = (data && data.keyword) || "CLARTÉ";
        const lettersHtml = keyword.split("").map((ch, idx) =>
          `<span class="keyword-letter" id="kw-letter-${idx}" style="opacity: 0; transform: scale(0.5);">${ch}</span>`
        ).join("");
        let heroTitle = (data && data.hero_title) || 'TON POST ÉCRIT EN <span class="highlight">VIDÉO</span>';
        const highlightWord = (data && data.highlight_word) || "VIDÉO";
        if (highlightWord && heroTitle.includes(highlightWord) && !heroTitle.includes('<span class="highlight">')) {
          heroTitle = heroTitle.replace(highlightWord, `<span class="highlight">${highlightWord}</span>`);
        }
        const instructionLabel = (data && data.instruction_label) || "ENVOIE CE MOT-CLÉ EN MESSAGE PRIVÉ :";
        const rawButton = (data && data.button_label) || `ENVOYER « ${keyword} » EN MESSAGE PRIVÉ ↗`;
        const buttonLabel = rawButton.replace(/\[|\]/g, "").trim();
        return `
          <div class="comp-face-dm" id="comp-face-dm">
            <div class="face-dm-avatar-stage" id="face-dm-avatar-stage">
              <div class="face-hero-title" style="top: 220px;">
                <span>${heroTitle}</span>
              </div>
              <div class="comp-face">
                <img src="${data.avatar || 'assets/avatars/pointing.png'}" alt="Avatar" class="avatar-sticker" id="avatar-img" />
              </div>
            </div>
            <div class="face-dm-cta-stage" id="face-dm-cta-stage" style="opacity: 0; pointer-events: none;">
              <div class="cta-direct-box">
                <div class="cta-hero-center">
                  <div class="cta-instruction-label">${instructionLabel}</div>
                  <div class="cta-giant-keyword-box" id="cta-giant-box">
                    ${lettersHtml}
                  </div>
                  <div class="cta-send-button-massive" id="cta-send-button">
                    ${buttonLabel}
                  </div>
                </div>
                <div class="virtual-cursor" id="cta-cursor" style="position: absolute; top: 0; left: 0; pointer-events: none; z-index: 70;">
                  <svg width="68" height="68" viewBox="0 0 24 24" fill="none">
                    <path d="M4 3L11 21L14 13L22 10L4 3Z" fill="var(--accent-warning)" stroke="var(--bg-dark)" stroke-width="2.5" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        `;
      case "zero_video_slam":
        return `
          <div class="comp-zero-slam" id="comp-zero-slam">
            <div class="zero-counter-box" id="zero-counter-box">
              <div class="zero-counter-label">POSTS ÉCRITS PUBLIÉS :</div>
              <div class="zero-counter-num" id="zero-counter-num">4</div>
            </div>
            <div class="zero-giant-wrap" id="zero-giant-wrap" style="opacity: 0;">
              <div class="zero-shockwave" id="zero-shockwave"></div>
              <div class="zero-giant-digit" id="zero-giant-digit">0</div>
              <div class="zero-slam-badge" id="zero-slam-badge" style="opacity: 0;">VIDÉO PUBLIÉE</div>
            </div>
          </div>
        `;
      case "shooting_wall_illustrations":
        return `
          <div class="comp-shooting-wall" id="comp-shooting-wall">
            <div class="sw-card pastel-pink" id="sw-card-0" style="transform: rotate(-1.5deg) scale(0.92);">
              <div class="sw-icon-wrap">
                <svg width="110" height="110" viewBox="0 0 120 120" fill="none">
                  <rect x="15" y="32" width="75" height="56" rx="6" fill="var(--surface-elevated)" stroke="var(--border-color)" stroke-width="3"/>
                  <path d="M38 32L44 22H62L68 32H38Z" fill="var(--surface-elevated)" stroke="var(--border-color)" stroke-width="3"/>
                  <circle cx="52" cy="60" r="22" fill="var(--white)" stroke="var(--border-color)" stroke-width="3"/>
                  <circle cx="52" cy="60" r="15" fill="none" stroke="var(--mint)" stroke-width="2.5"/>
                  <circle cx="52" cy="60" r="7" fill="var(--black)"/>
                  <circle cx="48" cy="56" r="3" fill="var(--white)"/>
                  <circle cx="78" cy="42" r="5" fill="var(--mint)"/>
                </svg>
              </div>
              <div class="sw-content">
                <div class="sw-title">1. ALLUMER LA CAMÉRA</div>
                <div class="sw-badge" id="sw-badge-rec">● REC 00:00:00</div>
              </div>
            </div>
            <div class="sw-card pastel-yellow" id="sw-card-1" style="transform: rotate(1.5deg) scale(0.92);">
              <div class="sw-icon-wrap">
                <svg width="110" height="110" viewBox="0 0 120 120" fill="none">
                  <line x1="60" y1="74" x2="60" y2="108" stroke="var(--border-color)" stroke-width="3.5" stroke-linecap="round"/>
                  <line x1="60" y1="95" x2="40" y2="114" stroke="var(--border-color)" stroke-width="3" stroke-linecap="round"/>
                  <line x1="60" y1="95" x2="80" y2="114" stroke="var(--border-color)" stroke-width="3" stroke-linecap="round"/>
                  <polygon points="60,16 88,28 98,54 84,76 36,76 22,54 32,28" fill="var(--surface-elevated)" stroke="var(--border-color)" stroke-width="3"/>
                  <circle cx="60" cy="50" r="14" fill="var(--amber)"/>
                  <circle cx="60" cy="50" r="20" fill="none" stroke="var(--black)" stroke-width="2"/>
                </svg>
              </div>
              <div class="sw-content">
                <div class="sw-title">2. RÉGLER LA LUMIÈRE</div>
                <div class="sw-badge">5600K STUDIO</div>
              </div>
            </div>
            <div class="sw-card pastel-blue" id="sw-card-2" style="transform: rotate(-1.5deg) scale(0.92);">
              <div class="sw-icon-wrap">
                <svg width="110" height="110" viewBox="0 0 120 120" fill="none">
                  <rect x="12" y="16" width="96" height="88" rx="6" fill="var(--surface-elevated)" stroke="var(--border-color)" stroke-width="3"/>
                  <rect x="12" y="16" width="96" height="24" rx="6" fill="var(--black)"/>
                  <text x="60" y="33" fill="var(--white)" font-family="Montserrat" font-size="12" font-weight="900" text-anchor="middle" letter-spacing="1">04:00:00</text>
                  <rect x="18" y="46" width="22" height="14" rx="3" fill="var(--mint)"/>
                  <rect x="43" y="46" width="38" height="14" rx="3" fill="var(--white)"/>
                  <rect x="84" y="46" width="18" height="14" rx="3" fill="var(--mint)"/>
                  <rect x="18" y="64" width="40" height="14" rx="3" fill="var(--border-color)"/>
                </svg>
              </div>
              <div class="sw-content">
                <div class="sw-title">3. 4H DE MONTAGE</div>
                <div class="sw-badge">TIMELINE BLOQUÉE</div>
              </div>
            </div>
          </div>
        `;
      case "real_clone_feed_skip":
      case "b2b_robot_clone_crash":
        return `
          <div class="comp-real-clone" id="comp-real-clone">
            <div class="rcf-top-banner" id="rcf-top-banner">
              <div class="rcf-top-banner-title">MÊME AVATAR CLONÉ SUR TOUS LES COMPTES</div>
            </div>
            <div class="rcf-stage" id="rcf-stage">
              <!-- Phase 1 : Post Unique -->
              <div class="rcf-post-single" id="rcf-post-single">
                <div class="rcf-post-header">
                  <div class="rcf-avatar-circle">
                    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                      <circle cx="14" cy="10" r="6" stroke="var(--mint)" stroke-width="2"/>
                      <path d="M4 24C4 19 8.5 17 14 17C19.5 17 24 19 24 24" stroke="var(--mint)" stroke-width="2"/>
                    </svg>
                  </div>
                  <div class="rcf-author-meta">
                    <div class="rcf-author-name">Créateur Synthétique • 1er</div>
                    <div class="rcf-author-sub">Modèle IA #404 • Sponsorisé 🌐</div>
                  </div>
                  <div style="font-size: 24px; color: var(--text-muted); font-weight: 900;">•••</div>
                </div>
                <div class="rcf-player-box">
                  <svg width="180" height="180" viewBox="0 0 180 180" fill="none">
                    <circle cx="90" cy="90" r="75" stroke="var(--border-subtle)" stroke-width="2" stroke-dasharray="4 4"/>
                    <path d="M60 55H120L135 90L120 135H60L45 90L60 55Z" fill="var(--surface-elevated)" stroke="var(--mint)" stroke-width="3"/>
                    <rect x="62" y="80" width="56" height="16" rx="4" fill="var(--surface-black)" stroke="var(--mint)" stroke-width="1.5"/>
                    <circle cx="78" cy="88" r="5" fill="var(--mint)"/>
                    <circle cx="102" cy="88" r="5" fill="var(--mint)"/>
                    <line x1="70" y1="112" x2="110" y2="112" stroke="var(--border-subtle)" stroke-width="2.5"/>
                    <line x1="75" y1="120" x2="105" y2="120" stroke="var(--border-subtle)" stroke-width="2.5"/>
                  </svg>
                  <div class="rcf-target-bracket">
                    <div class="rcf-target-label">SYNTHÈSE FACIALE IA</div>
                  </div>
                  <div class="rcf-wave-bar">
                    <div class="rcf-flat-wave"></div>
                    <div class="rcf-wave-label">TON MONOTONE • 0 ÉMOTION</div>
                    <div class="rcf-flat-wave"></div>
                  </div>
                </div>
                <div class="rcf-post-badge">MODÈLE AVATAR GÉNÉRIQUE</div>
              </div>

              <!-- Phase 2 : Grille de 3 clones -->
              <div class="rcf-clone-row" id="rcf-clone-row" style="display: none;">
                ${[1, 2, 3].map(num => `
                  <div class="rcf-clone-mini-card">
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <div style="width: 32px; height: 32px; border-radius: 50%; background: var(--bg-carbon); border: 1.5px solid var(--mint); display: flex; align-items: center; justify-content: center; font-size: 20px;">🤖</div>
                      <div style="font-family: 'Montserrat', sans-serif; font-size: 20px; font-weight: 800; color: var(--white);">Compte #${num}</div>
                    </div>
                    <div style="flex: 1; background: var(--bg-carbon); border-radius: 12px; border: 1.5px solid var(--border-subtle); display: flex; align-items: center; justify-content: center;">
                      <svg width="100" height="100" viewBox="0 0 180 180" fill="none">
                        <path d="M60 55H120L135 90L120 135H60L45 90L60 55Z" fill="var(--surface-elevated)" stroke="var(--mint)" stroke-width="3"/>
                        <rect x="62" y="80" width="56" height="16" rx="4" fill="var(--surface-black)" stroke="var(--mint)" stroke-width="1.5"/>
                        <circle cx="78" cy="88" r="5" fill="var(--mint)"/>
                        <circle cx="102" cy="88" r="5" fill="var(--mint)"/>
                      </svg>
                    </div>
                    <div class="rcf-clone-tag">CLONE IDENTIQUE #0${num}</div>
                  </div>
                `).join("")}
              </div>
            </div>

            <!-- Phase 3 : Carte Audit & Chute Crédibilité -->
            <div class="rcf-audit-card" id="rcf-audit-card">
              <div class="rcf-audit-title">RÉTENTION & <span>CRÉDIBILITÉ PROSPECT</span></div>
              <div class="rcf-gauge-box">
                <div class="rcf-gauge-labels">
                  <span>CONFIANCE AUDIENCE</span>
                  <span class="rcf-gauge-percent" id="rcf-gauge-percent">100%</span>
                </div>
                <div class="rcf-gauge-track">
                  <div class="rcf-gauge-fill" id="rcf-gauge-fill" style="width: 100%;"></div>
                </div>
              </div>
              <div class="rcf-stopwatch-num" id="rcf-stopwatch-num">00:01s</div>
              <div class="rcf-final-stamp" id="rcf-final-stamp" style="opacity: 0;">SWIPE EN 3 SECONDES — PROSPECT PERDU</div>
            </div>
          </div>
        `;
      case "overflowing_text_posts":
      case "locked_post_wall":
        return `
          <div class="comp-overflowing-posts" id="comp-overflowing-posts">
            <div class="otp-header-box">
              <div class="otp-header-title">TES MEILLEURS ARGUMENTS <span>NOYÉS DANS L'ÉCRIT</span></div>
            </div>
            <div class="otp-window">
              <div class="otp-window-bar">
                <div style="display: flex; gap: 8px;">
                  <div style="width: 14px; height: 14px; border-radius: 50%; background: var(--window-dot-close);"></div>
                  <div style="width: 14px; height: 14px; border-radius: 50%; background: var(--window-dot-min);"></div>
                  <div style="width: 14px; height: 14px; border-radius: 50%; background: var(--accent-primary);"></div>
                </div>
                <div class="otp-window-meta">Post publié • 1 850 mots • 8 min de lecture</div>
                <div style="font-size: 20px; color: var(--text-muted); font-weight: 700;">LinkedIn Feed</div>
              </div>
              <div class="otp-window-body" style="position: relative; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 32px;">
                <div class="otp-scroll-content" id="otp-scroll-content" style="width: 100%; display: flex; flex-direction: column; gap: 20px; align-items: flex-start;">
                  <div class="otp-skeleton" style="width: 92%; height: 24px; background: var(--grid-line); border: 2px solid var(--border-color); border-radius: 4px;"></div>
                  <div class="otp-skeleton" style="width: 78%; height: 24px; background: var(--border-color); border-radius: 4px;"></div>
                  <div class="otp-skeleton" style="width: 86%; height: 24px; background: var(--grid-line); border: 2px solid var(--border-color); border-radius: 4px;"></div>
                  <div class="otp-skeleton" style="width: 65%; height: 24px; background: var(--border-color); border-radius: 4px;"></div>
                  <div class="otp-skeleton" style="width: 82%; height: 24px; background: var(--grid-line); border: 2px solid var(--border-color); border-radius: 4px;"></div>
                </div>
                <div class="neo-stamp" id="otp-stamp" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-6deg); z-index: 25; text-align: center; white-space: nowrap; font-size: 28px !important; padding: 10px 22px !important;">PAVÉ DE 150 LIGNES = IGNORÉ !</div>
              </div>
            </div>
            <div class="otp-bottom-banner">PAVÉ DE 150 LIGNES : 92% DES PROSPECTS SCROLLENT SANS LIRE</div>
          </div>
        `;
      case "social_logos_carousel_rtl":
        const channelsData = [
          {
            id: "linkedin",
            name: "LINKEDIN",
            svg: `<svg width="180" height="180" viewBox="0 0 180 180" fill="none"><rect width="180" height="180" rx="36" fill="#0A66C2"/><path d="M52 74H76V142H52V74ZM64 42C56.3 42 50 48.3 50 56C50 63.7 56.3 70 64 70C71.7 70 78 63.7 78 56C78 48.3 71.7 42 64 42ZM92 74H115V83.5C118.5 77 127 72 138 72C160 72 165 86 165 107V142H141V111C141 102 140 93 128.5 93C116.5 93 115 102 115 110.5V142H92V74Z" fill="#FFFFFF"/></svg>`
          },
          {
            id: "tiktok",
            name: "TIKTOK",
            svg: `<svg width="180" height="180" viewBox="0 0 180 180" fill="none"><rect width="180" height="180" rx="36" fill="#000000"/><g transform="translate(18, 18) scale(3)"><path d="M33.5 17.5C31.5 17.5 29.8 16.6 28.5 15.2V27.8C28.5 33.2 24.1 37.5 18.8 37.5C13.4 37.5 9 33.1 9 27.8C9 22.4 13.4 18 18.8 18C19.3 18 19.8 18.05 20.3 18.15V22.9C19.8 22.75 19.3 22.65 18.8 22.65C16 22.65 13.7 24.95 13.7 27.75C13.7 30.55 16 32.85 18.8 32.85C21.6 32.85 23.8 30.55 23.8 27.75V9.5H28.5C28.5 12.3 30.7 14.5 33.5 14.5V17.5Z" fill="#25F4EE"/><path d="M34.5 16.5C32.5 16.5 30.8 15.6 29.5 14.2V26.8C29.5 32.2 25.1 36.5 19.8 36.5C14.4 36.5 10 32.1 10 26.8C10 21.4 14.4 17 19.8 17C20.3 17 20.8 17.05 21.3 17.15V21.9C20.8 21.75 20.3 21.65 19.8 21.65C17 21.65 14.7 23.95 14.7 26.75C14.7 29.55 17 31.85 19.8 31.85C22.6 31.85 24.8 29.55 24.8 26.75V8.5H29.5C29.5 11.3 31.7 13.5 34.5 13.5V16.5Z" fill="#FE2C55"/><path d="M34 17C32 17 30.3 16.1 29 14.7V27.3C29 32.7 24.6 37 19.3 37C13.9 37 9.5 32.6 9.5 27.3C9.5 21.9 13.9 17.5 19.3 17.5C19.8 17.5 20.3 17.55 20.8 17.65V22.4C20.3 22.25 19.8 22.15 19.3 22.15C16.5 22.15 14.2 24.45 14.2 27.25C14.2 30.05 16.5 32.35 19.3 32.35C22.1 32.35 24.3 30.05 24.3 27.25V9H29C29 11.8 31.2 14 34 14V17Z" fill="#FFFFFF"/></g></svg>`
          },
          {
            id: "reels",
            name: "REELS",
            svg: `<svg width="180" height="180" viewBox="0 0 180 180" fill="none"><defs><radialGradient id="ig-grad-real" cx="20%" cy="110%" r="130%"><stop offset="0%" stop-color="#FFDD55"/><stop offset="25%" stop-color="#FF5D3B"/><stop offset="50%" stop-color="#FF0069"/><stop offset="75%" stop-color="#D300C5"/><stop offset="100%" stop-color="#7638FA"/></radialGradient></defs><rect width="180" height="180" rx="42" fill="url(#ig-grad-real)"/><g transform="translate(18, 18) scale(3)"><rect x="10" y="10" width="28" height="28" rx="8" stroke="white" stroke-width="3" fill="none"/><circle cx="24" cy="24" r="6.5" stroke="white" stroke-width="3" fill="none"/><circle cx="31.5" cy="16.5" r="1.6" fill="white"/></g></svg>`
          },
          {
            id: "shorts",
            name: "SHORTS",
            svg: `<svg width="180" height="180" viewBox="0 0 180 180" fill="none"><rect width="180" height="180" rx="36" fill="#FF0000"/><g transform="translate(18, 18) scale(3)"><path d="M31.2 20.1C29.6 19.2 28.2 19.1 28.2 19.1L29.6 18.2C32.1 16.7 32.9 13.5 31.4 11C29.9 8.5 26.7 7.7 24.2 9.2L16.2 14C14.1 15.3 12.8 17.7 13 20.2C13.2 22.7 14.9 24.7 17.3 25.3L15.6 26.3C13.1 27.8 12.3 31 13.8 33.5C15.3 36 18.5 36.8 21 35.3L29 30.5C31.1 29.2 32.4 26.8 32.2 24.3C32 21.8 30.3 20.8 31.2 20.1Z" fill="#CC0000"/><path d="M29.5 17.5L24 14.2C21.8 12.9 19 13.6 17.7 15.8C16.4 18 17.1 20.8 19.3 22.1L20.8 23L16.5 25.5C14.3 26.8 13.6 29.6 14.9 31.8C16.2 34 19 34.7 21.2 33.4L26.7 30.1C28.9 28.8 29.6 26 28.3 23.8L26.8 22.9L31.1 20.4C33.3 19.1 34 16.3 32.7 14.1C31.7 12.4 29.5 17.5 29.5 17.5Z" fill="white"/><polygon points="21,19 21,29 29,24" fill="#FF0000"/></g></svg>`
          }
        ];
        return `
          <div class="comp-social-carousel" id="comp-social-carousel">
            <div class="slc-header">
              <div class="slc-header-title">DOMINER LES 4 RÉSEAUX EN SIMULTANÉ</div>
            </div>
            <div class="slc-stage" id="slc-stage">
              ${channelsData.map((ch, idx) => `
                <div class="slc-card" id="slc-card-${idx}">
                  <div class="slc-logo-wrap">${ch.svg}</div>
                  <div class="slc-card-title">${ch.name}</div>
                </div>
              `).join("")}
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

  function animateBlueprint(type, data, progress, elapsed, t, scene) {
    const spring = calcSpringOvershoot(elapsed);

    if (type === "blueprint_kinetic_type") {
      const el = document.getElementById("blueprint-kinetic-type");
      if (el) {
        el.style.transform = `translate(-50%, -50%) scale(${spring.scale})`;
      }
    } else if (type === "blueprint_cursor_ui") {
      const container = document.getElementById("blueprint-cursor-ui");
      const cursor = document.getElementById("bcui-cursor");
      const previewTitleEl = document.getElementById("bcui-preview-title");
      const ripple = document.getElementById("bcui-ripple");
      const clickAt = (data && data.click_at) || 46.84;
      const themeBeats = (data && data.theme_beats) || (data && data.beats) || [46.84, 47.98, 48.88, 49.94];
      const themeList = [
        { id: "claude", name: "01. ÉDITORIAL CHAUD" },
        { id: "cobalt-grid", name: "02. TECH SOMBRE" },
        { id: "editorial-forest", name: "03. CONSEIL FINANCIER" },
        { id: "bold-poster", name: "04. CRÉATEUR PERCUTANT" }
      ];

      const getBtnCoords = (idx) => {
        const btn = document.getElementById(`bcui-btn-${idx}`);
        if (!btn) return { x: 230, y: 460 };
        return {
          x: btn.offsetLeft + btn.offsetWidth * 0.55,
          y: btn.offsetTop + btn.offsetHeight * 0.55
        };
      };

      // Avant 46.84s : AUCUN thème n'est activé, reste en cyber-mint
      if (t < themeBeats[0]) {
        document.documentElement.setAttribute("data-theme", "cyber-mint");
        if (canvas) canvas.setAttribute("data-theme", "cyber-mint");
        if (previewTitleEl) previewTitleEl.textContent = "CHARTE GRAPHIQUE : PRÊTE À ADAPTER";
        for (let i = 0; i < 4; i++) {
          const btn = document.getElementById(`bcui-btn-${i}`);
          if (btn) {
            btn.classList.remove("is-active");
            btn.style.transform = "";
          }
        }
        if (ripple) ripple.style.opacity = "0";

        // Approche du curseur vers le bouton 0 (arrive 0.15s avant 46.84s)
        const b0Coords = getBtnCoords(0);
        const startX = b0Coords.x - 180;
        const startY = b0Coords.y + 120;
        const arriveT = themeBeats[0] - 0.15;
        const departT = themeBeats[0] - 0.70;
        const moveP = Math.min(1, Math.max(0, (t - departT) / (arriveT - departT)));
        const curX = startX + (b0Coords.x - startX) * easeInOutCubic(moveP);
        const curY = startY + (b0Coords.y - startY) * easeInOutCubic(moveP);
        if (cursor) {
          cursor.style.transform = `translate(${curX}px, ${curY}px) scale(1.0)`;
        }
      } else {
        // À partir de 46.84s : détermination du thème actif
        let activeThemeIdx = 0;
        for (let i = 0; i < themeBeats.length; i++) {
          if (t >= themeBeats[i]) {
            activeThemeIdx = i;
          }
        }

        const currentTarget = themeList[activeThemeIdx];
        const currentBeatT = themeBeats[activeThemeIdx];

        // Application dynamique immédiate du thème sur DOM et canvas
        document.documentElement.setAttribute("data-theme", currentTarget.id);
        if (canvas) canvas.setAttribute("data-theme", currentTarget.id);

        if (previewTitleEl) {
          previewTitleEl.textContent = currentTarget.name;
        }

        // Mise à jour de l'état actif des boutons
        for (let i = 0; i < 4; i++) {
          const btn = document.getElementById(`bcui-btn-${i}`);
          if (btn) {
            btn.classList.toggle("is-active", i === activeThemeIdx);
          }
        }

        const curCoords = getBtnCoords(activeThemeIdx);
        let curX = curCoords.x;
        let curY = curCoords.y;

        // Déplacement du curseur vers le bouton suivant s'il existe
        if (activeThemeIdx < themeBeats.length - 1) {
          const nextBeatT = themeBeats[activeThemeIdx + 1];
          const arriveNextT = nextBeatT - 0.15;
          const departNextT = currentBeatT + 0.30;
          if (t > departNextT && t <= arriveNextT) {
            const nextCoords = getBtnCoords(activeThemeIdx + 1);
            const pMove = Math.min(1, Math.max(0, (t - departNextT) / (arriveNextT - departNextT)));
            const eased = easeInOutCubic(pMove);
            curX = curCoords.x + (nextCoords.x - curCoords.x) * eased;
            curY = curCoords.y + (nextCoords.y - curCoords.y) * eased;
          } else if (t > arriveNextT) {
            const nextCoords = getBtnCoords(activeThemeIdx + 1);
            curX = nextCoords.x;
            curY = nextCoords.y;
          }
        }

        // Clic à l'instant du beat :
        // 1. Curseur : scale(0.82) -> scale(1.0)
        // 2. Bouton cliqué : translateY(4px) scale(0.96)
        // 3. Onde ripple sous la pointe
        const clickElapsed = t - currentBeatT;
        let cursorScale = 1.0;
        const activeBtn = document.getElementById(`bcui-btn-${activeThemeIdx}`);

        if (clickElapsed >= 0 && clickElapsed <= 0.22) {
          if (clickElapsed < 0.08) {
            const pPress = clickElapsed / 0.08;
            cursorScale = 1.0 - 0.18 * pPress;
            if (activeBtn) activeBtn.style.transform = `translateY(${4 * pPress}px) scale(${1.0 - 0.04 * pPress})`;
          } else {
            const pRel = (clickElapsed - 0.08) / 0.14;
            cursorScale = 0.82 + 0.18 * pRel;
            if (activeBtn) activeBtn.style.transform = `translateY(${4 * (1 - pRel)}px) scale(${0.96 + 0.04 * pRel})`;
          }
        } else {
          if (activeBtn) activeBtn.style.transform = "";
        }

        if (cursor) {
          cursor.style.transform = `translate(${curX}px, ${curY}px) scale(${cursorScale})`;
        }

        if (ripple) {
          if (clickElapsed >= 0 && clickElapsed <= 0.40) {
            const pRip = clickElapsed / 0.40;
            ripple.style.left = `${curCoords.x}px`;
            ripple.style.top = `${curCoords.y}px`;
            ripple.style.transform = `scale(${pRip * 2.2})`;
            ripple.style.opacity = `${1.0 - pRip}`;
          } else {
            ripple.style.opacity = "0";
          }
        }
      }
    } else if (type === "blueprint_terminal_scene") {
      const cmdEl = document.getElementById("bts-command-text");
      const outEl = document.getElementById("bts-output");
      const curBlock = document.getElementById("bts-cursor");
      const fullCmd = data.command || "agent404 compile --auto";
      const execAt = (data && data.execute_at) || (scene.start + 1.5);

      if (cmdEl) {
        const pType = Math.min(1, Math.max(0, (t - scene.start) / Math.max(0.001, execAt - scene.start)));
        const charCount = Math.floor(fullCmd.length * pType);
        cmdEl.textContent = fullCmd.slice(0, charCount);
      }
      if (curBlock) {
        curBlock.style.opacity = (Math.floor(t * 3.5) % 2 === 0) ? "1" : "0.2";
      }
      if (outEl) {
        if (t >= execAt) {
          outEl.style.display = "block";
          outEl.className = "bts-output bts-output-success";
        } else {
          outEl.style.display = "none";
        }
      }
    } else if (type === "blueprint_compare_split") {
      const cardAvant = document.getElementById("bcs-card-avant");
      const cardApres = document.getElementById("bcs-card-apres");
      const gaugeFill = document.getElementById("bcs-gauge-fill");
      const gaugeVal = document.getElementById("bcs-gauge-val");
      const revealAt = (data && data.reveal_at) !== undefined ? data.reveal_at : 17.52;
      const alertAt = (data && data.alert_at) !== undefined ? data.alert_at : 19.78;
      const gaugeStart = (data && data.gauge_start) !== undefined ? data.gauge_start : 19.78;
      const gaugeEnd = (data && data.gauge_end) !== undefined ? data.gauge_end : (scene ? scene.end - 0.4 : 21.66);

      if (cardAvant) {
        cardAvant.style.transform = `scale(${spring.scale}) rotate(-1.5deg)`;
      }
      if (cardApres) {
        if (t >= revealAt) {
          const apresElapsed = t - revealAt;
          const apresSpring = calcSpringOvershoot(apresElapsed);
          cardApres.style.transform = `scale(${apresSpring.scale}) rotate(1.5deg)`;
          cardApres.style.opacity = "1";

          // Alerte critique dès alertAt (19.78s sur "détruit")
          if (t >= alertAt) {
            cardApres.classList.add("bcs-card-alert");
            cardApres.classList.remove("bcs-card-warning");
          } else {
            cardApres.classList.remove("bcs-card-alert");
            cardApres.classList.add("bcs-card-warning");
          }

          // Jauge de confiance : chute de 100% à 0% entre 19.78s et 21.66s
          if (gaugeFill && gaugeVal) {
            if (t < gaugeStart) {
              gaugeFill.style.width = "100%";
              gaugeVal.textContent = "100%";
            } else if (t >= gaugeEnd) {
              gaugeFill.style.width = "0%";
              gaugeVal.textContent = "0%";
            } else {
              const pGauge = Math.min(1, Math.max(0, (t - gaugeStart) / Math.max(0.01, gaugeEnd - gaugeStart)));
              const remaining = Math.round((1 - pGauge) * 100);
              gaugeFill.style.width = `${remaining}%`;
              gaugeVal.textContent = `${remaining}%`;
            }
          }
        } else {
          cardApres.style.transform = "scale(0.8) rotate(5deg)";
          cardApres.style.opacity = "0";
        }
      }
    } else if (type === "blueprint_spatial_pan") {
      const st1 = document.getElementById("bsp-st-1");
      const st2 = document.getElementById("bsp-st-2");
      const st3 = document.getElementById("bsp-st-3");
      const conn1 = document.getElementById("bsp-conn-1");
      const conn2 = document.getElementById("bsp-conn-2");
      const pFill1 = document.getElementById("bsp-progress-1");
      const pFill2 = document.getElementById("bsp-progress-2");
      const pFill3 = document.getElementById("bsp-progress-3");
      const icon1 = document.getElementById("bsp-icon-1");
      const icon2 = document.getElementById("bsp-icon-2");
      const icon3 = document.getElementById("bsp-icon-3");

      const t1 = 29.00;
      const t2 = 33.68;
      const t3 = 37.84;
      const tEnd = (scene && scene.end) || 41.72;

      function updateStation(st, pFill, icon, startT, endT, isActiveNow, isPast, rotDeg) {
        if (!st) return;
        const rotStr = `rotate(${rotDeg}deg)`;
        if (t < startT) {
          st.style.opacity = "0.12";
          st.style.transform = `scale(0.88) translateY(30px) ${rotStr}`;
          st.classList.remove("is-active");
          if (pFill) pFill.style.width = "0%";
          if (icon) icon.style.transform = "scale(0.9)";
        } else if (isActiveNow) {
          const elapsed = t - startT;
          const sp = calcSpringOvershoot(elapsed);
          st.style.opacity = "1";
          st.style.transform = `scale(${sp.scale * 1.02}) ${rotStr}`;
          st.classList.add("is-active");

          const pProg = Math.min(1, Math.max(0, (t - startT) / (endT - startT)));
          if (pFill) pFill.style.width = `${Math.round(pProg * 100)}%`;

          const pulse = 1.0 + Math.sin(t * 14) * 0.16;
          if (icon) icon.style.transform = `scale(${pulse})`;
        } else if (isPast) {
          st.style.opacity = "0.85";
          st.style.transform = `scale(1.0) ${rotStr}`;
          st.classList.remove("is-active");
          if (pFill) pFill.style.width = "100%";
          if (icon) icon.style.transform = "scale(1.0)";
        }
      }

      updateStation(st1, pFill1, icon1, t1, t2, t >= t1 && t < t2, t >= t2, -1.5);
      updateStation(st2, pFill2, icon2, t2, t3, t >= t2 && t < t3, t >= t3, 1.5);
      updateStation(st3, pFill3, icon3, t3, tEnd, t >= t3, false, -1.5);

      if (conn1) conn1.style.opacity = t >= t2 ? "1" : "0.2";
      if (conn2) conn2.style.opacity = t >= t3 ? "1" : "0.2";
    } else if (type === "blueprint_overwhelm") {
      const beats = (data && data.beats) || [scene.start + 0.8, scene.start + 1.8, scene.start + 2.8, scene.start + 3.8];
      const avatar = document.getElementById("bow-avatar");
      if (avatar) {
        const floatY = Math.sin(t * 4.5) * 6;
        avatar.style.transform = `translateY(${floatY}px)`;
      }
      for (let i = 0; i < 4; i++) {
        const badge = document.getElementById(`bow-badge-${i}`);
        if (!badge) continue;
        const beatT = beats[i] !== undefined ? beats[i] : (scene.start + i * 1.0);
        if (t >= beatT) {
          badge.classList.add("is-active");
          const popElapsed = Math.min(0.35, t - beatT);
          const p = popElapsed / 0.35;
          const scale = 0.88 + 0.16 * p + (p < 1 ? 0.12 * Math.sin(p * Math.PI) : 0);
          badge.style.transform = `scale(${scale})`;
        } else {
          badge.classList.remove("is-active");
          badge.style.transform = "scale(0.92)";
        }
      }
    } else if (type === "blueprint_delivery_grid") {
      const renderBar = document.getElementById("bdg-render-bar");
      const beats = (data && data.beats) || [55.04, 55.82, 56.46, 56.85];

      // Compteur et barre de rendu de 0% à 100% à 55.00s
      if (renderBar) {
        const pPrep = Math.min(1, Math.max(0, (t - 51.10) / (55.00 - 51.10)));
        renderBar.style.width = `${Math.round(pPrep * 100)}%`;
      }

      // Pré-chauffage pulsé avant 55.04s
      if (t < 55.04) {
        const cycle = ((t - 51.10) * 3) % 4;
        for (let i = 0; i < 4; i++) {
          const card = document.getElementById(`channel-card-${i}`) || document.getElementById(`bdg-card-${i}`);
          if (!card) continue;
          card.classList.remove("is-active", "active");
          const isPulsing = Math.floor(cycle) === i;
          card.style.opacity = isPulsing ? "0.65" : "0.35";
          card.style.transform = isPulsing ? "scale(0.98)" : "scale(0.95)";
        }
      } else {
        // Allumage mot-à-mot des 4 cartes
        for (let i = 0; i < 4; i++) {
          const card = document.getElementById(`channel-card-${i}`) || document.getElementById(`bdg-card-${i}`);
          if (!card) continue;
          const beatT = beats[i] !== undefined ? beats[i] : (55.04 + i * 0.7);
          if (t >= beatT) {
            card.classList.add("is-active", "active");
            const popElapsed = Math.min(0.30, t - beatT);
            const p = popElapsed / 0.30;
            const scale = 0.95 + 0.10 * p + (p < 1 ? 0.08 * Math.sin(p * Math.PI) : 0);
            card.style.transform = `scale(${scale})`;
            card.style.opacity = "1";
          } else {
            card.classList.remove("is-active", "active");
            card.style.transform = "scale(0.95)";
            card.style.opacity = "0.35";
          }
        }
      }
    }
  }

  function animateComponent(type, data, progress, elapsed, t, scene) {
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
      let floatY = Math.sin(t * 5) * 10;
      let tiltDeg = Math.sin(t * 2.5) * 1.5;
      let camZoom = 1.0 + progress * 0.05;
      let sighScaleY = 1.0;

      // Mandatory fix #2: Soupir réaliste entre 7.95s et 8.50s
      if (data.is_sigh || (t >= 7.95 && t <= 8.50)) {
        const sighT = Math.max(0, Math.min(1, (t - 7.95) / 0.55));
        if (sighT < 0.3) {
          const p = sighT / 0.3;
          floatY += -8 * Math.sin(p * Math.PI * 0.5);
          sighScaleY = 1.0 + 0.02 * p;
        } else {
          const p = (sighT - 0.3) / 0.7;
          floatY += 18 * Math.sin(p * Math.PI * 0.5);
          sighScaleY = 1.0 - 0.03 * Math.sin(p * Math.PI * 0.5);
        }
      }

      // Mandatory fix #4: Punch-in dramatique à 13.06s
      if (data.is_punch_in || (t >= 13.06 && t < 13.96)) {
        camZoom = 1.15;
      }

      if (avatar) {
        if (isHeadOnly) {
          avatar.style.transform = `translateY(${spring.ty + floatY}px) rotate(${tiltDeg}deg) scale(${spring.scale * camZoom}) scaleY(${sighScaleY})`;
          avatar.style.transformOrigin = "center center";
        } else {
          avatar.style.transform = `translateX(-50%) translateY(${spring.ty + floatY}px) rotate(${tiltDeg}deg) scale(${spring.scale * camZoom}) scaleY(${sighScaleY})`;
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
      const beats = (data && data.beats) || null;
      let activeIdx = -1;
      if (beats && Array.isArray(beats)) {
        for (let b = 0; b < beats.length; b++) {
          if (t >= beats[b]) activeIdx = b;
        }
      } else {
        activeIdx = Math.min(total - 1, Math.floor(progress * total));
      }
      for (let i = 0; i < total; i++) {
        const itemEl = document.getElementById(`list-item-${i}`);
        if (!itemEl) continue;
        const itemDelay = beats ? (beats[i] !== undefined ? Math.max(0, beats[i] - scene.start) : i * 0.15) : i * 0.15;
        const itemElapsed = Math.max(0, elapsed - itemDelay);
        if (itemElapsed === 0 && (beats ? t < beats[i] : elapsed < itemDelay)) {
          itemEl.style.opacity = "0.2";
          itemEl.style.transform = "translateY(20px) scale(0.92)";
          itemEl.classList.remove("active");
        } else {
          const itemP = Math.min(1, itemElapsed / 0.2);
          const itemScale = 0.92 + 0.08 * itemP + (itemP < 1 ? 0.08 * Math.sin(itemP * Math.PI) : 0);
          itemEl.style.opacity = "1";
          if (i === activeIdx) {
            itemEl.classList.add("active");
            itemEl.style.transform = `scale(${itemScale * 1.04}) translateX(14px)`;
          } else {
            itemEl.classList.remove("active");
            itemEl.style.transform = `scale(${itemScale})`;
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
          statusEl.style.background = "var(--accent-primary)";
          statusEl.style.color = "var(--bg-carbon)";
        }
        if (silenceBadge) {
          silenceBadge.textContent = "RYTHME 100% ACTIF";
          silenceBadge.style.background = "var(--bg-carbon)";
          silenceBadge.style.color = "var(--accent-primary)";
        }
        if (btn) {
          btn.classList.add("pressed");
          btn.textContent = "✓ SILENCES PURGÉS";
        }
      } else {
        if (statusEl) {
          statusEl.textContent = "ANALYSE DU SPECTRE";
          statusEl.style.background = "var(--accent-primary)";
          statusEl.style.color = "var(--bg-carbon)";
        }
        if (silenceBadge) {
          silenceBadge.textContent = "SILENCE DÉTECTÉ : 0.38s";
          silenceBadge.style.background = "var(--bg-carbon)";
          silenceBadge.style.color = "var(--white)";
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
      let badgeBg = "var(--accent-primary)";
      let badgeColor = "var(--bg-carbon)";

      if (progress >= 0.66) {
        src = "assets/avatars/skeptic.png";
        text = "🤨 ÉMOTION : SCEPTIQUE";
        badgeBg = "var(--white)";
        badgeColor = "var(--bg-carbon)";
      } else if (progress >= 0.33) {
        src = "assets/avatars/shock.png";
        text = "😱 ÉMOTION : CHOQUÉ";
        badgeBg = "var(--accent-primary)";
        badgeColor = "var(--bg-carbon)";
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
          btn.style.boxShadow = "0 2px 0 var(--surface-black)";
          btn.style.background = "var(--mint-dark)";
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
        const mp = Math.min(1, elapsed / 0.3);
        const mscale = mp < 1 ? (0.85 + 0.15 * mp + 0.1 * Math.sin(mp * Math.PI)) : 1.0;
        marker.style.transform = `scale(${mscale})`;
        marker.style.opacity = `${mp}`;
      }
    } else if (type === "browser_tab_overload") {
      const el = document.getElementById("comp-browser-overload");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const alert = document.getElementById("overload-shock-alert");
      if (alert) {
        const ap = Math.min(1, elapsed / 0.3);
        const ascale = ap < 1 ? (0.88 + 0.12 * ap + 0.08 * Math.sin(ap * Math.PI)) : 1.0;
        alert.style.transform = `scale(${ascale})`;
        alert.style.opacity = `${ap}`;
      }
      for (let i = 0; i < 3; i++) {
        const tag = document.getElementById(`otag-${i}`);
        if (!tag) continue;
        const tagElapsed = Math.max(0, elapsed - 0.2 - i * 0.15);
        const tp = Math.min(1, tagElapsed / 0.2);
        tag.style.opacity = `${tp}`;
        tag.style.transform = `scale(${0.9 + 0.1 * tp})`;
      }
    } else if (type === "loom_3_flaws_timeline") {
      const el = document.getElementById("comp-flaws-timeline");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const card0 = document.getElementById("flaw-card-0");
      const card1 = document.getElementById("flaw-card-1");
      const card2 = document.getElementById("flaw-card-2");
      // Timing d'activation basé sur les mots prononcés :
      // 00:08.5 "des hésitations" | 00:09.6 "des silences" | 00:10.5 "et une voix fatiguée"
      const isCard0Active = t >= 8.5 || elapsed >= 0.1;
      const isCard1Active = t >= 9.6 || elapsed >= 1.0;
      const isCard2Active = t >= 10.5 || elapsed >= 1.9;

      if (card0) {
        if (isCard0Active) {
          card0.style.borderColor = "var(--accent-warning)";
          card0.style.transform = "scale(1.03)";
          card0.style.background = "var(--accent-warning-dim)";
        } else {
          card0.style.borderColor = "var(--border-subtle)";
          card0.style.transform = "scale(1.0)";
          card0.style.background = "var(--surface-card)";
        }
      }
      if (card1) {
        if (isCard1Active) {
          card1.style.borderColor = "var(--accent-warning)";
          card1.style.transform = "scale(1.03)";
          card1.style.background = "var(--accent-warning-dim)";
        } else {
          card1.style.borderColor = "var(--border-subtle)";
          card1.style.transform = "scale(1.0)";
          card1.style.background = "var(--surface-card)";
        }
      }
      if (card2) {
        if (isCard2Active) {
          card2.style.borderColor = "var(--accent-warning)";
          card2.style.transform = "scale(1.03)";
          card2.style.background = "var(--accent-warning-dim)";
        } else {
          card2.style.borderColor = "var(--border-subtle)";
          card2.style.transform = "scale(1.0)";
          card2.style.background = "var(--surface-card)";
        }
      }
    } else if (type === "tab_close_cursor") {
      const el = document.getElementById("comp-tab-close");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const cur = document.getElementById("tab-cursor");
      const btn = document.getElementById("tab-btn-close-action");
      const preview = document.getElementById("preview-mini-loom");
      const stamp = document.getElementById("tab-close-stamp");

      // Clic à t = 12.4s ou elapsed >= 0.4s
      const isClicked = t >= 12.4 || elapsed >= 0.45;
      const moveP = Math.min(1, elapsed / 0.45);
      const startX = 320, startY = 260;
      const targetX = 260, targetY = -230;
      const curX = startX + (targetX - startX) * moveP;
      const curY = startY + (targetY - startY) * moveP;

      if (cur) {
        cur.style.transform = `translate(${curX}px, ${curY}px) scale(${isClicked ? 0.9 : 1.0})`;
      }
      if (btn) {
        if (isClicked) {
          btn.style.background = "var(--accent-warning)";
          btn.style.color = "var(--bg-dark)";
          btn.style.transform = "scale(0.94)";
        } else {
          btn.style.background = "var(--border-subtle)";
          btn.style.color = "var(--accent-warning)";
          btn.style.transform = "scale(1.0)";
        }
      }
      if (preview) {
        if (isClicked) {
          preview.style.transform = "scale(0.92)";
          preview.style.opacity = "0.2";
          preview.style.filter = "grayscale(1)";
        } else {
          preview.style.transform = "scale(1.0)";
          preview.style.opacity = "1.0";
          preview.style.filter = "none";
        }
      }
      if (stamp) {
        if (isClicked) {
          const sp = Math.min(1, (elapsed - 0.45) / 0.2);
          stamp.style.opacity = "1";
          stamp.style.transform = `translate(-50%, -50%) rotate(-3deg) scale(${0.9 + 0.1 * sp})`;
        } else {
          stamp.style.opacity = "0";
          stamp.style.transform = "translate(-50%, -50%) rotate(-3deg) scale(0.85)";
        }
      }
    } else if (type === "product_vs_perception") {
      const el = document.getElementById("comp-product-perception");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const pip = document.getElementById("avatar-pip");
      if (pip) {
        const floatY = Math.sin(t * 4) * 6;
        pip.style.transform = `translateY(${floatY}px)`;
      }
      // Effondrement de la colonne valeur perçue (phase perception)
      if (data.phase === "perception") {
        const fillPerceived = document.getElementById("perceived-fill");
        const kpiPerceived = document.getElementById("col-kpi-perceived");
        const impactBanner = document.getElementById("perception-impact-banner");

        // De 100% à 18% au cours de la scène
        const dropProgress = Math.min(1, Math.max(0, elapsed / 0.8));
        const currentVal = Math.round(100 - (100 - 18) * dropProgress);
        if (fillPerceived) {
          fillPerceived.style.height = `${currentVal}%`;
        }
        if (kpiPerceived) {
          kpiPerceived.textContent = `${currentVal}%`;
        }
        if (impactBanner) {
          const bp = Math.max(0, Math.min(1, (elapsed - 0.5) / 0.25));
          impactBanner.style.opacity = `${bp}`;
          impactBanner.style.transform = `scale(${0.94 + 0.06 * bp})`;
        }
      }
    } else if (type === "interface_labyrinth_cut") {
      const el = document.getElementById("comp-labyrinth-cut");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const isCut = t >= 23.0 || progress >= 0.35;
      const grid = document.getElementById("labyrinth-grid");
      const line1 = document.getElementById("strike-line-1");
      const line2 = document.getElementById("strike-line-2");
      const banner = document.getElementById("labyrinth-central-banner");

      if (grid) {
        if (isCut) {
          grid.style.opacity = "0.2";
          grid.style.filter = "grayscale(1)";
        } else {
          grid.style.opacity = "1";
          grid.style.filter = "none";
        }
      }
      if (line1) line1.style.opacity = isCut ? "1" : "0";
      if (line2) line2.style.opacity = isCut ? "1" : "0";
      if (banner) {
        if (isCut) {
          banner.style.opacity = "1";
          banner.style.transform = "translate(-50%, -50%) scale(1.0)";
        } else {
          banner.style.opacity = "0";
          banner.style.transform = "translate(-50%, -50%) scale(0.92)";
        }
      }
    } else if (type === "sixty_sec_value_bridge") {
      const el = document.getElementById("comp-sixty-bridge");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const digits = document.getElementById("chrono-digits");
      const ring = document.getElementById("chrono-progress-ring");
      if (digits) {
        const beat = 1.0 + Math.sin(t * 8) * 0.04;
        digits.style.transform = `scale(${beat})`;
      }
      if (ring) {
        const ringP = Math.min(1, progress * 1.2);
        const dashoffset = 640 * (1 - ringP);
        ring.style.strokeDashoffset = `${dashoffset}`;
      }
    } else if (type === "code_to_ui_live") {
      const el = document.getElementById("comp-code-live");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;
      const cardCam = document.getElementById("code-card-camera");
      const cardRetakes = document.getElementById("code-card-retakes");

      // 00:33.3 "Zéro caméra" | 00:34.3 "zéro prise ratée"
      const isCamActive = t >= 33.3 || elapsed >= 1.2;
      const isRetakesActive = t >= 34.3 || elapsed >= 2.2;

      if (cardCam) {
        if (isCamActive) {
          cardCam.style.borderColor = "var(--white)";
          cardCam.style.transform = "scale(1.04)";
          cardCam.style.boxShadow = "0 14px 0 var(--surface-black), 0 0 20px rgba(255, 255, 255, 0.2)";
        } else {
          cardCam.style.borderColor = "var(--border-subtle)";
          cardCam.style.transform = "scale(1.0)";
          cardCam.style.boxShadow = "0 12px 0 var(--surface-black)";
        }
      }
      if (cardRetakes) {
        if (isRetakesActive) {
          cardRetakes.style.borderColor = "var(--accent-primary)";
          cardRetakes.style.transform = "scale(1.04)";
          cardRetakes.style.boxShadow = "0 14px 0 var(--surface-black), 0 0 24px rgba(0, 245, 160, 0.4)";
        } else {
          cardRetakes.style.borderColor = "var(--border-subtle)";
          cardRetakes.style.transform = "scale(1.0)";
          cardRetakes.style.boxShadow = "0 12px 0 var(--surface-black)";
        }
      }
    } else if (type === "voice_to_word_grid") {
      const el = document.getElementById("comp-word-grid");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;

      // Compression visuelle des silences lors de la phase 1 (00:38.5 - 00:40.8)
      const isCutPhase = t >= 40.5 || progress >= 0.4;
      const s1 = document.getElementById("silence-block-1");
      const s2 = document.getElementById("silence-block-2");
      const cleanTag = document.getElementById("tier-tag-clean");

      if (isCutPhase) {
        if (s1) { s1.style.width = "0px"; s1.style.opacity = "0"; s1.style.padding = "0"; s1.style.border = "none"; }
        if (s2) { s2.style.width = "0px"; s2.style.opacity = "0"; s2.style.padding = "0"; s2.style.border = "none"; }
        if (cleanTag) { cleanTag.style.background = "var(--accent-primary)"; cleanTag.style.color = "var(--bg-dark)"; }
      } else {
        if (s1) { s1.style.width = "180px"; s1.style.opacity = "1"; }
        if (s2) { s2.style.width = "220px"; s2.style.opacity = "1"; }
      }

      // Ondes actives dynamiques
      const barsCount = 28;
      for (let i = 0; i < barsCount; i++) {
        const bar = document.getElementById(`awbar-${i}`);
        if (!bar) continue;
        const waveOsc = Math.sin(t * 14 + i * 0.45) * Math.cos(t * 7 - i * 0.2);
        const dist = Math.abs(i - barsCount / 2) / (barsCount / 2);
        const baseH = (1 - dist * 0.5) * 140;
        const h = Math.max(18, baseH * Math.abs(waveOsc) + 24);
        bar.style.height = `${Math.round(h)}px`;
      }

      // Synchronisation mot-à-mot (00:40.8 - 00:43.5)
      const w0 = document.getElementById("word-card-0");
      const w1 = document.getElementById("word-card-1");
      const w2 = document.getElementById("word-card-2");
      const isW0 = t >= 40.8 || progress >= 0.50;
      const isW1 = t >= 41.6 || progress >= 0.68;
      const isW2 = t >= 42.4 || progress >= 0.82;

      if (w0) {
        if (isW0) w0.classList.add("active");
        else w0.classList.remove("active");
      }
      if (w1) {
        if (isW1) w1.classList.add("active");
        else w1.classList.remove("active");
      }
      if (w2) {
        if (isW2) w2.classList.add("active");
        else w2.classList.remove("active");
      }
    } else if (type === "saas_showcase_3steps") {
      const el = document.getElementById("comp-saas-showcase");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;

      const p1 = document.getElementById("theater-phase-1");
      const p2 = document.getElementById("theater-phase-2");
      const p3 = document.getElementById("theater-phase-3");
      const pill1 = document.getElementById("st-pill-1");
      const pill2 = document.getElementById("st-pill-2");
      const pill3 = document.getElementById("st-pill-3");

      // 3 PHASES VISUELLES DYNAMIQUES :
      // Phase 1 : 00:43.5 - 00:47.3 (Isolation de la fonctionnalité clé)
      // Phase 2 : 00:47.3 - 00:49.2 (Parcours utilisateur simulé avec curseur)
      // Phase 3 : 00:49.2 - 00:52.2 (Rendu Master HD 1080x1920)
      if (t < 47.3 || progress < 0.41) {
        if (p1) p1.style.display = "block";
        if (p2) p2.style.display = "none";
        if (p3) p3.style.display = "none";
        if (pill1) pill1.classList.add("active");
        if (pill2) pill2.classList.remove("active");
        if (pill3) pill3.classList.remove("active");
      } else if (t < 49.2 || progress < 0.65) {
        if (p1) p1.style.display = "none";
        if (p2) p2.style.display = "block";
        if (p3) p3.style.display = "none";
        if (pill1) pill1.classList.remove("active");
        if (pill2) pill2.classList.add("active");
        if (pill3) pill3.classList.remove("active");

        // Curseur sur bouton pipeline
        const cur = document.getElementById("journey-cursor");
        const ctaBtn = document.getElementById("journey-cta-btn");
        const step2 = document.getElementById("j-step-2");
        const step3 = document.getElementById("j-step-3");
        const phase2Elapsed = Math.max(0, elapsed - 3.8);
        const curP = Math.min(1, phase2Elapsed / 0.8);

        if (cur) {
          const cx = -180 + curP * 360;
          const cy = 60 + Math.sin(curP * Math.PI) * -30;
          cur.style.transform = `translate(${cx}px, ${cy}px) scale(${curP >= 0.8 ? 0.9 : 1.0})`;
        }
        if (ctaBtn && curP >= 0.8) {
          ctaBtn.style.transform = "scale(0.96)";
          ctaBtn.style.background = "var(--white)";
        }
        if (step2 && curP >= 0.4) step2.classList.add("checked");
        if (step3 && curP >= 0.8) step3.classList.add("checked");
      } else {
        if (p1) p1.style.display = "none";
        if (p2) p2.style.display = "none";
        if (p3) p3.style.display = "flex";
        if (pill1) pill1.classList.remove("active");
        if (pill2) pill2.classList.remove("active");
        if (pill3) pill3.classList.add("active");
      }
    } else if (type === "delivery_48h_3channels") {
      const el = document.getElementById("comp-delivery-channels");
      if (el) el.style.transform = `translateY(${spring.ty}px) scale(${spring.scale})`;

      // Synchronisation exclusive avec chaque mot prononcé :
      // 00:52.2 - 00:55.3 : aucune carte sur-allumée
      // 00:55.3 - 00:56.6 : Carte 01 (SUR LINKEDIN)
      // 00:56.6 - 00:57.5 : Carte 02 (EN PROSPECTION B2B)
      // 00:57.5 - 00:58.8 : Carte 03 (EN HAUT DE TA LANDING PAGE)
      const r0 = document.getElementById("channel-row-0");
      const r1 = document.getElementById("channel-row-1");
      const r2 = document.getElementById("channel-row-2");

      let isR0 = false;
      let isR1 = false;
      let isR2 = false;

      if (t >= 10) {
        isR0 = (t >= 55.3 && t < 56.6);
        isR1 = (t >= 56.6 && t < 57.5);
        isR2 = (t >= 57.5 && t <= 58.8);
      } else {
        isR0 = (progress >= 0.40 && progress < 0.59);
        isR1 = (progress >= 0.59 && progress < 0.725);
        isR2 = (progress >= 0.725 && progress <= 0.92);
      }

      if (r0) {
        if (isR0) r0.classList.add("active");
        else r0.classList.remove("active");
      }
      if (r1) {
        if (isR1) r1.classList.add("active");
        else r1.classList.remove("active");
      }
      if (r2) {
        if (isR2) r2.classList.add("active");
        else r2.classList.remove("active");
      }
    } else if (type === "face_to_dm_cta") {
      const avatarStage = document.getElementById("face-dm-avatar-stage");
      const ctaStage = document.getElementById("face-dm-cta-stage");
      const avatar = document.getElementById("avatar-img");
      const giantBox = document.getElementById("cta-giant-box");
      const sendBtn = document.getElementById("cta-send-button");
      const cursor = document.getElementById("cta-cursor");

      const sceneStart = (scene && scene.start) !== undefined ? scene.start : 52.0;
      const sceneEnd = (scene && scene.end) !== undefined ? scene.end : (sceneStart + 6.0);
      const sceneDur = Math.max(0.001, sceneEnd - sceneStart);

      // Bascule vers le CTA final monumental
      const ctaAt = (data && data.cta_at) !== undefined ? data.cta_at : (scene ? sceneStart + sceneDur * 0.45 : 63.0);
      const spokenAt = (data && data.spoken_at) !== undefined ? data.spoken_at : (scene ? sceneStart + sceneDur * 0.70 : 63.66);

      const isCtaActive = t >= ctaAt;

      if (!isCtaActive) {
        if (avatarStage) {
          avatarStage.style.opacity = "1";
          avatarStage.style.pointerEvents = "auto";
        }
        if (ctaStage) {
          ctaStage.style.opacity = "0";
          ctaStage.style.pointerEvents = "none";
        }
        if (avatar) {
          const floatY = Math.sin(t * 5) * 10;
          const tiltDeg = Math.sin(t * 2.5) * 1.5;
          avatar.style.transform = `translateX(-50%) translateY(${spring.ty + floatY}px) rotate(${tiltDeg}deg) scale(${spring.scale})`;
        }
      } else {
        if (avatarStage) {
          avatarStage.style.opacity = "0";
          avatarStage.style.pointerEvents = "none";
        }
        if (ctaStage) {
          ctaStage.style.opacity = "1";
          ctaStage.style.pointerEvents = "auto";
        }

        const keyword = (data && data.keyword) || "CLARTÉ";
        const cascadeStart = (data && data.cascade_start !== undefined) ? data.cascade_start : (spokenAt > ctaAt + 0.3 ? spokenAt - 0.05 : ctaAt);
        const letterStep = 0.04; // 0.04s par lettre

        for (let i = 0; i < keyword.length; i++) {
          const letterEl = document.getElementById(`kw-letter-${i}`);
          if (letterEl) {
            const letterStart = cascadeStart + i * letterStep;
            if (t < letterStart) {
              letterEl.style.opacity = "0";
              letterEl.style.transform = "scale(0.5)";
            } else {
              const p = Math.min(1, (t - letterStart) / 0.03);
              letterEl.style.opacity = "1";
              const scale = p < 0.8 ? (0.5 + 0.7 * (p / 0.8)) : (1.2 - 0.2 * ((p - 0.8) / 0.2));
              letterEl.style.transform = `scale(${scale})`;
            }
          }
        }

        // Support rétrocompatible pour letter-D, letter-E, letter-M, letter-O
        ["D", "E", "M", "O"].forEach((ch, idx) => {
          const legacyEl = document.getElementById(`letter-${ch}`);
          if (legacyEl) {
            const letterStart = cascadeStart + idx * letterStep;
            if (t < letterStart) {
              legacyEl.style.opacity = "0";
              legacyEl.style.transform = "scale(0.5)";
            } else {
              const p = Math.min(1, (t - letterStart) / 0.03);
              legacyEl.style.opacity = "1";
              legacyEl.style.transform = `scale(${0.7 + 0.3 * p})`;
            }
          }
        });

        // Punch-in monumental sur le mot-clé dès spokenAt (61.40s)
        const isSpoken = t >= spokenAt;
        if (giantBox) {
          if (isSpoken) {
            giantBox.style.transform = "scale(1.08)";
            giantBox.style.boxShadow = "18px 18px 0px var(--white), 0 0 60px rgba(0, 245, 160, 0.6)";
          } else {
            giantBox.style.transform = "scale(1.0)";
            giantBox.style.boxShadow = "14px 14px 0px var(--white), 0 0 40px rgba(0, 245, 160, 0.4)";
          }
        }

        if (cursor) {
          const directBox = document.querySelector(".cta-direct-box");
          if (directBox && sendBtn) {
            const boxRect = directBox.getBoundingClientRect();
            const btnRect = sendBtn.getBoundingClientRect();
            const btnX = (btnRect.left - boxRect.left) + btnRect.width * 0.48;
            const btnY = (btnRect.top - boxRect.top) + btnRect.height * 0.45;

            // Arrivée sur le bouton 0.15s avant spokenAt, clic à spokenAt
            const approachP = Math.min(1, Math.max(0, (t - (spokenAt - 0.35)) / 0.25));
            const cx = btnX + (1 - approachP) * 140;
            const cy = btnY + (1 - approachP) * 100;
            const curScale = isSpoken ? 0.82 : 1.0;
            cursor.style.transform = `translate(${cx}px, ${cy}px) scale(${curScale})`;
          } else {
            const ctaElapsed = Math.max(0, t - ctaAt);
            const moveCurP = Math.min(1, Math.max(0, (ctaElapsed - 0.4) / 0.4));
            const cx = 200 * (1 - moveCurP) + 120;
            const cy = 180 * (1 - moveCurP) + 195;
            cursor.style.transform = `translate(${cx}px, ${cy}px) scale(${isSpoken ? 0.82 : 1.0})`;
          }
        }

        if (sendBtn) {
          if (isSpoken) {
            sendBtn.style.transform = "translateY(4px) scale(0.96)";
            sendBtn.style.boxShadow = "2px 2px 0px var(--accent-primary)";
          } else {
            sendBtn.style.transform = "scale(1.0)";
            sendBtn.style.boxShadow = "8px 8px 0px var(--accent-primary)";
          }
        }
      }
    } else if (type === "zero_video_slam") {
        const box = document.getElementById("zero-counter-box");
        const num = document.getElementById("zero-counter-num");
        const giantWrap = document.getElementById("zero-giant-wrap");
        const shockwave = document.getElementById("zero-shockwave");
        const giantDigit = document.getElementById("zero-giant-digit");
        const slamBadge = document.getElementById("zero-slam-badge");

        // Countdown 4 -> 3 -> 2 -> 1 from 2.52s to 3.54s
        if (t < 2.52) {
          if (num) num.textContent = "4";
        } else if (t < 2.78) {
          if (num) num.textContent = "4";
        } else if (t < 3.03) {
          if (num) num.textContent = "3";
        } else if (t < 3.28) {
          if (num) num.textContent = "2";
        } else if (t < 3.54) {
          if (num) num.textContent = "1";
        }

        if (t < 3.54) {
          if (box) {
            box.style.opacity = "1";
            box.style.transform = "scale(1.0)";
          }
          if (giantWrap) giantWrap.style.opacity = "0";
        } else {
          if (box) {
            box.style.opacity = "0";
            box.style.transform = "scale(0.7)";
          }
          if (giantWrap) giantWrap.style.opacity = "1";

          // Claque monumentale du 0 à 3.54s avec rebond easeOutBack (scale 2.1 -> 1.0)
          const slamElapsed = t - 3.54;
          const slamP = Math.min(1, slamElapsed / 0.28);
          const c1 = 1.70158;
          const c3 = c1 + 1;
          const easeBack = 1 + c3 * Math.pow(slamP - 1, 3) + c1 * Math.pow(slamP - 1, 2);
          const scale = 2.1 - 1.1 * easeBack;
          if (giantDigit) {
            giantDigit.style.transform = `scale(${Math.max(1.0, scale)})`;
          }

          // Onde de choc circulaire
          if (shockwave) {
            const waveP = Math.min(1, slamElapsed / 0.40);
            const waveScale = 0.2 + 2.0 * waveP;
            const waveOpacity = Math.max(0, 1 - waveP);
            shockwave.style.transform = `scale(${waveScale})`;
            shockwave.style.opacity = String(waveOpacity);
          }

          // Badge "VIDÉO PUBLIÉE" qui claque à t = 4.10s
          if (slamBadge) {
            if (t >= 4.10) {
              const bElapsed = t - 4.10;
              const bP = Math.min(1, bElapsed / 0.22);
              const bScale = 1.8 - 0.8 * (1 + c3 * Math.pow(bP - 1, 3) + c1 * Math.pow(bP - 1, 2));
              slamBadge.style.opacity = "1";
              slamBadge.style.transform = `scale(${Math.max(1.0, bScale)})`;
            } else {
              slamBadge.style.opacity = "0";
            }
          }
        }
      } else if (type === "shooting_wall_illustrations") {
        const c0 = document.getElementById("sw-card-0");
        const c1 = document.getElementById("sw-card-1");
        const c2 = document.getElementById("sw-card-2");
        const recBadge = document.getElementById("sw-badge-rec");

        // Carte 1: Caméra à 9.48s (rotate -1.5deg)
        if (c0) {
          if (t >= 9.48) {
            c0.classList.add("active");
            const p0 = Math.min(1, (t - 9.48) / 0.22);
            const sc0 = 0.92 + 0.10 * p0 + (p0 < 1 ? 0.08 * Math.sin(p0 * Math.PI) : 0);
            c0.style.transform = `scale(${sc0}) rotate(-1.5deg)`;
          } else {
            c0.classList.remove("active");
            c0.style.transform = "scale(0.92) rotate(-1.5deg)";
          }
        }
        // Carte 2: Lumière Softbox à 10.52s (rotate 1.5deg)
        if (c1) {
          if (t >= 10.52) {
            c1.classList.add("active");
            const p1 = Math.min(1, (t - 10.52) / 0.22);
            const sc1 = 0.92 + 0.10 * p1 + (p1 < 1 ? 0.08 * Math.sin(p1 * Math.PI) : 0);
            c1.style.transform = `scale(${sc1}) rotate(1.5deg)`;
          } else {
            c1.classList.remove("active");
            c1.style.transform = "scale(0.92) rotate(1.5deg)";
          }
        }
        // Carte 3: Timeline 4h de montage à 11.34s (rotate -1.5deg)
        if (c2) {
          if (t >= 11.34) {
            c2.classList.add("active");
            const p2 = Math.min(1, (t - 11.34) / 0.22);
            const sc2 = 0.92 + 0.10 * p2 + (p2 < 1 ? 0.08 * Math.sin(p2 * Math.PI) : 0);
            c2.style.transform = `scale(${sc2}) rotate(-1.5deg)`;
          } else {
            c2.classList.remove("active");
            c2.style.transform = "scale(0.92) rotate(-1.5deg)";
          }
        }
        if (recBadge && t >= 9.48) {
          const blink = Math.floor((t - 9.48) * 3) % 2 === 0;
          recBadge.style.opacity = blink ? "1" : "0.5";
        }
      } else if (type === "real_clone_feed_skip" || type === "b2b_robot_clone_crash") {
        const topBanner = document.getElementById("rcf-top-banner");
        const stage = document.getElementById("rcf-stage");
        const postSingle = document.getElementById("rcf-post-single");
        const cloneRow = document.getElementById("rcf-clone-row");
        const auditCard = document.getElementById("rcf-audit-card");
        const gaugeFill = document.getElementById("rcf-gauge-fill");
        const gaugePercent = document.getElementById("rcf-gauge-percent");
        const stopwatch = document.getElementById("rcf-stopwatch-num");
        const stamp = document.getElementById("rcf-final-stamp");

        // Phase 1 (16.76 - 18.54): Post unique IA
        // Phase 2 (18.54 - 19.78): Dédoublement en 3 clones identiques
        // Phase 3 (19.78 - 22.06): Swipe-up post ignoré + Audit crédibilité chute 0%
        if (t < 18.54) {
          if (topBanner) topBanner.classList.remove("active");
          if (stage) stage.classList.remove("swipe-up");
          if (postSingle) postSingle.style.display = "flex";
          if (cloneRow) cloneRow.style.display = "none";
          if (auditCard) auditCard.classList.remove("active");
        } else if (t < 19.78) {
          if (topBanner) topBanner.classList.add("active");
          if (stage) stage.classList.remove("swipe-up");
          if (postSingle) postSingle.style.display = "none";
          if (cloneRow) cloneRow.style.display = "flex";
          if (auditCard) auditCard.classList.remove("active");

          const pClone = Math.min(1, (t - 18.54) / 0.22);
          if (cloneRow) {
            cloneRow.style.transform = `scale(${0.9 + 0.1 * pClone})`;
          }
        } else {
          // Phase 3 : Swipe up & audit card
          if (topBanner) topBanner.classList.remove("active");
          if (stage) stage.classList.add("swipe-up");
          if (auditCard) auditCard.classList.add("active");

          // Effondrement de la jauge 100% -> 0% de 19.78s à 20.60s
          const gaugeP = Math.min(1, Math.max(0, (t - 19.78) / 0.82));
          const currentPct = Math.round(100 * (1 - gaugeP));
          if (gaugeFill) gaugeFill.style.width = `${currentPct}%`;
          if (gaugePercent) gaugePercent.textContent = `${currentPct}%`;

          // Compteur chronomètre 00:01s -> 00:02s -> 00:03s entre 20.94 et 21.66
          if (t < 21.18) {
            if (stopwatch) stopwatch.textContent = "00:01s";
          } else if (t < 21.42) {
            if (stopwatch) stopwatch.textContent = "00:02s";
          } else {
            if (stopwatch) stopwatch.textContent = "00:03s";
          }

          // Tampon final SWIPE EN 3 SECONDES qui claque à 21.66s
          if (stamp) {
            if (t >= 21.66) {
              const sElapsed = t - 21.66;
              const sP = Math.min(1, sElapsed / 0.18);
              const sScale = 2.0 - 1.0 * sP;
              stamp.style.opacity = "1";
              stamp.style.transform = `rotate(-3deg) scale(${Math.max(1.0, sScale)})`;
            } else {
              stamp.style.opacity = "0";
            }
          }
        }
      } else if (type === "overflowing_text_posts" || type === "locked_post_wall") {
        const scrollContent = document.getElementById("otp-scroll-content");
        if (scrollContent) {
          const sStart = (scene && scene.start !== undefined) ? scene.start : 24.02;
          const sDur = (scene && scene.duration) ? scene.duration : 3.38;
          const pScroll = Math.min(1, Math.max(0, (t - sStart) / sDur));
          const ty = -140 * pScroll;
          scrollContent.style.transform = `translateY(${ty}px)`;
        }
        const stamp = document.getElementById("otp-stamp");
        if (stamp) {
          const sElapsed = (typeof elapsed === "number") ? elapsed : Math.max(0, t - 24.02);
          if (sElapsed >= 0.15) {
            const p = Math.min(1, (sElapsed - 0.15) / 0.22);
            const scale = p < 1 ? 1.0 + 1.2 * Math.cos(p * Math.PI * 0.5) * (1 - p) : 1.0;
            stamp.style.opacity = "1";
            stamp.style.transform = `translate(-50%, -50%) rotate(-6deg) scale(${scale.toFixed(3)})`;
          } else {
            stamp.style.opacity = "0";
            stamp.style.transform = `translate(-50%, -50%) rotate(-6deg) scale(2.2)`;
          }
        }
      } else if (type === "social_logos_carousel_rtl") {
        // Défilement 1 à 1 Droite -> Gauche
        // Timestamps exacts:
        // t < 55.45 : LinkedIn au centre
        // 55.45 <= t < 55.75 : easeOutBack de 0 vers 1
        // 55.75 <= t < 56.25 : TikTok verrouillé plein centre
        // 56.25 <= t < 56.45 : easeOutBack de 1 vers 2
        // 56.45 <= t < 56.78 : Reels verrouillé plein centre
        // 56.78 <= t < 56.95 : easeOutBack de 2 vers 3
        // t >= 56.95 : Shorts verrouillé plein centre
        const easeOutBackNorm = (p) => {
          const c1 = 1.70158;
          const c3 = c1 + 1;
          return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2);
        };

        let slidePos = 0;
        if (t < 55.45) {
          slidePos = 0;
        } else if (t < 55.75) {
          const p = (t - 55.45) / (55.75 - 55.45);
          slidePos = Math.max(0, easeOutBackNorm(Math.min(1, p)));
        } else if (t < 56.25) {
          slidePos = 1;
        } else if (t < 56.45) {
          const p = (t - 56.25) / (56.45 - 56.25);
          slidePos = 1 + Math.max(0, easeOutBackNorm(Math.min(1, p)));
        } else if (t < 56.78) {
          slidePos = 2;
        } else if (t < 56.95) {
          const p = (t - 56.78) / (56.95 - 56.78);
          slidePos = 2 + Math.max(0, easeOutBackNorm(Math.min(1, p)));
        } else {
          slidePos = 3;
        }

        for (let i = 0; i < 4; i++) {
          const cardEl = document.getElementById(`slc-card-${i}`);
          if (!cardEl) continue;
          const diff = i - slidePos;
          const offsetX = diff * 700;
          const scale = 1 - Math.min(0.25, Math.abs(diff) * 0.22);
          const opacity = Math.max(0.2, 1 - Math.abs(diff) * 0.65);
          cardEl.style.transform = `translate3d(calc(-50% + ${offsetX}px), -50%, 0) scale(${scale})`;
          cardEl.style.opacity = String(opacity);
          if (Math.abs(diff) < 0.35) {
            cardEl.classList.add("active");
          } else {
            cardEl.classList.remove("active");
          }
        }
      }
    }

  // Initialisation à l'évaluation du script
  initData();
})();
