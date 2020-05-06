# 堆栈是用来存储函数调用时函数的局部变量和参数的，后进先出数据结构

# 队列常用于数据传输处理，先进先出数据结构

class stack():
    def __init__(self):
        self._data = []

    # 压栈
    def push(self,item):
        self._data.append(item)

    # 弹栈
    def pop(self):
        return self._data.pop()

    def get_size(self):
        return len(self._data)

    def match(self,str):
        for i in str:
            if i in '{[(':
                self.push(i)
            elif i in ')]}':
                self.pop() 
        return self.get_size() == 0

    def r_data(self):
        if len(self._data) == 0:
            return ''
        else:
            return self._data[-1]

    def pattern(self,str):
        for i in str:
            if i in "{}[]()":
                if self.r_data() + i in ['{}','[]','()']:
                    self.pop()
                else:
                    self.push(i)
        return self.get_size() == 0

test_data="{xxxxx(dddddddd[xxxxx{ddddd}dfsfe)dfsefe]xxxx}"
s=stack()
print(s._data)
print(s.pattern(test_data))
print(s._data)





class queue():
    def __init__(self):
        self._data = []

    def put(self,item):
        self._data.append(item)

    def get(self):
        result = self._data[0]
        self._data.remove(result)
        return result