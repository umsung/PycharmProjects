from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pymongo import MongoClient
# from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy as By
# from logger import Logger
import logging
import subprocess
import time
from appium.webdriver.common.touch_action import TouchAction
import json
import inspect
import yaml
import allure

logger = logging.basicConfig()


class BasePage(object):
    _driver: WebDriver
    logging.basicConfig(level=logging.INFO)
    _black_list = [
        (By.ID, 'image_cancel'),
        (By.ID, 'tv_agree'),
        (By.XPATH, "//*[@text='下次再说']")
    ]
    _current_context = "NATIVE_APP"
    _retry_max = 1
    _retry = 0
    _default_implicitly_wait_seconds = 6
    _default_explicit_wait_seconds = 10
    _params = {}

    def __init__(self,driver: WebDriver = None):
        self.driver = driver
        # self._black_list=[]

    def back(self):
        self.driver.back()
        # logger.info('返回')

    def forward(self):
        self.driver.forward()
        # logger.info('Click forward on current page.')

    def open_url(self, url):
        self.driver.get(url)
        logging.info('打开')

    def quit_browser(self):
        self.driver.quit()
        logging.info('退出')

    def implicitly_wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        logging.info('wait for %d seconds' % seconds)


    def screenshot(self, name):
        self.driver.save_screenshot(name)

    def get_screenshot(self, filename):
        self.driver.get_screenshot_as_file(filename)

    def save_context(self):
        self._current_context = self.driver.context
        if "WEBVIEW" in self._current_context:
            self._current_window = self.driver.current_window_handle

    def restore_context(self):
        if self._current_context != self.driver.context:
            self.driver.switch_to.context(self._current_context)

        if "WEBVIEW" in self._current_context:
            self.driver.switch_to.window(self._current_window)
            logging.info(self.driver.page_source)

    @staticmethod
    def exception_handle1(fun):
        def magic(*args,**kw):
            instance: BasePage = args[0]
            try:
                result = fun(*args,**kw)
                instance._retry = 0
                return result
            except Exception as e:
                instance._retry += 1
                if instance._retry > instance._retry_max:
                    raise e
                instance.driver.implicitly_wait(0)
                for e in instance._black_list:
                    elements = instance.driver.find_elements(*e)
                    if len(elements) > 0:
                        elements[0].click()
                        instance.driver.implicitly_wait(15)
                        return fun(*args,**kw)
            return magic

    @staticmethod
    def exception_handle(fun):
        def magic(*args, **kwargs):
            instance: BasePage = args[0]
            try:
                logging.info(f"{fun.__name__} {args[1:]} {kwargs}")
                result = fun(*args, **kwargs)
                # 隐式等待回复原来的等待，
                instance.implicitly_wait(instance._default_explicit_wait_seconds)
                # 重置次数
                instance._retry = 0
                return result
            except Exception as e:
                instance.screenshot("tmp.png")
                with open("tmp.png", "rb") as f:
                    content = f.read()
                allure.attach(content, attachment_type=allure.attachment_type.PNG)
                logging.error("element not found, handle black list")

                if instance._retry > instance._retry_max:
                    raise e

                instance._retry += 1
                logging.warning("exception handle")
                instance.implicitly_wait(0)

                # 处理黑名单里面的弹框
                for e in instance._black_list:
                    logging.warning(e)
                    # 保存原来的上下文
                    if instance.driver.context != "NATIVE_APP":
                        instance.save_context()
                        instance.driver.switch_to.context("NATIVE_APP")

                    elements = instance.driver.find_elements(*e)
                    if len(elements) > 0:
                        elements[0].click()
                        instance.implicitly_wait()

                        # 切换回原来的context
                        instance.restore_context()
                        return magic(*args, **kwargs)
                    instance.restore_context()
                instance.implicitly_wait(0)
                return magic(*args, **kwargs)
        return magic

    # def handleAlertByPageSource(self):
    #     '''
    #     弹窗处理
    #     '''
    #     _black_list = {'温馨提示': (By.XPATH, '//android.widget.TextView[@text="同意"]')}
    #     self.driver.implicitly_wait(0)
    #     pageSource = self.driver.page_source
    #     for k, v in _black_list.items():
    #         if k in pageSource:
    #             element = self.driver.find_element(*v)
    #             element.click()
    #     self.driver.implicitly_wait(1)
    #
    # def find_element(self, locator, value: str = None):
    #     i = 1
    #     # return self.driver.find_elements(*args)
    #     try:
    #         if isinstance(locator, tuple):
    #             element = self.driver.find_element(*locator)
    #         elif isinstance(locator, str) and value is None:
    #             element = self.driver.find_element_by_android_uiautomator(locator)
    #         else:
    #             element = self.driver.find_element(locator, value)
    #         return element
    #     except Exception as e:
    #         if i > 2:
    #             i = 1
    #             print('弹窗处理大于两次')
    #             return self.find_element(locator, value)
    #         self.handleAlertByPageSource()
    #         i += 1
    #         return self.find_element(locator, value)
        # except Exception as e:
        #     if i > 2:
        #         i = 1
        #         print('弹窗处理大于两次')
        #         return self.find_element(by,value)
        #     for k,e in self._black_list:
        #         elements = self.driver.find_elements(*e)
        #         if len(elements) > 0:
        #             elements[0].click()
        #     i += 1
        #     return self.find_element(by,value)

    # def find_elements(self, *args):
    #     elements = self.driver.find_elements(*args)
    #     return elements

    @exception_handle
    def find_element(self, locator, value: str = None):
        if isinstance(locator, tuple):
            element = self.driver.find_element(*locator)
        elif isinstance(locator, str) and value is None:
            element = self.driver.find_element_by_android_uiautomator(locator)
        else:
            element = self.driver.find_element(locator, value)
        return element

    def find_elements(self, locator, value: str = None):
        if isinstance(locator, tuple):
            elements = self.driver.find_elements(*locator)
        elif isinstance(locator, str) and value is None:
            elements = self.driver.find_elements_by_android_uiautomator(locator)
        else:
            elements = self.driver.find_elements(locator, value)
        return elements

    @exception_handle
    def click(self, by, value):
        self.driver.find_element(by, value).click()

    @exception_handle
    def wait(self,locator,timeout=30):
        # 显示等待封装，根据传入的locator类型
        '''
        利用 PageSource 来判断弹框是否存在的方法
        '''
        wait = WebDriverWait(self.driver,timeout)
        if isinstance(locator,tuple):
            wait.until(lambda x: len(self.driver.find_elements(*locator)) > 0)
        elif isinstance(locator,str):
            wait.until(lambda x: locator in self.driver.page_source)
        elif isinstance(locator,list):
            def wait_list(driver:webdriver):
                source = driver.page_source
                # any() 函数用于判断给定的可迭代参数 iterable 是否全部为 False，则返回 False，如果有一个为 True，则返回 True。
                return any(map(lambda x: x in source,locator))
            wait.until(wait_list)
        elif isinstance(locator, object):
            logging.info(f"expection_conditions {locator}")
            wait.until(locator)
        else:
            logging.warning(f'how to deal with {locator}')


    # def swipeUp(self,locator,t=500):
    #     '''向上滑动屏幕'''
    #     size = self.driver.get_window_size()
    #     x1 = size['width'] * 0.5          # x坐标
    #     y1 = size['height'] * 0.75        # 起始y坐标
    #     y2 = size['height'] * 0.25         # 终点y坐标
    #     self.driver.implicitly_wait(0)
    #     count = 0
    #     while True:
    #         if self.driver.find_elements(*locator) != []:
    #             break
    #         self.driver.swipe(x1, y1, x1, y2,t)
    #         count += 1
    #     self.driver.implicitly_wait(20)
    #     print(count)
    #     return count  

    def swipeDown(self,t=500, n=30):
        '''向下滑动屏幕'''
        size = self.driver.get_window_size()
        x1 = size['width'] * 0.5          # x坐标
        y1 = size['height'] * 0.25        # 起始y坐标
        y2 = size['height'] * 0.75         # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2,t)

    def swipeUp(self,t=500, n=30):
        '''向上滑动屏幕'''
        size = self.driver.get_window_size()
        x1 = size['width'] * 0.5          # x坐标
        y1 = size['height'] * 0.75        # 起始y坐标
        y2 = size['height'] * 0.25         # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2,t)

    def swipLeft(self, t=500, n=1):
        '''向左滑动屏幕'''
        size = self.driver.get_window_size()
        x1 = size['width'] * 0.75
        y1 = size['height'] * 0.5
        x2 = size['width'] * 0.25
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y1, t)

    def swipByMove(self):
        action = TouchAction(self.driver)
        window_react = self.driver.get_window_rect()
        width = window_react['width']
        height = window_react['height']
        x1 = int(width/2)
        y_start = int(height * 4/5)
        y_end = int(height * 1/5)
        for i in range(3):
            action.press(x=x1,y=y_start).wait(500).move_to(x=x1,y=y_end).release().perform()

    def getContexts(self):
        return self.driver.contexts

    def getCurrentContext(self):
        return self.driver.current_context

    def swtchToContext(self,context):
        self.driver.switch_to.context(context)
    
    def fast_input(self, inp, element):
        '快速输入'
        x = subprocess.check_output('adb devices', shell=True).decode('utf-8').split('\n')[1][:-7].replace('\t','')
        print(x)
        element.click()
        time.sleep(0.3)
        subprocess.Popen('adb -s %s shell input text %s' % (x, inp), shell=True)
        time.sleep(0.5)

    def steps(self, path):
        with open(path, encoding='utf-8') as f:
            name = inspect.stack()[1].funciton
            datas = yaml.safe_load(f)[name]
            for key, value in self._params.items():
                datas = datas.replace('{%s}' % key, value)
            for data in json.loads(datas):
                if 'action' in data.keys():
                    if data['action'] == 'click':
                        self.find_element(data['by'], data['locator']).click()
                    if data['action'] == 'send':
                        self.find_element(data['by'], data['locator']).send_keys(data['value'])
                    if data['action'] == 'len > 0':
                        ele = self.find_elements(data['by'], data['locator'])
                        return len(ele) > 0
   