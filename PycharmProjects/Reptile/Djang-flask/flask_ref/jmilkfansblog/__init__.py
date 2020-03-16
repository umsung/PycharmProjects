from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import event
from jmilkfansblog.tasks import on_reminder_save
from jmilkfansblog.extensions import *
import os
from jmilkfansblog.controllers.flask_Trestful.posts import PostsApi
from jmilkfansblog.controllers.flask_Trestful.auth import AuthApi
from flask_principal import Permission,Principal,RoleNeed,UserNeed


def create_app(object_name):
    """Create the app instance via `Factory Method`"""

    app = Flask(__name__)
    # Set the app config  
    # 将 app.config.from_object(object_name) 接收的参数定义成一个变量，这样就可以通过接收不同类型的实参来生成不同的 app 对象。
    app.config.from_object(object_name)
    # app.config['SECRET_KEY'] = '123456'
    # Will be load the SQLALCHEMY_DATABASE_URL from config.py to db object
    from jmilkfansblog.models import db
    # 初始化方法：init_app()
    db.init_app(app)
    # with app.app_context(): 
    #     db.create_all() 

    from jmilkfansblog.controllers.admin import CustomView,CustomModelView,CustomFileView

    from jmilkfansblog.extensions import flask_admin,flask_celery
    
    flask_admin.init_app(app)

    from jmilkfansblog.models import Post,User,Comment,Tag,Reminder,Role

    flask_admin.add_view(CustomView(name="用户管理"))

    models = [Post,User,Comment,Tag]
    for model in models:
        flask_admin.add_view(CustomModelView(model,db.session,category='models'))

    models2 = [Reminder,Role]
    for model in models2:
        flask_admin.add_view(CustomModelView(model,db.session,category='learn'))

    flask_admin.add_view(CustomFileView(os.path.join(os.path.dirname(__file__),'static'),'static',name='static Files'))

    from jmilkfansblog.extensions import bcrypt
    bcrypt.init_app(app)

    cache.init_app(app)
    # flask_celery.init_app(app)

    login_manager.init_app(app)

    openid.init_app(app)

    principals.init_app(app)
    
    from flask_principal import identity_loaded
    from flask_login import current_user

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Change the role via add the Need object into Role.

           Need the access the app object.
        """

        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity user object
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity user object
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))



    from jmilkfansblog.models import Reminder
    event.listen(Reminder, 'after_insert', on_reminder_save)
    # 在 Model 上注册回调函数, 当 Model 对象发生特定的情景时, 就会执行这个回调函数, 这就是所谓的 event, 
    # 这里我们使用 after_insert 来指定当创建一个新的 Reminder 对象(插入一条记录)时就触发这个回调函数. 而是回调函数中的形参, 会由 event 来负责传入.
    
    restful_api.add_resource(PostsApi,'/api/posts','/api/posts/<string:post_id>',endpoint='restful_api_post')
    restful_api.add_resource(AuthApi,'/api/auth',endpoint='restful_api_auth')

    restful_api.init_app(app)
    
    @app.route('/')
    def index():
        # Redirect the Request_url '/' to '/blog/'
        return redirect(url_for('blog.home'))
        # return '111'

    # Register the Blueprint into app object
    from jmilkfansblog.controllers import blog,auth,main
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.ah)
    app.register_blueprint(main.ad)
    return app


    