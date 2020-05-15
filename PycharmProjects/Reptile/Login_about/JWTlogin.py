# JWT JSON WEB Token
# 登陆依赖JWT本身的token，token通过，服务器就会返回有效数据
# 先带上登陆信息请求，获取JWT结果，在后序的请求头中带上token

import requests

resp = requests.get('url')
data = resp.json()
jwt = data.get('token')
print(jwt)