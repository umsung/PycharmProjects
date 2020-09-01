#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: config.py 
@time: 2020-06-06 23:32 
@description：配置文件
"""

USERNAME = 'root'
PASSWORD = '123456'
HOSTNAME = "192.168.99.100"
PORT = '3306'
DATABASE = 'docker'

DIALECT = 'mysql'
DRIVER = 'pymysql'

# 连接数据的URI
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

SWAGGER_TITLE = "API"
SWAGGER_DESC = "API接口"
# 地址，必须带上端口号
SWAGGER_HOST = "localhost:5000"
