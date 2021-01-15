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


def moveBy():
    Chrome_options = Options()
    Chrome_options.add_experimental_option('debugaddr')
    driver = webdriver.Chrome(options= Chrome_options)
    driver.get('')

    # 切换到iframe中
    driver.switch_to_frame('iframeResult')
    div = driver.find_element_by_id('draggable')

    # 动作链
    action = ActionChains(driver)
    action.click_and_hold(div)

    for i in range(5):
        # perform()立即执行动作链
        # move_by_offset(x,y);x水平，y垂直
        action.move_by_offset(17,0).perform()
        sleep(0.5)

    # 释放
    action.release()
    # 关闭
    driver.quit()
    

def drag_to():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get('http://sahitest.com/demo/dragDropMooTools.htm')

    dragger = driver.find_element_by_id('dragger')  # 被拖拽元素
    item1 = driver.find_element_by_xpath('//div[text()="Item 1"]')  # 目标元素1
    item2 = driver.find_element_by_xpath('/html/body/div[3]')  # 目标2
    item3 = driver.find_element_by_xpath('/html/body/div[4]')  # 目标3
    item4 = driver.find_element_by_xpath('/html/body/div[5]"]')  # 目标4

    action = ActionChains(driver)
    action.drag_and_drop(dragger, item1).perform()  # 1.移动dragger到目标1
    sleep(1)
    action.click_and_hold(dragger).release(item2).perform()  # 2.效果与上句相同，也能起到移动效果
    sleep(1)
    action.click_and_hold(dragger).move_to_element(item3).release().perform()  # 3.效果与上两句相同，也能起到移动的效果
    sleep(2)
    # action.drag_and_drop_by_offset(dragger, 400, 150).perform()  # 4.移动到指定坐标
    action.click_and_hold(dragger).move_by_offset(400, 150).release().perform()  # 5.与上一句相同，移动到指定坐标
    sleep(2)
    driver.quit()


if __name__ == "__main__":
    drag_to()