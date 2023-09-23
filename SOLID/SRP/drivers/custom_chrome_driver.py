from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


class ChromeCustomDriver:
    def __init__(self):
        self.options = ChromeOptions()
        self.options.add_argument("--headless")

    def get_driver(self):
        return webdriver.Chrome(options=self.options)
