# Without Factory Pattern
# This approach has duplicate code and is harder to maintain

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


class TestUserManagement:
    def setup_method(self):
        # Browser setup repeated in multiple test classes
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = "https://example.com"
        self.api_url = "https://api.example.com"

    def test_create_user_ui(self):
        # UI Test implementation
        self.driver.get(f"{self.base_url}/users/new")
        self.driver.find_element(By.ID, "username").send_keys("testuser")
        self.driver.find_element(By.ID, "email").send_keys("test@example.com")
        self.driver.find_element(By.ID, "submit").click()

        assert self.driver.find_element(By.CLASS_NAME, "success-message").is_displayed()

    def test_create_user_api(self):
        # API Test implementation
        payload = {
            "username": "testuser",
            "email": "test@example.com"
        }
        response = requests.post(f"{self.api_url}/users", json=payload)
        assert response.status_code == 201

    def teardown_method(self):
        self.driver.quit()
