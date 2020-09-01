from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup
import requests
import os
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import time
from Crypto.Cipher import AES
import base64
from hashlib import md5

class Sky():
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.url = 'https://www.aqistudy.cn/historydata/daydata.php?city=%E6%88%90%E9%83%BD&month=201612'
        self.wait = WebDriverWait(self.driver, 15)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',}
        self.local_key = 'emhlbnFpcGFsbWtleQ=='
        self.local_vi = 'emhlbnFpcGFsbWl2'

    def get_data_by_selenium(self):
        self.driver.get(self.url)
        time.sleep(1)
        # items = self.driver.execute_script("return localStorage.getItem('781d10706b2d2ed381e835e06a3c5205')")
        items = self.driver.execute_script("return localStorage.key(0)")
        print(items)
        script = "return localStorage.getItem('{}')".format(items)
        print(script)
        items = self.driver.execute_script(script)
        print(items)
        return items

    def get_data_by_req(self):
        resp = requests.get(self.url, headers=self.headers)
        print(resp.status_code)
        print(resp.text)

    def AES_Decrypt(self, data):
        secretkey = md5(self.local_key.encode('utf-8')).hexdigest()[16:32]
        secretiv = md5(self.local_vi.encode('utf-8')).hexdigest()[0:16]
        print(secretkey,secretiv)
        data = data.encode('utf8')
        encodebytes = base64.decodebytes(data)
        # 将加密数据转换位bytes类型数据
        cryptos = AES.new(secretkey.encode('utf8'), AES.MODE_CBC, secretiv.encode('utf8'))
        text_decrypted = cryptos.decrypt(encodebytes)
        unpad = lambda s: s[0:-s[-1]]
        text_decrypted = unpad(text_decrypted)
        # 去补位
        text_decrypted = text_decrypted.decode('utf8')
        # if text_decrypted:
        #     self.driver.close()
        return text_decrypted


if __name__ == '__main__':
    s = Sky()
    items = s.get_data_by_selenium()
    print(items)
    text_decrypted = s.AES_Decrypt(items)
    print(text_decrypted)
    print(base64.b64decode(text_decrypted.encode('utf-8')).decode('utf-8'))
