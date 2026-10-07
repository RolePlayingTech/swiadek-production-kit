"""
Produce one A-Roll scene in Google Flow from project script.json.

Prerequisites:
  1. Chrome running via tools/keep_chrome.py (already signed into Flow)
  2. Project open in Flow with anchors uploaded
  3. Settings: Video / Frames / Omni 1.1 Flash / 10s / 16:9

Usage:
  python tools/generate_aroll_scene.py --project path/to/project --scene s01
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import zipfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from playwright.sync_api import sync_playwright

from flow_connect import connect, first_page
from qa_utils import audit_whisper, check_video_params, extract_qa_frames


def produce_scene(project: Path, scene_id: str) -> dict:
    script = json.loads((project / "script.json").read_text(encoding="utf-8"))
    scene = next((s for s in script["scenes"] if s["id"] == scene_id), None)
    if not scene:
        raise SystemExit(f"Scene {scene_id} not found in script.json")
    if scene.get("kind") != "aroll":
        raise SystemExit(f"Scene {scene_id} is not aroll (got {scene.get('kind')})")

    prompt_text = scene["prompt"]
    keywords = scene.get("keywords", [])
    anchor_fname = Path(scene["anchor"]).name
    anchor_stem = Path(anchor_fname).stem

    raw_dir = project / "raw"
    qc_dir = project / "qc"
    raw_dir.mkdir(parents=True, exist_ok=True)
    qc_dir.mkdir(parents=True, exist_ok=True)
    raw_video_path = project / scene.get("raw", f"raw/{scene_id}.mp4")

    print(f"Producing {scene_id}: {scene.get('speaker')}")
    print(f"Anchor: {anchor_fname}")
    print(f'Dialog: "{scene.get("dialog")}"')

    with sync_playwright() as p:
        browser = connect(p)
        page = first_page(browser)

        done_btn = page.locator("button:has-text('Done')").first
        if done_btn.is_visible():
            done_btn.click(force=True)
            time.sleep(1)
        page.keyboard.press("Escape")
        time.sleep(1)

        settings_trigger = page.locator("button[aria-label='Settings trigger']").first
        if settings_trigger.is_visible():
            st_text = settings_trigger.inner_text().replace("\n", " ")
            if "10s" not in st_text:
                settings_trigger.click(force=True)
                time.sleep(1)
                btn_10s = page.locator("button:has-text('10s')").first
                if btn_10s.is_visible():
                    btn_10s.click(force=True)
                    time.sleep(0.5)
                page.keyboard.press("Escape")
                time.sleep(1)

        for cc in page.locator("button[aria-label*='Remove'], button[aria-label*='close']").all():
            try:
                if cc.is_visible():
                    cc.click(force=True)
                    time.sleep(0.4)
            except Exception:
                pass

        start_btn = page.locator("button:has-text('Start')").first
        if start_btn.is_visible():
            start_btn.click(force=True)
            time.sleep(1.5)
            search_input = page.locator("input[placeholder*='Search']").first
            if search_input.is_visible():
                search_input.click(force=True)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(anchor_stem, delay=20)
                time.sleep(1.5)
            item = page.locator(
                f"div:has-text('{anchor_fname}'), button:has-text('{anchor_stem}')"
            ).first
            if item.is_visible():
                item.click(force=True)
                time.sleep(1)
            add_btn = page.locator("button:has-text('Add to prompt')").first
            if add_btn.is_visible():
                add_btn.click(force=True)
                time.sleep(1.5)
            else:
                page.keyboard.press("Escape")
                time.sleep(1)

        prompt_div = page.locator("div[contenteditable='true']").first
        prompt_div.click(force=True)
        time.sleep(0.4)
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        time.sleep(0.4)
        page.keyboard.type(prompt_text, delay=10)
        time.sleep(1)

        submit_btn = page.locator("button:has-text('arrow_forward')").first
        submit_btn.click(force=True)
        time.sleep(5)
        page.screenshot(path=str(qc_dir / f"{scene_id}_submitted.png"))

        print("Waiting ~85s for Omni render…")
        for remaining in range(85, 0, -15):
            print(f"  … {remaining}s")
            time.sleep(15)

        page.keyboard.press("Escape")
        time.sleep(2)
        page.keyboard.press("Home")
        time.sleep(1)
        imgs = page.locator("img").all()
        if len(imgs) > 1:
            imgs[1].click(force=True)
        elif imgs:
            imgs[0].click(force=True)
        time.sleep(3)

        body_text = page.locator("body").inner_text().lower()
        if "generation might violate" in body_text or "failed" in body_text:
            page.screenshot(path=str(qc_dir / f"{scene_id}_failed.png"))
            raise RuntimeError(f"Generation failed for {scene_id}")

        dl_menu = page.locator(
            "button[aria-label='Download media'], button[aria-label*='Download'], "
            "button:has-text('download')"
        ).first
        if dl_menu.is_visible():
            dl_menu.click(force=True)
            time.sleep(1)

        btn_720p = page.locator("button:has-text('720p')").first
        if not btn_720p.is_visible():
            page.screenshot(path=str(qc_dir / f"{scene_id}_no_720p.png"))
            raise RuntimeError(f"No 720p download for {scene_id}")

        temp_dl = raw_dir / f"{scene_id}_download.tmp"
        if temp_dl.exists():
            temp_dl.unlink()
        with page.expect_download(timeout=45000) as dl_info:
            btn_720p.click(force=True)
        dl_info.value.save_as(str(temp_dl))

        with open(temp_dl, "rb") as f:
            magic = f.read(4)
        if magic == b"PK\x03\x04":
            with zipfile.ZipFile(temp_dl, "r") as z:
                mp4s = [n for n in z.namelist() if n.lower().endswith(".mp4")]
                if not mp4s:
                    raise RuntimeError("ZIP without MP4")
                extracted = Path(z.extract(mp4s[0], raw_dir))
                if raw_video_path.exists():
                    raw_video_path.unlink()
                extracted.replace(raw_video_path)
            temp_dl.unlink()
        else:
            if raw_video_path.exists():
                raw_video_path.unlink()
            temp_dl.replace(raw_video_path)

        done_btn = page.locator("button:has-text('Done')").first
        if done_btn.is_visible():
            done_btn.click(force=True)
        page.keyboard.press("Escape")

    v_params = check_video_params(str(raw_video_path))
    frames = extract_qa_frames(str(raw_video_path), str(qc_dir))
    w_audit = audit_whisper(str(raw_video_path), expected_keywords=keywords, max_speech_end=9.5)
    report = {
        "scene_id": scene_id,
        "video_path": str(raw_video_path),
        "video_params": v_params,
        "qa_frames": frames,
        "whisper_audit": {
            "full_text": w_audit["full_text"],
            "last_end": w_audit["last_end"],
            "found_keywords": w_audit["found_keywords"],
            "missing_keywords": w_audit["missing_keywords"],
            "passed": w_audit["passed"],
        },
        "overall_status": (
            "APPROVED"
            if v_params["valid_duration"] and w_audit["passed"]
            else "REQUIRES_REVIEW"
        ),
    }
    report_path = qc_dir / f"{scene_id}_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"QC: {report['overall_status']} → {report_path}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--scene", required=True)
    args = parser.parse_args()
    produce_scene(Path(args.project).resolve(), args.scene.lower())


if __name__ == "__main__":
    main()
