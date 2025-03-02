import json


class Configuration:
    # Class variables shared across all instances
    _instance = None      # Will hold the single instance of the Configuration class
    browser = None        # Will store the browser type from config
    implicit_wait = 0     # Will store the wait time from config

    def __new__(cls):
        # SINGLETON PATTERN: Core implementation
        # This special method controls instance creation
        if cls._instance is None:
            # This message will only print once when the Configuration is first created
            print('Creating the object')
            # Create the single instance by calling the parent class's __new__ method
            cls._instance = super(Configuration, cls).__new__(cls)
            # Any one-time initialization can be placed here
            # Note: The actual config loading is separated into another method
            # for better control over when it happens
        # Always return the same instance for any subsequent instantiation
        return cls._instance

    def load_configuration(self):
        # Method to load configuration from a JSON file
        # This is separate from __new__ to allow explicit control over when
        # configuration is loaded or reloaded
        with open("config.json", "r") as configuration_file:
            # Parse the JSON config file
            data = json.load(configuration_file)
            # Store configuration values in the singleton instance
            # These values will be shared across all references to this class
            self.browser = data["browser"]
            self.implicit_wait = data["implicit_wait"]

    def get_browser(self):
        # Getter method for the browser configuration
        # Any part of the application can access this shared setting
        return self.browser

    def get_implicit_wait(self):
        # Getter method for the implicit wait time configuration
        # Any part of the application can access this shared setting
        return self.implicit_wait
