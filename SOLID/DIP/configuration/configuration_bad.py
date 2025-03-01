# Before applying DIP
# This implementation violates the Dependency Inversion Principle

class Config:
    # Configuration class that holds database connection details
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.username = user
        self.password = password
        self.host = host
        self.port = port


class DataBaseConnections:
    # PROBLEM: This class directly creates and depends on a specific Config instance
    # with hardcoded values, creating tight coupling
    def __init__(self):
        # Hard-coded configuration is created inside the class
        # This makes it impossible to use different configurations without modifying the class
        self.config = Config('sql', 'toni', '1234', 'localhost', '4444')

    def connect(self):
        #Code to connect Database
        pass

# ISSUES WITH THIS IMPLEMENTATION:
# 1. DataBaseConnections is tightly coupled to a specific configuration
# 2. It's impossible to reuse the class with different configurations (e.g., dev, test, prod)
# 3. Testing is difficult because configuration can't be mocked or controlled externally
# 4. Violates DIP because the high-level module (DataBaseConnections) directly depends on
#    low-level details (specific Config instance with hardcoded values)
# 5. Changing configuration requires modifying the database connection class
