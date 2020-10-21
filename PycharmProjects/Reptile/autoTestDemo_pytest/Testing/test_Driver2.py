from selenium import webdriver
import time
import pytest


class TestDD2:
    def test_dd2(self, browser):
        #  browser 是conftest文件中的browser固件，返回driver
        resp = browser.get('https://mall.wine-world.com/')
        time.sleep(1)
        assert '红酒世界' in browser.title


if __name__ == '__main__':
    t = TestDD2()
    pytest.main(['-q', 'test_Driver2.py', '--html=report.html', '--self-contained-html'])

