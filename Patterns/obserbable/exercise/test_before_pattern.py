import requests

# Sending a GET request
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(f"Sent GET request to {response.url}")
print(f"Response Status Code: {response.status_code}")

# Sending a POST request
data = {"title": "foo", "body": "bar", "userId": 1}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=data)
print(f"Sent POST request to {response.url}")
print(f"Response Status Code: {response.status_code}")

