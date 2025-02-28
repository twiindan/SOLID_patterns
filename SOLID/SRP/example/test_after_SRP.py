import requests
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.common.by import By


# APPLYING SRP: This class has a single responsibility - managing UI interactions with the login page
# It doesn't know about testing, assertions, or API interactions
class LoginPage:
    def __init__(self, driver):
        # Only concerned with the UI elements and their locators
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "submit")
        self.welcome_text = (By.CSS_SELECTOR, ".alert.alert-info")

    # Individual methods for each UI interaction, following the Page Object Model pattern
    def enter_username(self, username):
        self.driver.find_element(*self.username_input).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def get_welcome_message(self):
        return self.driver.find_element(*self.welcome_text).text


# APPLYING SRP: This class has a single responsibility - handling API interactions
# It doesn't know anything about UI or testing
class LoginAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    # Encapsulates the API call logic
    def login(self, username, password):
        return self.session.post(
            f"{self.base_url}/tokens",
            auth=HTTPBasicAuth(username, password),
        )


# APPLYING SRP: This class is solely responsible for testing
# It uses the specialized classes above rather than implementing their functionality
class TestLogin:
    # Proper test lifecycle management with setup method
    def setup_method(self):
        # Initialize dependencies
        self.driver = webdriver.Chrome()
        # Dependency injection: Using the specialized classes
        self.login_page = LoginPage(self.driver)
        self.login_api = LoginAPI("https://microblog-api.azurewebsites.net/api")

    def test_login_flow(self):
        # UI Test is now clearly separated
        self.driver.get("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")
        # Delegating UI interactions to the LoginPage class
        self.login_page.enter_username("user@example.com")
        self.login_page.enter_password("password123")
        self.login_page.click_login()
        # Test only performs assertions, not UI interactions
        assert self.login_page.get_welcome_message() == "Invalid username or password"

        # API Test is now clearly separated
        # Delegating API interaction to the LoginAPI class
        response = self.login_api.login("user@example.com", "password123")
        assert response.status_code == 401

    # Proper test lifecycle management with teardown method
    def teardown_method(self):
        # Clean up resources
        self.driver.quit()


"""
With SRP:

Responsibilities are split across specialized classes:

LoginPage: Handles only UI interactions (Page Object Model pattern)
LoginAPI: Manages only API interactions
TestLogin: Handles only test execution and assertions


Clear separation of concerns makes the code more maintainable
Proper test lifecycle management with setup and teardown methods
Element locators are encapsulated in the LoginPage class
Each class has a single, focused responsibility
More reusable components - the same LoginPage and LoginAPI classes could be used in other tests
"""