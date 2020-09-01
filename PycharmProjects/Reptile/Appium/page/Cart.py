from Search import SearchPage
from stock_select import StockSelectPage
from Trade import TradePage
from base_page import BasePage
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pymongo import MongoClient
from appium.webdriver.common.mobileby import MobileBy as By
import time


class CartPage(BasePage):
    def clearAll(self):
        pass

    def select(self):
        pass
    
    def buy(self):
        pass

    def delete(self):
        pass

    def getWineNum(self):
        pass