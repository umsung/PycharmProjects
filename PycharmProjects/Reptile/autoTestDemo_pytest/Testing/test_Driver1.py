from selenium import webdriver
import time


class TestDD1:

    def test_dd1(self, browser):
        #  browser 是conftest文件中的browser固件，返回driver
        resp = browser.get('https://mall.wine-world.com/')
        time.sleep(1)
        assert 'hongjiushijie' == browser.title
