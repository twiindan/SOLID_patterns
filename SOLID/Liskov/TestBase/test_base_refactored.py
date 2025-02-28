from selenium import webdriver
import requests
from abc import ABC, abstractmethod


# This file demonstrates code that adheres to the Liskov Substitution Principle (LSP)
# The Liskov Substitution Principle states that objects of a superclass should be replaceable
# with objects of a subclass without affecting the correctness of the program.

class TestBase(ABC):
    # Abstract base class that defines the contract for all test types
    # The key aspect of LSP is that this base class establishes a consistent interface
    # that all derived classes must follow exactly

    def __init__(self, url) -> None:
        # Base constructor that accepts the URL parameter required by all test types
        self.url = url

    @abstractmethod
    def run_test(self) -> bool:
        # Abstract method that:
        # 1. Takes no additional parameters (important for LSP!)
        # 2. Returns a boolean value (consistent return type for LSP)
        # This ensures all derived classes can be used interchangeably
        pass


class FrontendTest(TestBase):
    # Concrete implementation for frontend tests that follows LSP:
    # 1. It extends the behavior without changing the interface
    # 2. It maintains the parameter and return type contracts

    def __init__(self, url, element_id) -> None:
        # Constructor extends parent by adding element_id but still calls super().__init__
        # This preserves the base behavior while adding specialized behavior
        super().__init__(url)
        self.element_id = element_id  # Additional state stored as an instance variable
        self.driver = webdriver.Chrome()

    def run_test(self) -> bool:
        # Implementation adheres to LSP:
        # 1. Same method signature as the base class (no additional parameters)
        # 2. Same return type (bool) as promised in the base class
        # 3. Fulfills the same overall contract/purpose
        self.driver.get(self.url)
        element = self.driver.find_element("id", self.element_id)
        return element.is_displayed()


class BackendTest(TestBase):
    # Another concrete implementation showing how we can have different logic
    # while still conforming to the same interface

    def __init__(self, url, payload) -> None:
        # Similarly extends parent constructor while calling super().__init__
        super().__init__(url)
        self.payload = payload  # Store payload as instance variable rather than method parameter

    def run_test(self) -> bool:
        # Implementation adheres to LSP:
        # 1. Same method signature (no parameters)
        # 2. Returns a bool as specified in the contract
        # 3. Behavior is consistent with the base class expectation
        response = requests.post(self.url, json=self.payload)
        return response.status_code == 200  # Converts status code to boolean


def execute_test(test: TestBase):
    # This function demonstrates the power of LSP
    # It can work with ANY TestBase object without knowing the concrete type
    # This polymorphic behavior relies on proper LSP implementation
    result = test.run_test()
    print(f"Test executed, result: {result}")


def test_incorrect_login():
    # Client code creates concrete implementations and uses them polymorphically
    frontend_test = FrontendTest("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net/", "username")
    backend_test = BackendTest("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net",
                               {"user": "salle", "password": "salle"})

    # Both tests can be passed to the same function despite being different classes
    # This demonstrates the power of LSP - substitutability
    execute_test(frontend_test)  # ✅ Compatible with TestBase
    execute_test(backend_test)  # ✅ Compatible with TestBase
