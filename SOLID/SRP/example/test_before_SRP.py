import requests
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.common.by import By


# VIOLATION OF SRP: This class is handling multiple responsibilities:
# 1. Setting up and managing the WebDriver
# 2. Handling UI interactions
# 3. Making API calls
# 4. Performing test assertions
class TestLoginPage:
    def __init__(self):
        # WebDriver setup mixed with application URL configuration
        self.driver = webdriver.Chrome()
        self.base_url = "https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net"
        self.api_url = "https://microblog-api.azurewebsites.net/api"

    def test_incorrect_login_flow(self):
        # VIOLATION OF SRP: This method mixes several responsibilities:
        # 1. UI navigation
        # 2. Element interaction
        # 3. UI validation
        # 4. API interactions
        # 5. API validation

        # UI interaction logic mixed with test logic
        self.driver.get(self.base_url)
        self.driver.find_element(By.ID, "username").send_keys("user@example.com")
        self.driver.find_element(By.ID, "password").send_keys("password123")
        self.driver.find_element(By.ID, "submit").click()

        # UI Validation mixed with test assertions
        welcome_message = self.driver.find_element(By.CSS_SELECTOR, ".alert.alert-info")
        assert welcome_message.text == "Invalid username or password"

        # API testing logic mixed in the same method
        # This violates SRP because UI and API testing are different responsibilities
        session = requests.Session()
        response = session.post(
            f"{self.api_url}/tokens",
            auth=HTTPBasicAuth('user', 'password'),
        )
        assert response.status_code == 401


# VIOLATION OF SRP: Test initialization and execution are mixed
# No proper test lifecycle management (setup and teardown)
test_login_page = TestLoginPage()
test_login_page.test_incorrect_login_flow()


"""
Without SRP:

TestLoginPage class handles multiple responsibilities: WebDriver management, UI interactions, API calls, and test assertions
All test logic is mixed in a single method
No clear separation between UI and API testing concerns
No proper test lifecycle management (setup/teardown)
Hard-coded element locators mixed with test logic
Difficult to maintain or extend
"""