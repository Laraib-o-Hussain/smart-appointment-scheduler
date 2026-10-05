from __future__ import annotations

import logging
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base_page import BasePage

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AppointmentDetails:
    appointment_id: str
    patient_name: str
    doctor: str
    date: str
    time: str


class ConfirmationPage(BasePage):
    SECTION = (By.ID, "confirmation-section")
    APPOINTMENT_ID = (By.ID, "confirm-appointment-id")
    PATIENT_NAME = (By.ID, "confirm-patient-name")
    DOCTOR = (By.ID, "confirm-doctor")
    DATE = (By.ID, "confirm-date")
    TIME = (By.ID, "confirm-time")

    def wait_for_confirmation(self) -> None:
        self.visible(self.SECTION)
        self.visible(self.APPOINTMENT_ID)

    def get_details(self) -> AppointmentDetails:
        details = AppointmentDetails(
            appointment_id=self.text_of(self.APPOINTMENT_ID),
            patient_name=self.text_of(self.PATIENT_NAME),
            doctor=self.text_of(self.DOCTOR),
            date=self.text_of(self.DATE),
            time=self.text_of(self.TIME),
        )

        if not details.appointment_id or details.appointment_id == "—":
            raise ValueError("confirmation page has no appointment id")

        logger.info(
            "booked %s | %s | %s | %s %s",
            details.appointment_id,
            details.patient_name,
            details.doctor,
            details.date,
            details.time,
        )
        return details
