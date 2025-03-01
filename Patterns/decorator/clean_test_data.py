import functools


def cleanup_test_data(func):
    """
    Ensures test data is cleaned up after test execution.

    This is a decorator that wraps test functions to ensure any test data
    created during the test is properly cleaned up, even if the test fails.
    """

    # functools.wraps preserves the metadata of the original function
    # (like name, docstring, etc.) in the wrapped function
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # The wrapper function receives the same arguments as the original function
        try:
            # Execute the original test function
            return func(self, *args, **kwargs)
        finally:
            # The finally block ensures cleanup happens whether the test succeeds or fails

            # Clean up database records created during test
            if hasattr(self, 'created_records'):
                for record_id in self.created_records:
                    self.delete_test_record(record_id)

            # Clean up uploaded files
            if hasattr(self, 'uploaded_files'):
                for file_path in self.uploaded_files:
                    self.delete_test_file(file_path)

    # Return the wrapper function - this is what will be executed
    # when the decorated function is called
    return wrapper
