import os
import sys
import requests
import datetime
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

def get_movie():
    with open('D:/用户目录/下载/YaimFi8l','r') as f:
        all_content = f.read()

    file_line = all_content.split("\n")
    # print(file_line)
    header ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    for line in file_line:
        if '#EXT-X-KEY' in line:
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]

            uri_pos = line.find("URI")
            print(uri_pos)
            quotation_mark_pos = line.rfind('"')
            quotation_mark_pos2 = line.find('"')
            print(quotation_mark_pos)
            print(quotation_mark_pos2)
            key_path ='https://aszyw.com' + line[uri_pos:quotation_mark_pos].split('"')[1]
            print(key_path)
            res = requests.get(key_path,headers=header)
            key = res.content
            print(res)

        if '.ts'  in line:
            # /20191019/uyfQazNz
            url = 'https://aszyw.com' + line

            res = requests.get(url,headers=header)
            c_fule_name = line.rsplit('/', 1)[-1]
            # print(url)
            if len(key_path):
                cryptor = AES.new(key, AES.MODE_CBC, key)
                with open(c_fule_name+'.mp4','ab') as f:
                    f.write(cryptor.decrypt(res.content))
            else:
                with open(c_fule_name+'.mp4','ab') as f:
                    f.write(res.content)

def merge_file(path):
    os.chdir(path)
    cmd = "copy /b * new.tmp" # windows窗口命令——(copy/b)文件无缝拼接隐藏
    os.system(cmd)
    os.system('del /Q *.ts')
    os.system('del /Q *.mp4')
    os.rename("new.tmp", "new.mp4")



if __name__ == "__main__":
    get_movie()


