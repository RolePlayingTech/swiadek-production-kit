"""
Helpers for attaching Playwright to an already running Chrome CDP session.
"""
from __future__ import annotations

import time

import requests
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from env_util import get, load_env

load_env()


def cdp_url() -> str:
    return get("CDP_URL", "http://127.0.0.1:9222")


def wait_for_cdp(timeout_s: float = 5.0) -> None:
    deadline = time.time() + timeout_s
    url = cdp_url().rstrip("/") + "/json/version"
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                return
        except Exception:
            time.sleep(0.4)
    raise RuntimeError(
        f"Chrome CDP not reachable at {cdp_url()}. Start tools/keep_chrome.py first."
    )


def connect(playwright: Playwright) -> Browser:
    wait_for_cdp()
    return playwright.chromium.connect_over_cdp(cdp_url())


def first_page(browser: Browser) -> Page:
    if not browser.contexts:
        raise RuntimeError("No browser contexts on CDP session.")
    pages = browser.contexts[0].pages
    if not pages:
        raise RuntimeError("No open pages in Chrome context.")
    for page in pages:
        if "flow.google" in page.url or "labs.google" in page.url:
            return page
    return pages[0]


def with_flow_page():
    """Context-manager style helper for short scripts."""
    wait_for_cdp()
    pw = sync_playwright().start()
    browser = connect(pw)
    page = first_page(browser)
    return pw, browser, page
