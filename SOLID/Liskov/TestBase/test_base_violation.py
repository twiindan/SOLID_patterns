from selenium import webdriver
import requests


# This file demonstrates code that violates the Liskov Substitution Principle (LSP)
# LSP states that objects of a superclass should be replaceable with objects of a subclass
# without affecting the correctness of the program.

class TestBase:
    # Base class that attempts to define a common interface for tests
    # However, it uses NotImplementedError() instead of proper abstract methods

    def run_test(self) -> bool:
        # This method indicates a contract: no parameters, returns bool
        # But the subclasses will violate this contract
        pass


class FrontendTest(TestBase):
    # This subclass violates LSP in several ways

    def __init__(self, url):
        # Does not call super().__init__() which could lead to incomplete initialization
        self.url = url
        self.driver = webdriver.Chrome()

    def run_test(self, element_id) -> bool:
        # VIOLATION #1: Changes method signature by adding a parameter
        # This breaks substitutability because code expecting TestBase.run_test()
        # cannot call FrontendTest.run_test() without providing the extra argument
        self.driver.get(self.url)
        element = self.driver.find_element("id", element_id)
        return element.is_displayed()


class BackendTest(TestBase):
    # This subclass also violates LSP in multiple ways

    def __init__(self, url):
        # Similarly, doesn't call super().__init__()
        self.url = url

    def run_test(self, payload) -> int:
        # VIOLATION #1: Changes method signature by adding a parameter
        # VIOLATION #2: Changes return type from bool to int
        # Both changes break substitutability - a function expecting a TestBase
        # cannot correctly use a BackendTest without knowing its specific implementation
        response = requests.post(self.url, json=payload)
        return response.status_code  # Returns int instead of bool

# The problems with this design:
# 1. We cannot write a function like execute_test(test: TestBase) that works with any test
# 2. Client code must know which specific subclass it's working with
# 3. Polymorphism is broken - we cannot treat objects uniformly
# 4. Adding new test types is risky as each might have its own unique interface