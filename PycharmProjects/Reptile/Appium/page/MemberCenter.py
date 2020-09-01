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
from UserLogin import UserLoginPage


class MemberCenterPage(BasePage):
    def ToLoginOrRegister(self):
       
        self.wait('点击登录/注册')
        
        self.find_element('text("点击登录/注册")').click()
        
        return UserLoginPage(self.driver)

    def toSetting(self):
        self.find_element(By.XPATH,'').click()
        self.wait('设置')
        return Setting.SettingPage(self.driver)  

    def toCoump(self):
        class_text = 'className("android.widget.TextView").text("全部订单")'
        self.driver.find_element_by_android_uiautomator(class_text).click()
        time.sleep(10)
        contexts = self.driver.contexts
        context = self.driver.context
        print(self.driver.contexts)
        print(context, contexts)
        print(self.driver.current_context)
        print(self.driver.current_activity) # 打印当前的activity
        pagesource = self.driver.page_source
        print(pagesource)
        assert '去付款' in pagesource
    # def toHomePage(self):
    #     self.find_element(By.XPATH,'//*[@text="首页"]').click()
    #     return MainPage()

    def getUsername(self):
        pass