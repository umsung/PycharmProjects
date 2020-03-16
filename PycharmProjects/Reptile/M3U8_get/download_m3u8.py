import os
import time
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
    
    def __init__(self,m3u8_url,file_name):
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',}
        self.thread = ThreadPoolExecutor(max_workers=10)
        self.m3u8_url = m3u8_url
        self.file_name = file_name
        self.lock = threading.Lock()

    def get_urls(self):
        m3u8_obj = m3u8.load(self.m3u8_url)
        base_uri = m3u8_obj.base_uri
        for i in m3u8_obj.segments:
            yield urljoin(base_uri,i)

    def get_file_urls(self):
        a=[]
        with open('D:/用户目录/下载/YaimFi8l1','r') as f:
            a=f.readlines()
            for i in a:
                if '#' not in i:
                    domain = 'https://aszyw.com'
                    # url = domain + i
                    yield domain + i
            #         a.append(domain+i)
            # return a

    def download_single_ts(self,urlinfo):
        url,ts_name = urlinfo
        resp = requests.get(url,headers=self.header)
        key = requests.get('https://aszyw.com/20191019/uyfQazNz/1000kb/hls/key.key',headers=self.header).content
        cryptor = AES.new(key, AES.MODE_CBC, key)
        with open(ts_name,'wb') as f:
            f.write(cryptor.decrypt(resp.content))

    def download_all_ts(self):
        # ts_urls = self.get_urls()
        ts_urls = self.get_file_urls()
        print(ts_urls)
        with self.thread as executor:
            for index,ts_url in enumerate(ts_urls):
                print(ts_url)
                ts_url = ts_url.replace('\\n','').strip()
                print(ts_url)
                executor.submit(self.download_single_ts,[ts_url,f'{index}.ts'])


    def merge_mp4(self):
        pass

    def run(self):
        self.download_all_ts()
        ts_path = '*.ts'
        with open(self.file_name,'wb') as fn:
            for ts in natsorted(iglob(ts_path)):  # iglob() 函数获取一个可遍历对象，使用它可以逐个获取匹配的文件路径名。
                with open(ts,'rb') as ft:
                    ts_rb = ft.read()
                    fn.write(ts_rb)
        for ts in iglob(ts_path):
            os.remove(ts)






if __name__ == "__main__":
    m3u8_url='https://aszyw.com/20191019/uyfQazNz/index.m3u8'
    file_name='test.mp4'
    start_time = time.time()

    d = Download_M3U8(m3u8_url,file_name)
    d.run()

    end_time = time.time()
    print('use time:', end_time - start_time)