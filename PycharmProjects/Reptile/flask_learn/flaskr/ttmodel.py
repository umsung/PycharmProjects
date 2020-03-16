# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)

#     def __init__(self, username, email):
#         self.username = username
#         self.email = email

#     def __repr__(self):
#         return '<User %r>' % self.username


# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     addresses = db.relationship('Address', backref='person',
#                                 lazy='dynamic')

# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(50))
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

# db.relationship() 做了什么？这个函数返回一个可以做许多事情的新属性。
# 在本案例中，我们让它指向 Address 类并加载多个地址。
# 它如何知道会返回不止一个地址？因为 SQLALchemy 从您的声明中猜测了一个有用的默认值。 
# 如果您想要一对一关系，您可以把 uselist=False 传给 relationship() 。
# db.session.add(User.query.filter('username')='test') 
# User.query.filter(User.email.ilike('%example.com')).all():



