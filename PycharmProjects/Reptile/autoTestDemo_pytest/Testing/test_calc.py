import pytest
import os
import sys

sys.path.append('E:/gitL/PycharmProjects/Reptile/autoTestDemo_pytest')

from SourceCode.calc import Calculator

import allure

'''
-pytest命名规则
    .文件名要以test_开头
    .类名要以Test开头，首字母大写，方法名要以test_开头

-Allure
    .Allure.attch()
    .Allure.attch.file()

-Fixture固件，自定义用例预置条件，功能类似于setup、teardown，不过更为灵活
    .把固件名称当参数传入用例函数调用
    .默认级别是scope=function,每个函数可调用
    .scope=class，每个类可调用一次，scope=module，每个.py文件可调用一次，scope=session，多个.py文件调用一次
    .pytest会自动识别该文件，放在与用例同一package下，不需要导入
'''
test_user_data2 = ['admin1', 'admin2']


@pytest.fixture(scope="class")
def fix():
    print('first run fixture')


@pytest.fixture(scope="module")
def par(request):
    param = request.param
    print('测试request获取作用在用例上的数据: %s' % param)
    yield param


class TestCalc:

    @classmethod
    def setup_class(cls):
        print(os.path.abspath('.'))
        print(os.path.abspath(__file__))
        print(sys.path)
        print('所有测试用例运行前执行')
        # assert os.path.abspath('.') in sys.path
        cls.calc = Calculator()

    def test_add(self, login):
        print('run add')
        assert 2 == self.calc.add(1, 1)

    def test_div(self, fix):
        print('run div')
        assert 3 == self.calc.div(9, 3)

    @pytest.mark.parametrize('a,b,c', [
        (1, 2, 3),
        (-1, -2, -3),
        (0.2, 0.2, 0.4),
        (1000, 2000, 3000),
        (0, 0, 0)
    ])
    def test_param(self, a, b, c):
        print(c)
        assert c == a + b

    def teardown(self):
        print('每个用例运行后执行')

    @classmethod
    def teardown_class(cls):
        print('所有测试用例运行完后执行')


class TestCalc1:
    @classmethod
    def setup_class(cls):
        print('所有测试用例运行前执行')
        cls.calc1 = Calculator()

    def test_add(self):
        print('run add2')
        assert 2 == self.calc1.add(1, 1)

    def test_div(self, fix):
        print('run div2')
        assert 3 == self.calc1.div(9, 3)

    @pytest.mark.parametrize('par', test_user_data2, indirect=True)
    def test_par(self, par):
        # 添加indirect=True参数是为了把par当成一个函数去执行，而不是一个参数
        # par函数获取test_user_data2数据
        param = par
        print(param)
        assert 'admin' in param
