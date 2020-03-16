import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

# Python 内置了 SQLite 数据库
# 使用 SQLite 数据库（包括其他多数数据库的 Python 库）时，第一件事就是创建 一个数据库的连接。所有查询和操作都要通过该连接来执行，完事后该连接关闭
# 数据库连接和关闭

# def get_db():
#     if not hasattr(g,'db'):
#         # g 是一个特殊对象，独立于每一个请求。在处理请求过程中，它可以用于储存 可能多个函数都会用到的数据。
#         g.db = sqlite3.connect(
#             # current_app 是另一个特殊对象，该对象指向处理请求的 Flask 应用。
#             current_app.config['DATABASE'],
#             detect_types= sqlite3.PARSE_DECLTYPES                
#         ) 
#         # sqlite3.Row 告诉连接返回类似于字典的行，这样可以通过列名称来操作 数据。
#         g.db.row_factory = sqlite3.Row
#     return g.db

# def close_db(e=None):
#     db = g.pop('db',None)

#     if db is not None:
#         db.close()

#     if hasattr(g,'db'):
#         g.db.close()
#         g.pop('db')

# # 读取运行SQL 命令
# def init_db():
#     db = get_db()
#     # open_resource() 打开一个文件，该文件名是相对于 flaskr 包的
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))


# # click.command() 定义一个名为 init-db 命令行，它调用 init_db 函数，并为用户显示一个成功的消息。
# @click.command('init-db')
# @with_appcontext
# def init_db_command(): 
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')

# # close_db 和 init_db_command 函数需要在应用实例中注册，否则无法使用。 写一个函数，把应用作为参数，在函数中进行注册。
# # app.teardown_appcontext() 告诉 Flask 在返回响应后进行清理的时候调用此函数。
# # app.cli.add_command() 添加一个新的 可以与 flask 一起工作的命令。

# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
    
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)