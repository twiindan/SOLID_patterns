from abc import ABC, abstractmethod


# Browser Factory Interface
from selenium import webdriver
from selenium.webdriver.common.by import By


class BrowserFactory(ABC):
    @abstractmethod
    def create_browser(self):
        pass

    @abstractmethod
    def quit_browser(self, driver):
        pass


# Concrete Chrome Factory
class ChromeFactory(BrowserFactory):
    def create_browser(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        return driver

    def quit_browser(self, driver):
        driver.quit()


# Concrete Firefox Factory
class FirefoxFactory(BrowserFactory):
    def create_browser(self):
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)
        return driver

    def quit_browser(self, driver):
        driver.quit()


# Browser Factory Creator
class BrowserFactoryCreator:
    @staticmethod
    def get_factory(browser_type):
        if browser_type.lower() == "chrome":
            return ChromeFactory()
        elif browser_type.lower() == "firefox":
            return FirefoxFactory()
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")


# Test case using the Factory
class LoginWithFactory:

    def set_browser(self, browser):
        # You can easily change the browser here or via configuration
        self.factory = BrowserFactoryCreator.get_factory(browser)
        self.driver = self.factory.create_browser()

    def test_incorrect_login(self):
        # Test logic is now separate from browser setup
        self.driver.get("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")
        self.driver.find_element(By.ID, "username").send_keys("badusername")
        self.driver.find_element(By.ID, "password").send_keys("badpassword")
        self.driver.find_element(By.ID, "submit").click()

        # Assertions
        welcome_message = self.driver.find_element(By.CSS_SELECTOR, ".alert.alert-info")
        assert welcome_message.text == "Invalid username or password"

    def quit_browser(self):
        self.factory.quit_browser(self.driver)


test_login_chrome = LoginWithFactory()
test_login_chrome.set_browser('chrome')
test_login_chrome.test_incorrect_login()
test_login_chrome.quit_browser()

test_login_firefox = LoginWithFactory()
test_login_firefox.set_browser('firefox')
test_login_firefox.test_incorrect_login()
test_login_firefox.quit_browser()
