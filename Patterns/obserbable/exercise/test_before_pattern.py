import requests

# This file demonstrates code WITHOUT using the Observer pattern
# It uses a direct, procedural approach to making API requests

# Sending a GET request
# The logging/monitoring code is directly mixed with the API calling code
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(f"Sent GET request to {response.url}")
print(f"Response Status Code: {response.status_code}")

# Sending a POST request
# Again, the monitoring is tightly coupled with the actual functionality
data = {"title": "foo", "body": "bar", "userId": 1}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=data)
print(f"Sent POST request to {response.url}")
print(f"Response Status Code: {response.status_code}")

# PROBLEMS WITH THIS APPROACH:
# 1. No separation between making requests and monitoring them
# 2. Logging is scattered throughout the code and mixed with business logic
# 3. To add new monitoring capabilities (e.g., timing, error handling), we'd need to modify each request
# 4. Cannot easily enable/disable or modify monitoring behavior
# 5. Code duplication - each request needs its own monitoring code
