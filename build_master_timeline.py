import os
import sys
import re
import json
import wave
import shutil
import subprocess
import argparse
import unicodedata
from pathlib import Path

# Ajout dynamique du répertoire bin local du dépôt au PATH si présent
REPO_ROOT = Path(__file__).parent.resolve()
_local_bin = str(REPO_ROOT / "bin")
_path_elements = os.environ.get("PATH", "").split(os.pathsep) if os.environ.get("PATH") else []
if _local_bin not in _path_elements and Path(_local_bin).is_dir():
    _path_elements.insert(0, _local_bin)
os.environ["PATH"] = os.pathsep.join(_path_elements)


def load_project(project_path_str: str):
    """Charge et valide la configuration project.json d'un projet de studio."""
    target_path = Path(project_path_str)
    if target_path.is_file() and target_path.suffix == ".json":
        project_file = target_path.resolve()
        project_dir = project_file.parent
    else:
        project_dir = target_path.resolve()
        project_file = project_dir / "project.json"

    if not project_file.exists():
        raise FileNotFoundError(
            f"Fichier de configuration du projet introuvable : '{project_file}'. Champ fautif : 'project.json'."
        )

    with open(project_file, "r", encoding="utf-8") as f:
        try:
            project_data = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Fichier project.json syntaxiquement invalide : {exc}. Champ fautif : 'project.json'.")

    required_keys = [
        "video_number",
        "title",
        "audio_path",
        "reference_words",
        "scenes",
        "scene_end_words",
        "phonetic_map"
    ]
    for key in required_keys:
        if key not in project_data:
            raise ValueError(f"Champ obligatoire manquant dans {project_file} : '{key}'.")

    reference_words = project_data["reference_words"]
    if not isinstance(reference_words, list) or len(reference_words) == 0:
        raise ValueError(
            f"Liste des mots de référence invalide ou vide dans {project_file}. Champ fautif : 'reference_words'."
        )

    scenes = project_data["scenes"]
    if not isinstance(scenes, list) or len(scenes) == 0:
        raise ValueError(
            f"Liste des scènes invalide ou vide dans {project_file}. Champ fautif : 'scenes'."
        )

    scene_end_words = project_data["scene_end_words"]
    if not isinstance(scene_end_words, list) or len(scene_end_words) != len(scenes):
        raise ValueError(
            f"Le nombre de scènes ({len(scenes)}) ne correspond pas au nombre de mots terminaux ({len(scene_end_words)}). Champ fautif : 'scene_end_words'."
        )

    # Résolution et vérification de la présence de la source audio
    raw_audio_path = Path(project_data["audio_path"])
    if raw_audio_path.is_absolute():
        if not raw_audio_path.exists():
            raise FileNotFoundError(
                f"Fichier audio absolu introuvable : '{raw_audio_path}'. Champ fautif : 'audio_path'."
            )
        resolved_audio = raw_audio_path
    else:
        candidate_project = (project_dir / raw_audio_path).resolve()
        candidate_root = (REPO_ROOT / raw_audio_path).resolve()
        if candidate_project.exists():
            resolved_audio = candidate_project
        elif candidate_root.exists():
            resolved_audio = candidate_root
        else:
            raise FileNotFoundError(
                f"Fichier audio introuvable : '{raw_audio_path}' (vérifié dans {project_dir} et {REPO_ROOT}). Champ fautif : 'audio_path'."
            )
    project_data["_resolved_audio"] = resolved_audio

    # Vérification des fichiers référencés dans les données de scènes (notamment les avatars)
    for idx, sc in enumerate(scenes):
        sc_data = sc.get("data", {})
        avatar_path_str = sc_data.get("avatar")
        if avatar_path_str:
            av_p = Path(avatar_path_str)
            if not av_p.is_absolute():
                cand_root = REPO_ROOT / av_p
                cand_proj = project_dir / av_p
                if not cand_root.exists() and not cand_proj.exists():
                    raise FileNotFoundError(
                        f"Fichier avatar introuvable pour la scène {idx + 1} : '{avatar_path_str}'. Champ fautif : 'scenes[{idx}].data.avatar'."
                    )

    return project_dir, project_data


def get_audio_duration(audio_file_path: Path) -> float:
    """Calcule la durée précise en secondes d'un fichier audio via wave ou ffprobe."""
    if audio_file_path.suffix.lower() == ".wav":
        try:
            with wave.open(str(audio_file_path), "rb") as wf:
                sr = wf.getframerate()
                nframes = wf.getnframes()
                return nframes / float(sr)
        except Exception:
            pass

    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())


def validate_timeline(words, scenes, total_audio_dur, reference_words, scene_end_words):
    """
    Validation automatique rigoureuse de la timeline :
    1. Couverture stricte de la transcription (aucun mot inventé ou omis).
    2. Timestamps strictement chronologiques et start < end pour chaque mot.
    3. Bornes temporelles contenues dans la durée réelle audio.
    4. Exactitude du nombre de scènes dans le bon ordre chronologique.
    5. Chaque mot terminal de scène correspond exactement au repère textuel.
    6. Continuité parfaite des scènes : aucun trou, aucun chevauchement.
    7. Durée finale cohérente avec l'audio réel.
    """
    print("\n--- [CONTRÔLES AUTOMATIQUES DE VALIDATION TEMPORELLE] ---")

    # 1. Vérification du nombre et contenu des mots
    if len(words) != len(reference_words):
        raise ValueError(
            f"ÉCHEC VALIDATION : Nombre de mots ({len(words)}) différent de la référence ({len(reference_words)}). Champ fautif : 'words'."
        )
    for idx, (w, ref_w) in enumerate(zip(words, reference_words)):
        if w["word"] != ref_w:
            raise ValueError(
                f"ÉCHEC VALIDATION : Mot {idx} '{w['word']}' ne correspond pas à la référence '{ref_w}'. Champ fautif : 'words[{idx}]'."
            )
        s = float(w["start"])
        e = float(w["end"])
        if s >= e:
            raise ValueError(
                f"ÉCHEC VALIDATION : Mot {idx} '{w['word']}' invalide (start {s:.3f} >= end {e:.3f}). Champ fautif : 'words[{idx}]'."
            )
        if s < 0.0 or e > total_audio_dur + 0.15:
            raise ValueError(
                f"ÉCHEC VALIDATION : Mot {idx} '{w['word']}' [{s:.3f}s -> {e:.3f}s] hors bornes audio [0, {total_audio_dur:.3f}s]. Champ fautif : 'words[{idx}]'."
            )
        if idx > 0:
            prev_s = float(words[idx - 1]["start"])
            if s < prev_s:
                raise ValueError(
                    f"ÉCHEC VALIDATION : Décalage non-chronologique mot {idx} '{w['word']}' (start {s:.3f} < {prev_s:.3f}). Champ fautif : 'words[{idx}]'."
                )

    print(f"✓ {len(words)} mots validés : ordre strictement chronologique, bornés [0.0s, {total_audio_dur:.2f}s].")

    # 2. Vérification des scènes
    if len(scenes) != len(scene_end_words):
        raise ValueError(
            f"ÉCHEC VALIDATION : {len(scenes)} scènes trouvées au lieu des {len(scene_end_words)} attendues. Champ fautif : 'scenes'."
        )

    for i, sc in enumerate(scenes):
        sc_s = float(sc["start"])
        sc_e = float(sc["end"])
        if sc_s >= sc_e:
            raise ValueError(
                f"ÉCHEC VALIDATION : Scène {sc['id']} durée invalide [{sc_s:.3f}s -> {sc_e:.3f}s]. Champ fautif : 'scenes[{i}]'."
            )
        if i == 0:
            if sc_s != 0.0:
                raise ValueError(
                    f"ÉCHEC VALIDATION : La scène 1 doit débuter à 0.0s (trouvé: {sc_s}s). Champ fautif : 'scenes[0].start'."
                )
        else:
            prev_e = float(scenes[i - 1]["end"])
            if abs(sc_s - prev_e) > 0.001:
                raise ValueError(
                    f"ÉCHEC VALIDATION : Rupture de continuité entre scène {i} ({prev_e:.3f}s) et scène {i+1} ({sc_s:.3f}s). Champ fautif : 'scenes[{i}].start'."
                )

    final_sc_end = float(scenes[-1]["end"])
    if abs(final_sc_end - total_audio_dur) > 0.1:
        raise ValueError(
            f"ÉCHEC VALIDATION : Fin de la timeline ({final_sc_end:.3f}s) divergente de la durée audio ({total_audio_dur:.3f}s). Champ fautif : 'scenes[-1].end'."
        )

    print(f"✓ {len(scenes)} scènes validées sans aucun trou ni chevauchement (durée totale : {final_sc_end:.3f}s).")

    # 3. Rapport de diagnostic lisible
    print(f"\n--- [RAPPORT DE DIAGNOSTIC DE SYNCHRONISATION DES {len(scenes)} SCÈNES] ---")
    print(f"{'Scène':<10} | {'Début':<8} | {'Fin':<8} | {'Durée':<7} | {'Mot Terminal':<18} | {'Type':<14} | {'Décor'}")
    print("-" * 88)
    for i, sc in enumerate(scenes):
        sc_s = float(sc["start"])
        sc_e = float(sc["end"])
        dur = sc_e - sc_s
        end_w = scene_end_words[i]
        sc_type = sc["type"]
        sc_bg = sc["data"].get("bg", "default")
        print(f"{sc['id']:<10} | {sc_s:6.3f}s  | {sc_e:6.3f}s  | {dur:5.2f}s  | {end_w:<18} | {sc_type:<14} | {sc_bg}")
    print("-" * 88 + "\n")


def step3_build_timeline(words, scenes_configs, scene_end_words, reference_words, total_audio_dur, timeline_path="timeline.js"):
    num_scenes = len(scenes_configs)
    print(f"[Timeline] Génération des {num_scenes} scènes synchronisées dans {timeline_path}...")

    # Découpage strict et garanti des tranches de mots pour chaque scène
    scene_slices = []
    cur_idx = 0
    for i, end_w in enumerate(scene_end_words):
        start_idx = cur_idx
        while cur_idx < len(words) and words[cur_idx]["word"] != end_w:
            cur_idx += 1
        if cur_idx >= len(words):
            raise ValueError(
                f"ERREUR : Mot terminal '{end_w}' introuvable pour la scène {i + 1}. Champ fautif : 'scene_end_words[{i}]'."
            )
        end_idx = cur_idx
        cur_idx += 1
        scene_slices.append((start_idx, end_idx))

    # Construction des scènes avec synchronisation exacte sur l'amorce du discours
    scenes = []
    for i in range(num_scenes):
        cfg = scenes_configs[i]
        s_idx, e_idx = scene_slices[i]

        # La scène débute exactement au premier mot prononcé de son sujet
        if i == 0:
            sc_start = 0.0
        else:
            sc_start = words[s_idx]["start"]

        # La scène se termine exactement à l'amorce du sujet suivant (ou fin de fichier)
        if i == num_scenes - 1:
            sc_end = max(words[-1]["end"], round(total_audio_dur, 3))
        else:
            next_s_idx = scene_slices[i + 1][0]
            sc_end = words[next_s_idx]["start"]

        scenes.append({
            "id": f"scene_{i + 1:02d}",
            "type": cfg["type"],
            "start": round(sc_start, 3),
            "end": round(sc_end, 3),
            "data": cfg["data"]
        })

    # Contrôles automatiques obligatoires avant écriture
    validate_timeline(words, scenes, total_audio_dur, reference_words, scene_end_words)

    # Export JS
    js_content = f"// TIMELINE VIDÉO PROGRAMMATIQUE SUR-MESURE ({num_scenes} SCÈNES)\n"
    js_content += f"// Généré automatiquement par build_master_timeline.py\n\n"
    js_content += f"window.WORDS = {json.dumps(words, indent=2, ensure_ascii=False)};\n\n"
    js_content += f"window.SCENES = {json.dumps(scenes, indent=2, ensure_ascii=False)};\n"

    with open(timeline_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"✓ {num_scenes} scènes validées et exportées dans {timeline_path}.")
    return scenes


def align_reference_audio(audio_source_path: Path, reference_words: list, phonetic_map: dict, special_cases: dict, output_words_json: Path, output_voix_wav: Path):
    """
    Alignement forcé déterministe et vérifié du texte de référence
    sur la voix off exacte, sans fabrication ni interpolation artificielle.
    """
    if not audio_source_path.exists():
        raise FileNotFoundError(
            f"ERREUR CRITIQUE : La source audio '{audio_source_path}' est introuvable. "
            "Le pipeline refuse de basculer silencieusement vers un ancien audio. Champ fautif : 'audio_path'."
        )

    if not output_voix_wav.exists() or audio_source_path.stat().st_mtime > output_voix_wav.stat().st_mtime:
        print(f"[Audio Reference] Conversion technique en PCM WAV : {output_voix_wav}...")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(audio_source_path),
            "-c:a", "pcm_s16le",
            "-ar", "44100",
            "-ac", "1",
            str(output_voix_wav)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    total_dur = get_audio_duration(output_voix_wav)

    print(f"[Audio Reference] Alignement acoustique forcé sur {output_voix_wav} ({total_dur:.2f}s)...")
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
    segments, _ = model.transcribe(str(output_voix_wav), word_timestamps=True, language="fr", temperature=0.0)

    raw_words = []
    for s in segments:
        for w in s.words:
            clean = w.word.strip()
            if clean:
                raw_words.append({
                    "word": clean,
                    "start": round(w.start, 3),
                    "end": round(w.end, 3)
                })

    def strip_accents(text):
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

    def norm(s):
        s = strip_accents(s.lower())
        s = s.replace('œ', 'oe').replace('æ', 'ae')
        return re.sub(r'[^a-z0-9]', '', s)

    aligned_words = []
    r_idx = 0
    w_idx = 0
    n_ref = len(reference_words)
    n_raw = len(raw_words)
    handle_zero_euro = special_cases.get("zero_euro_split", False)

    while r_idx < n_ref and w_idx < n_raw:
        rw = reference_words[r_idx]
        ww = raw_words[w_idx]["word"]
        r_n = norm(rw)
        w_n = norm(ww)

        # 1. Ignorer les bruits purs / soupirs de respiration hors texte
        if w_n == '' or w_n in ['ah', 'euh']:
            w_idx += 1
            continue

        # 2. Cas spécifique des devises combinées : '0€.' dans Whisper pour ['0', 'euro.']
        if handle_zero_euro and rw == '0' and r_idx + 1 < n_ref and 'euro' in reference_words[r_idx + 1].lower() and '€' in ww:
            t_s = float(raw_words[w_idx]["start"])
            t_e = float(raw_words[w_idx]["end"])
            mid = round((t_s + t_e) / 2.0, 3)
            aligned_words.append({"word": reference_words[r_idx], "start": t_s, "end": mid})
            aligned_words.append({"word": reference_words[r_idx + 1], "start": mid, "end": t_e})
            r_idx += 2
            w_idx += 1
            continue

        # 3. Correspondance directe ou phonétique validée
        if r_n == w_n or phonetic_map.get(r_n) == w_n:
            aligned_words.append({
                "word": rw,
                "start": float(raw_words[w_idx]["start"]),
                "end": float(raw_words[w_idx]["end"])
            })
            r_idx += 1
            w_idx += 1
            continue

        # 4. Mots composés / contractions découpées par Whisper (ex: l'ai, j'ai, c'est, envoie-moi)
        if r_n.startswith(w_n):
            start_t = float(raw_words[w_idx]["start"])
            end_t = float(raw_words[w_idx]["end"])
            accum = w_n
            w_next = w_idx + 1
            while w_next < n_raw and len(accum) < len(r_n):
                next_norm = norm(raw_words[w_next]["word"])
                if next_norm == '':
                    end_t = max(end_t, float(raw_words[w_next]["end"]))
                    w_next += 1
                    continue
                accum += next_norm
                end_t = float(raw_words[w_next]["end"])
                w_next += 1

            if accum == r_n:
                aligned_words.append({
                    "word": rw,
                    "start": start_t,
                    "end": end_t
                })
                r_idx += 1
                w_idx = w_next
                continue

        # En cas de divergence non résolue, arrêt immédiat sans fabrication de timestamps
        context_ref = reference_words[max(0, r_idx - 2):min(n_ref, r_idx + 3)]
        context_raw = [rw_item["word"] for rw_item in raw_words[max(0, w_idx - 2):min(n_raw, w_idx + 3)]]
        raise RuntimeError(
            f"ERREUR D'ALIGNEMENT ACOUSTIQUE : divergence stricte détectée à l'index {r_idx}.\n"
            f"  Mot référence attendu : '{rw}' (norm: '{r_n}')\n"
            f"  Token Whisper détecté : '{ww}' (norm: '{w_n}')\n"
            f"  Contexte référence   : {context_ref}\n"
            f"  Contexte Whisper     : {context_raw}\n"
            "Arrêt immédiat : le pipeline refuse d'inventer des timestamps."
        )

    # Règle absolue : aucun mot manquant n'est toléré
    if len(aligned_words) != n_ref:
        raise RuntimeError(
            f"ERREUR D'ALIGNEMENT ACOUSTIQUE : {len(aligned_words)}/{n_ref} mots alignés. "
            "Tous les mots de référence doivent correspondre à l'audio réel."
        )

    # Sauvegarde de words.json
    with open(output_words_json, "w", encoding="utf-8") as f:
        json.dump(aligned_words, f, indent=2, ensure_ascii=False)

    print(f"✓ Alignement forcé 100% réussi : {len(aligned_words)}/{n_ref} mots synchronisés dans {output_words_json}.")
    return aligned_words, total_dur


def run_pipeline(project_path_str: str, force_realign: bool = False):
    """Exécute l'orchestration complète de génération de timeline pour un projet donné."""
    project_dir, project_data = load_project(project_path_str)
    audio_source = project_data["_resolved_audio"]
    ref_words = project_data["reference_words"]
    scenes_configs = project_data["scenes"]
    scene_end_words = project_data["scene_end_words"]
    phonetic_map = project_data.get("phonetic_map", {})
    special_cases = project_data.get("special_cases", {})

    output_words_json = project_dir / "words.json"
    output_voix_wav = project_dir / "voix.wav"
    output_timeline_js = project_dir / "timeline.js"

    # Vérification de la nécessité d'un réalignement acoustique Whisper
    should_align = False
    if force_realign:
        should_align = True
    elif not output_words_json.exists():
        should_align = True
    elif audio_source.stat().st_mtime > output_words_json.stat().st_mtime:
        should_align = True

    if should_align:
        print(f"[Pipeline] Alignement Whisper requis pour {project_dir.name}...")
        words, total_dur = align_reference_audio(
            audio_source_path=audio_source,
            reference_words=ref_words,
            phonetic_map=phonetic_map,
            special_cases=special_cases,
            output_words_json=output_words_json,
            output_voix_wav=output_voix_wav
        )
    else:
        print(f"[Pipeline] Alignement existant réutilisé ({output_words_json}).")
        with open(output_words_json, "r", encoding="utf-8") as f:
            words = json.load(f)

        # Garantir l'existence de voix.wav si non présent
        if not output_voix_wav.exists() or audio_source.stat().st_mtime > output_voix_wav.stat().st_mtime:
            print(f"[Pipeline] Génération de {output_voix_wav} depuis {audio_source.name}...")
            cmd = [
                "ffmpeg", "-y",
                "-i", str(audio_source),
                "-c:a", "pcm_s16le",
                "-ar", "44100",
                "-ac", "1",
                str(output_voix_wav)
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        total_dur = get_audio_duration(output_voix_wav)

    step3_build_timeline(
        words=words,
        scenes_configs=scenes_configs,
        scene_end_words=scene_end_words,
        reference_words=ref_words,
        total_audio_dur=total_dur,
        timeline_path=str(output_timeline_js)
    )

    print(f"✓ Pipeline timeline terminé avec succès pour {project_dir.name} ({total_dur:.2f}s).")
    return words, total_dur


def main():
    parser = argparse.ArgumentParser(description="Générateur de timeline vidéo programmatique AGENT404.")
    parser.add_argument(
        "--projet", "-p",
        default="studio_perso/video_01",
        help="Chemin vers le dossier du projet ou vers project.json (défaut: studio_perso/video_01)"
    )
    parser.add_argument(
        "--realigner",
        action="store_true",
        help="Force le réalignement acoustique via faster-whisper même si words.json est à jour"
    )
    args = parser.parse_args()

    run_pipeline(args.projet, force_realign=args.realigner)


if __name__ == "__main__":
    main()
