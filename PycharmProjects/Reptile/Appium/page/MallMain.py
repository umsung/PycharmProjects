# from framework.base_page import BasePage
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient
# from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy as By
import time
from base_page import BasePage
from page.Search import SearchPage
from stock_select import StockSelectPage
from Trade import TradePage
from UserLogin import UserLoginPage
from MemberCenter import MemberCenterPage
from MemberShopMall import MemberShoppingMallPage


class MainPage(BasePage):
    def __init__(self):
        '''
        定义启动driver
        '''
        desired_caps = {
            'platformName': 'Android',
            'deviceName':'5184209b',
            'platformVersion':'5.1.1',
            'appPackage': 'com.keruiyun.redwine',             # apk包名
            'appActivity': 'com.keruiyun.redwine.MainActivity',   # apk的launcherActivity
            'noReset':True,
            'unicodeKeyboard':True,
            'resetKeyboard':True,
        }
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps)
        self.driver.implicitly_wait(1)
        self.wait('会员商城')
        contexts = self.driver.contexts
        context = self.driver.context
        print(self.driver.contexts)
        print(context, contexts)
        print(self.driver.current_context)
        print(self.driver.current_activity) # 打印当前的activity
        print('Main')

    def waitAlert(self):
        ac = self.driver.current_activity
        print(ac)

        # 等主页面activity出现,15秒内
        # self.driver.wait_activity(ac, 15)
        # time.sleep(15)

        contexts = self.driver.contexts
        context = self.driver.context
        print(self.driver.contexts)
        print(context, contexts)
        print(self.driver.current_context)
        print(self.driver.current_activity) # 打印当前的activity
        self.wait('温馨提示')
        # self.wait((By.XPATH,'//*[@text="温馨提示"]'))
        agreeelement = self.driver.find_element(By.XPATH,'//android.widget.TextView[@text="同意"]')
        agreeelement.click()
        return self
        # self.driver.tap([(409, 698), (469, 729)], 500)

    def getSource(self):
        pagesource = self.driver.page_source
        return pagesource

    def btnConfirm(self,locator):
        self.driver.find_elements_by_id(By.ID,locator)

    def toMemberShoppingMall(self):
        class_text = 'className("android.widget.TextView").text("会员商城")'
        self.driver.find_element_by_android_uiautomator(class_text).click()
        # self.find_element(By.XPATH,'//*[@text="会员商城"]').click()
        self.wait('全部酒款')
        ac = self.driver.current_activity
        print(ac)
        return MemberShoppingMallPage(self.driver)


    def toCrossBorderShoppingMall(self):
      
        class_text = 'className("android.widget.TextView").text("跨境商城")'
        self.driver.find_element_by_android_uiautomator(class_text).click()
        # self.find_element(By.XPATH,'//*[@text="跨境商城"]').click()
        self.wait('全部酒款')
        # //android.widget.TextView[@text='跨境商城']   appuim的*号表示任意class值

    def tohongKongMall(self):
        class_text = 'className("android.widget.TextView").text("香港商城")'
        self.driver.find_element_by_android_uiautomator(class_text).click()
        # self.find_element(By.XPATH,'//*[@text="香港商城"]').click()
        self.wait('全部酒款')

    def toPlusList(self):
        class_text = 'className("android.widget.TextView").text("会员专享")'
        
        self.driver.find_element_by_android_uiautomator(class_text).click()
        # self.find_element(By.XPATH,'//*[@text="会员专享"]').click()
        self.wait('全部酒款')

    def toHomePage(self):
        # self.find_element(By.XPATH,'//*[@text="首页"]').click()
        self.driver.find_element_by_android_uiautomator('text("首页")').click()
        return self

    def ToMemberCenter(self):
        self.find_element('text("会员中心")').click()
        # self.find_element(By.XPATH,'//*[@text="会员中心"]').click()
        # self.wait((By.XPATH,'//android.view.View[@text="全部订单"]'))
        
        return MemberCenterPage(self.driver)

    def search(self):
        self.find_element(By.ID,'TV_SEARCH').click()
        return SearchPage(self.driver)

    def stock_select(self):
        self.find_element(By.XPATH,"//*[@resource-id='com.xueqiu.android:id/tab_name'  and @text='行情']").click()
        return StockSelectPage(self.driver)

    def trade(self):
        self.find_element(By.XPATH,"//*[@resource-id='com.xueqiu.android:id/tab_name'  and @text='交易']").click()
        return TradePage(self.driver)


        

if __name__ == "__main__":
    main = MainPage()
    # main.waitAlert()
    # main.swipeUp()
    # main.swipeDown()
    # main.toMemberShoppingMall()
    # main.back()
    mCenter = main.ToMemberCenter()
    mCenter.toCoump()
    # login = mCenter.ToLoginOrRegister()
    # if login.LoginPagejud:
    #     login.toVerCodeLogin()
    # login.toPwdLogin()
    # login.LoginSuccess('19900000077','a123456')
    # main.toHomePage()
    # small=main.toMemberShoppingMall()
    # main.back()
    # main.toCrossBorderShoppingMall()
    # main.back()
    # main.tohongKongMall()
    # main.back()
    # main.toPlusList()
    # print(main.getContexts())
    # main.back()