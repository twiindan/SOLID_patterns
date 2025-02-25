from typing import Optional, Dict, Any
import requests
from requests import Response


class RestBuilder:

    def __init__(self, url: str = 'https://catfact.ninja/fact'):
        """
        Initialize RestBuilder with default values

        Args:
            url (str): Target URL for the request
        """
        self.url: str = url
        self.params: Optional[Dict[str, Any]] = None
        self.body: Optional[Dict[str, Any]] = None
        self.headers: Optional[Dict[str, str]] = None

    def with_body(self, body: Dict[str, Any]) -> 'RestBuilder':

        self.body = body
        return self

    def with_headers(self, headers: Dict[str, str]) -> 'RestBuilder':

        self.headers = headers
        return self

    def with_query_parameters(self, params: Dict[str, Any]) -> 'RestBuilder':

        self.params = params
        return self

    def send_request(self) -> Response:

        try:
            response = requests.get(
                url=self.url,
                json=self.body,
                headers=self.headers,
                params=self.params,
                timeout=30
            )
            response.raise_for_status()
            return response

        except requests.RequestException as e:
            # Re-raise the exception after logging if needed
            raise


# Example usage
if __name__ == "__main__":
    user_model = {'name': 'Toni'}
    headers = {'accept': "application/json"}

    rest_service = RestBuilder()
    response = (
        rest_service
            .with_body(user_model)
            .with_headers(headers)
            .send_request()
    )
    print(response.text)