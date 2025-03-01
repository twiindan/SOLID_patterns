import sqlite3


class DataBaseManager:
    """
    Manages database connections.
    Responsible for creating and providing database connections.
    """

    def __init__(self):
        self.connection = None

    def create_connection(self):
        """Creates and returns a connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect("../data.db")
            return self.connection
        except:
            print("error creating connection")


class TableCreation:
    """
    Handles the creation of database tables.

    ANTI-PATTERN: No Dependency Injection
    - This class creates its own dependencies internally (tight coupling)
    - Dependencies are hardcoded within the class
    - Makes testing difficult as you cannot easily substitute components
    """

    def __init__(self):
        # PROBLEM: Creates its own DatabaseManager instance (tight coupling)
        database_manager = DataBaseManager()

        # PROBLEM: Directly depends on the concrete implementation
        self.db_connection = database_manager.create_connection()
        self.cursor = self.db_connection.cursor()

    def create_tables(self):
        """
        Creates tables with hardcoded SQL queries.

        PROBLEMS:
        - SQL queries are hardcoded in the method (not separated)
        - No way to create only one table or use different queries
        - Changes to the queries require changing this class
        """
        # Hardcoded SQL for projects table
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS projects (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            begin_date text,
                                            end_date text
                                        ); """)
        # Hardcoded SQL for tasks table
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        priority integer,
                                        status_id integer NOT NULL,
                                        project_id integer NOT NULL,
                                        begin_date text NOT NULL,
                                        end_date text NOT NULL,
                                        FOREIGN KEY (project_id) REFERENCES projects (id)
                                    );""")
        print("table created")


def main():
    """
    Main function that shows the usage without dependency injection:
    - Components are tightly coupled
    - No way to easily change or mock components for testing
    """
    # Creates TableCreation which internally creates all its dependencies
    table_creator = TableCreation()

    # Limited flexibility - can only create both tables with hardcoded queries
    table_creator.create_tables()


if __name__ == '__main__':
    main()
