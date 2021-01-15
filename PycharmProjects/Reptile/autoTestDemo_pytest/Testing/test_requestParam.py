import pytest


test_user_data = [{"user": "admin1", "psw": "111111"},
                  {"user1": "admin1", "psw1": ""}]
test_user_data2 = ['admin1','admin2']


@pytest.fixture(scope='function')
def login(request):
    user = request.param['user']
    pwd = request.param['psw']
    print('user: %s, pwd %s' % (user, pwd))
    if pwd:
        return True
    else:
        return False


class TestRequestParam:

    def setup_class(self):
        print('setup_class')

    @pytest.mark.parametrize('login', test_user_data, indirect=True)
    def test_login(self, login):

        a = login
        print("测试用例中login的返回值:%s" % a)
        assert a
