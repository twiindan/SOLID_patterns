# With Factory Pattern
# This approach provides better organization, reusability, and maintainability

from abc import ABC, abstractmethod
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


# Data model for our tests
@dataclass
class UserData:
    username: str
    email: str


# Abstract Factory Interface
class UserTestFactory(ABC):
    @abstractmethod
    def create_user(self, user_data: UserData):
        pass

    @abstractmethod
    def verify_user_created(self) -> bool:
        pass


# Concrete Factory for UI Tests
class UIUserTestFactory(UserTestFactory):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.base_url = "https://example.com"

    def create_user(self, user_data: UserData):
        self.driver.get(f"{self.base_url}/users/new")
        self.driver.find_element(By.ID, "username").send_keys(user_data.username)
        self.driver.find_element(By.ID, "email").send_keys(user_data.email)
        self.driver.find_element(By.ID, "submit").click()

    def verify_user_created(self) -> bool:
        return self.driver.find_element(By.CLASS_NAME, "success-message").is_displayed()

    def cleanup(self):
        self.driver.quit()


# Concrete Factory for API Tests
class APIUserTestFactory(UserTestFactory):
    def __init__(self):
        self.api_url = "https://api.example.com"

    def create_user(self, user_data: UserData):
        self.response = requests.post(
            f"{self.api_url}/users",
            json={
                "username": user_data.username,
                "email": user_data.email
            }
        )

    def verify_user_created(self) -> bool:
        return self.response.status_code == 201

    def cleanup(self):
        pass


# Test class using the Factory Pattern
class TestUserManagementWithFactory:
    def setup_method(self):
        self.test_data = UserData(
            username="testuser",
            email="test@example.com"
        )

    def test_create_user_ui(self):
        factory = UIUserTestFactory()
        try:
            factory.create_user(self.test_data)
            assert factory.verify_user_created()
        finally:
            factory.cleanup()

    def test_create_user_api(self):
        factory = APIUserTestFactory()
        try:
            factory.create_user(self.test_data)
            assert factory.verify_user_created()
        finally:
            factory.cleanup()
