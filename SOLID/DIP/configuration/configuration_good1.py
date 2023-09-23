class Config():

    def __init__(self, database, user, password, host, port):

        self.database = database
        self.username = user
        self.password = password
        self.host = host
        self.port = port


class DataBaseConnection():

    def __init__(self, config):
        self.config = config

    def connect(self):

        #Code to connect Database
        pass


development_config = ('sql', 'toni', '1234', 'localhost', '4444')
testing_config = ('sql', 'toni2', '0000', 'testing_server.com', '4444')
production_config = ('sql', 'toni3', '9999', 'production_server.com', '4444')

dev_database_connection = DataBaseConnection(development_config)
testing_database_connection = DataBaseConnection(testing_config)
prod_database_connection = DataBaseConnection(production_config)
