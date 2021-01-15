import requests
import json

class GetParkAppData(object):
    def __init__(self):
        self.url = "https://www.soargift.com/parkApp/park/parkingHomePage.do"
        self.header = {"User-Agent":"Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; vivo Y51A Build/LMY47V) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
                        }
        self.data = {
            "lng":"13.96171512635402",
            "lat":"202.548056306565286",
            "city":"深圳市",
            "isReserve":"2",
            "displayType":"2",
            "type":"1",
            "pageSize":"10",
            "currentPage":"1",
            "lng":"113.96171512635402",
            "isFree":"0",
        }

    def getJson(self):
        response = requests.post(self.url, data=self.data, headers = self.header, verify=False)
        print(response.status_code)
        print(response.json())

if __name__ == "__main__":
    
    g = GetParkAppData()
    g.getJson()