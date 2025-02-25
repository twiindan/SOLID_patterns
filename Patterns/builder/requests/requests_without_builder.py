import requests
from typing import Dict, Any, Optional


class RestClient:

    def __init__(self, url: str = 'https://catfact.ninja/fact'):
        self.url = url

    def send_get_request(
            self,
            body: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None
    ):

        try:
            response = requests.get(
                url=self.url,
                json=body,
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response

        except requests.RequestException as e:
            raise


# Example usage - Method 1: Passing all parameters at once
rest_client = RestClient()
user_model = {'name': 'Toni'}
headers = {'accept': "application/json"}
response = rest_client.send_get_request(
    body=user_model,
    headers=headers
)
print(response.text)

# Example usage - Method 2: Creating variables first
rest_client2 = RestClient()
body_data = {'name': 'Toni'}
header_data = {'accept': "application/json"}
param_data = {'page': 1}

response = rest_client2.send_get_request(
    body=body_data,
    headers=header_data,
    params=param_data
)
print(response.text)

# Example usage - Method 3: Direct call with dictionaries
response = RestClient().send_get_request(
    body={'name': 'Toni'},
    headers={'accept': "application/json"},
    params={'page': 1}
)
print(response.text)