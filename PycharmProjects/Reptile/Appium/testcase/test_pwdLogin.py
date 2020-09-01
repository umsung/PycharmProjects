import pytest
from page import Main,App

'''
测试文件以test_开头（以_test结尾也可以）
测试类以Test开头，并且不能带有 __init__ 方法
测试函数以test_开头
断言使用assert
所有的包pakege必须要有__init__.py文件
'''


class TestPwdLogin:

    def setup(self):
        self.login_page = App().start().main().ToMallCenter().ToLoginOrRegister()
        # if cls.login_page.LoginPagejud():
        #     cls.test_login.toVerCodeLogin()
        # cls.login_page = cls.login_page.toPwdLogin()

    def test_OneClickLogin(self):
        name = ''
        mcp = self.login_page.OneClickLogin()
        usename = mcp.getUsername()
        assert name == usename


    def test_PwdLoginWithErrUsername(self,username='',pwd=''):
        ErrMsg = self.login_page.isOneclickLogin().loginWithErrUsername(username,pwd)
        assert ErrMsg == ''

    def test_PwdLoginWithErrPwd(self,username='',pwd=''):
        ErrMsg = self.login_page.isOneclickLogin().loginWithErrPwd(username,pwd)
        assert ErrMsg == ''

    def test_PwdLgoinWithoutPwd(self):
        pass
    
    def test_PwdLoginSuccess(self,username='',pwd=''):
        mallpage = self.login_page.isOneclickLogin().LoginSuccess(username,pwd)
        str = mallpage.getUsername()
        assert str == ''


    def teardown(self):
        App().stop()


if __name__ == "__main__":
    '''
    执行pytest用例有三种方法
    1.pytest,2.py.test, 3,python -m pytest
    如果不带参数，在某个文件夹下执行时，它会查找该文件夹下所有的符合条件的用例
    '''
    pytest.main(['-q','TestPwdLogin.py'])