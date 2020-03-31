# 继承多态
# 鸭子类型，传入run_twice对象不一定是继承了Aminal类型的对象，而是传入的对象有run方法就可以

class Animal(object):
    def run(self):
        print('Animal is running')


class Dog(Animal):
    def run(self):
        print('Dog is runing')

class Cat(Animal):
    pass

class People(object):
    def run(self):
        print('People is not the subclass of Animal')

def run_twice(fun):
    fun.run()
    fun.run()

run_twice(Animal())
run_twice(Dog())
run_twice(Cat())
run_twice(People())

print(type(Dog()))
print(isinstance(Dog(),Dog))