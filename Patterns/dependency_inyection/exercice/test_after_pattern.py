# After applying Dependency Injection
# This approach is more flexible, testable and maintainable
from abc import ABC, abstractmethod

import requests
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.common.by import By


class WebDriver(ABC):
    @abstractmethod
    def navigate_to(self, url):
        pass

    @abstractmethod
    def find_and_input(self, locator, value):
        pass

    @abstractmethod
    def click(self, locator):
        pass

    @abstractmethod
    def quit(self):
        pass


class ApiClient(ABC):
    @abstractmethod
    def login_user(self, username, password):
        pass


class ChromeWebDriver(WebDriver):
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
    def __init__(self, base_url):
        self.base_url = base_url

    def login_user(self, username, password):
        return requests.post(f'{self.base_url}/tokens', auth=HTTPBasicAuth('testing', 'testing'))


class UserTest:
    def __init__(self, web_driver: WebDriver, api_client: ApiClient):
        # Dependencies are injected through constructor
        self.web_driver = web_driver
        self.api_client = api_client

    def test_user_registration(self):
        # Frontend test using abstracted web driver
        self.web_driver.navigate_to("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")
        self.web_driver.find_and_input("username", "testing")
        self.web_driver.find_and_input("password", "testing")
        self.web_driver.click("submit")

        # Backend verification using abstracted API client
        response = self.api_client.login_user("testing", "testing")
        assert response.status_code == 200

    def teardown(self):
        self.web_driver.quit()


# Usage example
def run_tests():
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
