from flask import Flask
import io
import os
from . import db
from .import auth
from .import blog

# flask链接 https://dormousehole.readthedocs.io/en/latest/tutorial/database.html
# __init__.py 有两个作用：一是包含应用工厂；二是 告诉 Python flaskr 文件夹应当视作为一个包。
# 在一个函数内部创建 Flask 实例来代替创建全局实例。这个函数被 称为 应用工厂 。
# 所有应用相关的配置、注册和其他设置都会在函数内部完成， 然后返回这个应用。
# create_app 是一个应用工厂函数

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # 创建 Flask 实例。
    # __name__ 是当前 Python 模块的名称。应用需要知道在哪里设置路径， 使用 __name__ 是一个方便的方法。
    # instance_relative_config=True 告诉应用配置文件是相对于 instance folder 的相对路径。实例文件夹在 flaskr 包的外面，用于存放本地数据（例如配置密钥和数据库），不应当 提交到版本控制系统。

    app.config.from_mapping(  # 设置一个应用的 缺省配置：
        SECRET_KEY=os.urandom(16),
        # SECRET_KEY='dev',
        DATABASE = os.path.join(app.instance_path,'flaskr.sqlite'),
    )
    if test_config is None:
        # 使用 config.py 中的值来重载缺省配置
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass
    
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # 注册数据操作函数
    db.init_app(app)
    # 导入并注册 验证蓝图
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint='index')
    # 与验证蓝图不同，博客蓝图没有 url_prefix 。把博客索引作为主索引
    # 在博客视图中index 视图的端点会被定义为 blog.index 。但是在验证视图 会指定向普通的 index 端点。 
    # 我们使用 app.add_url_rule() 关联端点名称 'index' 和 / URL ，这样 url_for('index') 或 url_for('blog.index') 都会有效，会生成同样的 / URL 。
    return app

print(__name__)