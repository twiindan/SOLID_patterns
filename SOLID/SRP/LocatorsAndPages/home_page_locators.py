from selenium.webdriver.common.by import By


class HomePageLocators():
    yt_search_field = (By.ID, 'search')
    yt_search_button = (By.CLASS_NAME, 'style-scope ytd-searchbox')