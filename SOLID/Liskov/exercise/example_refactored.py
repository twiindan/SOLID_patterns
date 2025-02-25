from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime
from selenium import webdriver


class TestCase(ABC):
    @abstractmethod
    def setup(self) -> None:
        """Prepare test environment"""
        pass

    @abstractmethod
    def execute(self) -> 'TestResult':
        """Execute the test and returns the TestResult"""
        pass

    @abstractmethod
    def teardown(self) -> None:
        """Clean all data"""
        pass


class TestResult:
    def __init__(self, passed: bool, message: str = "", data: Optional[Dict] = None):
        self.passed = passed
        self.message = message
        self.data = data or {}
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "passed": self.passed,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }


class UITest(TestCase):
    def __init__(self, url: str):
        self.url = url
        self.driver = None

    def setup(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.maximize_window()

    def execute(self) -> TestResult:
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
        if self.driver:
            self.driver.quit()


class APITest(TestCase):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.session = None

    def setup(self) -> None:
        import requests
        self.session = requests.Session()

    def execute(self) -> TestResult:
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
        if self.session:
            self.session.close()


# TestRunner
class TestRunner:
    def __init__(self):
        self.tests: List[TestCase] = []
        self.results: List[TestResult] = []

    def add_test(self, test: TestCase) -> None:
        self.tests.append(test)

    def run_all(self) -> List[TestResult]:
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
    runner = TestRunner()
    runner.add_test(ui_test)
    runner.add_test(api_test)

    # Execute all the tests
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