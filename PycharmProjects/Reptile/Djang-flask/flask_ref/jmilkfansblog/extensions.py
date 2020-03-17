'''此模块存放flask扩展 '''
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_celery import Celery
from flask_login import LoginManager
from flask_openid import OpenID
from flask_principal import Permission,Principal,RoleNeed
from flask_restful import Api
from flask_cache import Cache

cache = Cache()

restful_api = Api()

principals = Principal()
# 每个user用户都有一种身份identity，每一种身份identity都会关联一个需求Needs，（RoleNeed/UserNeed）
# Need本质是一个元祖，定义了身份identity能做什么事，就是说 Permission 其实是通过 Needs 来定义和初始化的, 其中 Permission 可以是一个权限的集合.
# 这里设定了 3 种权限, 这些权限会被绑定到 Identity 之后才会发挥作用.
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

# Create the Flask-Bcrypt's instance
bcrypt = Bcrypt()

flask_admin = Admin()
# admin = Admin(app, name=‘env manager‘)

flask_celery = Celery()

openid = OpenID()

login_manager = LoginManager()

login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Load the user's info.
        它的作用是在用户登录并调用 login_user() 的时候, 
        根据 user_id 找到对应的 user, 如果没有找到，返回None, 
        此时的 user_id 将会自动从 session 中移除, 
        若能找到 user ，则 user_id 会被继续保存.
    """

    from jmilkfansblog.models import User
    return User.query.filter_by(id=user_id).first()


