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
        """
        Send a GET request with optional body, headers, and query parameters.

        Args:
            body: JSON body to send with the request
            headers: HTTP headers to include in the request
            params: Query parameters to append to the URL

        Returns:
            Response object from the requests library

        Raises:
            requests.RequestException: If the request fails
        """
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


# Example usage - Method 1: Creating variables first
# Using variables makes the code more readable, but all parameters
# still need to be passed in a single function call
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

# Example usage - Method 2: Direct call with dictionaries
# This is a more compact approach, but becomes harder to read with more parameters
response = RestClient().send_get_request(
    body={'name': 'Toni'},
    headers={'accept': "application/json"},
    params={'page': 1}
)
print(response.text)
