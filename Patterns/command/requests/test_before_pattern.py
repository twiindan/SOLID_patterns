import requests

# PROBLEM: This approach lacks structure for API operations
# Issues with this implementation:
# 1. No way to track API operations for potential rollback
# 2. Hard-coded API endpoints scattered throughout the code
# 3. Operations cannot be reused or parameterized easily
# 4. No mechanism to undo changes if something goes wrong
# 5. Difficult to maintain as the number of API operations grows

# Create a new user
# Direct API call with no abstraction
print("Creating a new user...")
response = requests.post("https://jsonplaceholder.typicode.com/users", json={"name": "John Doe"})
print(f"Response: {response.status_code}, {response.json()}")

# Get user details
# Another direct API call with hardcoded endpoint
print("Fetching user details...")
response = requests.get("https://jsonplaceholder.typicode.com/users/1")
print(f"Response: {response.status_code}, {response.json()}")

# Update user info
# Update operation with no way to revert to previous state
print("Updating user info...")
response = requests.put("https://jsonplaceholder.typicode.com/users/1", json={"name": "John Updated"})
print(f"Response: {response.status_code}, {response.json()}")

# Delete user
# Delete operation with no way to recover the deleted resource
print("Deleting user...")
response = requests.delete("https://jsonplaceholder.typicode.com/users/1")
print(f"Response: {response.status_code}")