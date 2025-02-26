import requests


# Observer class
class APIObserver:
    @staticmethod
    def before_request(method, url, **kwargs):
        print(f"Sending {method.upper()} request to {url}")
        if "json" in kwargs:
            print(f"Payload: {kwargs['json']}")

    @staticmethod
    def after_response(response):
        print(f"Response from {response.url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text[:100]}...")  # Limit output


# Wrapper around requests.Session with event hooks
class ObservableSession(requests.Session):
    def __init__(self, observer):
        super().__init__()
        self.observer = observer

    def request(self, method, url, *args, **kwargs):
        self.observer.before_request(method, url, **kwargs)
        response = super().request(method, url, *args, **kwargs)
        self.observer.after_response(response)
        return response


# Instantiate observer and session
observer = APIObserver()
session = ObservableSession(observer)

# Sending a GET request
session.get("https://jsonplaceholder.typicode.com/posts/1")

# Sending a POST request
data = {"title": "foo", "body": "bar", "userId": 1}
session.post("https://jsonplaceholder.typicode.com/posts", json=data)