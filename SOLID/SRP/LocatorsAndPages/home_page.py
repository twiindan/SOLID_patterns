from home_page_locators import HomePageLocators


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.driver.get('http://www.youtube.com')

    def search_video(self, video_text):
        self.driver.find_element(HomePageLocators.yt_search_field).send_keys(video_text)
        self.driver.find_element(HomePageLocators.yt_search_button).click()
