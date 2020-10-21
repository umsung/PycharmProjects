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

class Download_M3U8(object):
    
    def __init__(self,dir, file_name = None):
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',}
        self.thread = ThreadPoolExecutor(max_workers=10)
        self.dir = dir
        self.file_name = file_name
        self.m3u8_url = ''
        self.lock = threading.Lock()

    def get_urls(self):
        m3u8_obj = m3u8.load(self.m3u8_url)
        base_uri = m3u8_obj.base_uri
        for i in m3u8_obj.segments:
            yield urljoin(base_uri, i)

    def get_m3u8_filenames(self):
        a = []
        for root, dirs, files in os.walk(self.dir):
            for filename in files:
                if '.m3u8' in filename and len(filename) > 10:
                    m3u8FilePath = root + '/' + filename
                    createTimestamp = os.path.getctime(m3u8FilePath)
                    # 文件创建时间戳
                    createTime = datetime.fromtimestamp(createTimestamp).date()
                    now = datetime.now()
                    threedayAge = now - timedelta(days=1)
                    if createTime >= threedayAge.date():
                        # yield m3u8FilePath
                        a.append(m3u8FilePath)
        # print(a)
        return a

    def get_file_urls(self, m3u8FilePath):
        dir = 'D:/用户目录/下载'
        aa = []
        with open(m3u8FilePath, 'r') as f:

            for i in f:
                if '#' not in i:
                    if len(i) > 2 and not i.startswith('https:'):
                        i = 'https://www.gentaji.com:65/' + i
                    domain = 'https://aszyw.com'
                    # url = domain + i
                    # yield domain + i
                    # yield i
                    aa.append(i)
        # print(aa)
        return aa

    def download_single_ts_withoutKey(self,urlinfo):
        url,ts_name = urlinfo
        resp = requests.get(url,headers=self.header)
        # key = requests.get('https://aszyw.com/20191019/uyfQazNz/1000kb/hls/key.key',headers=self.header).content
        # cryptor = AES.new(key, AES.MODE_CBC, key)
        with open(ts_name,'wb') as f:
            f.write(resp.content)

    def download_single_ts(self,urlinfo):
        url,ts_name = urlinfo
        print(url,ts)
        resp = requests.get(url,headers=self.header)
        # key = requests.get('https://aszyw.com/20191019/uyfQazNz/1000kb/hls/key.key',headers=self.header).content
        key = requests.get('https://ts.hao123apps.com/?m3u8=/useruploadfiles/2741e97f73f327e6d57638d82ff88711/2741e97f73f327e6d57638d82ff88711.m3u8',headers=self.header).content
        cryptor = AES.new(key, AES.MODE_CBC, key)
        with open(ts_name,'wb') as f:
            f.write(cryptor.decrypt(resp.content))

    def download_all_ts(self, ts_urls):
        with ThreadPoolExecutor(max_workers=2) as executor:
            for index, ts_url in enumerate(ts_urls):
                ts_url = ts_url.replace('\\n','').strip()
                print(ts_url)
                # executor.submit(self.download_single_ts,[ts_url,f'{index}.ts'])
                executor.submit(self.download_single_ts_withoutKey,[ts_url,f'{index}.ts'])

    def merge_mp4(self):
        ts_path = '*.ts'
        # time.sleep(5)
        with open(self.file_name, 'wb') as fn:
            for ts in natsorted(iglob(ts_path)):  # iglob() 函数获取一个可遍历对象，使用它可以逐个获取匹配的文件路径名。
                with open(ts, 'rb') as ft:
                    ts_rb = ft.read()
                    fn.write(ts_rb)
        for ts in iglob(ts_path):
            os.remove(ts)

    def run(self):
        filenames = self.get_m3u8_filenames()
        for filename in filenames:
            self.file_name = os.path.split(filename)[1].split('.')[0] + ".mp4"
            print(filename, self.file_name)
            ts_urls = self.get_file_urls(filename)
            self.download_all_ts(ts_urls)
            ts_path = '*.ts'
            time.sleep(8)
            with open(self.file_name, 'wb') as fn:
                for ts in natsorted(iglob(ts_path)):  # iglob() 函数获取一个可遍历对象，使用它可以逐个获取匹配的文件路径名。
                    with open(ts,'rb') as ft:
                        ts_rb = ft.read()
                        fn.write(ts_rb)
            for ts in iglob(ts_path):
                os.remove(ts)



if __name__ == "__main__":
    # m3u8_url = 'https://aszyw.com/20191019/uyfQazNz/index.m3u8'
    # m3u8_file_path = 'D:/用户目录/下载/466d2c1e4d8807f56c7c7a73f962d027.m3u8'
    # file_name = '466d2c1e4d8807f56c7c7a73f962d027.mp4'
    dir = 'D:/用户目录/下载'
    start_time = time.time()

    d = Download_M3U8(dir)
    d.run()

    end_time = time.time()
    print('use time:', end_time - start_time)