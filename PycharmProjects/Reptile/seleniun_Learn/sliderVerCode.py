import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


class SVC(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://account.wine-world.com/account/accountreg?returnurl=https%3a%2f%2fmall.wine-world.com%2f'
        self.wait = WebDriverWait(self.driver,10)
        self.driver.maximize_window()
        self.location = {}
        self.size = {}

    def open(self):
        self.driver.get(self.url)
    
    def close(self):
        self.driver.close()

    def get_vc_but(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.verPhone.ww-verif')))
        return button

    def get_slider(self):
        slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'btnico')))
        return slider

    def getImg(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.ww-bigimg')))
        imgElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.ww-slideCode > div.ww-slideImg')))
        time.sleep(1)
        self.location = imgElement.location
        self.size = imgElement.size
        print(self.location,self.size)
        screenshot = self.driver.get_screenshot_as_png()
        imgObj = Image.open(BytesIO(screenshot))
        imgObj.save('1.png')
        return imgObj
    
    def imgCrop(self):
        imgObj = self.getImg()
        top,bottom,left,right = self.location['y'],self.location['y']+self.size['height'],self.location['x'],self.location['x']+self.size['width']
        captcha = imgObj.crop((left,top,right,bottom))
        print(captcha.size,captcha.size[0],captcha.size[1])
        captcha.save('2.png')
        return captcha

    def setAttr(self,elementObj,attrName,value):
        self.driver.execute('argument[0].setAttribute(argument[1],argument[2])',elementObj,attrName,value)

    def start(self):
        self.open()
        button = self.get_vc_but()
        button.click()
        self.imgCrop()

if __name__ == "__main__":
    s = SVC()
    s.start()