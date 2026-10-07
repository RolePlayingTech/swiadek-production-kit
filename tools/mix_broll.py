"""
Mix B-Roll video ambient with ElevenLabs narrator.

Rules encoded here:
- Narrator is the first amix input (duration=first) so speech is never truncated
  by a shorter ambient bed.
- Ambient stays quiet (~8%).
- For multi-shot sequences, concat video first, then call this tool once.

Usage:
  python tools/mix_broll.py --video shot.mp4 --voice s02.mp3 --out scene.mp4
  python tools/mix_broll.py --video shot.mp4 --voice s02.mp3 --out scene.mp4 --tail 0.8
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def probe_duration(path: Path) -> float:
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


def mix(video: Path, voice: Path, out: Path, ambient_vol: float = 0.08, tail: float = 0.8) -> None:
    voice_dur = probe_duration(voice)
    total = voice_dur + tail
    # Lektor first — never cut speech to ambient length.
    filter_complex = (
        f"[0:a]volume={ambient_vol},aresample=48000,"
        f"aformat=sample_fmts=fltp:channel_layouts=stereo,apad=whole_dur={total:.3f}[ambient];"
        "[1:a]loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000,"
        "aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"apad=whole_dur={total:.3f}[lektor];"
        "[lektor][ambient]amix=inputs=2:duration=first:weights=1 1:normalize=0[aout]"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video),
        "-i",
        str(voice),
        "-filter_complex",
        filter_complex,
        "-map",
        "0:v:0",
        "-map",
        "[aout]",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-t",
        f"{total:.3f}",
        str(out),
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True)
    print(f"Wrote {out} (t={total:.3f}s)")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True)
    p.add_argument("--voice", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--ambient", type=float, default=0.08)
    p.add_argument("--tail", type=float, default=0.8)
    args = p.parse_args()
    mix(Path(args.video), Path(args.voice), Path(args.out), args.ambient, args.tail)


if __name__ == "__main__":
    main()
