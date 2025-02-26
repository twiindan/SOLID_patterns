from selenium import webdriver
from selenium.webdriver.common.by import By


class TestLoginPage:
    def test_login_chrome(self):
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
