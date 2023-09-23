from selenium import webdriver
from selenium.webdriver.common.selenium_manager import SeleniumManager
from Patterns.page_object.home_page import HomePage

#SeleniumManager.get_binary()

# driver = webdriver.Chrome()
# home_page = HomePage(driver)
# home_page.search_video('python')

# ChromeDriver
# FirefoxDriver
# SafariDriver
# EdgeDriver


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