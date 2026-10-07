"""
Synthesize ElevenLabs narrator audio for all B-Roll scenes in a project script.json.

Usage:
  python tools/synthesize_broll.py --project path/to/project

Requires ELEVENLABS_API_KEY in .env
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

import requests

from env_util import get, require


def duration(path: Path) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(path),
    ]
    info = json.loads(subprocess.run(cmd, capture_output=True, check=True).stdout)
    return float(info["format"]["duration"])


def synthesize_one(text: str, out_mp3: Path, api_key: str, voice_id: str, model_id: str) -> None:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {"stability": 0.50, "similarity_boost": 0.80},
    }
    res = requests.post(url, json=payload, headers=headers, timeout=120)
    if res.status_code != 200:
        raise RuntimeError(f"ElevenLabs error {res.status_code}: {res.text[:400]}")
    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    out_mp3.write_bytes(res.content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Project directory with script.json")
    parser.add_argument("--tail", type=float, default=0.8, help="Hold after narrator ends")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    script_path = root / "script.json"
    script = json.loads(script_path.read_text(encoding="utf-8"))
    broll = [s for s in script["scenes"] if s.get("kind") == "broll"]

    api_key = require("ELEVENLABS_API_KEY")
    voice_id = get("ELEVENLABS_VOICE_ID", "gFl0NeqphJUaoBLtWrqM")
    model_id = get("ELEVENLABS_MODEL_ID", "eleven_v3")

    measured: dict = {}
    print(f"Synthesizing {len(broll)} B-Roll scenes with voice {voice_id} / {model_id}")

    for scene in broll:
        sid = scene["id"]
        text = scene["tts"]
        out_mp3 = root / scene.get("audio", f"audio/{sid}.mp3")
        meta = out_mp3.with_suffix(".tts.json")

        if out_mp3.exists() and meta.exists():
            print(f"[{sid}] exists, measuring…")
        else:
            print(f"[{sid}] synthesizing…")
            synthesize_one(text, out_mp3, api_key, voice_id, model_id)
            meta.write_text(
                json.dumps({"id": sid, "text": text, "model": model_id}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            time.sleep(1.0)

        dur = duration(out_mp3)
        measured[sid] = {
            "id": sid,
            "title": scene.get("title", sid),
            "audioFile": str(out_mp3),
            "duration": round(dur, 3),
            "sceneDuration": round(dur + args.tail, 3),
        }
        print(f"[{sid}] audio={dur:.2f}s scene={dur + args.tail:.2f}s")

    out = root / "audio" / "measured.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(measured, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(m["sceneDuration"] for m in measured.values())
    print(f"\nB-Roll total: {total:.2f}s ({total / 60:.2f} min) → {out}")


if __name__ == "__main__":
    main()
