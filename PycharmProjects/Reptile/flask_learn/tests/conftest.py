# 测试代码位于 tests 文件夹中，该文件夹位于 flaskr 包的 旁边 ， 而不是里面。 
# tests/conftest.py 文件包含名为 fixtures （固件）的配置 函数。每个测试都会用到这个函数。
# 测试位于 Python 模块中，以 test_ 开头， 并且模块中的每个测试函数也以 test_ 开头。
# Pytest 通过匹配固件函数名称和测试函数的参数名称来使用固件。
from flask import g,session
import os
import tempfile
import pytest
# from ..flaskr import create_app PycharmProjects.Reptile.flask_learn.
import unittest
from flaskr.db import init_db, get_db
from flaskr import create_app

# class SampleTestCase(unittest.TestCase):

#     def setUp(self):
#         self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#         app.config['TESTING'] = True
#         self.init_db(app.config['DATABASE'])

#     def tearDown(self):
#         os.close(self.db_fd)
#         os.unlink(app.config['DATABASE'])

#     def init_db(self, db_file):
#         with closing(sqlite3.connect(db_file)) as db:
#             with app.open_resource('init.sql', mode='r') as f:
#                 db.cursor().executescript(f.read())



with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.sql')) as f:
    _data_sql = f.read().encode('utf-8').decode('utf8')

# app 固件会调用工厂并为测试传递 test_config 来配置应用和数据库，而 不使用本地的开发配置。
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()  # mkstemp() 函数返回两个东西： 一个低级别的文件句柄和一个随机文件名。创建并打开一个临时文件，返回该文件对象和路径。
    app = create_app({  # 重载database路径，指向临时路径,TESTING告诉flask当前处于测试环境，flask会改变一些内部行为方便测试
        'TESTING':True,
        'DATABASE':db_path,
    })

    with app.app_context():
        init_db() # 创建表
        get_db().executescript(_data_sql)  # 
    
    yield app

    os.close(db_fd)
    os.unlink(db_path)

# client 固件调用 app.test_client() 由 app 固件创建的应用 对象。测试会使用客户端来向应用发送请求，而不用启动服务器。
@pytest.fixture
def client(app):
    return app.test_client()  # 获取一个werkzeug.test.Client类型的对象来模拟客户端

# runner 固件类似于 client 。 app.test_cli_runner() 创建一个运行器， 可以调用应用注册的 Click 命令。
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self.client = client
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        # self.db = get_db()

    def register(self,username='test123',password='123456'):
        self.client.post('/auth/register',data={'username':username,'password':password})

    def login(self, username='umsung', password='123456'):
        return self.client.post('/auth/login', data={'username':username,'password':password}, follow_redirects=True)
    # follow_redirects参数为True时，请求函数（即视图函数）内的redirect()重定向才有效。因为我们的login成功后会redirect到index页面，所以这个参数必须设为True。
    def logout(self):
        return self.client.get('/auth/logout')

    def index(self):
        return self.client.get('/')

    # def db(self):
    #     return self.db

@pytest.fixture
def Auth(client):
    return AuthActions(client)
