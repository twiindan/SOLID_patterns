from typing import Dict
from selenium import webdriver


# This file demonstrates code that violates the Liskov Substitution Principle (LSP)
# LSP states that objects of a superclass should be replaceable with objects of a subclass
# without affecting the correctness of the program.

class WebTest:
    # Base class that defines methods for web testing with Selenium
    # This establishes a contract that all subclasses should follow

    def setup(self) -> None:
        # Sets up a Chrome browser and navigates to a specific URL
        # All subclasses are expected to honor this behavior
        self.driver = webdriver.Chrome()
        self.driver.get("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net/")
        self.driver.maximize_window()

    def execute(self) -> bool:
        # Base implementation that returns a boolean result
        # This establishes a contract: execute() should return a boolean
        # Implementation
        return True

    def teardown(self) -> None:
        # Cleans up resources by quitting the browser
        # All subclasses should maintain this cleanup capability
        self.driver.quit()


class APITest(WebTest):  # LSP violation
    # This subclass shows multiple violations of the Liskov Substitution Principle

    def setup(self) -> None:
        # VIOLATION #1: Refuses to implement the expected behavior
        # Instead of providing compatible functionality, it throws an exception
        # This breaks substitutability - code expecting WebTest.setup() will fail with APITest
        raise NotImplementedError("API tests don't need browser setup")  # ❌ LSP violation

    def execute(self) -> Dict:
        # VIOLATION #2: Changes the return type from bool to Dict
        # This breaks the contract established by the parent class
        # Code expecting a boolean result will break when it receives a dictionary
        return {"status": "success", "response": {}}  # ❌ The return type is different

    # VIOLATION #3: Missing implementation of teardown()
    # The subclass inherits teardown() but it references self.driver which won't exist
    # This would cause runtime errors when teardown() is called

# The problems with this design:
# 1. APITest cannot be used anywhere WebTest is expected without breaking the code
# 2. The inheritance hierarchy doesn't make sense - API tests fundamentally work differently
# 3. Client code cannot rely on a consistent interface
# 4. Runtime errors will occur when using APITest polymorphically
