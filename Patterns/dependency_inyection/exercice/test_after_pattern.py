# After applying Dependency Injection
# This approach is more flexible, testable and maintainable
from abc import ABC, abstractmethod

import requests
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.common.by import By


class WebDriver(ABC):
    """
    Abstract interface for web drivers.

    DEPENDENCY INJECTION PATTERN:
    - Defines a contract that any web driver implementation must follow
    - Allows for different browser implementations or mocks for testing
    - Abstracts away the specific web driver implementation details
    """

    @abstractmethod
    def navigate_to(self, url):
        """Navigate to a specific URL."""
        pass

    @abstractmethod
    def find_and_input(self, locator, value):
        """Find an element by ID and input a value."""
        pass

    @abstractmethod
    def click(self, locator):
        """Find an element by ID and click it."""
        pass

    @abstractmethod
    def quit(self):
        """Close the browser and quit the driver."""
        pass


class ApiClient(ABC):
    """
    Abstract interface for API clients.

    DEPENDENCY INJECTION PATTERN:
    - Defines a contract that any API client implementation must follow
    - Allows for different implementations or mocks for testing
    - Abstracts away the specific HTTP client details
    """

    @abstractmethod
    def login_user(self, username, password):
        """Login a user with credentials and return the response."""
        pass


class ChromeWebDriver(WebDriver):
    """
    Concrete implementation of WebDriver using Chrome.

    - Implements the WebDriver interface for Chrome browser
    - Can be replaced with Firefox, Edge, or mock implementations
    """

    def __init__(self):
        self.driver = webdriver.Chrome()

    def navigate_to(self, url):
        self.driver.get(url)

    def find_and_input(self, locator, value):
        self.driver.find_element(By.ID, locator).send_keys(value)

    def click(self, locator):
        self.driver.find_element(By.ID, locator).click()

    def quit(self):
        self.driver.quit()


class RequestsApiClient(ApiClient):
    """
    Concrete implementation of ApiClient using the requests library.

    - Implements the ApiClient interface
    - Can be replaced with other HTTP clients or mock implementations
    - Configuration is injected via constructor (base_url)
    """

    def __init__(self, base_url):
        # Configuration is injected, not hardcoded
        self.base_url = base_url

    def login_user(self, username, password):
        return requests.post(f'{self.base_url}/tokens', auth=HTTPBasicAuth('testing', 'testing'))


class UserTest:
    """
    Test class that uses dependency injection.

    DEPENDENCY INJECTION PATTERN:
    - Dependencies are injected through constructor
    - Class depends on abstractions, not concrete implementations
    - Makes the class more flexible, testable, and maintainable
    """

    def __init__(self, web_driver: WebDriver, api_client: ApiClient):
        # Dependencies are injected through constructor
        # Note the use of type hints with abstract interfaces
        self.web_driver = web_driver
        self.api_client = api_client

    def test_user_registration(self):
        """
        Test user registration using injected dependencies.

        - Uses abstractions (web_driver, api_client) instead of direct implementation
        - No direct dependencies on Selenium or requests
        """
        # Frontend test using abstracted web driver
        self.web_driver.navigate_to("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")
        self.web_driver.find_and_input("username", "testing")
        self.web_driver.find_and_input("password", "testing")
        self.web_driver.click("submit")

        # Backend verification using abstracted API client
        response = self.api_client.login_user("testing", "testing")
        assert response.status_code == 200

    def teardown(self):
        """Clean up resources after tests."""
        self.web_driver.quit()


# Usage example
def run_tests():
    """
    Example of running tests with dependency injection.

    - Creates concrete implementations
    - Injects them into the test class
    - This setup can be easily changed for different environments or testing
    """
    # Create concrete implementations
    web_driver = ChromeWebDriver()
    api_client = RequestsApiClient("https://microblog-api.azurewebsites.net/api")

    # Inject dependencies
    test = UserTest(web_driver, api_client)

    try:
        test.test_user_registration()
    finally:
        test.teardown()


run_tests()
