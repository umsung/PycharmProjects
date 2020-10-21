class ProptyDes:

    def __init__(self, name, math, chinese, english):
        self.name = name
        self.math = math
        self.chinese = chinese
        self.english = english

    @property
    def math(self):
        return self.math

    @math.setter
    def math(self, value):
        if 0 <= value <= 100:
            self.math = value
        else:
            raise ValueError('Vaild value must be in [0,100]')

    @property
    def chinese(self):
        return self.chinese

    @chinese.setter
    def chinese(self, value):
        if 0 <= value <= 100:
            self.chinese = value
        else:
            raise ValueError('Vaild value must be in [0,100]')


class DataDes:
    """
    # 数据描述符
    实现了 __set__和__get__两种方法则是 数据描述符
    只实现了__get__一种方法的是 非数据描述符
    """
    def __init__(self, default=0):
        self._data = default

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Data must be Integer')

        if not 0 <= value <= 100:
            raise ValueError('Vaild value must be in [0,100]')

        self._data = value

    def __get__(self, instance, owner):
        return self._data

    def __delete__(self, instance):
        del self._data


class Student:
    math = DataDes()
    chinese = DataDes()
    english = DataDes()

    def __init__(self, name, math, chinese, english):
        self.name = name
        self.math = math
        self.chinese = chinese
        self.english = english

    def __repr__(self):
        return '<Student: {}, math: {}, chinese: {}, english: {}>'.format(self.name, self.math, self.chinese, self.english)


if __name__ == '__main__':
    s = Student('duan', 80, 90, 99)
    print(s)



