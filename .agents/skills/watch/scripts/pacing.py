#!/usr/bin/env python3
"""
ANALYSEUR DE PACING & RYTHME — AGENT404 / WATCH ENRICHED
========================================================
Calcule les métriques de rétention d'une vidéo courte : cadence des cuts,
débit vocal en mots par minute (WPM), changements de plan et découpage
en scènes candidates pour Blueprint.
"""

from __future__ import annotations
from typing import Any
from pathlib import Path


def analyze_pacing(
    duration: float,
    frames: list[Path] | list[str],
    words: list[dict[str, Any]]
) -> dict[str, Any]:
    """
    Calcule l'ensemble des métriques de rythme et structure.
    """
    duration = max(0.1, round(float(duration), 2))
    cut_count = len(frames)
    word_count = len(words)

    # 1. Débit vocal WPM
    wpm = round((word_count / (duration / 60))) if duration > 3 else 0

    # 2. Rythme moyen par plan (Secondes par cut)
    seconds_per_cut = round(duration / max(1, cut_count), 2) if cut_count > 0 else duration

    # 3. Qualification du rythme
    if seconds_per_cut <= 1.5:
        pacing_level = "Ultra-Dynamique (Pattern Interrupts permanents)"
        retention_diagnosis = "Excellent pour TikTok et Reels grand public. Rétention maximale < 3s."
    elif seconds_per_cut <= 2.5:
        pacing_level = "Dynamique B2B (Standard Haute Rétention Agent404)"
        retention_diagnosis = "Équilibre idéal entre clarté du message d'autorité et stimulation visuelle continue."
    elif seconds_per_cut <= 4.0:
        pacing_level = "Modéré / Storytelling"
        retention_diagnosis = "Adapté aux récits personnels ou démonstrations techniques posées."
    else:
        pacing_level = "Lent / Monologue"
        retention_diagnosis = "Risque élevé de décrochage sur mobile sans pattern interrupts fréquents."

    # 4. Découpage en blocs de scènes candidats (clusters temporels)
    scenes = []
    if cut_count > 0:
        step = max(1, cut_count // min(6, max(3, int(duration // 8))))
        for i in range(0, cut_count, step):
            t_start = round(i * seconds_per_cut, 1)
            t_end = min(duration, round((i + step) * seconds_per_cut, 1))
            
            # Mots dans cette tranche
            scene_words = [w["word"] for w in words if t_start <= w.get("start", 0.0) <= t_end]
            preview_text = " ".join(scene_words[:7]) + ("..." if len(scene_words) > 7 else "")
            
            frame_ref = str(frames[i].name) if hasattr(frames[i], "name") else str(frames[i])
            scenes.append({
                "scene_index": len(scenes) + 1,
                "start": t_start,
                "end": t_end,
                "duration": round(t_end - t_start, 1),
                "frame_preview": frame_ref,
                "dialogue_snippet": preview_text or "[Action visuelle]"
            })

    return {
        "duration_seconds": duration,
        "cuts_count": cut_count,
        "seconds_per_cut": seconds_per_cut,
        "word_count": word_count,
        "words_per_minute": wpm,
        "pacing_level": pacing_level,
        "retention_diagnosis": retention_diagnosis,
        "estimated_scenes_count": len(scenes),
        "scenes_breakdown": scenes
    }
