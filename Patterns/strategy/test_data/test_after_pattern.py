# The strategy pattern allows us to define a family of algorithms
# and make them interchangeable based on different test environments

from abc import ABC, abstractmethod
import requests


class TestDataStrategy(ABC):
    """Strategy interface for handling test data in different environments"""

    @abstractmethod
    def get_test_data(self):
        pass


class ProductionTestData(TestDataStrategy):
    """Strategy for handling test data in production-like environment"""

    def get_test_data(self):
        # Real API call with limited test data
        response = requests.get("https://api.example.com/test-data")
        return response.json()


class StagingTestData(TestDataStrategy):
    """Strategy for handling test data in staging environment"""

    def get_test_data(self):
        # Full test data set with mock data
        return {
            "users": [
                {"id": 1, "name": "Test User 1", "role": "admin"},
                {"id": 2, "name": "Test User 2", "role": "user"}
            ]
        }


class LocalTestData(TestDataStrategy):
    """Strategy for handling test data in local environment"""

    def get_test_data(self):
        # Minimal test data for quick local testing
        return {
            "users": [
                {"id": 1, "name": "Test User 1", "role": "admin"}
            ]
        }


class UserPermissionTest:
    """Test class that uses different test data strategies"""

    def __init__(self, data_strategy: TestDataStrategy):
        # The strategy can be changed at runtime
        self.data_strategy = data_strategy

    def test_user_permissions(self):
        # Get test data using the current strategy
        test_data = self.data_strategy.get_test_data()

        for user in test_data["users"]:
            if user["role"] == "admin":
                print(f"Testing admin permissions for {user['name']}")
            else:
                print(f"Testing basic permissions for {user['name']}")


# Usage example
def run_tests(environment):
    # Choose strategy based on environment
    strategies = {
        "prod": ProductionTestData(),
        "staging": StagingTestData(),
        "local": LocalTestData()
    }

    # Create test with selected strategy
    test = UserPermissionTest(strategies[environment])
    test.test_user_permissions()


# Running tests in different environments
run_tests("local")  # Uses minimal test data
run_tests("staging")  # Uses full mock data