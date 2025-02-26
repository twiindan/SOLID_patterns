import requests


# Base Handler
class Handler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, response):
        if self.next_handler:
            return self.next_handler.handle(response)
        return True


# Concrete Handlers
class StatusCodeValidator(Handler):
    def handle(self, response):
        if response.status_code != 200:
            print(f"❌ Invalid status code: {response.status_code}")
            return False
        print("✅ Status code is valid")
        return super().handle(response)


class JsonValidator(Handler):
    def handle(self, response):
        try:
            response.json()
            print("✅ Response is valid JSON")
        except ValueError:
            print("❌ Response is not valid JSON")
            return False
        return super().handle(response)


class FieldValidator(Handler):
    def __init__(self, required_fields, next_handler=None):
        super().__init__(next_handler)
        self.required_fields = required_fields

    def handle(self, response):
        data = response.json()
        for field in self.required_fields:
            if field not in data:
                print(f"❌ Missing field: {field}")
                return False
        print("✅ All required fields are present")
        return super().handle(response)


# API Test using Chain of Responsibility
def test_api():
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")

    # Define chain of responsibility
    validator_chain = StatusCodeValidator(
        JsonValidator(
            FieldValidator(["id", "name", "email"])
        )
    )

    # Execute chain
    if validator_chain.handle(response):
        print("🎉 API Test Passed:", response.json())
    else:
        print("❌ API Test Failed")


# Run test
test_api()
