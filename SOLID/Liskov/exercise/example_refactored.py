from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime
from selenium import webdriver


# This file demonstrates code that properly follows the Liskov Substitution Principle (LSP)
# It creates a proper abstraction hierarchy that allows objects to be substitutable

class TestCase(ABC):
    # Abstract base class that defines a contract for all test types
    # By using proper abstractions, we avoid forcing inappropriate behavior

    @abstractmethod
    def setup(self) -> None:
        """Prepare test environment"""
        # This is now abstract - subclasses can implement appropriate setup
        # without being forced to use a browser when it doesn't make sense
        pass

    @abstractmethod
    def execute(self) -> 'TestResult':
        """Execute the test and returns the TestResult"""
        # The return type is consistently TestResult for all subclasses
        # This ensures that client code can handle results uniformly
        pass

    @abstractmethod
    def teardown(self) -> None:
        """Clean all data"""
        # Abstract cleanup method allows different resource management
        # approaches while maintaining the same interface
        pass


class TestResult:
    # A common result type that standardizes what all tests return
    # This is a key part of making the tests substitutable - they all
    # return the same type of result that can be processed uniformly

    def __init__(self, passed: bool, message: str = "", data: Optional[Dict] = None):
        self.passed = passed
        self.message = message
        self.data = data or {}
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict:
        # Provides a standard way to convert results to a dictionary
        return {
            "passed": self.passed,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }


class UITest(TestCase):
    # Concrete implementation for UI testing
    # Follows LSP by adhering to the contract defined in TestCase

    def __init__(self, url: str):
        self.url = url
        self.driver = None  # Initialized as None to prevent issues if teardown runs before setup

    def setup(self) -> None:
        # Implements setup appropriately for UI tests
        # Fully compatible with the TestCase contract
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.maximize_window()

    def execute(self) -> TestResult:
        # Returns a TestResult object as promised in the contract
        # Uses try/except to ensure robustness
        try:
            # UI Test example
            title = self.driver.title
            print(title)
            if "Sign In - Microblog" in title:
                return TestResult(True, "Page title verified successfully")
            return TestResult(False, f"Unexpected title: {title}")
        except Exception as e:
            return TestResult(False, f"Test failed: {str(e)}")

    def teardown(self) -> None:
        # Safely cleans up resources with a null check
        # This prevents errors if teardown runs when setup wasn't completed
        if self.driver:
            self.driver.quit()


class APITest(TestCase):
    # Concrete implementation for API testing
    # Also follows LSP by adhering to the TestCase contract

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.session = None  # Safe initialization

    def setup(self) -> None:
        # Implements setup appropriate for API tests
        # No browser needed, uses requests session instead
        import requests
        self.session = requests.Session()

    def execute(self) -> TestResult:
        # Returns a TestResult, fully compatible with the contract
        # Has different implementation details but same interface
        try:
            response = self.session.get(self.endpoint)
            if response.status_code == 200:
                return TestResult(
                    passed=True,
                    message="API request successful",
                    data={"status_code": 200, "response": response.json()}
                )
            return TestResult(
                passed=False,
                message=f"API request failed with status {response.status_code}",
                data={"status_code": response.status_code}
            )
        except Exception as e:
            return TestResult(False, f"Test failed: {str(e)}")

    def teardown(self) -> None:
        # Safely cleans up resources with a null check
        if self.session:
            self.session.close()


# TestRunner
class TestRunner:
    # This class demonstrates the power of LSP
    # It can work with ANY TestCase object without knowing the concrete type

    def __init__(self):
        self.tests: List[TestCase] = []
        self.results: List[TestResult] = []

    def add_test(self, test: TestCase) -> None:
        # Takes any TestCase - demonstrates substitutability
        self.tests.append(test)

    def run_all(self) -> List[TestResult]:
        # Runs all tests polymorphically - this is only possible
        # because all TestCase implementations follow LSP
        for test in self.tests:
            try:
                test.setup()
                result = test.execute()
                self.results.append(result)
            except Exception as e:
                self.results.append(TestResult(False, f"Test execution failed: {str(e)}"))
            finally:
                test.teardown()
        return self.results

    def get_summary(self) -> Dict[str, Any]:
        # Processes results uniformly regardless of test type
        total = len(self.results)
        passed = sum(1 for result in self.results if result.passed)
        return {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": (passed / total * 100) if total > 0 else 0
        }


# Example
if __name__ == "__main__":
    # Create different test types
    ui_test = UITest("https://microblog-hwepgvgtb6hchvcf.westeurope-01.azurewebsites.net/")
    api_test = APITest("https://microblog-api.azurewebsites.net/api/tokens")

    # We can use the TestRunner with different types of tests
    # This demonstrates true substitutability - the key benefit of LSP
    runner = TestRunner()
    runner.add_test(ui_test)
    runner.add_test(api_test)

    # Execute all the tests through the same interface
    results = runner.run_all()

    # Show results
    print("Test Results:")
    for i, result in enumerate(results, 1):
        print(f"\nTest {i}:")
        print(f"Passed: {result.passed}")
        print(f"Message: {result.message}")
        print(f"Data: {result.data}")

    # Show summary
    summary = runner.get_summary()
    print("\nTest Summary:")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {summary['success_rate']:.2f}%")
