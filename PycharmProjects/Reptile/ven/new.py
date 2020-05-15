import requests
headers={'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'Cookie': 'Hm_lvt_9352f2494d8aed671d970e0551ae3758=1589425635; Hm_lpvt_9352f2494d8aed671d970e0551ae3758=1589436320',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

res = requests.get('http://www.paoshu8.com/52_52542?yyvadc=ehlai3&xuxipo=trf01&eydefy=ehjaq2',headers=headers)
res.encoding='utf-8'
print(res.status_code,res.text,res.url,res.headers)