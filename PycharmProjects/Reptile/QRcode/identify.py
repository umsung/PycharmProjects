import requests
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') #改变标准输出的默认编码

def test_identify():
    header = {
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'UM_distinctid=1751a44e3fb349-003f2f2dc3c8e7-63131f79-13c680-1751a44e3fc257; ASPSESSIONIDCWBATARS=EGGHFHDCIKNNEJAOBEBOHHKP; CNZZDATA1277886419=556514235-1602462083-%7C1602556127',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    data = {'str':210402199904270148}
    url = 'https://bajiu.cn/sfz/'
    r = requests.post(url, headers = header, data=data)
    print(r.status_code)
    print(r.text)


test_identify()
