from selenium import webdriver
from Patterns.page_object.home_page import HomePage


class DriverFactory():

    @staticmethod
    def get_driver(browser):
        if browser == 'chrome':
            return webdriver.Chrome()
        if browser == 'firefox':
            return webdriver.Firefox()
        if browser == 'safari':
            return webdriver.Safari()
        if browser == 'edge':
            return webdriver.ChromiumEdge()


driver_factory = DriverFactory()
driver = driver_factory.get_driver("firefox")
home_page = HomePage(driver)