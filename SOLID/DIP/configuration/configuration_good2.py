from abc import ABC, abstractmethod


# SOLUTION PART 1: Create an abstract base configuration class
# This follows DIP by defining an abstraction that both high and low-level modules depend on
class Config(ABC):
    # Abstract base class that defines the configuration interface
    @abstractmethod
    def __init__(self, host, port):
        # Basic configuration that all database configs should have
        self.host = host
        self.port = port


# SOLUTION PART 2: Create specific configuration implementations
# Each concrete config class extends the abstract base class
class SQLConfig(Config):
    # SQL-specific configuration
    def __init__(self, user, password, host, port):
        self.username = user
        self.password = password
        self.host = host
        self.port = port


class RedisConfig(Config):
    # Redis-specific configuration (simpler, doesn't need credentials)
    def __init__(self, host, port):
        self.host = host
        self.port = port


class MongoConfig(Config):
    # MongoDB-specific configuration (more complex, needs database name)
    def __init__(self, user, password, host, port, database):
        self.username = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database


# SOLUTION PART 3: Database connection class depends on the abstraction
class DataBaseConnections:
    # Type hint enforces that only Config or its subclasses can be passed
    def __init__(self, config: Config):
        # Takes any implementation of Config interface
        self.config = config

    def connect(self):
        #Code to connect Database
        pass

# COMPLETE BENEFITS OF THIS IMPLEMENTATION:
# 1. High-level module (DataBaseConnections) depends on abstraction (Config), not concrete implementations
# 2. Different database types have their own specialized config classes, all following the same interface
# 3. New database types can be added by creating new Config subclasses without changing existing code
# 4. Type checking ensures only valid Config objects are passed to DataBaseConnections
# 5. Clear separation between different types of configurations
# 6. Fully follows DIP: "Depend upon abstractions, not concretions"
# 7. Easy to test with mock implementations
# 8. Different environments (dev, test, prod) can be supported by creating different instances
#    of the appropriate config classes
