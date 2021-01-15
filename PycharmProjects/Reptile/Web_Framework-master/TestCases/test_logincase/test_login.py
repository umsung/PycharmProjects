#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/3/2
# @Author  : Mcen (mmocheng@163.com)
# @Name    : test_login


import allure
import sys
from PageObjects.LoginPage.login_page import LoginPage
from Common.ElementPath import Element


class Test_Login():

    @allure.story('测试账号为空')
    def test_login_usernameNull_error(self, Driver):
        app = {"driver": Driver,"path": Element.test_login_data,"caseName": sys._getframe().f_code.co_name,"num" :0}
        page=LoginPage(app)
        page.operate()
        assert page.checkPoint()

    @allure.story('测试账号错误')
    def test_login_usernameFormat_error(self, Driver):
        app = {"driver": Driver,"path": Element.test_login_data,"caseName": sys._getframe().f_code.co_name,"num" :1}
        page=LoginPage(app)
        page.operate()
        assert page.checkPoint()

    @allure.story('测试密码错误')
    def test_login_pwdFormat_error(self, Driver):
        app = {"driver": Driver,"path": Element.test_login_data,"caseName": sys._getframe().f_code.co_name,"num":2}
        page=LoginPage(app)
        page.operate()
        assert page.checkPoint()

    @allure.story('测试登录成功')
    def test_login_success(self, Driver):
        app = {"driver": Driver,"path": Element.test_login_data,"caseName": sys._getframe().f_code.co_name,"num":3}
        page=LoginPage(app)
        page.operate()
        assert page.checkPoint()



        # with open(Element.IMAGES + "/images20200302141947_登录.png", mode='rb') as f:
        #     file = f.read()
        #     allure.attach(file, '登录界面', allure.attachment_type.PNG)
        #
        # assert LoginPage(Driver).login() == 2
