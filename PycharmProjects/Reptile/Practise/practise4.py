
# num = input('输入数字：').strip()
# num = int(num)
# for i in range(1, num):
    
#     print(' '*(num-i),'* '*i)


for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n/x)
            break
    else:
        # loop fell through without finding a factor
        print(n, 'is a prime number')
