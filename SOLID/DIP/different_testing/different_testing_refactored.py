# Now we depend on abstractions instead of concrete implementations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


# Domain Models
@dataclass
class LoginCredentials:
    username: str
    password: str


# Abstract interfaces
class UIDriver(ABC):
    @abstractmethod
    def navigate_to(self, url: str) -> None:
        pass

    @abstractmethod
    def input_text(self, locator: tuple, text: str) -> None:
        pass

    @abstractmethod
    def click(self, locator: tuple) -> None:
        pass

    @abstractmethod
    def get_text(self, locator: tuple) -> str:
        pass

    @abstractmethod
    def quit(self) -> None:
        pass


# Concrete implementations
class ChromeDriver(UIDriver):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def navigate_to(self, url: str) -> None:
        self.driver.get(url)

    def input_text(self, locator: tuple, text: str) -> None:
        self.driver.find_element(*locator).send_keys(text)

    def click(self, locator: tuple) -> None:
        self.driver.find_element(*locator).click()

    def get_text(self, locator: tuple) -> str:
        return self.driver.find_element(*locator).text

    def quit(self) -> None:
        self.driver.quit()


# Test class now depends on abstractions
class LoginTest:
    def __init__(self, ui_driver: UIDriver):
        self.ui_driver = ui_driver
        self.base_url = "https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net/"

    def test_login_ui(self):
        # UI test implementation using abstraction
        self.ui_driver.navigate_to(f"{self.base_url}/login")
        self.ui_driver.input_text((By.ID, "username"), "testing")
        self.ui_driver.input_text((By.ID, "password"), "testing")
        self.ui_driver.click((By.ID, "submit"))

        # Assert login success
        assert "Home - Microblog" in self.ui_driver.title

    def teardown(self):
        self.ui_driver.quit()


# Usage example
def run_tests():
    # Initialize concrete implementations
    chrome_driver = ChromeDriver()

    # Create test instance with dependencies
    login_test = LoginTest(chrome_driver)

    # Run tests
    try:
        login_test.test_login_ui()
    finally:
        login_test.teardown()
