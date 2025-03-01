import sqlite3

# Factory class to handle database connections, improving code reuse and maintainability.
class DBFactory:
    """Simple factory for database connections"""

    @staticmethod
    def get_connection(db_type, mysql=None):
        """Create and return a database connection based on type"""
        if db_type == "sqlite":
            return sqlite3.connect('test.db')
        elif db_type == "mysql":
            return mysql.connector.connect(
                host="localhost",
                user="test_user",
                password="test_password",
                database="test_db"
            )
        else:
            # Handles unsupported database types cleanly
            raise ValueError(f"Unsupported database type: {db_type}")


# This class now relies on the factory to obtain database connections,
# removing duplicated connection logic and making the code more maintainable.
class TestDatabaseWithFactory:
    def execute_query(self, db_type, query):
        # Get connection from factory (removes the need to handle connections in each test method)
        conn = DBFactory.get_connection(db_type)
        cursor = conn.cursor()

        try:
            # Execute query
            cursor.execute(query)
            result = cursor.fetchone()
            return result
        finally:
            # Always cleanup (ensuring proper resource management)
            cursor.close()
            conn.close()

    def test_sqlite_query(self):
        # Now the test method simply calls execute_query without handling the connection manually
        result = self.execute_query("sqlite", "SELECT name FROM users WHERE id = 1")
        assert result[0] == "John Doe"

    def test_mysql_query(self):
        # Uses the factory to handle MySQL connection
        result = self.execute_query("mysql", "SELECT name FROM users WHERE id = 1")
        assert result[0] == "John Doe"

# Benefits of this approach:
# - Removes redundant database connection handling.
# - If a new database type is added, we only modify the factory.
# - Follows the DRY principle, making the code more scalable and maintainable.
