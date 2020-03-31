# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 19:04:00 2019

@author: iHJX_Alienware
"""

import numpy as np
import pandas as pd  
# 导入numpy、pandas模块

'''
1、series
'''
s = pd.Series(np.random.rand(5))
print(s)
print(type(s))
# 查看数据、数据类型

print(s.index,type(s.index))
print(s.values,type(s.values))
# .index查看series索引，类型为rangeindex
# .values查看series值，类型是ndarray

# 核心：series相比于ndarray，是一个自带索引index的数组 → 一维数组 + 对应索引
# 所以当只看series的值的时候，就是一个ndarray
# series和ndarray较相似，索引切片功能差别不大
# series和dict相比，series更像一个有顺序的字典（dict本身不存在顺序），其索引原理与字典相似（一个用key，一个用index）


# 数据查看
s = pd.Series(np.random.rand(50))
print(s.head(10))
print(s.tail())
    # .head()查看头部数据
    # .tail()查看尾部数据


'''
2、Dataframe
"二维数组"Dataframe：是一个表格型的数据结构，包含一组有序的列，其列的值类型可以是数值、字符串、布尔值等。
Dataframe中的数据以一个或多个二维块存放，不是列表、字典或一维数组结构。
'''
# Dataframe 数据结构
# Dataframe是一个表格型的数据结构，“带有标签的二维数组”。
# Dataframe带有index（行标签）和columns（列标签）

data = {'name':['Jack','Tom','Mary'],
        'age':[18,19,20],
       'gender':['m','m','w']}
frame = pd.DataFrame(data)
print(frame)  
print(type(frame))
print(frame.index,'\n该数据类型为：',type(frame.index))
print(frame.columns,'\n该数据类型为：',type(frame.columns))
print(frame.values,'\n该数据类型为：',type(frame.values))
    # 查看数据，数据类型为dataframe
    # .index查看行标签
    # .columns查看列标签
    # .values查看值，数据类型为ndarray


# Dataframe 创建方法一：由数组/list组成的字典
data1 = {'one':np.random.rand(3),'two':np.random.rand(3), 'three': [1,2,3]} 

# Dataframe 创建方法二：由Series组成的字典
data2 = {'one':pd.Series(np.random.rand(2)),
         'two':pd.Series(np.random.rand(3))
         }

# Dataframe 创建方法三：通过二维数组直接创建
ar = np.random.rand(9).reshape(3,3)
data3 = pd.DataFrame(ar, index = ['a', 'b', 'c'], columns = ['one','two','three'])  # 可以尝试一下index或columns长度不等于已有数组的情况

# Dataframe 创建方法四：由字典组成的列表
dic = [{'one': 1, 'two': 2}, {'one': 5, 'two': 10, 'three': 20}]
data4 = pd.DataFrame(dic)

# Dataframe 创建方法五：由字典组成的字典
dic = {'Jack':{'math':90,'english':89,'art':78},
       'Marry':{'math':82,'english':95,'art':92},
       'Tom':{'math':78,'english':67}}
data5 = pd.DataFrame(dic)


'''
3、索引问题
'''


'''
4、文本数据处理
'''
# 字符串常用方法（1） - lower，upper，len，startswith，endswith
s = pd.Series(['A','b','bbhello','123',np.nan])
print(s.str.lower(),'→ lower小写\n')
print(s.str.upper(),'→ upper大写\n')
print(s.str.len(),'→ len字符长度\n')
print(s.str.startswith('b'),'→ 判断起始是否为a\n')
print(s.str.endswith('3'),'→ 判断结束是否为3\n')

s = pd.Series([
     'Washington, D.C. 20003',
     'Brooklyn, NY 11211-1755',
     'Omaha, NE 68154',
     'Pittsburgh, PA 15211'
 ]) 
print(s.str.count(r'\d'),'→ count对指定字符计数\n')
print(s.count(),'统计s的元素个数')
print(s.str.replace('h','H')，'s.str.replace对字符串进行替换')
print(s.replace('bbhello','BBHello'),'s.replace对整个元素进行替换')
regex = (r'?P<city>[a-zA-Z]+,?P<state>[0-9]{2}?P<zip>\d{5}(?:-\d{4})?')
print(s.str.replace('.','').str.extract(regex))

# 字符串常用方法（2） - replace
df = pd.DataFrame(np.random.randn(3, 2), columns=[' Column A ', ' Column B '],
                  index=range(3))
df.columns = df.columns.str.replace(' ','-')

# 字符串常用方法（3） - split
s = pd.Series(['a,b,c','1,2,3',['a,,,c'],np.nan])
print(s.str.split(','))

# 字符串索引
s = pd.Series(['A','b','C','bbhello','123',np.nan,'hj'])
df = pd.DataFrame({'key1':list('abcdef'),
                  'key2':['hee','fv','w','hija','123',np.nan]})
print(s.str[0])  # 取第一个字符串
print(s.str[:2])  # 取前两个字符串
print(df['key2'].str[0]) 


'''
5、merge与concat
'''
# merge合并 → 类似excel的vlookup
df1 = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
df2 = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
pd.merge(df1, df2, on='key')

# 参数how → 合并方式
df3 = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                    'key2': ['K0', 'K1', 'K0', 'K1'],
                    'A': ['A0', 'A1', 'A2', 'A3'],
                    'B': ['B0', 'B1', 'B2', 'B3']})
df4 = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                    'key2': ['K0', 'K0', 'K0', 'K0'],
                    'C': ['C0', 'C1', 'C2', 'C3'],
                    'D': ['D0', 'D1', 'D2', 'D3']})
print(pd.merge(df3, df4,on=['key1','key2'], how = 'inner'))  
    # inner：默认，取交集
print(pd.merge(df3, df4, on=['key1','key2'], how = 'outer'))  
    # outer：取并集，数据缺失范围NaN
print(pd.merge(df3, df4, on=['key1','key2'], how = 'left'))  
    # left：按照df3为参考合并，数据缺失范围NaN
print(pd.merge(df3, df4, on=['key1','key2'], how = 'right'))  
    # right：按照df4为参考合并，数据缺失范围NaN

# 参数 left_on, right_on, left_index, right_index → 当键不为一个列时，可以单独设置左键与右键

df1 = pd.DataFrame({'lkey':list('bbacaab'),
                   'data1':range(7)})
df2 = pd.DataFrame({'rkey':list('abd'),
                   'date2':range(3)})
print(pd.merge(df1, df2, left_on='lkey', right_on='rkey'))
    # df1以‘lkey’为键，df2以‘rkey’为键
df1 = pd.DataFrame({'key':list('abcdfeg'),
                   'data1':range(7)})
df2 = pd.DataFrame({'date2':range(100,105)},
                  index = list('abcde'))
print(pd.merge(df1, df2, left_on='key', right_index=True))
    # df1以‘key’为键，df2以index为键
# left_index：为True时，第一个df以index为键，默认False
# right_index：为True时，第二个df以index为键，默认False
# 所以left_on, right_on, left_index, right_index可以相互组合：
# left_on + right_on, left_on + right_index, left_index + right_on, left_index + right_index


# 连接：concat

s1 = pd.Series([1,2,3])
s2 = pd.Series([2,3,4])
s3 = pd.Series([1,2,3],index = ['a','c','h'])
s4 = pd.Series([2,3,4],index = ['b','e','d'])
print(pd.concat([s1,s2]))
print(pd.concat([s3,s4]).sort_index())
    # 默认axis=0，行+行

print(pd.concat([s3,s4], axis=1))
    # axis=1,列+列，成为一个Dataframe


df = pd.read_excel('tt.xlsx', sheet_name=0, header=None, names = ['电话', '地址', '公司'])
df['省会'] = df['地址'].str.split('.').str[0]
df['城市'] = df['地址'].str.split('.').str[1]
df['详细地址'] = df['地址'].str.split('.').str[2]
df['电话'] = df['电话'].str.split('：').str[1]

# 去重
df.drop_duplicates()

# 删除指定行、列
# df.drop('地址', axis=1) # 删除指定列
# df.drop(['1', '2']) # 删除指定行
# del df['地址']  # 删除指定列

# 删除含有空值的行或列 df.dropna()  返回删除后的表
# print(df.dropna())  # 默认删除行，有空值的行就删除
# print(df.dropna(axis=1))  # 删除列，有空值的列就删除
# print(df.dropna(how='all'))  # 所有值全为缺失值的行才删除
# print(df.dropna(thresh=2)) # "至少出现过两个缺失值才删除"
# print(df.dropna(subset=['电话', '城市']))  # "返回删除这个subset中的含有缺失值的行或列的df表"

# 排序
# df.sort_values(by='地址') 指定列排序
# df.sort_values(by='1'，axis=1) 指定行排序，与删除相反

# fillna能够使用指定的方法填充NA/NaN值。。（空值是” “， 缺失值是NAN）

a = np.arange(100,dtype=float).reshape((10,10))
for i in range(len(a)):
    a[i,:i] = np.nan
a[6,0] = 100.0

d=pd.DataFrame(a)
# 用0填补空值
print(d.fillna(value=0)
# 用前一行的值填补空值
print(d.fillna(method='pad',axis=0))

# 用后一列的值填补空值
print(d.fillna(method='backfill', axis=1))
# 连续空值，最多填补3个
print(d.fillna(method='ffill',axis=0, limit=3))

# 每条轴上，最多填补3个
print(d.fillna(value=-1,axis=0, limit=3))

df['公司'] = df['公司'].fillna('缺失项').head(10)
print(df['公司'].head(10).tolist())
df['公司'][df['公司'] == ''] = '测试'   # 获取公司一列的空值，再赋值测试

print(df.dropna()['公司'].head(10))
print(df['公司'].head(10))

# df['公司'] = df['公司'].str.strip()  # 去除电话一列中数据中间的空格
# print(df['公司'].head(10))


df1 = df[(df['电话'].str.contains('暂无')) & (df['城市'] != '东城区')]  # 筛选指定数据
print(df1.head(10).loc[[1,16,10]])
# df1.to_excel('11.xlsx') 生成清洗后的excel

# 对于Series数据结构使用_accessors方法，可以得到了3个对象：cat，str，dt。
pd.Series._accessors
# .cat：用于分类数据（Categorical data）

# .str：用于字符数据（String Object data）

# .dt：用于时间数据（datetime-like data）

# Series数据类型：str字符串
addr = pd.Series([
     'Washington, D.C. 20003',
     'Brooklyn, NY 11211-1755',
     'Omaha, NE 68154',
     'Pittsburgh, PA 15211'
 ]) 

print(s.str.count(r'\d'),'→ count对指定字符计数\n')
print(s.count(),'统计s的元素个数')
print(s.str.replace('h','H')，'s.str.replace对字符串进行替换')
print(s.replace('bbhello','BBHello'),'s.replace对整个元素进行替换')
regex = (r'?P<city>[a-zA-Z]+,?P<state>[0-9]{2}?P<zip>\d{5}(?:-\d{4})?')
print(s.str.replace('.','').str.extract(regex))


# dt对象的使用
daterng = pd.Series(pd.date_range('2017', periods=9, freq='Q'))
daterng.dt.day_name()    #  返回日期所属星期
daterng[daterng.dt.quarter > 2]     #  返回日期所属季度
daterng[daterng.dt.is_year_end]     #  判断日期是否属于年低