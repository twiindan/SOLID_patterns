from selenium import webdriver
from selenium.webdriver.common.selenium_manager import SeleniumManager
from Patterns.page_object.home_page import HomePage

path = SeleniumManager.get_binary()

driver = webdriver.Chrome()
home_page = HomePage(driver)
home_page.search_video('python')

