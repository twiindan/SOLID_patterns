import requests
import time


# Observer class
class APIObserver:
    def __init__(self, slow_threshold=2.0):  # Threshold for slow responses in seconds
        self.slow_threshold = slow_threshold

    @staticmethod
    def before_request(method, url, **kwargs):
        print(f"➡️ Sending {method.upper()} request to {url}")
        if "json" in kwargs:
            print(f"📤 Payload: {kwargs['json']}")

    def after_response(self, response, elapsed_time):
        print(f"✅ Response from {response.url}")
        print(f"🔄 Status Code: {response.status_code}")
        print(f"📄 Response Body: {response.text[:100]}...")  # Truncated output

        # Check if the request was slow
        if elapsed_time > self.slow_threshold:
            print(f"⚠️ WARNING: Slow response ({elapsed_time:.2f}s) for {response.url}")

    @staticmethod
    def on_error(method, url, error):
        print(f"❌ ERROR: {method.upper()} request to {url} failed with error: {error}")


# Wrapper around requests.Session with event hooks
class ObservableSession(requests.Session):
    def __init__(self, observer):
        super().__init__()
        self.observer = observer

    def request(self, method, url, *args, **kwargs):
        self.observer.before_request(method, url, **kwargs)
        start_time = time.time()  # Start time tracking

        try:
            response = super().request(method, url, *args, **kwargs)
            elapsed_time = time.time() - start_time  # Calculate response time
            self.observer.after_response(response, elapsed_time)
            return response

        except requests.RequestException as e:  # Catch request errors
            self.observer.on_error(method, url, e)
            return None


# Instantiate observer and session
observer = APIObserver(slow_threshold=2.0)  # Set slow response threshold
session = ObservableSession(observer)

# Sending a GET request (Normal response)
session.get("https://jsonplaceholder.typicode.com/posts/1")

# Sending a POST request (Normal response)
data = {"title": "foo", "body": "bar", "userId": 1}
session.post("https://jsonplaceholder.typicode.com/posts", json=data)

# Sending a request to a non-existent URL (Triggers error handling)
session.get("https://notexisturlinallinternet.com")

# Simulating a slow request using a delayed API endpoint (Adjust timeout as needed)
session.get("https://httpbin.org/delay/3")  # Should trigger slow request warning