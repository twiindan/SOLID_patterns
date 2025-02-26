import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import functools
from datetime import datetime
import os
import time

# Make sure the directory to save screenshots exists
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")


def screenshot_on_failure(func):
    """
    Takes a screenshot when a UI test fails and attaches it to the test report
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/failure_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Test failed. Screenshot saved at: {screenshot_path}")
            raise

    return wrapper


class DuckDuckGoSearchTest(unittest.TestCase):

    def setUp(self):
        """Setup before each test."""
        # Configuration to make Selenium less detectable

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        """Cleanup after each test."""
        self.driver.quit()

    @screenshot_on_failure
    def test_duckduckgo_search_success(self):
        """Test that searches for Python on DuckDuckGo and verifies python.org appears."""
        # Open DuckDuckGo
        self.driver.get("https://duckduckgo.com/")

        # Give time for the page to fully load
        time.sleep(2)

        # Search for "Python"
        search_box = self.driver.find_element(By.ID, "searchbox_input")
        search_box.click()
        search_box.clear()
        search_box.send_keys("Python programming language")
        search_box.send_keys(Keys.RETURN)

        # Give time for results to load
        time.sleep(3)

        # Verify that python.org appears in the results
        page_source = self.driver.page_source.lower()
        self.assertTrue("python.org" in page_source)

        print("Test successful: python.org found in search results")

    @screenshot_on_failure
    def test_duckduckgo_search_failure(self):
        """Test designed to fail to demonstrate screenshot capture."""
        # Open DuckDuckGo
        self.driver.get("https://duckduckgo.com/")

        # Give time for the page to fully load
        time.sleep(2)

        # Search for something unlikely to have results
        search_box = self.driver.find_element(By.ID, "searchbox_input")
        search_box.click()
        search_box.clear()
        search_box.send_keys("XYZ123456789neverfindthisguaranteed")
        search_box.send_keys(Keys.RETURN)

        # Give time for results to load
        time.sleep(3)

        # This assertion will fail on purpose
        self.assertTrue("nonexistentresult.com" in self.driver.page_source)


if __name__ == "__main__":
    unittest.main()
