import sqlite3


class QueryRepository:

    def __init__(self):
        self.sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            begin_date text,
                                            end_date text
                                        ); """

        self.sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
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
        return self.sql_create_projects_table

    def get_create_tasks_table(self):
        return self.sql_create_tasks_table


class DataBaseManager():
    def __init__(self):
        self.connection = None

    def create_connection(self):
        try:
            self.connection = sqlite3.connect("data.db")
            return self.connection
        except:
            print("error creating connection")


class TableCreation():
    def __init__(self, database_connection):
        self.db_connection = database_connection
        self.cursor = self.db_connection.cursor()

    def create_table(self, table_query):
        self.cursor.execute(table_query)
        print("table created")


def main():

    database_manager= DataBaseManager()
    database_connection = database_manager.create_connection()
    query_repository = QueryRepository()
    table_creator = TableCreation(database_connection)
    table_creator.create_table(query_repository.sql_create_projects_table)
    table_creator.create_table(query_repository.sql_create_tasks_table)

if __name__ == '__main__':
    main()
