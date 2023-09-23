from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class FirefoxCustomDriver:
    def __init__(self):
        self.options = FirefoxOptions()
        self.options.add_argument("--headless")

    def get_driver(self):
        return webdriver.Firefox(options=self.options)
