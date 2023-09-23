from abc import ABC, abstractmethod


class Config(ABC):

    @abstractmethod
    def __init__(self, host, port):

        self.host = host
        self.port = port


class SQLConfig(Config):

    def __init__(self, user, password, host, port):
        self.username = user
        self.password = password
        self.host = host
        self.port = port


class RedisConfig(Config):

    def __init__(self, host, port):

        self.host = host
        self.port = port


class MongoConfig(Config):

    def __init__(self, user, password, host, port, database):
        self.username = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database


class DataBaseConnections:

    def __init__(self, config: Config):
        self.config = config

    def connect(self):

        #Code to connect Database
        pass
