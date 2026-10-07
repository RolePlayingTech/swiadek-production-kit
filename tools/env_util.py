"""Load local .env without committing secrets."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]


def load_env() -> Path:
    env_path = ROOT / ".env"
    load_dotenv(env_path)
    return env_path


def require(name: str) -> str:
    load_env()
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env var: {name}. Copy .env.example to .env.")
    return value


def get(name: str, default: str = "") -> str:
    load_env()
    return os.getenv(name, default).strip() or default
