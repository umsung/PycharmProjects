# -*- coding: utf-8 -*-

from PycharmProjects.Reptile.yaml import tools

pages = tools.parseyaml()


def get_locater(clazz_name, method_name):
    locators = pages[clazz_name]['locators']
    for locator in locators:
        if locator['name'] == method_name:
            return locator


class HomePage:
    '城市选择' = get_locater('HomePage', '城市选择')
    '首页搜索' = get_locater('HomePage', '首页搜索')

    
class LoginPage:
    '微信登录' = get_locater('LoginPage', '微信登录')
    '手机号登录' = get_locater('LoginPage', '手机号登录')
    '其它登录' = get_locater('LoginPage', '其它登录')
    'QQ' = get_locater('LoginPage', 'QQ')
    '微博' = get_locater('LoginPage', '微博')
    '账号密码' = get_locater('LoginPage', '账号密码')
    '输入账号' = get_locater('LoginPage', '输入账号')
    '输入密码' = get_locater('LoginPage', '输入密码')
    '登录按钮' = get_locater('LoginPage', '登录按钮')

    