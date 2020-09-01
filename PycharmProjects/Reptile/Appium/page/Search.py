# from framework.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pymongo import MongoClient
from appium.webdriver.common.mobileby import MobileBy as By
from page.base_page import BasePage


class SearchPage(BasePage):
    # def __init__(self,driver):
    #     self.driver = driver

    def search_by(self,keyword):
        # self.find_element(By.ID,'seach_input_text').send_keys('keyword')
        # self.find_element(By.ID,'name').click()
        self._params[keyword] = keyword
        self.steps('../data/search.yaml')
        return self

    def select(self):
        pass

    def cancel(self):
        pass

    def get_price(self):
        return self

    def close(self):
        self.driver.close()