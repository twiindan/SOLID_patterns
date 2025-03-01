import sqlite3
import mysql.connector

# This class directly manages database connections and queries without abstraction,
# leading to duplicated code and making it harder to maintain.
class TestDatabaseWithoutFactory:
    def test_sqlite_query(self):
        # SQLite setup (Direct connection handling)
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()

        # Execute test query
        cursor.execute("SELECT name FROM users WHERE id = 1")
        result = cursor.fetchone()

        # Cleanup (Needs to be repeated in each test method)
        cursor.close()
        conn.close()

        # Assertion
        assert result[0] == "John Doe"

    def test_mysql_query(self):
        # MySQL setup - duplicated database handling logic
        conn = mysql.connector.connect(
            host="localhost",
            user="test_user",
            password="test_password",
            database="test_db"
        )
        cursor = conn.cursor()

        # Execute test query
        cursor.execute("SELECT name FROM users WHERE id = 1")
        result = cursor.fetchone()

        # Cleanup (Repeated again)
        cursor.close()
        conn.close()

        # Assertion
        assert result[0] == "John Doe"

# The issue with this approach:
# - The connection logic is duplicated for each database type.
# - If a new database is introduced, every method must be modified.
# - Violates the DRY (Don't Repeat Yourself) principle.
