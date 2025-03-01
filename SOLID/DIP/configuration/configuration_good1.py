# First step of DIP application
# Moving from hardcoded configuration to dependency injection

class Config:
    # Configuration class remains the same
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.username = user
        self.password = password
        self.host = host
        self.port = port


class DataBaseConnection:
    # IMPROVEMENT 1: The class now accepts a configuration object through constructor
    # instead of creating it internally
    def __init__(self, config):
        # Configuration is now injected, enabling different configurations to be used
        self.config = config

    def connect(self):
        # Code to connect Database
        pass


# IMPROVEMENT 2: Different configurations can be defined outside the class
# and passed in as needed
development_config = ('sql', 'toni', '1234', 'localhost', '4444')
testing_config = ('sql', 'toni2', '0000', 'testing_server.com', '4444')
production_config = ('sql', 'toni3', '9999', 'production_server.com', '4444')

# IMPROVEMENT 3: We can now create different database connection instances
# with different configurations without modifying the class
dev_database_connection = DataBaseConnection(development_config)
testing_database_connection = DataBaseConnection(testing_config)
prod_database_connection = DataBaseConnection(production_config)

# BENEFITS OF THIS INITIAL IMPROVEMENT:
# 1. The high-level module (DataBaseConnection) no longer creates its dependencies
# 2. Different configurations can be used without modifying the class
# 3. Testing is easier because configurations can be injected
# 4. Follows the DIP principle of "dependencies should be injected"
# 
# REMAINING ISSUES:
# 1. No abstraction for different types of configs (SQL, MongoDB, Redis, etc.)
# 2. The Config class isn't truly abstract yet
