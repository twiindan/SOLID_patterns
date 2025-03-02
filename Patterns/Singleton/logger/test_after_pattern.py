import json
import logging
import sqlite3


class DatabaseManager:
    # Class variables shared by all instances
    _instance = None  # Will store the singleton instance
    _connection = None  # Will store the database connection

    def __new__(cls):
        # SINGLETON PATTERN: This method controls instance creation
        # If an instance doesn't exist, create it. Otherwise, return existing instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def connection(self):
        # LAZY INITIALIZATION: Only create the connection when first needed
        # This saves resources if the connection isn't used
        if self._connection is None:
            self._connection = sqlite3.connect('test.db')
            self._connection.row_factory = sqlite3.Row  # Returns rows as dict-like objects
            self.setup_database()
        return self._connection

    def execute_query(self, query, params=None):
        # Centralized query execution method
        # Allows for consistent error handling and connection management
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor

    def close(self):
        # Proper resource cleanup
        if self._connection:
            self._connection.close()
            self._connection = None

    def setup_database(self):
        # Now part of the DatabaseManager class
        # Only runs once when the connection is first established
        cursor = self._connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        self._connection.commit()


class TestLogger:
    # Another Singleton implementation for logger
    _instance = None
    _logger = None

    def __new__(cls):
        # SINGLETON PATTERN: Ensures only one TestLogger instance exists
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def logger(self):
        # LAZY INITIALIZATION: Only create logger when needed
        if self._logger is None:
            self._logger = logging.getLogger('test_logger')
            self._logger.setLevel(logging.INFO)

            # Add file handler if not exists
            # Prevents duplicate handlers by checking first
            if not self._logger.handlers:
                handler = logging.FileHandler('test.log')
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                handler.setFormatter(formatter)
                self._logger.addHandler(handler)

        return self._logger


class TestBase:
    # Base class for all test classes
    # Provides common functionality and access to shared resources
    def __init__(self):
        # Use singleton instances for both database and logger
        self.db = DatabaseManager()
        self.logger = TestLogger().logger

    def teardown(self):
        # Common cleanup method
        self.db.connection.commit()


class UserTests(TestBase):
    # Inherits from TestBase to get access to db and logger
    def test_create_user(self):
        try:
            user_data = {
                "name": "John Doe",
                "email": "john@example.com"
            }

            # Uses the centralized execute_query method
            self.db.execute_query(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (user_data["name"], user_data["email"])
            )

            self.logger.info(f"Created user: {json.dumps(user_data)}")
            return True

        except Exception as e:
            self.logger.error(f"Error creating user: {str(e)}")
            return False

    def test_get_user(self, name):
        try:
            # Reuses the same database connection
            cursor = self.db.execute_query(
                "SELECT * FROM users WHERE name = ?",
                (name,)
            )
            user = cursor.fetchone()

            if user:
                self.logger.info(f"Retrieved user: {dict(user)}")
            else:
                self.logger.warning(f"User not found: {name}")

            return dict(user) if user else None

        except Exception as e:
            self.logger.error(f"Error retrieving user: {str(e)}")
            return None


class ProductTests(TestBase):
    # Also inherits from TestBase
    def test_add_product(self):
        try:
            product_data = {
                "name": "Test Product",
                "price": 99.99
            }

            # Reuses the same database connection
            self.db.execute_query(
                "INSERT INTO products (name, price) VALUES (?, ?)",
                (product_data["name"], product_data["price"])
            )

            self.logger.info(f"Added product: {json.dumps(product_data)}")
            return True

        except Exception as e:
            self.logger.error(f"Error adding product: {str(e)}")
            return False


# Example usage
def run_tests():
    # User tests
    user_tests = UserTests()
    user_tests.test_create_user()
    user = user_tests.test_get_user("John Doe")
    user_tests.teardown()

    # Product tests
    product_tests = ProductTests()
    product_tests.test_add_product()
    product_tests.teardown()

    # Clean up database connection at the end
    # Only one connection to close, regardless of how many tests ran
    DatabaseManager().close()


run_tests()
