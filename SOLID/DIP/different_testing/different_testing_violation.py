# Before applying Dependency Inversion Principle
# In this implementation, the test class is tightly coupled to specific implementations

from selenium import webdriver
from selenium.webdriver.common.by import By


class LoginTest:
    def __init__(self):
        # VIOLATION: Direct dependency on concrete implementations
        # The test class is directly instantiating a concrete Chrome driver
        # This makes it impossible to use a different browser or mock implementation for testing
        self.driver = webdriver.Chrome()
        self.base_url = "https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net/"

    def test_login_ui(self):
        # VIOLATION: UI test implementation tightly coupled to Selenium
        # The test is directly calling Selenium-specific methods
        # If we want to use a different UI testing framework, we would need to rewrite the entire test
        self.driver.get(f"{self.base_url}")
        self.driver.find_element(By.ID, "username").send_keys("testing")
        self.driver.find_element(By.ID, "password").send_keys("testing")
        self.driver.find_element(By.ID, "submit").click()

        # Assert login success
        # Again, using Selenium-specific property
        assert "Home - Microblog" in self.driver.title

    def teardown(self):
        # Cleanup is also tightly coupled to Selenium's interface
        self.driver.quit()


# VIOLATION: Direct instantiation and execution
# This creates a hard dependency that can't be easily modified or injected
test_login = LoginTest()
test_login.test_login_ui()
test_login.teardown()
