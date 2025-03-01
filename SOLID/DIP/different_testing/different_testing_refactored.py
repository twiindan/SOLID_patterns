# Now we depend on abstractions instead of concrete implementations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By


# Domain Models
# Reusable data structure that isn't tied to any specific implementation
@dataclass
class LoginCredentials:
    username: str
    password: str


# GOOD: Abstract interfaces
# This defines a contract that any UI driver must fulfill
# High-level modules now depend on this abstraction, not concrete implementations
class UIDriver(ABC):
    @abstractmethod
    def navigate_to(self, url: str) -> None:
        # Navigate to a specific URL
        pass

    @abstractmethod
    def input_text(self, locator: tuple, text: str) -> None:
        # Input text into a UI element
        pass

    @abstractmethod
    def click(self, locator: tuple) -> None:
        # Click on a UI element
        pass

    @abstractmethod
    def get_text(self, locator: tuple) -> str:
        # Get text from a UI element
        pass

    @abstractmethod
    def get_title(self, locator: tuple) -> str:
        # Get text from a UI element
        pass

    @abstractmethod
    def quit(self) -> None:
        # Clean up resources
        pass


# GOOD: Concrete implementations
# This implements the abstract interface
# We can have multiple implementations (Chrome, Firefox, Mock, etc.)
class ChromeDriver(UIDriver):
    def __init__(self):
        # Initializes the concrete Selenium Chrome driver
        self.driver = webdriver.Chrome()

    def navigate_to(self, url: str) -> None:
        # Implementation specific to Chrome
        self.driver.get(url)

    def input_text(self, locator: tuple, text: str) -> None:
        # Implementation specific to Chrome
        self.driver.find_element(*locator).send_keys(text)

    def click(self, locator: tuple) -> None:
        # Implementation specific to Chrome
        self.driver.find_element(*locator).click()

    def get_text(self, locator: tuple) -> str:
        # Implementation specific to Chrome
        return self.driver.find_element(*locator).text

    def get_title(self) -> str:
        # Implementation specific to Chrome
        return self.driver.title

    def quit(self) -> None:
        # Implementation specific to Chrome
        self.driver.quit()


# GOOD: Test class now depends on abstractions
# The test doesn't know or care which specific driver is used
class LoginTest:
    def __init__(self, ui_driver: UIDriver):
        # Dependency injection - the concrete implementation is passed in
        # This allows for easy swapping of implementations (e.g., for testing)
        self.ui_driver = ui_driver
        self.base_url = "https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net/"

    def test_login_ui(self):
        # UI test implementation using abstraction
        # The test only uses methods defined in the UIDriver interface
        # It doesn't know or care about the specific implementation
        self.ui_driver.navigate_to(f"{self.base_url}/login")
        self.ui_driver.input_text((By.ID, "username"), "testing")
        self.ui_driver.input_text((By.ID, "password"), "testing")
        self.ui_driver.click((By.ID, "submit"))

        # Assert login success
        # Note: There's an issue here - ui_driver doesn't have a 'title' attribute in the interface
        # This should be fixed to use a method from the UIDriver interface
        assert "Home - Microblog" in self.ui_driver.get_title()

    def teardown(self):
        # Cleanup uses the abstraction, not specific implementation details
        self.ui_driver.quit()


# GOOD: Usage example with proper dependency injection
def run_tests():
    # Initialize concrete implementations
    # We could easily swap this with a different implementation
    chrome_driver = ChromeDriver()

    # Create test instance with dependencies injected
    # This is a form of Dependency Injection, a related pattern
    login_test = LoginTest(chrome_driver)

    # Run tests with proper error handling
    try:
        login_test.test_login_ui()
    finally:
        # Ensure cleanup happens even if tests fail
        login_test.teardown()
