import sqlite3


class DBFactory:
    """Simple factory for database connections"""

    @staticmethod
    def get_connection(db_type):
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
            raise ValueError(f"Unsupported database type: {db_type}")


class TestDatabaseWithFactory:
    def execute_query(self, db_type, query):
        # Get connection from factory
        conn = DBFactory.get_connection(db_type)
        cursor = conn.cursor()

        try:
            # Execute query
            cursor.execute(query)
            result = cursor.fetchone()
            return result
        finally:
            # Always cleanup
            cursor.close()
            conn.close()

    def test_sqlite_query(self):
        result = self.execute_query("sqlite", "SELECT name FROM users WHERE id = 1")
        assert result[0] == "John Doe"

    def test_mysql_query(self):
        result = self.execute_query("mysql", "SELECT name FROM users WHERE id = 1")
        assert result[0] == "John Doe"
