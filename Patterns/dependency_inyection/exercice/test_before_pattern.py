# Before applying Dependency Injection
# This approach has tight coupling and is harder to maintain/test
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests


class UserTest:
    def __init__(self):
        # Direct instantiation of dependencies - tight coupling
        self.driver = webdriver.Chrome()
        self.api_base_url = "https://microblog-api.azurewebsites.net/api"

    def test_user_login(self):
        # Frontend test
        self.driver.get("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net")
        self.driver.find_element(By.ID, "username").send_keys("testing")
        self.driver.find_element(By.ID, "password").send_keys("testing")
        self.driver.find_element(By.ID, "submit").click()

        # Backend verification
        response = requests.post(f'{self.api_base_url}/tokens', auth=HTTPBasicAuth('testing', 'testing'))
        assert 200 == response.status_code

    def teardown(self):
        self.driver.quit()


user_test = UserTest()
user_test.test_user_login()
