# coding:utf-8
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
from hashlib import md5
from PIL import Image
from io import BytesIO

USERNAME='umsung'
PASSWORD='a123456'
SOFT_ID='905152'


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

class CrackCaptcha():
    def __init__(self):
        self.url = 'https://captcha3.scrape.cuiqingcai.com/'
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 15)
        self.username = USERNAME
        self.password = PASSWORD
        self.soft_id = SOFT_ID
        self.chaojiying = Chaojiying_Client(self.username,self.password,self.soft_id)

    def get_captcha_element(self):
        try:
            self.browser.get(self.url)
            button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'button[type="button"]')))
            button.click()
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'img.geetest_item_img')))
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div:nth-child(6) > div.geetest_panel_box.geetest_panelshowclick')))
            print(element)
            location = element.location
            size = element.size
            print(location,size,location['x'],location['x']+size['width'],location['y'],location['y']+size['height'])
            # top,bottom,left,right = location['y']-8,location['y']+size['height']+9,location['x'],location['x']+size['width']
            # screenshot = self.browser.get_screenshot_as_png()
            # screenshot = Image.open(BytesIO(screenshot))
            # screenshot.save('111.png')
            # screenshot2 = self.browser.get_screenshot_as_file('222.png')
            # screenshot2 = Image.open('222.png')
            # captcha = screenshot.crop((left,top,right,bottom))
            # captcha2 = screenshot2.crop((left,top,right,bottom))
            # captcha.save('1.png')
            # captcha2.save('2.png')
            locations = [[132,127],[59,77]]
            for location in locations:
                ActionChains(self.browser).move_to_element_with_offset(element,location[0],location[1]).click().perform()
            # return captcha
        except TimeoutError:
            return self.get_captcha_element()

    def getzuobiao(self):
        captcha = self.get_captcha_element()
        with open('1.png','rb') as f:
            im = f.read()
            zuobiao = self.chaojiying.PostPic(im,9004)
            print(zuobiao)
            return zuobiao

if __name__ == '__main__':
    # chaojiying = Chaojiying_Client('超级鹰用户名', '超级鹰用户名的密码', '905152')	  # 用户中心>>软件ID 生成一个替换 96001
    # im = open('a.jpg', 'rb').read()													# 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    # print (chaojiying.PostPic(im, 1902))											# 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

    cc = CrackCaptcha()
    cc.get_captcha_element()