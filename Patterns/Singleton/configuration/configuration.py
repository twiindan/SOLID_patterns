import json


class Configuration():

    _instance = None
    browser = None
    implicit_wait = 0

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Configuration, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def load_configuration(self):
        with open("config.json", "r") as configuration_file:
            data = json.load(configuration_file)
            self.browser = data["browser"]
            self.implicit_wait = data["implicit_wait"]

    def get_browser(self):
        return self.browser

    def get_implicit_wait(self):
        return self.implicit_wait


