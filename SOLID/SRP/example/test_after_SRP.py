import requests
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "submit")
        self.welcome_text = (By.CSS_SELECTOR, ".alert.alert-info")

    def enter_username(self, username):
        self.driver.find_element(*self.username_input).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def get_welcome_message(self):
        return self.driver.find_element(*self.welcome_text).text


class LoginAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def login(self, username, password):
        return self.session.post(
            f"{self.base_url}/tokens",
            auth=HTTPBasicAuth(username, password),
        )


class TestLogin:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)
        self.login_api = LoginAPI("https://microblog-api.azurewebsites.net/api")

    def test_login_flow(self):
        # UI Test
        self.driver.get("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")
        self.login_page.enter_username("user@example.com")
        self.login_page.enter_password("password123")
        self.login_page.click_login()
        assert self.login_page.get_welcome_message() == "Invalid username or password"

        # API Test
        response = self.login_api.login("user@example.com", "password123")
        assert response.status_code == 401

    def teardown_method(self):
        self.driver.quit()
