import sqlite3
import mysql.connector


class TestDatabaseWithoutFactory:
    def test_sqlite_query(self):
        # SQLite setup
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()

        # Execute test query
        cursor.execute("SELECT name FROM users WHERE id = 1")
        result = cursor.fetchone()

        # Cleanup
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

        # Cleanup
        cursor.close()
        conn.close()

        # Assertion
        assert result[0] == "John Doe"
