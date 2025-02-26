import functools


def cleanup_test_data(func):
    """
    Ensures test data is cleaned up after test execution
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        finally:
            # Clean up database records created during test
            if hasattr(self, 'created_records'):
                for record_id in self.created_records:
                    self.delete_test_record(record_id)

            # Clean up uploaded files
            if hasattr(self, 'uploaded_files'):
                for file_path in self.uploaded_files:
                    self.delete_test_file(file_path)

    return wrapper