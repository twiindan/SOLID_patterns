from abc import ABC, abstractmethod

# Browser Factory Interface
from selenium import webdriver
from selenium.webdriver.common.by import By


class BrowserFactory(ABC):
    """
    Abstract Factory: Defines the interface for creating and managing browser instances.

    FACTORY PATTERN PRINCIPLES:
    - Provides an interface for creating families of related objects
    - Hides the implementation details of browser creation
    - Allows for easy extension to support new browser types
    """

    @abstractmethod
    def create_browser(self):
        """
        Abstract method to create a browser instance.
        Each concrete factory will implement this with browser-specific logic.

        Returns:
            WebDriver: A browser driver instance
        """
        pass

    @abstractmethod
    def quit_browser(self, driver):
        """
        Abstract method to properly close a browser instance.

        Args:
            driver: The browser driver instance to quit
        """
        pass


# Concrete Chrome Factory
class ChromeFactory(BrowserFactory):
    """
    Concrete Factory: Creates and manages Chrome browser instances.

    This class encapsulates all Chrome-specific creation and configuration logic.
    """

    def create_browser(self):
        """
        Creates and configures a Chrome browser instance.

        Returns:
            WebDriver: A configured Chrome WebDriver instance
        """
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)  # Chrome-specific configuration
        return driver

    def quit_browser(self, driver):
        """
        Properly closes a Chrome browser instance.

        Args:
            driver: The Chrome WebDriver instance to quit
        """
        driver.quit()


# Concrete Firefox Factory
class FirefoxFactory(BrowserFactory):
    """
    Concrete Factory: Creates and manages Firefox browser instances.

    This class encapsulates all Firefox-specific creation and configuration logic.
    """

    def create_browser(self):
        """
        Creates and configures a Firefox browser instance.

        Returns:
            WebDriver: A configured Firefox WebDriver instance
        """
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)  # Firefox-specific configuration
        return driver

    def quit_browser(self, driver):
        """
        Properly closes a Firefox browser instance.

        Args:
            driver: The Firefox WebDriver instance to quit
        """
        driver.quit()


# Browser Factory Creator
class BrowserFactoryCreator:
    """
    Factory Creator: Provides a centralized way to get browser factories.

    BENEFITS:
    - Adds an extra level of abstraction for factory creation
    - Centralizes the logic for determining which factory to create
    - Makes it easy to add support for new browsers in one place
    """

    @staticmethod
    def get_factory(browser_type):
        """
        Creates and returns the appropriate browser factory based on browser type.

        Args:
            browser_type (str): The type of browser ('chrome' or 'firefox')

        Returns:
            BrowserFactory: An instance of the appropriate browser factory

        Raises:
            ValueError: If an unsupported browser type is specified
        """
        if browser_type.lower() == "chrome":
            return ChromeFactory()
        elif browser_type.lower() == "firefox":
            return FirefoxFactory()
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")


# Test case using the Factory
class LoginWithFactory:
    """
    Client code: Uses the Factory Pattern to run tests with different browsers.

    ADVANTAGES OVER PREVIOUS APPROACH:
    - Test logic is written once, regardless of which browser is used
    - Browser-specific details are completely isolated in factory classes
    - Adding new browsers doesn't require modifying the test logic
    - Better separation of concerns between test logic and browser management
    """

    def set_browser(self, browser):
        """
        Sets up the browser for testing using the factory pattern.

        Args:
            browser (str): The type of browser to use ('chrome' or 'firefox')
        """
        # You can easily change the browser here or via configuration
        self.factory = BrowserFactoryCreator.get_factory(browser)
        self.driver = self.factory.create_browser()

    def test_incorrect_login(self):
        """
        Tests the incorrect login scenario.

        This test logic is completely independent of browser specifics,
        making it reusable across different browser types.
        """
        # Test logic is now separate from browser setup
        self.driver.get("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")
        self.driver.find_element(By.ID, "username").send_keys("badusername")
        self.driver.find_element(By.ID, "password").send_keys("badpassword")
        self.driver.find_element(By.ID, "submit").click()

        # Assertions
        welcome_message = self.driver.find_element(By.CSS_SELECTOR, ".alert.alert-info")
        assert welcome_message.text == "Invalid username or password"

    def quit_browser(self):
        """
        Properly closes the browser using the factory.

        The factory handles the specifics of closing each browser type.
        """
        self.factory.quit_browser(self.driver)


# Demonstrating how to run the same test with different browsers
# Run test with Chrome
test_login_chrome = LoginWithFactory()
test_login_chrome.set_browser('chrome')  # Configuring for Chrome
test_login_chrome.test_incorrect_login()  # Running test logic
test_login_chrome.quit_browser()  # Proper cleanup

# Run the exact same test with Firefox
test_login_firefox = LoginWithFactory()
test_login_firefox.set_browser('firefox')  # Configuring for Firefox
test_login_firefox.test_incorrect_login()  # Reusing same test logic
test_login_firefox.quit_browser()  # Proper cleanup

# BENEFITS DEMONSTRATED:
# 1. No code duplication in test logic
# 2. Browser-specific code is isolated in factory classes
# 3. Adding a new browser (e.g., Edge) would only require:
#    - Creating a new EdgeFactory class
#    - Adding a new condition in BrowserFactoryCreator
#    - Test code remains unchanged
# 4. Test configuration is flexible and can be easily modified
