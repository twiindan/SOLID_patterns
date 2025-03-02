import sqlite3
import logging


def setup_database():
    # Creates a new database connection each time it's called
    # This is inefficient as connections are expensive resources
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
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

    # Commit changes and close connection
    # After this function returns, the connection is lost
    conn.commit()
    conn.close()


class UserTests:
    def __init__(self):
        # PROBLEM: Creates new logger for each test class instance
        # This causes duplicate log handlers and repeated log entries
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('test.log')
        self.logger.addHandler(handler)  # Logger handlers accumulate with each instance

    def test_create_user(self):
        # PROBLEM: Creates another connection for each test
        # No connection reuse or management
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                       ("John Doe", "john@example.com"))
        conn.commit()

    def test_get_user(self):
        # PROBLEM: Yet another connection created
        # Resource-intensive and lacks connection management
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", ("John Doe",))
        return cursor.fetchone()


class ProductTests:
    def __init__(self):
        # PROBLEM: Another separate logger instance
        # Creates duplicate handlers again
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('test.log')
        self.logger.addHandler(handler)  # More handler duplication

    def test_add_product(self):
        # PROBLEM: Another separate DB connection
        # No reuse of existing connections
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)",
                       ("Test Product", 99.99))
        conn.commit()


# Main execution
# Multiple connections are created and never properly closed
setup_database()
user_test = UserTests()
user_test.test_create_user()
user_test.test_get_user()

product_test = ProductTests()
product_test.test_add_product()
