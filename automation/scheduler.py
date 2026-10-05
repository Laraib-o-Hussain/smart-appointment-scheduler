"""
Books a fake appointment on the local demo site.

Usage (site must already be running):
    python -m automation.scheduler
"""

from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from automation.config import Settings, get_settings
from automation.pages import (
    AppointmentPage,
    ConfirmationPage,
    LoginPage,
    PatientPage,
)

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("scheduler")


def create_driver(settings: Settings) -> WebDriver:
    browser = settings.browser
    logger.info("browser=%s headless=%s", browser, settings.headless)

    if browser == "chrome":
        options = ChromeOptions()
        if settings.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,900")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )
    elif browser == "edge":
        options = EdgeOptions()
        if settings.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,900")
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options,
        )
    else:
        raise ValueError(f"BROWSER must be chrome or edge, got {browser!r}")

    driver.implicitly_wait(settings.implicit_wait_seconds)
    return driver


def run_scheduler(settings: Settings | None = None) -> dict[str, str]:
    settings = settings or get_settings()
    timeout = settings.explicit_wait_seconds
    driver = create_driver(settings)

    try:
        login = LoginPage(driver, settings.base_url, timeout)
        patients = PatientPage(driver, timeout)
        booking = AppointmentPage(driver, timeout)
        confirm = ConfirmationPage(driver, timeout)

        login.open()
        login.login(settings.username, settings.password)

        patients.search_patient(settings.patient_query)
        patients.select_first_result()

        booking.select_doctor_by_name(settings.doctor_name)
        booking.select_first_available_date()
        booking.select_first_time_slot()
        booking.confirm_appointment()

        confirm.wait_for_confirmation()
        details = confirm.get_details()

        print()
        print("Appointment booked")
        print(f"  id:      {details.appointment_id}")
        print(f"  patient: {details.patient_name}")
        print(f"  doctor:  {details.doctor}")
        print(f"  when:    {details.date} @ {details.time}")
        print()

        return {
            "appointment_id": details.appointment_id,
            "patient_name": details.patient_name,
            "doctor": details.doctor,
            "date": details.date,
            "time": details.time,
        }

    except TimeoutException:
        logger.exception(
            "timed out — is the demo site up at %s ?", settings.base_url
        )
        raise
    except WebDriverException:
        logger.exception("webdriver blew up")
        raise
    finally:
        driver.quit()


def main() -> int:
    try:
        run_scheduler()
        return 0
    except ValueError as exc:
        logger.error("%s", exc)
        return 2
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
