import sqlite3


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
    def __init__(self):
        database_manager = DataBaseManager()
        self.db_connection = database_manager.create_connection()
        self.cursor = self.db_connection.cursor()

    def create_tables(self):
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS projects (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            begin_date text,
                                            end_date text
                                        ); """)
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

    table_creator = TableCreation()
    table_creator.create_tables()


if __name__ == '__main__':
    main()
