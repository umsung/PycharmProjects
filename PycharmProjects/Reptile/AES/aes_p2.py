import base64
from Crypto.Cipher import AES
import base64
import json
import pandas as pd
import csv
from hashlib import md5
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
# 密钥（key）, 密斯偏移量（iv） CBC模式加密

class WeatherData(object):
    def __init__(self,aes_local_key,aes_local_iv):
        self.aes_local_key = aes_local_key
        self.aes_local_iv = aes_local_iv
        self.secretkey = md5(self.aes_local_key.encode('utf-8')).hexdigest()[16:32]
        self.secretvi = md5(self.aes_local_iv.encode('utf-8')).hexdigest()[:16]
        # 3c06ccb862a7f3b7 b79d844d6b437a7c

    def AES_Encrypt(self,data,key,vi):
        #vi = '0102030405060708'
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        data = pad(data)
        # 字符串补位
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
        encryptedbytes = cipher.encrypt(data.encode('utf8'))
        # 加密后得到的是bytes类型的数据
        encodestrs = base64.b64encode(encryptedbytes)
        # 使用Base64进行编码,返回byte字符串
        enctext = encodestrs.decode('utf8')
        # 对byte字符串按utf-8进行解码
        return enctext


    def AES_Decrypt(self,data,key,vi):
        #vi = 'b79d844d6b437a7c'
        data = data.encode('utf8')
        encodebytes = base64.decodebytes(data)
        # print(encodebytes)
        # 将加密数据转换位bytes类型数据
        cryptos = AES.new(key.encode('utf8'), AES.MODE_CBC, self.secretvi.encode('utf8'))
        text_decrypted = cryptos.decrypt(encodebytes)
        unpad = lambda s: s[0:-s[-1]]
        text_decrypted = unpad(text_decrypted)
        # 去补位
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted

    def getJson(self):
        options = Options()
        # chrome_options.add_argument("--headless")
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = Chrome(options=options)

        # 打开能识别selenium页面前先运行这个stealth.min.js
        with open('D:/Git/PycharmProjects/PycharmProjects/Reptile/seleniun_Learn/stealth.min.js') as f:
            js = f.read()

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
        })
        driver.get('https://www.aqistudy.cn/historydata/daydata.php?city=%E9%98%BF%E5%9D%9D%E5%B7%9E&month=2015-01')
        
        a = driver.execute_script("return localStorage.length")
        time.sleep(0.7)
        print(a)
        js = "return localStorage.getItem(localStorage.key(0))"
        storageValue = driver.execute_script(js)
        driver.
        # 3340f063da2796c669f4dd4c61a29924
        # print(storageValue)
        resultJsonData =base64.b64decode(self.AES_Decrypt(storageValue,self.secretkey,self.secretvi).encode('utf-8')).decode('utf-8')
        print(resultJsonData)
        return resultJsonData


    def get_data(self,jsonData):
        result = json.loads(jsonData)
        if 'data' in result.keys() and 'items' in result['data'].keys():
            datas = result["data"]["items"]
            print(datas)
            # save_data_pd(datas)

    def save_data_csv(self):
        f = open('连接.csv', 'a', encoding='utf-8', newline='')
        a = csv.writer(f)
        return a

    def save_data_pd(self,data):
        data = pd.DataFrame(data,columns = ['time_point','aqi','max_aqi','min_aqi','pm2_5','pm10','co','no2','o3','so2','rank','quality'])
        # data = pd.DataFrame(data)
        print(data)
        # header为false或-1表示无头，默认为0
        data.to_csv('E:/视频3url.csv', encoding='gbk', index=0, mode='a+', header=0)


if __name__ == "__main__":
    aes_local_key = 'emhlbnFpcGFsbWtleQ=='
    aes_local_iv = 'emhlbnFpcGFsbWl2'
    w = WeatherData(aes_local_key,aes_local_iv)
    w.get_data(w.getJson())

# key = '3c06ccb862a7f3b7'

# # enctext = AES_Encrypt(key, data)
# # print(enctext)
# text_decrypted = AES_Decrypt(key, data2)
# # print(text_decrypted)
# print(base64.b64decode(text_decrypted.encode('utf-8')).decode('utf-8'))
# get_data(base64.b64decode(text_decrypted.encode('utf-8')).decode('utf-8'))

# # 7b47fcf4a135c2d024ff327f8544803e

