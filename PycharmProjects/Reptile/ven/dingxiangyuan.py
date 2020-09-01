import pymongo
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import json
import os
import csv
from hashlib import md5
from multiprocessing import Pool
from json.decoder import JSONDecodeError
import time
import numpy as np
import pandas as pd
from lxml import etree


class ForthcomingConference():
    
    def __init__(self):
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Cookie': 'DXY_USER_GROUP=28; route=fe9340375d898dc58dc46edbbdbb48f8; cms_token=8461510b-ed1d-449e-a938-ec523bf0abb5; CMSSESSIONID=100C3F99213DD147190987453364FD0B-n1; __asc=434c4a5817326bab52655070450; __auc=434c4a5817326bab52655070450; Hm_lvt_8a6dad3652ee53a288a11ca184581908=1594082637; __utma=256353815.737374217.1594082637.1594082637.1594082637.1; __utmc=256353815; __utmz=256353815.1594082637.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=256353815.737374217.1594082637.1594082637.1594082637.1; __utmc=256353815; __utmz=256353815.1594082637.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=256353815.41.9.1594083966017; __utmb=256353815.42.9.1594083966017; Hm_lpvt_8a6dad3652ee53a288a11ca184581908=1594084008' 
        }
        self.url = 'http://meeting.dxy.cn/tag/list/category/medicine'
        self.gzUrl = ['http://meeting.dxy.cn/tag/list/category/exhibition','http://meeting.dxy.cn/tag/list/category/others','http://meeting.dxy.cn/tag/list/category/oncology']

    def sendReq(self,url):
        try:
            resp = requests.get(url,headers = self.headers)
            if resp.status_code == 200:
                return resp
        except ConnectionError:
            print("error occur")
            return None

    def getListUrl(self):
        resp = self.sendReq(self.url)
        html = resp.content.decode(resp.apparent_encoding)
        selector = etree.HTML(html)
        item_li_node_list = selector.xpath('//*[@id="j_btn1_ct"]/ul/li[1]//following-sibling::li')
        city_li_node_list = selector.xpath('//*[@id="j_select_a_ct"]/ul/li')
        count = 1
        url_list = []
        for item_li_node in item_li_node_list:
            # print(node)
            try:
                url = item_li_node.xpath("./a/@href")[0]
                if 'category/oncology' in url:
                    continue
                count += 1
         
                url_list.append(url)
            except IndexError:
                print('item error')
            continue
        return url_list
    
    def getCityCode(self):
        code_list = []
        resp = self.sendReq(self.url)
        html = resp.content.decode(resp.apparent_encoding)
        selector = etree.HTML(html)
        city_li_node_list = selector.xpath('//*[@id="j_select_a_ct"]/ul/li')
        for city_li_node in city_li_node_list:
            try:
                code_url = city_li_node.xpath('./a/@href')[0]
                if code_url:
                    code = code_url.split('/')[-1:][0]
               
                    for gzUrl in self.gzUrl:
                        realUrl = gzUrl + '/' + code
                        code_list.append(realUrl)
            except IndexError:
                print('code error')
            continue
        return code_list


    def getDetailUrl(self,url):
        try:
            print('pid:',os.getpid())
            resp = self.sendReq(url)
            html = resp.content.decode(resp.apparent_encoding)
            selector1 = etree.HTML(html)
            detailUrlLsitNode = selector1.xpath('//*[@class="x_title"]')
            for node in detailUrlLsitNode:
                detailUrl = node.xpath('./a/@href')[0]
                print(url,detailUrl)
                item = self.getDetailData(detailUrl)
                self.getDtatByCsv(item)

            if '下一页' in html:
                nextPage = selector1.xpath('//a[contains(text(),"下一页")]/@href')[0]
                if nextPage:
                    return self.getDetailUrl(nextPage)
            print(f'{url} 地址全部获取完成')
            return None
        except AttributeError:
            raise
      


    def getDetailData(self,detailUrl):
        item = {}
        response = self.sendReq(detailUrl)
        detailHtml = response.text
        selector = etree.HTML(detailHtml)
        item['url'] = detailUrl
        item['title'] = selector.xpath('//div[@id="j_article_desc"]//h1[@class="title"]/text()')
        item['meetTime'] = ''.join(selector.xpath('//li[contains(text(),"会议时间")]/text()')).replace('\t','').replace('\n','').replace('会议时间：','').strip()
        item['meetAddr'] = ''.join(selector.xpath('//li[contains(text(),"会议地点")]/text()')).replace('\t','').replace('\n','').replace('会议地点：    ','').strip()
        item['Phone'] = ''.join(selector.xpath('//li[contains(text(),"电话")]/text()')).replace('\t','').replace('\n','').replace('电话：','').strip()
        item['fax'] = ''.join(selector.xpath('//li[contains(text(),"传真")]/text()')).replace('\t','').replace('\n','').replace('传真：','').strip()
        item['linkPerson'] = ''.join(selector.xpath('//li[contains(text(),"联系人")]/text()')).replace('\t','').replace('\n','').replace('联系人：','').strip()
        item['Email'] = ''.join(selector.xpath('//li[contains(text(),"Email")]/a/text()')).replace('\t','').replace('\n','').strip()
        item['linkAddr'] = ''.join(selector.xpath('//li[contains(text(),"联系地址")]/text()')).replace('\t','').replace('\n','').replace('联系地址：','').strip()
        item['meetUrl'] = ''.join(selector.xpath('//li[contains(text(),"会议网址")]/a/text()')).replace('\t','').replace('\n','').strip()
        print(item)
        return item

    def getDtatByCsv(self,item):
        try:
            with open('test3.csv','a',encoding='utf-8-sig',newline='') as f:
                fieldnames = ['url','title', 'meetTime','meetAddr','Phone','fax','linkPerson','Email','linkAddr','meetUrl']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                # writer.writeheader()
                writer.writerow(item)
        except UnicodeEncodeError:
            raise
     


if __name__ == "__main__":
    import pandas as pd
    a='http://meeting.dxy.cn/tag/list/category/oncology/loc_500000'
    fc = ForthcomingConference()
    all_url = fc.getListUrl() + fc.getCityCode()
    print(len(all_url))
    print(len(set(all_url)))
    df = pd.DataFrame({'url':all_url})
    df.to_excel('aa.xlsx', encoding='utf-8', index=0)
    for url in all_url:
        print(url)
    # fc.getDeatilUrl(a)
   
    # p = Pool(4)
    # p.map(fc.getDetailUrl,all_url[10:30])
    # p.close()   # 关闭进程池
    # p.join()
    


