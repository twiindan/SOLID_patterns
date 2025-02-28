import requests


class UserPermissionTest:
    """Test class with hardcoded logic for different environments"""

    def __init__(self, environment):
        self.environment = environment

    def get_test_data(self):
        # Complex conditional logic to handle different environments
        if self.environment == "prod":
            # Real API call with limited test data
            response = requests.get("https://api.example.com/test-data")
            return response.json()

        elif self.environment == "staging":
            # Full test data set with mock data
            return {
                "users": [
                    {"id": 1, "name": "Test User 1", "role": "admin"},
                    {"id": 2, "name": "Test User 2", "role": "user"}
                ]
            }

        elif self.environment == "local":
            # Minimal test data for quick local testing
            return {
                "users": [
                    {"id": 1, "name": "Test User 1", "role": "admin"}
                ]
            }
        else:
            raise ValueError(f"Unknown environment: {self.environment}")

    def test_user_permissions(self):
        # Get test data using environment-specific logic
        test_data = self.get_test_data()

        for user in test_data["users"]:
            if user["role"] == "admin":
                print(f"Testing admin permissions for {user['name']}")
            else:
                print(f"Testing basic permissions for {user['name']}")


# Usage example
def run_tests(environment):
    test = UserPermissionTest(environment)
    test.test_user_permissions()


# Running tests in different environments
run_tests("local")  # Uses minimal test data
run_tests("staging")  # Uses full mock data
