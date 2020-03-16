import os
import time,requests
import m3u8
from urllib.parse import urljoin

# m3u8_obj = m3u8.load('https://aszyw.com/ppvod/YaimFi8l')
# base_uri = m3u8_obj.base_uri
# print(base_uri)
# for seg in m3u8_obj.segments:
#             a= urljoin(base_uri,seg.uri)
#             print(a)

# with open('D:/用户目录/下载/YaimFi8l','r') as f:
#     a=f.readlines()

#     for i in a:
#         if '#' not in i:
#             domain = 'https://aszyw.com'
#             url = domain + i
#             print(url)

# def get_file_urls():
#     a=[]
#     with open('D:/用户目录/下载/YaimFi8l','r') as f:
#         a=f.readlines()
#         for i in a:
#             if '#' not in i:
#                 domain = 'https://aszyw.com'
#                 # url = domain + i
#                 yield domain + i
        #         a.append(domain+i)
        # return a

# ts_urls = get_file_urls()
# for index,ts_url in enumerate(ts_urls):
#     print(index,ts_url)

header ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
all_content  = requests.get('https://aszyw.com/ppvod/YaimFi8l',headers=header).text
file_line = all_content.split("\n")
print(file_line)