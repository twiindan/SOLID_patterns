import requests

# Create a new user
print("Creating a new user...")
response = requests.post("https://jsonplaceholder.typicode.com/users", json={"name": "John Doe"})
print(f"Response: {response.status_code}, {response.json()}")

# Get user details
print("Fetching user details...")
response = requests.get("https://jsonplaceholder.typicode.com/users/1")
print(f"Response: {response.status_code}, {response.json()}")

# Update user info
print("Updating user info...")
response = requests.put("https://jsonplaceholder.typicode.com/users/1", json={"name": "John Updated"})
print(f"Response: {response.status_code}, {response.json()}")

# Delete user
print("Deleting user...")
response = requests.delete("https://jsonplaceholder.typicode.com/users/1")
print(f"Response: {response.status_code}")
