import functools
import time
import requests
import pytest
import allure


def measure_api_performance(threshold_ms=1000):
    """
    Measures API response time and fails the test if it exceeds the threshold
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            response_time = (end_time - start_time) * 1000  # Convert to milliseconds

            # Add performance metrics to Allure report
            allure.attach(
                f"Response Time: {response_time:.2f}ms\nThreshold: {threshold_ms}ms",
                name="Performance Metrics",
                attachment_type=allure.attachment_type.TEXT
            )

            assert response_time <= threshold_ms, (
                f"API response time ({response_time:.2f}ms) "
                f"exceeded threshold ({threshold_ms}ms)"
            )
            return result

        return wrapper

    return decorator


class TestAPIPerformance:

    @allure.title("Test public API response time")
    @allure.description("Verifies that the JSONPlaceholder API responds within the threshold")
    @measure_api_performance(threshold_ms=500)  # Set a 500ms threshold
    def test_jsonplaceholder_api(self):
        """Test the performance of a public API endpoint"""
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        response.raise_for_status()  # Raise exception for 4XX/5XX responses

        # Verify the response content
        data = response.json()
        assert data["id"] == 1
        return response

    @allure.title("Test slow API response time")
    @allure.description("This test will likely fail due to the API being slower than threshold")
    @measure_api_performance(threshold_ms=50)  # Set a very strict 50ms threshold
    def test_slow_api(self):
        """Test that will likely fail due to strict threshold"""
        response = requests.get("https://httpbin.org/delay/1")  # This API has a deliberate 1 second delay
        response.raise_for_status()
        return response


if __name__ == "__main__":
    pytest.main(["-v"])