from __future__ import annotations

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage

logger = logging.getLogger(__name__)


class PatientPage(BasePage):
    SEARCH_INPUT = (By.ID, "patient-search")
    SEARCH_BTN = (By.ID, "patient-search-btn")
    FIRST_RESULT_BTN = (By.CSS_SELECTOR, "#patient-results .select-patient-btn")
    DOCTOR_STEP = (By.ID, "step-doctor")
    SELECTED_LABEL = (By.ID, "selected-patient-label")

    def search_patient(self, query: str) -> None:
        logger.info("searching patient: %s", query)
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BTN)
        self.wait.until(EC.element_to_be_clickable(self.FIRST_RESULT_BTN))

    def select_first_result(self) -> str:
        self.click(self.FIRST_RESULT_BTN)
        self.visible(self.DOCTOR_STEP)
        label = self.text_of(self.SELECTED_LABEL)
        logger.info("picked patient: %s", label)
        return label
