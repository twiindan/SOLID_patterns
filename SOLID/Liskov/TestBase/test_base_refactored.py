from selenium import webdriver
import requests
from abc import ABC, abstractmethod


class TestBase(ABC):
    def __init__(self, url) -> None:
        self.url = url

    @abstractmethod
    def run_test(self) -> bool:
        pass


class FrontendTest(TestBase):
    def __init__(self, url, element_id) -> None:
        super().__init__(url)
        self.element_id = element_id
        self.driver = webdriver.Chrome()

    def run_test(self) -> bool:
        self.driver.get(self.url)
        element = self.driver.find_element("id", self.element_id)
        return element.is_displayed()


class BackendTest(TestBase):
    def __init__(self, url, payload) -> None:
        super().__init__(url)
        self.payload = payload

    def run_test(self) -> bool:
        response = requests.post(self.url, json=self.payload)
        return response.status_code == 200


def execute_test(test: TestBase):
    result = test.run_test()
    print(f"Test executed, result: {result}")


def test_incorrect_login():
    frontend_test = FrontendTest("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net/", "username")
    backend_test = BackendTest("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net",
                               {"user": "salle", "password": "salle"})

    execute_test(frontend_test)  # ✅ Compatible with TestBase
    execute_test(backend_test)   # ✅ Compatible with TestBase
