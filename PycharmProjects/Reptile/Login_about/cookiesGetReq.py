import requests
import time
import re
import io
from bs4 import BeautifulSoup 
import sys
import urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

class TakeCookiesReq(object):

    def __init__(self):
        self.listurl = 'http://bbs.oncity.cc/'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        self.url = 'http://bbs.oncity.cc/forum-5-{}.html'
        self.s = requests.session()

    def getListCookies(self):
        r = requests.get(self.listurl, headers = self.headers)
        print(r.cookies)
        lastact = r.cookies['B2uw_21bb_lastact'] 
        sid = r.cookies['B2uw_21bb_sid']
        print(lastact,sid)
        return lastact,sid

    def getAA(self , lastact, sid): 
        url = self.url.format(1)
        r = requests.get(url, headers = self.headers)
        dd = re.findall(r'dd=\[(.*?),\]', r.text, re.S)
        # print(r.text)
        print(dd)
        for i in dd:
            dd = i.split(',')
        dd.reverse()
        chr_dd = ''.join([chr(int(i)) for i in dd])
        cc= re.findall(r'cc=\[(.*?)\]', r.text, re.S)
        print(cc)
        t = time.time()
        ht = str(int(t))
        wt = int(t*1000)
        chr_cc = ''.join([chr(int(i)) for i in cc[0].split(',') ])
        print(chr_dd,chr_cc)
        cookies = "aa={}; B2uw_21bb_lastvisit={}; B2uw_21bb_sid={}; B2uw_21bb_visitedfid=5D4;  B2uw_21bb_lastact={}".format(chr_dd,str(wt),sid,lastact+'forumdisplay')
        self.headers['cookie'] = cookies

    def getdata(self):

        for i in range(1,3):
            url = self.url.format(i)
            r = requests.get(url, headers = self.headers)
            # print(r.cookies)
            # print(r.text)
            selector = BeautifulSoup(r.text, 'html.parser')
            nodes = selector.select('th.new > a.xst')
            print("-----第{}页----".format(i))
            for node in nodes:
                print(node.text,node.get('href'))



tcr = TakeCookiesReq()
lastact,sid = tcr.getListCookies()
tcr.getAA(lastact,sid)
tcr.getdata()