import sqlite3
import pytest
from flaskr import create_app
from flaskr.db import get_db

# 测试数据库连接后返回的对象是否都是同一个，及退出环境后，数据库是否关闭

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('select 1')
    assert 'closed' in str(e.value)

# 测试调用init-db命令后是否输出信息

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        call = False
    def fake_init_db():
        Recorder.call = True
    
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.call
    