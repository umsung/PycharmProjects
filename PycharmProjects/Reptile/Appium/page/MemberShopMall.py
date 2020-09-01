from Search import SearchPage
from stock_select import StockSelectPage
from Trade import TradePage
# from framework.base_page import BasePage
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient
from appium.webdriver.common.mobileby import MobileBy as By
import time
from base_page import BasePage


class MemberShoppingMallPage(BasePage):
    def search(self):
        self.find_element(By.XPATH,'//*[@text,"葡萄酒搜索"]').click()
        return SearchPage(self.driver)

    def preparation(self):
        self.find_element(By.XPATH,'//*[@text,"选酒"]')
        return 

    def CrossBorderShoppingMall(self):
        pass
    
    def cart(self):
        pass

    def memberCenter(self):
        pass