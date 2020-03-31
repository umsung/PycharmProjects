class parent(object):
    def __init__(self,name,age):
        self.age = age
        self.name = name

    def sing(self):
        print(self.name,self.age)


class child(parent):
    pass


class child2(parent):
    def __init__(self,name,age):
        parent.__init__(self,name,age)  # 类调用，self参数需要显式传递
        # super().__init__(name,age)    等效于 super(child2,self).__init__(name,age)
  


c=child('aa',11)
c.sing()

c2 = child2('bb',22)
c2.sing()