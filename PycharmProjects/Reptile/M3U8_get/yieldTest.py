import os
import time
from datetime import datetime, timedelta
import m3u8
import requests
from glob import iglob
from natsort import natsorted
from urllib.parse import urljoin
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import threading


class YieldTest(object):


    def __init__(self,dir, file_name = None):
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',}
        self.thread = ThreadPoolExecutor(max_workers=10)
        self.dir = dir
        self.file_name = file_name
        self.m3u8_url = ''
        self.lock = threading.Lock()

    def get_file_urls(self):
        dir = 'D:/用户目录/下载'
        a = []
        for root, dirs, files in os.walk(dir):
            for filename in files:
                if '.m3u8' in filename and len(filename) > 10:
                    self.file_name = filename
                    m3u8FilePath = root + '/' + filename
                    createTimestamp = os.path.getctime(m3u8FilePath)
                    # 文件创建时间戳
                    createTime = datetime.fromtimestamp(createTimestamp).date()
                    now = datetime.now().date()
                    withintenday = datetime.now() - timedelta(days=10)
                    if createTime >= withintenday.date():
                        print(m3u8FilePath)
                        with open(m3u8FilePath, 'r') as f:

                            for i in f:
                                if '#' not in i:
                                    if len(i) > 1 and not i.startswith('https:'):
                                        i = 'https:' + i
                                    domain = 'https://aszyw.com'
                                    # url = domain + i
                                    # yield domain + i
                                    yield i
                            #         a.append(domain+i)
                            # return a

    def get_file_urls_list(self):
        dir = 'D:/用户目录/下载'
        urllist = []
        for root, dirs, files in os.walk(dir):
            for filename in files:
                if '.m3u8' in filename and len(filename) > 10:
                    self.file_name = filename
                    m3u8FilePath = root + '/' + filename
                    createTimestamp = os.path.getctime(m3u8FilePath)
                    # 文件创建时间戳
                    createTime = datetime.fromtimestamp(createTimestamp).date()
                    tenHourAge = datetime.now().date()
                    if createTime == tenHourAge:
                        with open(m3u8FilePath, 'r') as f:
                            a = f.readlines()
                        for i in a:
                            if '#' not in i:
                                if not i.startswith('https:'):
                                    urllist.append('https:' + i)
                                domain = 'https://aszyw.com'
                                # url = domain + i
                                # yield domain + i

                                urllist.append(i)
                        return urllist

    def download_single_ts_withoutKey(self,urlinfo):
        url,ts_name = urlinfo
        resp = requests.get(url,headers=self.header)
        # key = requests.get('https://aszyw.com/20191019/uyfQazNz/1000kb/hls/key.key',headers=self.header).content
        # cryptor = AES.new(key, AES.MODE_CBC, key)
        # with open(ts_name,'wb') as f:
        #     f.write(resp.content)

    def test(self):
        ll = [
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_000.ts?auth_key=1597478084-0-0-92dddd6b9b790fa8382fd55bc18f43f8\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_001.ts?auth_key=1597478084-0-0-c72cce8bc891a2c7b5e8cbb15084679e\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_002.ts?auth_key=1597478084-0-0-d19af608c456c93599f18c7c725e40fc\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_003.ts?auth_key=1597478084-0-0-b93e950abb550cd21e31b6b4e87450a0\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_004.ts?auth_key=1597478084-0-0-140daeebcd5671095e644678e02fd880\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_005.ts?auth_key=1597478084-0-0-eff647c60c37dcdfe8d1a41ae06d045f\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_006.ts?auth_key=1597478084-0-0-cac2f0fccf8f859d89ea21cfb1073f90\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_007.ts?auth_key=1597478084-0-0-460c3c5c7edba41300dec84556bc7bb2\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_008.ts?auth_key=1597478084-0-0-edb7b5ab0cb3c6ee1b1f41ed781d020d\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_009.ts?auth_key=1597478084-0-0-b9dd9cc6a00e7d72d8d604b7d920d415\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_010.ts?auth_key=1597478084-0-0-17f00ea185b7fd7f98aab0d5204da419\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_011.ts?auth_key=1597478084-0-0-0d7c27b763a8e9287d512721a47db643\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_012.ts?auth_key=1597478084-0-0-710dcaba9ceb0e07018166f712319029\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_013.ts?auth_key=1597478084-0-0-6b88e8f250fc21dbddedb8b6d284b092\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_014.ts?auth_key=1597478084-0-0-215afd3ec480fdfa744337d3d31dba1d\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_015.ts?auth_key=1597478084-0-0-bfa16f7a2f16987c7c7bab3a349a6427\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_016.ts?auth_key=1597478084-0-0-ca4bf77a2fef5ed211e05f96cd30fd1e\n',
            'https://p.hbqxyl.com/useruploadfiles/466d2c1e4d8807f56c7c7a73f962d027/466d2c1e4d8807f56c7c7a73f962d027_017.ts?auth_key=1597478084-0-0-1c014defc00a5421ec485f5440342ffa\n']
        for i in range(2):
            with self.thread as executor:
                for index, ts_url in enumerate(ll):
                    ts_url = ts_url.replace('\\n', '').strip()
                    print(ts_url)
                    # executor.submit(self.download_single_ts,[ts_url,f'{index}.ts'])
                    executor.submit(self.download_single_ts_withoutKey, [ts_url, f'{index}.ts'])

if __name__ == '__main__':
    dir = 'D:/用户目录/下载'
    y = YieldTest(dir)
    y.test()






















