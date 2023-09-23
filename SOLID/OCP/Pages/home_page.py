from SOLID.OCP.Pages.base_page import BaseWebDriverElement
from home_page_locators import HomePageLocators


class HomePage(BaseWebDriverElement):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get('http://www.youtube.com')

    def search_video(self, video_text):
        self.enter_text(HomePageLocators.yt_search_field, video_text)
        self.click(HomePageLocators.yt_search_button)
