
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pymongo import MongoClient
from appium.webdriver.common.mobileby import MobileBy as By
import time
from base_page import BasePage


class UserLoginPage(BasePage):

    def LoginPagejud(self):
        self.wait(['本机号码一键登录','账号密码登录'])
        time.sleep(1.5)
        source = self.driver.page_source
        if '本机号码一键登录' in source:
            return True
        if '登陆/注册' in source:
            return False

    def OneClickLogin(self):
        self.find_element('text("本机号码一键登录")').click()
        # from MallCenter import MallCenterPage
        # return MallCenterPage(self.driver)

    def toVerCodeLogin(self):
        self.find_element('text("其他方式登录")').click()
        return self

    def toPwdLogin(self):
        self.find_element('text("账号密码登录")').click()
        return self

    def isOneclickLogin(self):
        if '本机号码一键登录' in self.driver.page_source:
            return self.toVerCodeLogin().toPwdLogin()
        else:
            return self.toPwdLogin()

    def PwdLogin(self,username,pwd,locator=None):
        usernameInp = self.find_element('textContains("请输入手机号")')
        pwdInp = self.find_element(By.XPATH,'//*[@text="密码"]/../android.widget.EditText[1]')
        loginBtn = self.find_element('text("登 录")')
        self.fast_input(username,usernameInp)
        self.fast_input(pwd,pwdInp)
        loginBtn.click()
        # msg = self.find_element(*locator)
        # return msg

    def loginWithErrUsername(self,username,pwd):
        self.PwdLogin(username,pwd)
        time.sleep(0.5)
        ErrMsg = self.find_element(By.XPATH,'')
        return ErrMsg

    def loginWithErrPwd(self,username,pwd):
        self.PwdLogin(username,pwd)
        time.sleep(0.5)
        ErrMsg = self.find_element(By.XPATH,'')
        return ErrMsg

    def loginWithoutPwd(self,username,pwd):
        self.PwdLogin(username,pwd)
        time.sleep(0.5)
        ErrMsg = self.find_element(By.XPATH,'')
        return ErrMsg

    def LoginSuccess(self,username,pwd):
        self.PwdLogin(username,pwd)

        # from MallCenter import MallCenterPage
        # return MallCenterPage(self.driver)

    