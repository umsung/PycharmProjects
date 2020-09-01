from appium import webdriver
from MallMain import MainPage
from base_page import BasePage
import os
from data.config import * 
from appium.webdriver.common.mobileby import MobileBy as By
from selenium.webdriver.support.wait import WebDriverWait

class App(BasePage):

    _appPackage = 'com.keruiyun.redwine'
    _appActivity = 'com.keruiyun.redwine.MainActivity'

    def start(self):

        '''
        定义启动driver
        '''

        if self.driver == None:
            desired_caps = {
                'platformName': 'Android',
                'deviceName':'5184209b',
                'platformVersion':'5.1.1',
                'appPackage': self._appActivity,             # apk包名
                'appActivity': self._appActivity,   # apk的launcherActivity
                # 'noReset': True,   #启动app时不要清除app里的原有的数据
                'unicodeKeyboard':True,
                'resetKeyboard':True,
            }
            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps)
            self.driver.implicitly_wait(2)
        else:
            print(self.driver)
            self.driver.start_activity(self._appPackage,self._appActivity)
        return self

    
    def stop(self):
        self._driver.close_app()
        self._driver.quit()
        # os.popen('adb shell am force-stop %s' % self._appPackage)

    def restart(self):
        self._driver.close()
        self._driver.launch_app()

    # def stop(self):
    #     self._driver.quit()

    def start_my_app(self):
        """
        打开应用
        adb shell am start -n com.tencent.mm/.ui.LauncherUI
        :param package_name:
        :return:
        """
        os.popen('adb shell am start -n %s/%s' % (self._appPackage,self._appActivity))
  
    def kill_all():
        """
        关闭所有的应用
        :return:
        """
        os.popen('adb shell am kill-all')


    def main(self):
        return MainPage(self.driver)


if __name__ == "__main__":
    
    app = App()
    main = app.start().main()
    main.waitAlert()
    main.swipeUp()
    main.swipeDown()
    mCenter = main.ToMallCenter()
    login = mCenter.ToLoginOrRegister()
    if login.LoginPagejud:
        login.toVerCodeLogin()
    login.toPwdLogin()
    login.LoginSuccess(USERNAME,PASSWORD)
    main.toHomePage()
    small=main.MemberShoppingMall()
    main.back()
    main.CrossBorderShoppingMall()
    main.back()
    main.hongKongMall()
    main.back()
    main.PlusList()
    print(main.getContexts())
    main.back()