import requests


def test_api_without_pattern():
    # Make API request to an external service
    response = requests.get("https://jsonplaceholder.typicode.com/users/1")

    # PROBLEM: Sequential validation approach with many early returns
    # This implementation suffers from:
    # 1. Poor maintainability - Each new validation requires modifying this function
    # 2. Low reusability - Validation logic cannot be easily reused in other tests
    # 3. Fixed execution order - Validations always run in the same sequence
    # 4. Rigid error handling - Each validation immediately stops the process

    # Validation 1: Check if status code is 200 (OK)
    if response.status_code != 200:
        print(f"❌ Invalid status code: {response.status_code}")
        print("❌ API Test Failed")
        return
    print("✅ Status code is valid")

    # Validation 2: Ensure response can be parsed as valid JSON
    try:
        data = response.json()
        print("✅ Response is valid JSON")
    except ValueError:
        print("❌ Response is not valid JSON")
        print("❌ API Test Failed")
        return

    # Validation 3: Verify all required fields exist in the JSON response
    required_fields = ["id", "name", "email"]
    for field in required_fields:
        if field not in data:
            print(f"❌ Missing field: {field}")
            print("❌ API Test Failed")
            return
    print("✅ All required fields are present")

    # If all validations pass, report success and show response data
    print("🎉 API Test Passed:", data)


# Run test
test_api_without_pattern()
