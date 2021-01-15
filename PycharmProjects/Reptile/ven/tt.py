import requests
import os
# url = 'http://mall.wine-world.com/'

# s = requests.session()
# r = s.get(url)
# # print(r.content.decode('utf-8'))
# print(r.headers)

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

a = lambda p: os.path.join(os.path.dirname(__file__), p)
    

print(a("../TestData/Login/test_login_data.yml"))