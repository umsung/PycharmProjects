from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from bs4 import BeautifulSoup
import requests
import os,json
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging

options = webdriver.ChromeOptions()
options.add_argument('--headless')
# 无头模式启动
# option.add_argument('--headless')
# 谷歌文档提到需要加上这个属性来规避bug
# option.add_argument('--disable-gpu')
# 禁用图片
# chrome_options.add_argument('blink-settings=imagesEnabled=false')
# 修改User-Agent
# chrome_options.add_argument('user-agent= '你想修改成的User-Agent')
# 添加代理
# chrome_options.add_argument("--proxy-server=http://" + ip：port)
browser = webdriver.chrome(options=options)
wait = WebDriverWait(browser,5)
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
MAX_COUNT = 5

def getHTML(url,condition,locator,count=1):
    if count > MAX_COUNT:
        logging.error('trid to many count')
        return None
    try:
        browser.get(url)
        wait.until(condition(locator))
    except TimeoutError:
        count += 1
        getHTML(url,condition,locator)

def analysisIndexPage():
    elements = browser.find_elements_by_xpath('')
    for element in elements:
        href = element.get_attribute('href')
        yield href

def analysisDetailPage():
    item = {}
    item['url'] = browser.current_url
    item['name'] = browser.find_element_by_xpath('').text
    cover = browser.find_element_by_id('').get_attribute('src')
    return item

def save_data(data):
    name = data['name']
    try:
        os.mkdir('results')
    except FileExistsError:
        pass
    path = f'results/{name}.json'
    json.dumps(data +"\n",open(path,'w',encoding='utf-8'),ensure_ascii=False,indent=2)


if __name__ == "__main__":
    url=''
    try:
        for i in range(5):
            getHTML(url,condition=EC.visibility_of_all_elements_located,locator=(By.XPATH,''))
            for href in analysisIndexPage():
                getHTML(href,condition=EC.visibility_of_all_elements_located,locator=(By.XPATH,''))
                data = analysisDetailPage()
                save_data(data)
    finally:
        browser.quit()