import requests
import asyncio
import aiohttp
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent,FakeUserAgentError
import random

def get_page(url, options={}):
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    header = {
        'Cookie': '__jsluid=cbfffb32c3181e2d8a04bf2ad00ef041; __jsl_clearance=1560909043.173|0|CGs6ghgbNIxCBNKmMyi9VkpD5fs%3D; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1560843572,1560909047; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1560909052',

        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    base_headers = {
        'Cookie': '__jsluid=cbfffb32c3181e2d8a04bf2ad00ef041; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1560843572; __jsl_clearance=1560847785.481|0|fuDiD0ZRORlV6vMks29qNjj66JI%3D; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1560848231',
        'User-Agent':  ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    headers = dict(base_headers, **options)
    print('Getting', url)
    try:
        r = requests.get(url, headers=header)
        print('Getting result', url, r.status_code)
        if r.status_code == 200:
            return r.text
    except ConnectionError:
        print('Crawling Failed', url)
        return None


class Downloader(object):
    """
    一个异步下载器，可以对代理源异步抓取，但是容易被BAN。
    """

    def __init__(self, urls):
        self.urls = urls
        self._htmls = []

    async def download_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                self._htmls.append(await resp.text())

    def download(self):
        loop = asyncio.get_event_loop()
        tasks = [self.download_single_page(url) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))

    @property
    def htmls(self):
        self.download()
        return self._htmls
