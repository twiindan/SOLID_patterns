# Before implementing Singleton Pattern
# This approach creates new instances every time, which is inefficient

from selenium import webdriver
import requests


class UITest:

    def login_test(self):
        # PROBLEM: Creates a new browser instance for each test method
        # Browser initialization is slow and resource-intensive
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/login")

    def search_test(self):
        # PROBLEM: Creates another browser instance
        # If these methods are called sequentially, previous browser instances
        # may remain open, leading to resource leaks
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/search")


class APITest:
    def __init__(self):
        # Only setting base URL in constructor
        self.base_url = "https://api.example.com"

    def test_get_users(self):
        # PROBLEM: Creates new session for each test method
        # Sessions are designed to be reused for multiple requests
        # Creating a new one loses benefits like connection pooling and cookies
        self.session = requests.Session()
        response = self.session.get(f"{self.base_url}/users")


    def test_create_user(self):
        # PROBLEM: Creates another session
        # If both test methods are called, we now have two separate sessions
        # This is inefficient and doesn't maintain state between requests
        self.session = requests.Session()
        response = self.session.post(f"{self.base_url}/users")

