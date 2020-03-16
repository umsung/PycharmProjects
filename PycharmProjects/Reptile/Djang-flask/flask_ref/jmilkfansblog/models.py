from flask_sqlalchemy import SQLAlchemy

from jmilkfansblog.extensions import bcrypt,cache
from flask_login import AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import abort,current_app
import json
# INIT the sqlalchemy object                            
# Will be load the SQLALCHEMY_DATABASE_URL from config.py
# SQLAlchemy 会自动的从 app 对象中的 DevConfig 中加载连接数据库的配置项
# # 在 jmilkfansblog/__init__.py 中再初始化 db 对象
# db = SQLAlchemy(app)

db = SQLAlchemy()

users_roles = db.Table('users_roles',
    db.Column('user_id', db.String(45), db.ForeignKey('users.id')),
    db.Column('role_id', db.String(45), db.ForeignKey('roles.id')))

class User(db.Model):
    """Represents Proected users."""

    # Set the name for table
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship('Post',backref='users',lazy='dynamic')
    roles = db.relationship('Role',secondary=users_roles, backref=db.backref('users', lazy='dynamic'))

    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = self.set_password(password)

        # Setup the default-role for user.
        # default = Role.query.filter_by(name="default").one()
        # self.roles.append(default)

    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)

    def set_password(self,password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self,password):
        try:
            return bcrypt.check_password_hash(self.password, password)
        except Exception:
            return None

    def is_authenticated(self):
        """Check the user whether logged in.检验 User 的实例化对象是否登录了."""

        # Check the User's instance whether Class AnonymousUserMixin's instance.
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active():
        """Check the user whether pass the activation process.检验用户是否通过某些验证 """

        return True

    def is_anonymous(self):
        """Check the user's login status whether is anonymous.检验用户是否为匿名用户 """

        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        """Get the user's uuid from database.返回 User 实例化对象的唯一标识 id"""

        return self.id

    @staticmethod
    @cache.memoize(500)
    def verify_auth_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except Exception:
            return None
        uid=data['id']
        user = User.query.filter_by(id=uid).first()
        return user




class Role(db.Model):

    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return "<Model Role `{}`>".format(self.name)


posts_tags = db.Table('posts_tags',
    db.Column('post_id', db.String(45), db.ForeignKey('posts.id')),
    db.Column('tag_id', db.String(45), db.ForeignKey('tags.id')))


class Post(db.Model):
    """Represents Proected posts."""

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    # Set the foreign key for Post
    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))
    # Establish contact with Comment's ForeignKey: post_id
    comments = db.relationship(
        'Comment',
        backref='posts',
        lazy='dynamic')
    # many to many: posts <==> tags
    tags = db.relationship(
        'Tag',
        secondary=posts_tags,
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)


class Tag(db.Model):
    """Represents Proected tags."""

    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Model Tag `{}`>".format(self.name)


class Comment(db.Model):
    """Represents Proected comments."""

    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime)
    post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.name)


class Ts(db.Model):
    """Represents Proected tags."""

    __tablename__ = 'Ts'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Model T `{}`>".format(self.name)

class Reminder(db.Model):
    """Represents Proected reminders."""

    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    email = db.Column(db.String(255))
    text = db.Column(db.Text())

    def __init__(self, id, text):
        self.id = id
        self.email = text

    def __repr__(self):
        return '<Model Reminder `{}`>'.format(self.text[:20])
