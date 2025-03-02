# The strategy pattern allows us to define a family of algorithms
# and make them interchangeable based on different test environments

from abc import ABC, abstractmethod
import requests


class TestDataStrategy(ABC):
    """Strategy interface for handling test data in different environments"""

    @abstractmethod
    def get_test_data(self):
        # All concrete strategies must implement this method
        pass


class ProductionTestData(TestDataStrategy):
    """Strategy for handling test data in production-like environment"""

    def get_test_data(self):
        # Real API call with limited test data
        # This strategy encapsulates all production-specific data logic
        response = requests.get("https://api.example.com/test-data")
        return response.json()


class StagingTestData(TestDataStrategy):
    """Strategy for handling test data in staging environment"""

    def get_test_data(self):
        # Full test data set with mock data
        # This strategy encapsulates all staging-specific data logic
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
        # This strategy encapsulates all local-specific data logic
        return {
            "users": [
                {"id": 1, "name": "Test User 1", "role": "admin"}
            ]
        }


class UserPermissionTest:
    """Test class that uses different test data strategies"""

    def __init__(self, data_strategy: TestDataStrategy):
        # The strategy is injected via constructor - dependency injection
        # Type hinting ensures we only accept valid strategies
        self.data_strategy = data_strategy

    def test_user_permissions(self):
        # Get test data using the current strategy
        # This method is decoupled from the specific data retrieval implementation
        test_data = self.data_strategy.get_test_data()

        # Process the test data (same as before)
        for user in test_data["users"]:
            if user["role"] == "admin":
                print(f"Testing admin permissions for {user['name']}")
            else:
                print(f"Testing basic permissions for {user['name']}")


# Usage example
def run_tests(environment):
    # Choose strategy based on environment
    # This dictionary maps environment names to strategy instances
    # BENEFIT: Adding a new environment only requires adding an entry here
    strategies = {
        "prod": ProductionTestData(),
        "staging": StagingTestData(),
        "local": LocalTestData()
    }

    # Create test with selected strategy
    test = UserPermissionTest(strategies[environment])
    test.test_user_permissions()


# Running tests in different environments
# The client code is much cleaner and doesn't need to know about strategy details
run_tests("local")  # Uses minimal test data
run_tests("staging")  # Uses full mock data
