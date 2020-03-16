from flask import g,session
from flaskr.db import get_db
import pytest


def test_auth_register(client, app):
    # 测试注册，get请求到注册页面，响应码要=200，post请求注册成功后会重定向到登陆页面，且注册的数据会插入数据库

    assert client.get('/auth/register').status_code == 200
    response = client.post('/auth/register', data={'username':'umsungr','password':'123456'})
    assert response.status_code == 302
    assert 'http://localhost/auth/login' == response.headers['Location']
    with app.app_context():
        db = get_db()
        assert db.execute("select*from user where username='umsung' ").fetchone() is not None

@pytest.mark.parametrize(('username','password','message'),(
    ('', '123456', b'Username is required.'),
    ('a', '123456', b'length must be more than six'),
    ('aaaaaa', '', b'Password is required.'),
    ('aaaaaa', '123', b'length must be more than six'),
    ('test11', '123456', b'already registered.'),
))
def test_register_validate_input(client,username,password,message):
    response = client.post('/auth/register', data={'username':username,'password':password})
    assert message in response.data
   

def test_auth_login(client,Auth):
    assert client.get('/auth/login').status_code == 200
    Auth.register()
    response = Auth.login()
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/' 

    # with app.app_context():
    #     db = get_db()
    #     d = db.execute("select * from user where username ='testRegister' ").fetchone()
    #     assert d is not None
    #     assert d['password'] == '123456'
    # 保持环境 在 with 块中使用 client ，可以在响应返回之后操作环境变量，比如 session 。离开with语句，request和session对象都无法获取
    with client:
        client.get('/')
        assert session['user_id'] == 3
        assert g.user['username'] == 'umsung'

@pytest.mark.parametrize(('username','password','message'),(
    ('','123456', b'username cant not null'),
    ('umsung', '', b'password can not null'),
    ('aaaaaa', '123456', b'username is error'),
    ('test11', '111', b'password is error'),
))
def test_login_validate_input(Auth,username,password,message):
    response = Auth.login(username,password)
    assert message in response.data


def test_auth_logout(client,Auth):
    Auth.register()
    Auth.login()

    with client:
        response = Auth.logout()
        # assert response.status_code == 302
        # assert response.headers['Location'] == 'http://localhost/'
        assert 'user_id' not in session
        Auth.index()
        assert g.user is None

def test_not_found(client):
    response = client.get('/abc')
    assert response.status_code == 404