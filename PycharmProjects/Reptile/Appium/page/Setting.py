from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pymongo import MongoClient
from appium.webdriver.common.mobileby import MobileBy as By
import time
from base_page import BasePage


class SettingPage(BasePage):
    def Logout(self):
        self.find_element(By.XPATH,'//*[@text="退出登录"]').click()
        return MallCenterPage(self.driver)