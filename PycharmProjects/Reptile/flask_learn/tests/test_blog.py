from flask import g,session
from flaskr.db import get_db
import pytest

def test_auth_index(client,Auth):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data

    Auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by umsung on 2019-11-13 00:00:00' in response.data
    assert b'/1/update' in response.data
    assert b'/1/detail' in response.data
    assert b'body' in response.data
    # 重定向的响应response的值是没有跳转到最终页面的


@pytest.mark.parametrize('path',(
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(client, app, Auth):
    with app.app_context():
        db = get_db()
        db.execute('update post set author_id=2 where id=1')
        db.commit()
    Auth.login()
    assert client.get('/1/update').status_code == 403
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    assert b"href='/1/update'" not in client.get('/').data


def test_id_required(client,Auth,app):
    with app.app_context():
        db=get_db()
        db.execute('delete from post where id=1')
        db.commit()
    Auth.login()
    assert client.get('/1/update').status_code == 404
    assert client.post('/1/update').status_code == 404
    assert client.post('/1/delete').status_code == 404


def test_create(client, Auth,app):
    Auth.login()
    assert client.get('/create').status_code == 200
    response = client.post('/create', data={'title':'test post create','body':'test body'})
    response.status_code = 302
    response.headers['Location'] == 'http://localhost'
    with app.app_context():
        db = get_db()
        assert db.execute("select*from post where id=2").fetchone() is not None


@pytest.mark.parametrize(('title','body','message'),(
    ('','body',b'Title is required'),
    ('title','',b'Body is required'),
))
def test_create_validate_input(client, Auth,title,body,message):
    Auth.login()
    response = client.post('/create',data={'title':title,'body':body})
    assert message in response.data

def test_update(client, Auth, app):
    Auth.login()
    assert client.get('/1/update').status_code == 200

    response = client.post('/1/update', data={'title':'updated title','body':'updated body'})
    response.status_code = 302
    response.headers['Location'] == 'http://localhost/'
    with app.app_context():
        db = get_db()
        result = db.execute('select * from post where id=1').fetchone()
        assert result['title'] == 'updated title'
        assert result['body'] == 'updated body'


@pytest.mark.parametrize('path',(
    '/create',
    '/1/update'
))
def test_update_create_validate_input(client,Auth,path):
    Auth.login()
    response = client.post(path, data={'title':'', 'body':'body'})
    assert b'Title is required' in response.data
    response = client.post(path, data={'title':'title', 'body':''})
    assert b'Body is required' in response.data

def test_delete(client,Auth,app):
    Auth.login()
    response = client.post('/1/delete')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'
    with app.app_context():
        db = get_db()
        assert db.execute('select * from post where id=1').fetchone() is None

def test_detail(client, Auth):
    Auth.login()
    response = client.get('/1/detail')
    assert response.status_code == 200
    assert b'test title' in response.data

def test_session_clear_required(client, Auth):
    Auth.register()
    Auth.login()
    Auth.login('test123','123456')
    with client:
        response = client.get('/')
        assert b'test123' in response.data
        assert session['user_id'] == 4
        assert g.user['username'] == 'test123'