import requests
import os
import hashlib

host = 'localhost'


def token(user='test', psw='123456'):
    """
    登陆获取token
    :param user: 用户名
    :param psw: 密码
    :return: token
    """
    url = host + 'api/v1/login'
    headers = {
        "Content-Type": "application/json",
        "User-Agent": ""
    }
    data = {
        'user': user,
        'pwd':  psw,
    }
    try:
        r = requests.post(url, headers=headers, data=data)
        return_token = r.json['token']
        return return_token
    except:
        print('返回错误,返回值为{}'.format(r.text))
        return_token = ''
    return return_token


def ENV(keyname):
    value = os.environ.get(keyname)
    return value


def hook_up():
    print("前置操作：setup!")


def hook_down():
    print("后置操作：teardown!")



def sign_body(body, apikey="12345678"):
    '''请求body sign签名'''
    # 列表生成式，生成key=value格式
    a = ["".join(i) for i in body.items() if i[1] and i[0] != "sign"]
    # print(a)
    # 参数名ASCII码从小到大排序
    strA = "".join(sorted(a))
    # print(strA)

    # 在strA后面拼接上apiKey得到striSignTemp字符串
    striSignTemp = strA+apikey

    # 将strSignTemp字符串转换为小写字符串后进行MD5运算

    # MD5加密
    def jiamimd5(src):
        m = hashlib.md5()
        m.update(src.encode('UTF-8'))
        return m.hexdigest()
    sign = jiamimd5(striSignTemp.lower())
    # print(sign)

    return sign

def setup_request(request):
    '''setuphook函数，发请求前预处理'''
    body = request.get("json")
    print(body)
    # 由body请求参数生成sign值
    sign = sign_body(body, apikey="12345678")
    print("sign值：%s" % sign)
    request["json"]["sign"] = sign






