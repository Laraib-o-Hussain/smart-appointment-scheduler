from __future__ import annotations

import logging

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from .base_page import BasePage

logger = logging.getLogger(__name__)


class AppointmentPage(BasePage):
    DOCTOR_STEP = (By.ID, "step-doctor")
    APPOINTMENT_STEP = (By.ID, "step-appointment")
    DATE_SELECT = (By.ID, "appointment-date")
    FIRST_SLOT = (By.CSS_SELECTOR, "#time-slots .slot-btn")
    FIRST_DOCTOR_BTN = (By.CSS_SELECTOR, "#doctor-list .select-doctor-btn")
    CONFIRM_BTN = (By.ID, "confirm-booking-btn")
    DOCTOR_LABEL = (By.ID, "booking-doctor-label")

    def select_doctor_by_name(self, doctor_name: str) -> str:
        logger.info("picking doctor: %s", doctor_name)
        self.visible(self.DOCTOR_STEP)

        locator = (
            By.XPATH,
            f"//ul[@id='doctor-list']//li[contains(., '{doctor_name}')]"
            "//button[contains(@class, 'select-doctor-btn')]",
        )

        try:
            self.click(locator)
        except TimeoutException:
            # name mismatch / typo in .env — just grab the first one
            logger.warning("%s not found, using first doctor instead", doctor_name)
            self.click(self.FIRST_DOCTOR_BTN)

        self.visible(self.APPOINTMENT_STEP)
        label = self.text_of(self.DOCTOR_LABEL)
        logger.info("doctor set: %s", label)
        return label

    def select_first_available_date(self) -> str:
        select = Select(self.visible(self.DATE_SELECT))
        if not select.options:
            raise NoSuchElementException("no dates in dropdown")
        select.select_by_index(0)
        selected = select.first_selected_option.text.strip()
        logger.info("date: %s", selected)
        return selected

    def select_first_time_slot(self) -> str:
        self.wait.until(EC.element_to_be_clickable(self.FIRST_SLOT))
        slot = self.find(self.FIRST_SLOT)
        text = slot.text.strip()
        slot.click()
        # confirm stays disabled until a slot is picked
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BTN))
        logger.info("time: %s", text)
        return text

    def confirm_appointment(self) -> None:
        logger.info("confirming booking")
        self.click(self.CONFIRM_BTN)
