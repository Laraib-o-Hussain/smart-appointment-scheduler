from __future__ import annotations

import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class BasePage:
    """Tiny helpers so page objects don't repeat wait boilerplate."""

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator: tuple[str, str]) -> WebElement:
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException as exc:
            logger.error("couldn't find %s", locator)
            raise TimeoutException(f"Element not found: {locator}") from exc

    def click(self, locator: tuple[str, str]) -> None:
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except TimeoutException as exc:
            logger.error("couldn't click %s", locator)
            raise TimeoutException(f"Element not clickable: {locator}") from exc

    def type_text(self, locator: tuple[str, str], text: str, clear: bool = True) -> None:
        el = self.find(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def visible(self, locator: tuple[str, str]) -> WebElement:
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException as exc:
            logger.error("not visible: %s", locator)
            raise TimeoutException(f"Element not visible: {locator}") from exc

    def text_of(self, locator: tuple[str, str]) -> str:
        return self.visible(locator).text.strip()
