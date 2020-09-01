import pytest

# 固件（Fixture）是一些函数，pytest 会在执行测试函数之前（或之后）加载运行它们，也称测试夹具。

# 我们可以利用固件做任何事情，其中最常见的可能就是数据库的初始连接和最后关闭操作。

@pytest.fixture(scope='function')
def login():
    print('登录....')

def test_index(login):
    print('主页....')


@pytest.fixture()
def db():
    print('Connection successful')

    yield

    print('Connection closed')

def search_user(user_id):
    d = {
        '001': 'xiaoming',
        '002': 'xiaohua'
    }
    return d[user_id]

def test_case_01(db):
    assert search_user('001') == 'xiaoming'

def test_case_02():
    assert search_user('002') == 'xiaohua'


if __name__ == '__main__':
    pytest.main(["-s","-v","test_fixture2.py"])