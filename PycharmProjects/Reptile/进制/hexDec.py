import math

hex(16)     # 10进制转16进制
oct(8)      # 10进制转8进制
bin(8)      # 10进制转2进制


# 16进制转换为10进制
# 逐位相乘: AB12(16)= A*163 + B*162 + 1*161 + 2*160

def hex_to_dec():
    hex= [ord(n) - 55 if n in list("ABCDEF") else ord(n) - 48 for n in input('Input a hex number: ').upper()]
    dec = [hex[-i - 1] * math.pow(16, i) for i in range(len(hex))]
    return sum(dec)

int('10')       # 字符串转换成10进制整数
int('10',16)    # 字符串转换成16进制整数
int('0x10',16)  # 字符串转换成16进制整数
int('10',8)     # 字符串转换成8进制整数
int('010',8)    # 字符串转换成8进制整数
int('10',2)     # 字符串转换成2进制整数