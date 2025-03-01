from selenium import webdriver
from selenium.webdriver.common.by import By


class TestLoginPage:
    """
    Test class that violates the Factory Pattern principles.

    PROBLEMS WITH THIS APPROACH:
    - Duplicated test code across multiple methods
    - Browser setup logic is mixed with test logic
    - Adding a new browser requires creating a whole new test method
    - Changes to test logic must be replicated in multiple places
    """

    def test_login_chrome(self):
        """
        Test login functionality using Chrome browser.

        ISSUES:
        - Browser creation and setup is embedded in the test method
        - Test logic is tightly coupled with Chrome-specific code
        - No separation of concerns between test logic and browser setup
        """
        # Chrome-specific setup
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)

        try:
            # Test logic
            driver.get("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")
            driver.find_element(By.ID, "username").send_keys("testing")
            driver.find_element(By.ID, "password").send_keys("testing")
            driver.find_element(By.ID, "submit").click()

            # Assertions
            welcome_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-info")
            assert welcome_message.text == "Invalid username or password"

        finally:
            driver.quit()

    def test_login_firefox(self):
        """
        Test login functionality using Firefox browser.

        ISSUES:
        - Almost identical to test_login_chrome method - violates DRY principle
        - Only the browser creation differs, yet the entire method is duplicated
        - Any changes to test steps must be made in both methods
        - Adding a third browser (e.g., Edge) would require another duplicate method
        """
        # Firefox-specific setup
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)

        try:
            # Test logic (duplicated)
            driver.get("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")
            driver.find_element(By.ID, "username").send_keys("testing")
            driver.find_element(By.ID, "password").send_keys("testing")
            driver.find_element(By.ID, "submit").click()

            # Assertions
            welcome_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-info")
            assert welcome_message.text == "Invalid username or password"

        finally:
            driver.quit()
