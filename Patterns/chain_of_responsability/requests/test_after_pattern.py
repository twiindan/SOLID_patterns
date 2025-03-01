import requests


# Chain of Responsibility Pattern Implementation for API Testing

# Base Handler - Abstract handler class that defines the chain structure
# Each handler can process a request and pass it to the next handler in the chain
class Handler:
    def __init__(self, next_handler=None):
        # Store reference to the next handler in the chain
        self.next_handler = next_handler

    def handle(self, response):
        # If there's a next handler, forward the request to it
        # This implements the "chain" part of Chain of Responsibility
        if self.next_handler:
            return self.next_handler.handle(response)
        # Default behavior at the end of the chain is to return success
        return True


# Concrete Handler 1: Validates HTTP status code
class StatusCodeValidator(Handler):
    def handle(self, response):
        # Check if the status code is 200 (OK)
        if response.status_code != 200:
            print(f"❌ Invalid status code: {response.status_code}")
            return False  # Stop the chain if validation fails
        print("✅ Status code is valid")
        # Continue the chain by calling the parent class's handle method
        return super().handle(response)


# Concrete Handler 2: Validates that the response is valid JSON
class JsonValidator(Handler):
    def handle(self, response):
        # Attempt to parse the response as JSON
        try:
            response.json()
            print("✅ Response is valid JSON")
        except ValueError:
            print("❌ Response is not valid JSON")
            return False  # Stop the chain if validation fails
        # Continue the chain
        return super().handle(response)


# Concrete Handler 3: Validates that the required fields exist in the JSON
class FieldValidator(Handler):
    def __init__(self, required_fields, next_handler=None):
        super().__init__(next_handler)
        # Store the list of fields that must be present
        self.required_fields = required_fields

    def handle(self, response):
        # Parse the JSON data
        data = response.json()
        # Check if each required field exists
        for field in self.required_fields:
            if field not in data:
                print(f"❌ Missing field: {field}")
                return False  # Stop the chain if validation fails
        print("✅ All required fields are present")
        # Continue the chain
        return super().handle(response)


# API Test using Chain of Responsibility pattern
def test_api():
    # Make the API request
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")

    # BENEFITS OF CHAIN OF RESPONSIBILITY PATTERN:
    # 1. Separation of concerns - Each validator handles a specific aspect
    # 2. Extensibility - New validators can be added without changing existing code
    # 3. Flexibility - The chain can be reconfigured or reused in different tests
    # 4. Single Responsibility - Each class has one reason to change

    # Define the validation chain by nesting handlers
    # Each handler gets the next one as a constructor parameter
    validator_chain = StatusCodeValidator(
        JsonValidator(
            FieldValidator(["id", "name", "email"])
        )
    )

    # Start the validation chain with the first handler
    if validator_chain.handle(response):
        print("🎉 API Test Passed:", response.json())
    else:
        print("❌ API Test Failed")


# Run test
test_api()
