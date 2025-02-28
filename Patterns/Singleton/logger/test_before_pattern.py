import sqlite3
import logging


def setup_database():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()


class UserTests:
    def __init__(self):
        # Creates new logger for each test class
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('test.log')
        self.logger.addHandler(handler)

    def test_create_user(self):
        # Creates another connection
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                       ("John Doe", "john@example.com"))
        conn.commit()

    def test_get_user(self):
        # Yet another connection
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", ("John Doe",))
        return cursor.fetchone()


class ProductTests:
    def __init__(self):
        # Another separate logger instance
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('test.log')
        self.logger.addHandler(handler)

    def test_add_product(self):
        # Another separate DB connection
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)",
                       ("Test Product", 99.99))
        conn.commit()


setup_database()
user_test = UserTests()
user_test.test_create_user()
user_test.test_get_user()

product_test = ProductTests()
product_test.test_add_product()
