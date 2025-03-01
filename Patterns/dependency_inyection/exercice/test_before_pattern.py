# Before applying Dependency Injection
# This approach has tight coupling and is harder to maintain/test
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


class UserTest:
    """
    Test class without dependency injection.

    ANTI-PATTERN:
    - Tightly coupled to specific implementations (Chrome, requests)
    - No abstractions or interfaces
    - Hard to test with different browsers or in different environments
    - Not easily mockable for unit testing
    """

    def __init__(self):
        # PROBLEM: Direct instantiation of dependencies - tight coupling
        # The class is directly creating its dependencies rather than having them injected
        self.driver = webdriver.Chrome()  # Hard dependency on Chrome browser

        # PROBLEM: Hardcoded API URL
        # This cannot be easily changed for different environments (dev, test, prod)
        self.api_base_url = "https://microblog-api.azurewebsites.net/api"

    def test_user_login(self):
        """
        Test user login without abstraction layers.

        PROBLEMS:
        1. Direct dependency on Selenium API (By.ID, find_element, etc.)
        2. Direct dependency on requests library
        3. Cannot be unit tested without a real browser and API
        4. Cannot easily switch to a different browser or HTTP client
        5. Test is tightly coupled to the implementation details
        """
        # PROBLEM: Direct use of Selenium API
        # This makes it difficult to use a different automation tool or mock for testing
        self.driver.get("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")
        self.driver.find_element(By.ID, "username").send_keys("testing")
        self.driver.find_element(By.ID, "password").send_keys("testing")
        self.driver.find_element(By.ID, "submit").click()

        # PROBLEM: Direct use of requests library
        # This makes it difficult to mock HTTP requests for testing
        response = requests.post(f'{self.api_base_url}/tokens', auth=HTTPBasicAuth('testing', 'testing'))
        assert 200 == response.status_code

    def teardown(self):
        """Clean up resources after tests."""
        self.driver.quit()


# PROBLEM: Direct instantiation and execution
# No flexibility in how tests are created or run
user_test = UserTest()
user_test.test_user_login()

# Additional problems with this approach:
# 1. No way to run with a different browser without changing the code
# 2. No way to point to different environments (dev/test/prod) without changing the code
# 3. No way to mock dependencies for unit testing
# 4. Tests are difficult to parallelize due to tight coupling
# 5. Tests will fail if Chrome is not installed or compatible
