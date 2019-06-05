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
import pandas as pd


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Referer': 'http://dyjy.dtdjzx.gov.cn/resourcelist?tdsourcetag=s_pctim_aiomsg',
    'Content-Type': 'application/json;charset=UTF-8'
  }

def get_page_index(pageNo):
    pyload = {
        "isSort": "1",
        "pageNo": pageNo,
        "pageSize": "10",
              }

    url = 'http://dyjy.dtdjzx.gov.cn/course/special/findAll'
    resp = requests.post(url, data=json.dumps(pyload), headers=headers)
    resp.encoding = 'utf-8'
    print(resp.text)
    return resp.text


def parse_page_index(html):
    try:
        data = json.loads(html)
        specialId = []
        if data and 'data' in data.keys():
            for item in data.get('data'):
                # specialId.append(item.get('specialId'))
                yield item.get('specialId')
        # print(specialId)
        # return specialId

    except JSONDecodeError:
        pass


def get_page_detail(specialId):
    pyload = {
        "pageNo": "1",
        "pageSize": "6",
        "specialId": specialId,
    }
    try:
        resp = requests.post('http://dyjy.dtdjzx.gov.cn/course/special/findCourseBySpecialId', headers=headers, data=json.dumps(pyload))
        resp.encoding = 'utf-8'
        if resp.status_code == 200:
            # print(resp.text)
            results = resp.text
            results = json.loads(results)
            count = int(results['count'])
            print('count',count)
            return count
        return None
    except ConnectionError:
        print("error occur")
        return None


def parse_page_detail(count, specialId):

    # results = json.loads(detail_json)
    # if 'count' in results.keys():
    #     count = int(results['count'])
    #     print(count)
    if count <= 6:
        pyload = {
            "pageNo": 1,
            "pageSize": "6",
            "specialId": specialId,
        }

        try:
            resp = requests.post('http://dyjy.dtdjzx.gov.cn/course/special/findCourseBySpecialId', headers=headers,
                                 data=json.dumps(pyload))
            resp.encoding = 'utf-8'
            if resp.status_code == 200:
                # print(resp.text)
                results = resp.text
                results = json.loads(results)
                a = []
                if 'data' in results.keys():
                    for data in results['data']:
                        courseId = data['courseId']
                        courseName = data['courseName']
                        url = 'http://dyjy.dtdjzx.gov.cn/resourcedetailed/' + str(courseId)
                        print("是否都走这里")
                        print('url:', url, courseName)
                        a.append([url, courseName])
                save_data_pd(a)

            return None
        except ConnectionError:
            print("error occur")
            return None

    elif count > 6 and count % 6 == 0:
        pageNo = int(count / 6)
        pageNo = pageNo + 1
        print('pageNo:', pageNo)
        for i in range(1, pageNo+1):
            print('i:', i)
            pyload = {
                "pageNo": i,
                "pageSize": "6",
                "specialId": specialId,
            }
            try:
                resp = requests.post('http://dyjy.dtdjzx.gov.cn/course/special/findCourseBySpecialId', headers=headers,
                                     data=json.dumps(pyload))
                resp.encoding = 'utf-8'
                a = []
                if resp.status_code == 200:
                    # print(resp.text)
                    results = resp.text
                    results = json.loads(results)
                    if 'data' in results.keys():
                        for data in results['data']:
                            courseId = data['courseId']
                            courseName = data['courseName']
                            url = 'http://dyjy.dtdjzx.gov.cn/resourcedetailed/' + str(courseId)
                            print("是否都走这里第二")
                            print('url:', url, courseName)
                            a.append([url, courseName])
                        save_data_pd(a)
                # return None
            except ConnectionError:
                print("error occur")
                # return None
    else:
        pageNo = int(count//6) + 1
        print('pageNo:', pageNo)
        for i in range(1, pageNo+1):
            print('i:', i)
            pyload = {
                "pageNo": i,
                "pageSize": "6",
                "specialId": specialId,
            }

            try:
                resp = requests.post('http://dyjy.dtdjzx.gov.cn/course/special/findCourseBySpecialId', headers=headers,
                                     data=json.dumps(pyload))
                resp.encoding = 'utf-8'
                if resp.status_code == 200:
                    # print(resp.text)
                    results = resp.text
                    results = json.loads(results)
                    a = []
                    if 'data' in results.keys():
                        for data in results['data']:
                            courseId = data['courseId']
                            courseName = data['courseName']
                            url = 'http://dyjy.dtdjzx.gov.cn/resourcedetailed/' + str(courseId)
                            print("是否都走这里第三")
                            print('url:', url, courseName)
                            a.append([url, courseName])
                        save_data_pd(a)
                # return None
            except ConnectionError:
                print("error occur")
                # return None


def save_data_csv():
    f = open('连接.csv', 'a', encoding='utf-8', newline='')
    a = csv.writer(f)
    return a


def save_data_pd(data):
    data = pd.DataFrame(data,columns = ['url','name'])
    data.to_csv('视频url.csv', encoding='utf-8', index=0, mode='a+', header=False)

def save_data_json(data):
    f = open('json.csv', 'w', encoding='utf-8')
    line = json.dumps(data, ensure_ascii=False) + '\n'
    return f.write(line)


if __name__ == '__main__':
    for num in range(1, 47):
        html = get_page_index(num)
        for id in parse_page_index(html):
            count = get_page_detail(id)
            parse_page_detail(count, id)