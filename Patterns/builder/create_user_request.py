import requests


class UserService:

    def __init__(self):
        self.url = 'https://catfact.ninja/fact'
        self.params = None
        self.body = None
        self.headers = None

    def with_body(self, body):
        self.body = body
        return self
    
    def with_headers(self, headers):
        self.headers = headers
        return self
    
    def with_query_parameters(self, qp):
        self.params = qp
        return self

    def send_request(self):
        return requests.get(url=self.url, json=self.body, headers=self.headers, params=self.params)


user_model = {'name': 'Toni'}
headers = {'accept': "application/json"}
user_service = UserService()
response = user_service.with_body(user_model).with_headers(headers).send_request()
print(response.text)