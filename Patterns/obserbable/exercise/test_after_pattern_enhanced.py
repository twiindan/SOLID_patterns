import requests
import time


# Observer class - advanced implementation
# This class is responsible for monitoring API requests and responses with enhanced capabilities
class APIObserver:
    def __init__(self, slow_threshold=2.0):  # Constructor with configurable threshold
        # Threshold for identifying slow responses (in seconds)
        self.slow_threshold = slow_threshold

    # Method called before a request is sent
    # Provides detailed logging about the outgoing request
    @staticmethod
    def before_request(method, url, **kwargs):
        print(f"➡️ Sending {method.upper()} request to {url}")
        if "json" in kwargs:
            print(f"📤 Payload: {kwargs['json']}")

    # Method called after a response is received
    # Provides detailed logging about the response and timing analysis
    def after_response(self, response, elapsed_time):
        print(f"✅ Response from {response.url}")
        print(f"🔄 Status Code: {response.status_code}")
        print(f"📄 Response Body: {response.text[:100]}...")  # Truncated output

        # Performance monitoring - detect slow responses
        # This demonstrates how the Observer can be extended with new capabilities
        if elapsed_time > self.slow_threshold:
            print(f"⚠️ WARNING: Slow response ({elapsed_time:.2f}s) for {response.url}")

    # Method called when an error occurs
    # Handles and logs error situations
    @staticmethod
    def on_error(method, url, error):
        print(f"❌ ERROR: {method.upper()} request to {url} failed with error: {error}")


# Subject class in the Observer pattern - enhanced version
# This class extends requests.Session with comprehensive monitoring capabilities
class ObservableSession(requests.Session):
    def __init__(self, observer):
        super().__init__()
        self.observer = observer  # The observer that will monitor this session

    # Override the request method to add observation hooks with error handling and timing
    def request(self, method, url, *args, **kwargs):
        # Notify observer before making the request
        self.observer.before_request(method, url, **kwargs)

        # Start timing the request for performance monitoring
        start_time = time.time()

        try:
            # Make the actual request (core functionality)
            response = super().request(method, url, *args, **kwargs)

            # Calculate response time
            elapsed_time = time.time() - start_time

            # Notify observer after receiving the response
            self.observer.after_response(response, elapsed_time)

            return response

        except requests.RequestException as e:  # Error handling
            # Notify observer about the error
            self.observer.on_error(method, url, e)
            return None  # Return None instead of raising exception


# Instantiate observer with custom configuration
observer = APIObserver(slow_threshold=2.0)  # Set slow response threshold
session = ObservableSession(observer)

# Sending a GET request (Normal response)
# The code remains clean while providing enhanced monitoring
session.get("https://jsonplaceholder.typicode.com/posts/1")

# Sending a POST request (Normal response)
data = {"title": "foo", "body": "bar", "userId": 1}
session.post("https://jsonplaceholder.typicode.com/posts", json=data)

# Sending a request to a non-existent URL (Triggers error handling)
# This demonstrates the error handling capabilities
session.get("https://notexisturlinallinternet.com")

# Simulating a slow request using a delayed API endpoint
# This demonstrates the performance monitoring capabilities
session.get("https://httpbin.org/delay/3")  # Should trigger slow request warning

# ADVANCED BENEFITS OF THIS APPROACH:
# 1. All basic Observer pattern benefits (separation of concerns, reusability)
# 2. Enhanced error handling - centralized and consistent
# 3. Performance monitoring capabilities
# 4. Configurable behavior (e.g., slow_threshold)
# 5. The code can handle edge cases without disrupting the main functionality
# 6. Can be further extended with additional monitoring capabilities
