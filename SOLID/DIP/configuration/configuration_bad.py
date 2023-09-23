class Config():

    def __init__(self, database, user, password, host, port):

        self.database = database
        self.username = user
        self.password = password
        self.host = host
        self.port = port


class DataBaseConnections():

    def __init__(self):
        self.config = Config('sql', 'toni', '1234', 'localhost', '4444')

    def connect(self):

        #Code to connect Database
        pass

