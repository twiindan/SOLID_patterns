import requests
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestLoginPage:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.base_url = "https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net"
        self.api_url = "https://microblog-api.azurewebsites.net/api"

    def test_incorrect_login_flow(self):

        self.driver.get(self.base_url)
        self.driver.find_element(By.ID, "username").send_keys("user@example.com")
        self.driver.find_element(By.ID, "password").send_keys("password123")
        self.driver.find_element(By.ID, "submit").click()

        # UI Validation
        welcome_message = self.driver.find_element(By.CSS_SELECTOR, ".alert.alert-info")
        assert welcome_message.text == "Invalid username or password"

        # API Validation
        session = requests.Session()
        response = session.post(
            f"{self.api_url}/tokens",
            auth=HTTPBasicAuth('user', 'password'),
        )
        assert response.status_code == 401


test_login_page = TestLoginPage()
test_login_page.test_incorrect_login_flow()
