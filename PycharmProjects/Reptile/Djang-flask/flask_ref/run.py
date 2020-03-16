import os
from flask_script import Manager, Server,Shell
from flask_migrate import Migrate, MigrateCommand
from jmilkfansblog import create_app
from jmilkfansblog.models import *

dev = os.environ.get('BLOG_ENV','dev')
app = create_app('jmilkfansblog.config.%sConfig' % dev.capitalize())
# app = create_app('jmilkfansblog.config.DevConfig')
# Init manager object via app object 管理器

if __name__ == '__main__':
   
    app.run(debug=True)