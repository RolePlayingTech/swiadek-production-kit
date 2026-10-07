"""Quality gates for A-Roll clips: ffprobe, inspection frames, Whisper audit."""
from __future__ import annotations

import json
import os
import subprocess

import cv2
import whisper

_WHISPER_MODEL = None


def get_whisper(model_name: str = "medium"):
    global _WHISPER_MODEL
    if _WHISPER_MODEL is None:
        print(f"[QA] Loading Whisper model ({model_name})...")
        _WHISPER_MODEL = whisper.load_model(model_name)
    return _WHISPER_MODEL


def check_video_params(video_path: str) -> dict:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "stream=width,height,r_frame_rate,codec_type,codec_name:format=duration",
        "-of",
        "json",
        video_path,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = json.loads(res.stdout)

    duration = float(info.get("format", {}).get("duration", 0))
    streams = info.get("streams", [])
    v_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    a_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    width = v_stream.get("width") if v_stream else None
    height = v_stream.get("height") if v_stream else None
    has_audio = a_stream is not None

    print(
        f"[QA ffprobe] {os.path.basename(video_path)} | "
        f"{width}x{height} | dur: {duration:.2f}s | audio: {has_audio}"
    )
    return {
        "duration": duration,
        "width": width,
        "height": height,
        "has_audio": has_audio,
        "valid_16x9": (width, height) in {(1280, 720), (1920, 1080)},
        "valid_duration": 9.5 <= duration <= 10.5,
    }


def extract_qa_frames(
    video_path: str,
    output_dir: str,
    timestamps=(1.0, 5.0, 8.5),
) -> list[str]:
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    extracted: list[str] = []
    base_name = os.path.splitext(os.path.basename(video_path))[0]

    for t in timestamps:
        frame_idx = int(t * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = cap.read()
        if ok:
            out_name = f"{base_name}_frame_{int(t)}s.jpg"
            out_path = os.path.join(output_dir, out_name)
            cv2.imwrite(out_path, frame)
            extracted.append(out_path)
            print(f"[QA Frame] t={t:.1f}s -> {out_name}")
    cap.release()
    return extracted


def audit_whisper(
    video_path: str,
    expected_keywords: list[str] | None = None,
    max_speech_end: float = 9.6,
    model_name: str = "medium",
) -> dict:
    model = get_whisper(model_name)
    print(f"[QA Whisper] Transcribing {os.path.basename(video_path)}...")
    res = model.transcribe(video_path, fp16=False, language="pl", word_timestamps=True)

    full_text = res.get("text", "").strip()
    segments = res.get("segments", [])

    last_end = 0.0
    if segments:
        last_seg = segments[-1]
        words = last_seg.get("words", [])
        if words:
            last_end = words[-1].get("end", last_seg.get("end", 0.0))
        else:
            last_end = last_seg.get("end", 0.0)

    print(f"[QA Whisper] \"{full_text}\"")
    print(f"[QA Whisper] Speech ends at {last_end:.2f}s (limit < {max_speech_end:.2f}s)")

    found_keywords: list[str] = []
    missing_keywords: list[str] = []
    lower_text = full_text.lower()
    if expected_keywords:
        for kw in expected_keywords:
            if kw.lower() in lower_text:
                found_keywords.append(kw)
            else:
                missing_keywords.append(kw)

    passed = (last_end <= max_speech_end) and (len(missing_keywords) <= 1)
    return {
        "full_text": full_text,
        "last_end": last_end,
        "segments": segments,
        "found_keywords": found_keywords,
        "missing_keywords": missing_keywords,
        "passed": passed,
    }
