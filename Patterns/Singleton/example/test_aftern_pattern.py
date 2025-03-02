from selenium import webdriver
import requests
from typing import Optional


class WebDriverManager:
    # Class variables for the singleton instance and browser driver
    _instance: Optional['WebDriverManager'] = None
    _driver: Optional[webdriver.Chrome] = None

    def __new__(cls):
        # SINGLETON PATTERN: Ensure only one instance of WebDriverManager exists
        # This controls the object creation process
        if cls._instance is None:
            # First time initialization - create the instance
            cls._instance = super().__new__(cls)
        # Return the existing instance for all subsequent calls
        return cls._instance

    @property
    def driver(self):
        # LAZY INITIALIZATION: Only create the WebDriver when first accessed
        # This delays the resource-intensive browser initialization until needed
        if self._driver is None:
            self._driver = webdriver.Chrome()
        return self._driver

    def quit(self):
        # Centralized cleanup method ensures proper resource management
        # Prevents browser process leaks
        if self._driver:
            self._driver.quit()  # Close the browser properly
            self._driver = None  # Reset the reference for potential reuse


class APISession:
    # Class variables for the singleton instance and session
    _instance: Optional['APISession'] = None
    _session: Optional[requests.Session] = None

    def __new__(cls):
        # SINGLETON PATTERN: Ensure only one instance of APISession exists
        # Similar implementation as WebDriverManager
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def session(self):
        # LAZY INITIALIZATION: Only create the Session when first accessed
        # Delays session creation until needed
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def close(self):
        # Centralized cleanup method ensures connections are properly closed
        if self._session:
            self._session.close()
            self._session = None


class UITest:
    def __init__(self):
        # Use the singleton WebDriverManager
        # All test methods in this class will use the same browser instance
        self.driver_manager = WebDriverManager()

    def login_test(self):
        # Access the shared browser instance
        self.driver_manager.driver.get("https://example.com/login")
        # Test implementation

    def search_test(self):
        # Reuses the same WebDriver instance
        # No need to initialize a new browser, maintaining state and cookies
        self.driver_manager.driver.get("https://example.com/search")
        # Test implementation

    def teardown(self):
        # Proper cleanup method that calls the manager's quit method
        # This separates test logic from resource management
        self.driver_manager.quit()


class APITest:
    def __init__(self):
        # Use the singleton APISession
        # All API tests will use the same session
        self.session_manager = APISession()
        self.base_url = "https://api.example.com"

    def test_get_users(self):
        # Use the shared session instance
        response = self.session_manager.session.get(f"{self.base_url}/users")
        # Test implementation

    def test_create_user(self):
        # Reuses the same session
        # Benefits from connection pooling, cookie persistence, etc.
        response = self.session_manager.session.post(f"{self.base_url}/users")
        # Test implementation

    def teardown(self):
        # Proper cleanup that calls the manager's close method
        self.session_manager.close()


# Example usage
def test_suite():
    # UI Tests
    ui_tests = UITest()
    ui_tests.login_test()
    ui_tests.search_test()
    ui_tests.teardown()  # Ensures browser is properly closed

    # API Tests
    api_tests = APITest()
    api_tests.test_get_users()
    api_tests.test_create_user()
    api_tests.teardown()  # Ensures session is properly closed
