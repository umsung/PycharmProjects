# session and cookies
import requests

gurl = 'https://pan.baidu.com/'
purl = 'https://pan.baidu.com/login'
data = {'':''}
response =requests.post(purl,data='data')
cookies = response.cookies()

response2 = requests.get(gurl,cookies=cookies)
print(response2.text)


# 或者  内置session对象自动处理cookies
session = requests.Session()
response = session.post(purl,data=data)
cookies = session.cookies

response2 = session.get(gurl)
print(response2.text)