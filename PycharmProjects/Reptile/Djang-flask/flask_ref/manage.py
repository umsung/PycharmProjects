import os
from flask_script import Manager, Server,Shell
from flask_migrate import Migrate, MigrateCommand
from jmilkfansblog import create_app
from jmilkfansblog.models import *


dev = os.environ.get('BLOG_ENV','dev')
app = create_app('jmilkfansblog.config.%sConfig' % dev.capitalize())
# app = create_app('jmilkfansblog.config.DevConfig')
# Init manager object via app object 管理器

manager = Manager(app)

# Alembic(Database migration 数据迁移跟踪记录) 提供的数据库升级和降级的功能
# Init migrate object via app and db object  数据库迁移
migrate = Migrate(app, db)

# # Create some new commands

manager.add_command("server", Server(host='192.168.1.222', port=8089))
manager.add_command("db", MigrateCommand)
# # db.drop_all(app=app)
# # db.create_all(app=app)

# python manage.py db init：初始化一个迁移脚本的环境，只需要执行一次。
# python manage.py db migrate`：将模型生成迁移文件，只要模型更改了，就需要执行一遍这个命令。
# python manage.py db upgrade`：将迁移文件真正的映射到数据库中。每次运行了`migrate`命令后，就要运行这个命令


@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(app=app,
                db=db,
                User=User,
                Post=Post,
                Comment=Comment,
                Tag=Tag,
                Reminder=Reminder,
                Role=Role,
                Server=Server)

# manager.add_command("shell", Shell(make_context=make_shell_context))
# # make_shell_context： 就是启动Shell时，默认加载db，app（falsk相关的web运行context），要不然shell不会跟踪到
# # 从现在开始我们每在 models.py 中新定义一个数据模型, 都需要在 manager.py 中导入并添加到返回 dict 中.

# @manager.command
# def create_db():
#     with app.app_context():
#         db.create_all()



if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)