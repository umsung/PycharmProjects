import requests
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

url = 'https://www.tiobe.com/tiobe-index/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}

def getHTML(count=1):
    if count > 5:
        print('Tried Too Many Counts')
        return None
    try:
        res = requests.get(url,headers = headers)
        if res.status_code == 200:
            html = res.text
            return html
    except ConnectionError:
        count += 1
        return getHTML(count)
    

def praseIndex(html):
    total_content = re.findall(r'series: (.*?)\}\);',html,re.S)[0]
    total_content = re.findall(r'({.*?})',total_content,re.S)
    # print(total_content)
    with open('test.csv','w',encoding='utf-8',newline='') as f:
        writer = csv.DictWriter(f,['name','value','data'])
        writer.writeheader()
        for content in total_content:
            name = ''.join(re.findall(r"name : '(.*?)',",content,re.S))
            if name == 'Visual Basic':
                name = 'VB'
            if name == 'JavaScript':
                name = 'JS'
            datas = re.findall(r'\[Date.UTC\((.*?)\),(.*?)\]',content,re.S)
            # print(datas)
            for strTime,data in datas:
                data = data.replace(' ','')
                timelist = strTime.replace(' ','').split(',')
                timelist[1] = '12' if timelist[1] == '0' else timelist[1]
                month = '0'+timelist[1] if len(timelist[1]) == 1 else timelist[1]
                day = '0'+timelist[2] if len(timelist[2]) == 1 else timelist[2]
                print(timelist)
                print(month)
                strTime = timelist[0] + '/' + month + '/' + day
                print(strTime)
               
                writer.writerow({'name':name,'value':strTime,'data':data})
                # timelist = strTime.split(',')
                # for index,t in enumerate(timelist):
                #     if index != 0 and len(t) = 1:
                #         t = '0'+ t

def readData(filePath='E:/gitL/test.csv'):
    df = pd.read_csv(filePath)
    name = set(df['name'].tolist())
    
    monthList = df[df['name'].isin(['Java'])]['value']
    # print(monthList,type(monthList),type(monthList.tolist()),monthList.index)
    # print(df[(df['value'] == monthList[0]) & (df['name'] == 'Java')])
    # print(df[(df['value'] == monthList[0]) & (df['name'] == 'Java')]['data'].values)
    item = {}
    for month in monthList:
        temp = {}
        for n in name:
            try:
                temp[n] = df[(df['value'] == month) & (df['name'] == n)]['data'].values[0]
            except:
                temp[n] = 0
        item[month] = temp
    # print(item)
    return item,name

def Show(datas,name):
    ax = plt.gca()
    color = ['k','r','sienna','yellow','g','aquamarine','dodgerblue','pink','b','darkviolet']
    color_dict = dict(zip(name,color))
    for data in datas.items():
        # [('C#', 0.38), ('Python', 1.25), ('JS', 1.55), ('PHP', 1.9), ('SQL', 2.96), ('C+
# +', 14.2), ('C', 20.24), ('Java', 26.49)]
        plt.cla()
        temp = sorted(data[1].items(),key = lambda x: x[1])
        x = [item[0] for item in temp]
        color = [color_dict[t] for t in x]
        y = [item[1] for item in temp]
        plt.barh(range(1,11),y,color=color)
        plt.title(data[0],fontsize=24,fontproperties='ssimhei')
        plt.yticks(range(1,11),list(x),fontsize=16,fontproperties='simhei')
        plt.xticks(range(0,30,100))
        for x,y in zip(range(1,11),y):
            plt.text(y+0.1,x-0.1,str(y))
        plt.pause(0.12)
    plt.show()

# praseIndex(getHTML())

item,name = readData()
# Show(item,name)