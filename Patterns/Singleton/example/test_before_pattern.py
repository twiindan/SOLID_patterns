# Before implementing Singleton Pattern
# This approach creates new instances every time, which is inefficient

from selenium import webdriver
import requests


class UITest:

    def login_test(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/login")
        # Test implementation

    def search_test(self):
        # Creates another browser instance
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/search")
        # Test implementation


class APITest:
    def __init__(self):
        # Creates new session for each test
        self.base_url = "https://api.example.com"

    def test_get_users(self):
        self.session = requests.Session()
        response = self.session.get(f"{self.base_url}/users")
        # Test implementation

    def test_create_user(self):
        # Creates another session
        self.session = requests.Session()
        response = self.session.post(f"{self.base_url}/users")
