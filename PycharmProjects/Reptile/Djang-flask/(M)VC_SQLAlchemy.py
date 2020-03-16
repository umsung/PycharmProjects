from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

app = Flask(__name__)
# 实例化应用对象app

app.config.from_object('blog.setting')
# 记载配置文件

# 创建数据库对象
db = SQLAlchemy(app)

class User(db.Model):
    """Represents Proected users."""

    # Set the name for table
    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship('Post',backref='users',lazy='dynamic')
    # db.relationship会在 SQLAlchemy 中创建一个虚拟的列，该列会与 Post.user_id (db.ForeignKey) 建立联系。
    # backref：用于指定表之间的双向关系，如果在一对多的关系中建立双向的关系，这样的话在对方看来这就是一个多对一的关系。
    # lazy：指定 SQLAlchemy 加载关联对象的方式
    # lazy=subquery: 会在加载 Post 对象后，将与 Post 相关联的对象全部加载，这样就可以减少 Query 的动作，也就是减少了对 DB 的 I/O 操作。但可能会返回大量不被使用的数据，会影响效率。
    # lazy=dynamic: 只有被使用时，对象才会被加载，并且返回式会进行过滤，如果现在或将来需要返回的数据量很大，建议使用这种方式。Post 就属于这种对象。
    
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)

posts_tags = db.Table('post_tags',
                    db.Column('post_id',db.String(45),db.ForeignKey('posts.id')),
                    db.Column('tag_id',db.String(45),db.ForeignKey('tags.id')))
    # posts_tags 表对象之所以使用 db.Table 不使用 db.Model 来定义，
    # 是因为我们不需要对 posts_tags (self.name)进行直接的操作(不需要对象化)，
    # posts_tags 代表了两张表之间的关联，会由数据库自身来进行处理。

class Post(db.Model):
    """Represents Proected posts."""

    __tablename__ = 'posts'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    # Set the foreign key for Post
    user_id = db.Column(db.String(45), db.ForeignKey('users.id')) # or db.ForeignKey('User.id')
    tags = db.relationship('Tag',secondary=posts_tags,backref=db.backref('posts',lazy='dynamic'))
    # many to many 的关系仍然是由 db.relationship() 来定义,多对多关系会在两个类之间增加一个关联表。
    # seconddary(次级)：会告知 SQLAlchemy 该 many to many 的关联保存在 posts_tags 表中
    # backref：声明表之间的关系是双向，帮助手册 help(db.backref)。
    # 需要注意的是：在 one to many 中的 backref 是一个普通的对象，而在 many to many 中的 backref 是一个 List 对象。
    
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)


class Tag(db.Model):
    """Represents Proected tags."""

    __tablename__ = 'tags'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Model Tag `{}`>".format(self.name)


#  SQLAlchemy 实现 CRUD 的语句,
# -----Create 增添数据
# 为新建的 User models 添加一条记录的操作看起来跟 Git 的提交操作非常类似,
# 其包含的意义也大致相同, 是为了尽量减少不必要的 I/O 操作:
# add: 把数据添加到会话对象中 (数据状态为待保存)
# commit: 将会话对象中的数据提交 (数据被写入数据库中)

user = User(id=str(uuid4()), username='jmilkfan', password='fanguiju')
user2 = User(id=8,  username='jmilkfan', password='fanguiju')
db.session.add(user)
db.session.add_all([user1, user2])
db.session.commit()


# -----Retrieve 读取数据
# 读取一条数据: 需要指定唯一的过滤条件来获取, 一般会使用主键作为过滤条件.
user = User.query.first()
user.username
# u'fanguiju'
# 返回表中的第一条记录

user = User.query.get('49f86ede-f1e5-410e-b564-27a97e12560c')

user = db.session.query(User).filter_by(id='49f86ede-f1e5-410e-b564-27a97e12560c').first()
# 返回符合过滤条件的第一条记录，filter_by的参数形式如‘aa’=‘bb’，而filter的参数形式是boolean型

# 读取多条数据: 指定任意条件作为过滤条件或者不过滤的获取全部数据
user = db.session.query(User).filter_by(username='fanguiju').all()
user = db.session.query(User).filter(User.username == 'fanguiju').all()
# 返回符合过滤条件的所有User表记录, 将所有 username == fanguiju 的记录都获取

users = User.query.all()  
db.session.query(User).all()
# 以上两种效果一样

# query括号里表示要查询的字段内容，写表名则是查询全部字段，也可填表字段名称
db.session.qeury(User.id,User.username)

# 多条件查询
db.session.query(User).filter(and_(User.id==1,User.username.like('aa'))).all()
db.session.query(User).filter(or_(User.name.like("user%"), User.password != None)).all()


# 关联查询
User.query.join(Post).all()
User.query.join(Post,User.id = Post.user_id).all()
db.session.query(User,Post).filter(User.id = Post.user_id).all()
db.session.query(User).join(User.sposts).all()


# 聚合查询
db.session.query(Post.user_id,func.count('*').label('id_count')).group_by(Post.user_id).all()
db.session.query(User.name, func.sum(User.id).label("user_id_sum")).group_by(User.name).all()

users = db.session.query(User).limit(10).all()

# 正向排序
users = db.session.query(User).order_by(User.username).all()

# 反向排序
users = db.session.query(User).order_by(User.username.desc()).all()

# 查询函数的链式调用
users = db.session.query(User).order_by(User.username).limit(10).all()

# NOTE: 一条读取语句的链式操作都是一个 first() 或 all() 函数结束的. 它们会终止链式调用并返回结果.

User.query.paginate(1,10)     # 查询第 1 页,且 1 页显示 10 条内容
# 第一个参数表示查询返回第几页的内容
# 第二个参数表示每页显示的对象数量


# SQLAlchemy 提供了过滤器 query.filter_by() 和 query.filter(), 过滤器接受的参数就是过滤条件, 有下面几种形式:
# 字段键值对, EG. username='fanguiju'
# 比较表达式, EG. User.id > 100
# 逻辑函数, EG. in_/not_/or_
user = db.session.query(User).filter(User.username.in_(['fanguiju', 'jmilkfan'])).limit(1).all()
user = db.session.query(User).filter(or_(not_(User.username == None), User.password != None)).all()

recent = db.session.query(Post).order_by(Post.publish_date.desc()).limit(5).all()
Post.query.order_by(Post.publish_date.desc())

# -----Update 更新数据
user = db.session.query(User).update({'username': 'update_fanguiju'})
user = User.query.get(uid).update({'neckname':'test'})
# 先定位到你希望更新的记录, 然后通过 Query 对象的 update() 传递要更新内容. 
# 注意: 更新的内容必须是 Dict 数据类型., 
# 如果没有指定要更新具体的哪一条记录的话, 会将该字段所在列的所有记录值一同更新

# -----Delete 删除数据
user = db.session.query(User).first()
db.session.delete(user)

# 将查询返回的 User 实例化对象进行 session 的 delete 操作, 就能够删除该对象所映射的记录数据了.

# ------一对多联合查询
# 实例化一个 User 的对象
user = User(id=str(uuid4()), username='jmilkfan', password='fanguiju')
db.session.add(user)
db.session.commit()

user.posts.all() # 返回该user对象关联的posts对象，这时候返回为空列表[]，因为post表还没有数据
# 实例化一个post对象

post_one = Post('post title')
post_one.id = str(uuid4)
# 指定该 post 是属于哪一个 user 的
post_one.user_id = user.id
db.session.add(post_one)
db.session.commit()

user.posts.all()  # 返回该user对象关联的posts对象  [<Model Post `First Post`>]
db.session.query(User).filter_by(id='').posts.all()

# 反向 post.users
user = db.session.query(User).first()
user.id

post_second = Post('s post')
# 必须为其设置主键值
post_second.id = str(uuid4)
# 现在该 post_second 对象是没有关联到任何 user 的
post_second.users
# 为 post_second 指定一个 user 对象
post_second.users = user
# 或者
user.posts.append(post_second)

db.session.add(post_second)
db.session.commit()



# -----多对多
post = db.session.query(Post).all()
post_one = post[1]
post_two = post[2]

# 实例化tag对象
tag1 = Tag('flask1')
tag1.id = str(uuid4)

tag2 = Tag('flask2')
tag1.id = str(uuid4)

tag3 = Tag('flask3')
tag3.id = str(uuid4)

post_one.tags = tag1
post_two.tags = [tag1,tag2]

db.session.add(post_one)
db.session.add(post_two)
db.session.commit()

# 反向
tag1.posts.all()

tag1.posts.append(post_three)
db.session.add(post_one)
db.session.commit()

db.session.query(Tag).filter_by(name='JmilkFan').first().posts.all()
db.session.query(Post).filter_by(title='First Post').first().tags