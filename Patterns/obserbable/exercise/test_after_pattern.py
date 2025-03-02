import requests


# Observer class - implements the Observer pattern
# This class is responsible for monitoring API requests and responses
class APIObserver:
    # Method called before a request is sent
    # Observes and logs details about the outgoing request
    @staticmethod
    def before_request(method, url, **kwargs):
        print(f"Sending {method.upper()} request to {url}")
        if "json" in kwargs:
            print(f"Payload: {kwargs['json']}")

    # Method called after a response is received
    # Observes and logs details about the incoming response
    @staticmethod
    def after_response(response):
        print(f"Response from {response.url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text[:100]}...")  # Limit output


# Subject class in the Observer pattern
# This class wraps requests.Session to add observation points
class ObservableSession(requests.Session):
    def __init__(self, observer):
        super().__init__()
        self.observer = observer  # The observer that will monitor this session

    # Override the request method to add observation hooks
    def request(self, method, url, *args, **kwargs):
        # Notify observer before making the request
        self.observer.before_request(method, url, **kwargs)

        # Make the actual request (core functionality)
        response = super().request(method, url, *args, **kwargs)

        # Notify observer after receiving the response
        self.observer.after_response(response)

        return response


# Instantiate observer and observable session
observer = APIObserver()
session = ObservableSession(observer)

# Sending a GET request
# Note how the code focuses on what to do, not on monitoring
session.get("https://jsonplaceholder.typicode.com/posts/1")

# Sending a POST request
# Again, clean code without monitoring logic mixed in
data = {"title": "foo", "body": "bar", "userId": 1}
session.post("https://jsonplaceholder.typicode.com/posts", json=data)

# BENEFITS OF THIS APPROACH:
# 1. Clear separation between making requests and monitoring them
# 2. Centralized monitoring logic in the Observer class
# 3. Can modify monitoring behavior without changing the request code
# 4. Reusable - all requests automatically get the same monitoring
