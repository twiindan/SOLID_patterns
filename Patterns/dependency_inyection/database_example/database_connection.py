import sqlite3


class QueryRepository:
    """
    Repository class that encapsulates SQL queries.
    This separates query definitions from their execution.
    """

    def __init__(self):
        # SQL query to create the projects table if it doesn't exist
        self.sql_create_projects_table_query = """ CREATE TABLE IF NOT EXISTS projects (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            begin_date text,
                                            end_date text
                                        ); """

        # SQL query to create the tasks table if it doesn't exist
        self.sql_create_tasks_table_query = """CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        priority integer,
                                        status_id integer NOT NULL,
                                        project_id integer NOT NULL,
                                        begin_date text NOT NULL,
                                        end_date text NOT NULL,
                                        FOREIGN KEY (project_id) REFERENCES projects (id)
                                    );"""

    def get_create_project_table_query(self):
        """Returns the SQL query for creating the projects table."""
        return self.sql_create_projects_table_query

    def get_create_tasks_table(self):
        """Returns the SQL query for creating the tasks table."""
        return self.sql_create_tasks_table_query


class DataBaseManager():
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


class TableCreation():
    """
    Handles the creation of database tables.

    DEPENDENCY INJECTION PATTERN:
    - This class receives its database connection from outside (injected)
    - It doesn't create its own dependencies internally
    """

    def __init__(self, database_connection):
        # Dependency is injected through the constructor
        self.db_connection = database_connection
        self.cursor = self.db_connection.cursor()

    def create_table(self, table_query):
        """
        Creates a table using the provided SQL query.
        The query is also injected rather than hardcoded.
        """
        self.cursor.execute(table_query)
        print("table created")


def main():
    """
    Main function that demonstrates dependency injection:
    1. Creates the dependencies
    2. Injects them where needed
    3. Components are loosely coupled
    """
    # Create the database manager
    database_manager = DataBaseManager()

    # Get a connection from the manager
    database_connection = database_manager.create_connection()

    # Create the query repository
    query_repository = QueryRepository()

    # Inject the database connection into TableCreation
    table_creator = TableCreation(database_connection)

    # Use the table creator with queries from the repository
    table_creator.create_table(query_repository.get_create_project_table_query())
    table_creator.create_table(query_repository.get_create_tasks_table())


if __name__ == '__main__':
    main()
