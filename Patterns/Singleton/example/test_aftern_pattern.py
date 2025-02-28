from selenium import webdriver
import requests
from typing import Optional


class WebDriverManager:
    _instance: Optional['WebDriverManager'] = None
    _driver: Optional[webdriver.Chrome] = None

    def __new__(cls):
        # Ensure only one instance of WebDriverManager exists
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def driver(self):
        # Lazy initialization of WebDriver
        if self._driver is None:
            self._driver = webdriver.Chrome()
        return self._driver

    def quit(self):
        # Cleanup method
        if self._driver:
            self._driver.quit()
            self._driver = None


class APISession:
    _instance: Optional['APISession'] = None
    _session: Optional[requests.Session] = None

    def __new__(cls):
        # Ensure only one instance of APISession exists
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def session(self):
        # Lazy initialization of Session
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def close(self):
        # Cleanup method
        if self._session:
            self._session.close()
            self._session = None


class UITest:
    def __init__(self):
        # Use the singleton WebDriverManager
        self.driver_manager = WebDriverManager()

    def login_test(self):
        self.driver_manager.driver.get("https://example.com/login")
        # Test implementation

    def search_test(self):
        # Reuses the same WebDriver instance
        self.driver_manager.driver.get("https://example.com/search")
        # Test implementation

    def teardown(self):
        self.driver_manager.quit()


class APITest:
    def __init__(self):
        # Use the singleton APISession
        self.session_manager = APISession()
        self.base_url = "https://api.example.com"

    def test_get_users(self):
        response = self.session_manager.session.get(f"{self.base_url}/users")
        # Test implementation

    def test_create_user(self):
        # Reuses the same session
        response = self.session_manager.session.post(f"{self.base_url}/users")
        # Test implementation

    def teardown(self):
        self.session_manager.close()


# Example usage
def test_suite():
    # UI Tests
    ui_tests = UITest()
    ui_tests.login_test()
    ui_tests.search_test()
    ui_tests.teardown()

    # API Tests
    api_tests = APITest()
    api_tests.test_get_users()
    api_tests.test_create_user()
    api_tests.teardown()
