class Date(object):
    count = 0

    def __init__(self,year,month,day):
        self.y = year
        self.m = month
        self.d = day

    @classmethod
    def get_format_date(cls,dateStr):
        y,m,d = dateStr.split('-')
        return cls(y,m,d)

    @staticmethod
    def get_format_date2(dataStr):
        y,m,d = dataStr.split('-')
        return Date(y,m,d)


    def addNum(self):
        Date.count +=1

    def getYesterdar(self):
        self.day -=1

    def __str__(self):
        return '{}/{}/{}'.format(self.y,self.m,self.d)
    __repr__ = __str__

    def __call__(self):
        print(Date.count)


d = Date.get_format_date('2020-3-19')
print(d)

d()