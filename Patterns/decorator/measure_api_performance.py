import functools
import time
import requests
import pytest
import allure


def measure_api_performance(threshold_ms=1000):
    """
    Measures API response time and fails the test if it exceeds the threshold.

    This is a parametrized decorator - it takes an argument (threshold_ms)
    and returns a decorator function. This allows us to customize the
    decorator's behavior when applying it to different functions.
    """

    # This is the actual decorator function that receives the function to be decorated
    def decorator(func):
        # Preserve the metadata of the original function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Record the start time before calling the function
            start_time = time.time()
            # Call the original function
            result = func(*args, **kwargs)
            # Record the end time after the function completes
            end_time = time.time()

            # Calculate response time in milliseconds
            response_time = (end_time - start_time) * 1000

            # Add performance metrics to Allure report for visualization
            allure.attach(
                f"Response Time: {response_time:.2f}ms\nThreshold: {threshold_ms}ms",
                name="Performance Metrics",
                attachment_type=allure.attachment_type.TEXT
            )

            # Assert that the response time is within the threshold
            # If not, the test will fail with this message
            assert response_time <= threshold_ms, (
                f"API response time ({response_time:.2f}ms) "
                f"exceeded threshold ({threshold_ms}ms)"
            )
            # Return the original function's result
            return result

        # Return the wrapper function
        return wrapper

    # Return the decorator function
    return decorator


class TestAPIPerformance:

    @allure.title("Test public API response time")
    @allure.description("Verifies that the JSONPlaceholder API responds within the threshold")
    # Apply our decorator with a custom threshold of 500ms
    @measure_api_performance(threshold_ms=1000)
    def test_jsonplaceholder_api(self):
        """Test the performance of a public API endpoint"""
        # Make the actual API call
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        response.raise_for_status()  # Raise exception for 4XX/5XX responses

        # Verify the response content
        data = response.json()
        assert data["id"] == 1
        return response

    @allure.title("Test slow API response time")
    @allure.description("This test will likely fail due to the API being slower than threshold")
    # Apply our decorator with a very strict threshold that will likely cause the test to fail
    @measure_api_performance(threshold_ms=50)
    def test_slow_api(self):
        """Test that will likely fail due to strict threshold"""
        # This API has a deliberate 1 second delay, which will exceed our 50ms threshold
        response = requests.get("https://httpbin.org/delay/1")
        response.raise_for_status()
        return response


if __name__ == "__main__":
    pytest.main(["-v"])
