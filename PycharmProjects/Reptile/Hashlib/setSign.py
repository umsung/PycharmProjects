from hashlib import md5

# body参数去掉 空值和key为sign的值，按照字母排序成字符串，在加上Key，md5加密
class Tools(object):
    def __init__(self,key):
        self.key = key
        self.body =  {
                "username": "test",
                "password": "123456",
                "mail": ""
            }

    def getSign(self):
        bodyList = [ "".join(i) for i in self.body.items() if i[1] and i[0] != "sign"]
        signStr = "".join(sorted(bodyList)) + self.key 
        sign = md5(signStr.encode('utf-8')).hexdigest()
        return sign


if __name__ == "__main__":
    s = Tools("sercet")
    print(s.getSign())