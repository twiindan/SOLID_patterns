# Example in Software Testing

"""
We can apply the SRP in our daily work in several ways. For example in the Page Objects and Webdriver Classes
"""

from selenium.webdriver.common.by import By
from selenium import webdriver


class LoginPage:
    yt_search_field = (By.ID, 'search')
    yt_search_button = (By.CLASS_NAME, 'style-scope ytd-searchbox')

    def __init__(self, driver):
        self.driver = driver
        self.driver.get('http://www.youtube.com')

    def search_video(self, video_text):
        self.driver.find_element(self.yt_search_field).send_keys(video_text)
        self.driver.find_element(self.yt_search_button).click()

driver = webdriver.Chrome()
login_page = LoginPage(driver)
login_page.search_video('testing')

""" We can do more fine tunning regarding the SRP principle splitting the content in two different classes: 
One for save locators and another to describe the actions
"""







