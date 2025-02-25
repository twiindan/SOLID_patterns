# Before applying Dependency Inversion Principle
# In this implementation, the test class is tightly coupled to specific implementations

from selenium import webdriver
from selenium.webdriver.common.by import By


class LoginTest:
    def __init__(self):
        # Direct dependency on concrete implementations
        self.driver = webdriver.Chrome()
        self.base_url = "https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net/"

    def test_login_ui(self):
        # UI test implementation tightly coupled to Selenium
        self.driver.get(f"{self.base_url}")
        self.driver.find_element(By.ID, "username").send_keys("testing")
        self.driver.find_element(By.ID, "password").send_keys("testing")
        self.driver.find_element(By.ID, "submit").click()

        # Assert login success
        assert "Home - Microblog" in self.driver.title

    def teardown(self):
        self.driver.quit()


test_login = LoginTest()
test_login.test_login_ui()
