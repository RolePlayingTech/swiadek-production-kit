"""
Start Google Chrome with remote debugging for Google Flow automation.

Does not log in for you — use a Chrome profile that is already signed into
Flow / Google Labs with a valid subscription.

Usage:
  python tools/keep_chrome.py
"""
from __future__ import annotations

import os
import subprocess
import sys

from env_util import get, load_env

load_env()

CHROME_PATH = get(
    "CHROME_PATH",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
)
USER_DATA = get("CHROME_USER_DATA") or os.path.expandvars(
    r"%LOCALAPPDATA%\Google\Chrome\User Data"
)
PROFILE = get("CHROME_PROFILE", "Profile 60")
FLOW_URL = get("FLOW_URL", "https://flow.google.com/")
PORT = get("CDP_URL", "http://127.0.0.1:9222").rsplit(":", 1)[-1].rstrip("/")


def main() -> None:
    if not os.path.isfile(CHROME_PATH):
        print(f"Chrome not found at: {CHROME_PATH}", file=sys.stderr)
        sys.exit(1)

    cmd = [
        CHROME_PATH,
        f"--remote-debugging-port={PORT}",
        f"--user-data-dir={USER_DATA}",
        f"--profile-directory={PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
        FLOW_URL,
    ]
    print("Starting Chrome daemon for Flow CDP...")
    print(f"  profile={PROFILE}")
    print(f"  port={PORT}")
    print(f"  url={FLOW_URL}")
    proc = subprocess.Popen(cmd)
    print(f"Chrome running with PID {proc.pid}")
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("Exiting.")


if __name__ == "__main__":
    main()
