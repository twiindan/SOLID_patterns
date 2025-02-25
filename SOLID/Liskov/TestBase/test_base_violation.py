from selenium import webdriver
import requests


class TestBase:
    def run_test(self) -> bool:
        raise NotImplementedError()


class FrontendTest(TestBase):
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def run_test(self, element_id) -> bool:
        self.driver.get(self.url)
        element = self.driver.find_element("id", element_id)
        return element.is_displayed()


class BackendTest(TestBase):
    def __init__(self, url):
        self.url = url

    def run_test(self, payload) -> int:
        response = requests.post(self.url, json=payload)
        return response.status_code
