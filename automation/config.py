from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    base_url: str
    username: str
    password: str
    browser: str
    headless: bool
    implicit_wait_seconds: float
    explicit_wait_seconds: float
    patient_query: str
    doctor_name: str


def get_settings() -> Settings:
    username = os.getenv("DEMO_USERNAME", "").strip()
    password = os.getenv("DEMO_PASSWORD", "").strip()

    if not username or not password:
        raise ValueError(
            "Missing DEMO_USERNAME / DEMO_PASSWORD. Copy .env.example to .env first."
        )

    return Settings(
        base_url=os.getenv("BASE_URL", "http://localhost:5500").rstrip("/"),
        username=username,
        password=password,
        browser=os.getenv("BROWSER", "chrome").strip().lower(),
        headless=_as_bool(os.getenv("HEADLESS"), default=False),
        implicit_wait_seconds=float(os.getenv("IMPLICIT_WAIT_SECONDS", "0")),
        explicit_wait_seconds=float(os.getenv("EXPLICIT_WAIT_SECONDS", "10")),
        patient_query=os.getenv("PATIENT_QUERY", "Ava Chen").strip(),
        doctor_name=os.getenv("DOCTOR_NAME", "Dr. Sofia Rivera").strip(),
    )
