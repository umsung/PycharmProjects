from Search import SearchPage
# from framework.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.mobileby import MobileBy as By

class StockSelectPage():
    # def __init__(self,driver):
    #     self.driver = driver

    def clear_all(self):
        pass

    def search(self):
        return SearchPage(self.driver)
    
    def select(self,keyword):
        self.search().search(keyword).select().cancel()
        return self

    def get_stocks(self):
        return [element.text for element in self.find_elements(By.ID,'portname')]