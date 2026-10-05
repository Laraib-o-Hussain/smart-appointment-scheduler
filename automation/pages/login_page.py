from __future__ import annotations

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-btn")
    DASHBOARD = (By.ID, "dashboard-section")
    LOGIN_SECTION = (By.ID, "login-section")

    def __init__(self, driver: WebDriver, base_url: str, timeout: float = 10) -> None:
        super().__init__(driver, timeout)
        self.base_url = base_url.rstrip("/")

    def open(self) -> None:
        logger.info("opening %s", self.base_url)
        self.driver.get(self.base_url)
        self.visible(self.LOGIN_SECTION)

    def login(self, username: str, password: str) -> None:
        logger.info("logging in as %s", username)
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        self.visible(self.DASHBOARD)
        logger.info("login ok")
