from selenium import webdriver
import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import requests

def seleniumScrollDown():
    driver=webdriver.Chrome()
    wait = WebDriverWait(driver,10)

    url = ''
    driver.get(url)
    html = driver.page_source

    wait.until(EC.title_is('测试','失败'))
    wait.until(EC.title_contains('测试','失败'))
    wait.until(EC.presence_of_element_located((By.ID,'')))  # 判断某个locator元素是否被加到DOM树里，并不代表该元素一定可见(元素是隐藏的)
    wait.until(EC.visibility_of_element_located((By.ID,'')))  # 判断某个locator元素是否可见。可见代表非隐藏、可显示，并且元素的宽和高都大于0

    for i in range(1,11):
        h = i/10
        js = 'window.scrollTo(0,%s*documnet.body.clientHeight)' %h
        driver.execute_script(js)
        time.sleep(1)

    # 每次滚动 1/10,“window.scrollTo”为向下滑动的命令，
    # “document.body.clientHeight”为整个窗口的高度，“h=(i/10)”为每次滑动的高度。