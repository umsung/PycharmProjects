from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient
from selenium.webdriver.common.by import By
import allure
import logging
import yaml
import inspect
import json


def exception_handle(fun):
    def magic(*args, **kwargs):
        instance: BasePage = args[0]
        try:
            logging.info(f"{fun.__name__} {args[1:]} {kwargs}")
            result = fun(*args, **kwargs)
            instance._retry = 0
            # 隐式等待回复原来的等待，
            instance.implicitly_wait(instance._default_explicit_wait_seconds)
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


class BasePage(object):

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
    _params = None


    def __init__(self, driver):
        self.driver = driver
        self._black_list=[]

    def back(self, num=1):
        for i in range(num):
            self.driver.back()

    def forward(self):
        self.driver.forward()
        logging.info('Click forward on current page.')

    def open_url(self, url):
        self.driver.get(url)
        logging.info('打开')

    def quit_browser(self):
        self.driver.quit()
        logging.info('退出')

    def screenshot(self, name):
        self.driver.save_screenshot(name)

    def get_screenshot(self, filename):
        self.driver.get_screenshot_as_file(filename)

    @exception_handle
    def find_element(self, by, value):
        return self.driver.find_element(by, value)
    #
    # def find_element(self, by, value):
    #     # return self.driver.find_elements(*args)
    #     try:
    #         element = self.driver.find_element(by, value)
    #         return element
    #     except Exception as e:
    #         for e in self._black_list:
    #             elements = self.driver.find_elements(*e)
    #             if len(elements) > 0:
    #                 elements[0].click()
    #         return self.find_element(by, value)

    def find_elements(self, by, value):
        return self.driver.find_elements(by, value)

    @exception_handle
    def click(self, by, value):
        self.driver.find_element(by, value).click()

    def implicitly_wait(self, seconds=_default_implicitly_wait_seconds):
        self.driver.implicitly_wait(seconds)

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

    @exception_handle
    def wait(self,locator,timeout=20):
        # 显示等待封装，根据传入的locator类型
        wait = WebDriverWait(self.driver,timeout)
        if isinstance(locator,tuple):
            wait.until(lambda x: len(self.driver.find_elements(*locator)) > 0)
        elif isinstance(locator,str):
            wait.until(lambda x: locator in self.driver.page_source)
        elif isinstance(locator,list):
            def wait_list(driver:webdriver):
                source = driver.page_source
                return any(map(lambda x: x in source,locator))
            wait.until(wait_list)
        elif isinstance(locator, object):
            logging.info(f"expection_conditions {locator}")
            wait.until(locator)
        else:
            logging.warning(f'how to deal with {locator}')

    def steps(self, path):
        with open(path, encoding='utf-8') as f:
            name = inspect.stack().funciton
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

    def fast_input(self, username, pwd):

        x = subprocess.check_output('adb devices', shell=True).split('\n')[1][:-7]
        element.click()
        time.sleep(0.3)
        subprocess.Popen('adb -s %s shell input text %s' % (x, str), shell=True)
        time.sleep(0.5)