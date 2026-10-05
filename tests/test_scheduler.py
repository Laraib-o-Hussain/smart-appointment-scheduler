"""Basic checks. Full booking test expects the demo site on :5500."""

from __future__ import annotations

import pytest

from automation.config import get_settings
from automation.scheduler import run_scheduler


def test_settings_load_from_env():
    settings = get_settings()
    assert settings.base_url.startswith("http")
    assert settings.username
    assert settings.password


def test_missing_credentials_raise(monkeypatch):
    monkeypatch.setenv("DEMO_USERNAME", "")
    monkeypatch.setenv("DEMO_PASSWORD", "")

    with pytest.raises(ValueError, match="DEMO_USERNAME"):
        get_settings()


@pytest.mark.integration
def test_full_booking_flow():
    result = run_scheduler()
    assert result["appointment_id"].startswith("APT-")
    assert result["patient_name"]
    assert result["doctor"]
    assert result["date"]
    assert result["time"]
