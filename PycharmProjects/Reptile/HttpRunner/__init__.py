import re

status_dict={
        '1': 'Sucess',
        '2': 'Fail'
    }

func_dict = {
    'status': lambda x: status_dict[x],
    'data_size': lambda x: int(x)/1024
}

r = {'status': '1', 'Time': '2020-02-17 11:04:34', 'LogLevel': 'ERROR', 'ERROR_Message': '连接XXX服务失败，正在重连。。。。'}


a = {k: func_dict.get(k, lambda x: x)(v) for k, v in r.items()}
print(a)

d = {}

for k, v in r.items():
    print(func_dict.get(k, lambda x: x)(v))
    d[k] = func_dict.get(k, lambda x: x)(v)

print(d)
