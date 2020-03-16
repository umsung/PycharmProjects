from flask import render_template
from sqlalchemy import func

from main import app
from models import db, User, Post, Tag, Comment, posts_tags
from flask_wtf import Form
from wtforms import StringField, TextField
from wtforms.validators import DataRequired, Length

def sidebar_data():
    """Set the sidebar function."""

    # Get post of recent
    recent = db.session.query(Post).order_by(
            Post.publish_date.desc()
        ).limit(5).all()

    # Get the tags and sort by count of posts.
    top_tags = db.session.query(
            Tag, func.count(posts_tags.c.post_id).label('total')
        ).join(
            posts_tags
        ).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags



@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    """View function for home page"""

    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).paginate(page, 10)

    recent, top_tags = sidebar_data()

    return render_template('home.html',
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)

class CommentForm(Form):
    """Form vaildator for comment."""

    # Set some field(InputBox) for enter the data.
    # patam validators: setup list of validators
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)])

    text = TextField(u'Comment', validators=[DataRequired()])
# WTF 的基础使用
# WTForms 由 字段、检验器、表单 三部分组成： 
# 字段：表示表单的输入框，会做一些初步的输入检查 
# 检验器：是一组被附加到字段(输入框)上的函数，用于对输入数据的检验，确保输入我们期望的数据 
# 表单：是一个 Python 类，其中包含了 字段(类属性) 和 检验器，在接收到 HTTP POST 请求时，会根据定义的检验器规则来对输入数据进行检验

# NOTE 1：表单类需要继承 Flask WTF 扩展提供的 Form 类 
# NOTE 2：表单类中的一个类属性，就代表了一个字段，即输入框。wtforms 提供了多种类型的字段类 
# NOTE 3：字段类的第一个参数为输入框标题，第二个参数为绑定到该字段的检验器列表，由 wtforms.validators 提供


@app.route('/post/<string:post_id>', methods=('GET', 'POST'))
def post(post_id):
    """View function for post page"""
    # form.validata_on_submit() 方法会隐式的判断该 HTTP 请求是不是 POST, 若是, 则将请求中提交的表单数据对象传入上述的 form 对象并进行数据检验.

    # 若提交的表单数据对象通过了 form 对象的检验, 则 form.validata_on_submit() 返回为 True 并且将这些数据传给 form 对象, 成为其实例属性.
    # Form object: `Comment`
    form = CommentForm()
    # form.validate_on_submit() will be true and return the
    # data object to form instance from user enter,
    # when the HTTP request is POST
    if form.validate_on_submit():
        new_comment = Comment(id=str(uuid4()),
                              name=form.name.data)
        new_comment.text = form.text.data
        new_comment.date = datetime.datetime.now()
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('post.html',
                           post=post,
                           tags=tags,
                           comments=comments,
                           form=form,
                           recent=recent,
                           top_tags=top_tags)



@app.route('/post/<string:post_id>')
def post(post_id):
    """View function for post page"""

    post = db.session.query(Post).get_or_404(post_id)
    tags = post.tags
    comments = post.comment.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('post.html',
                           post=post,
                           tags=tags,
                           comments=comments,
                           recent=recent,
                           top_tags=top_tags)


@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    """View function for tag page"""

    tag = db.session.query(Tag).filter_by(name=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('tag.html',
                           tag=tag,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)


@app.route('/user/<string:username>')
def user(username):
    """View function for user page"""
    user = db.session.query(User).filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('user.html',
                           user=user,
                           posts=posts,
                           recent=recent,
                           top_tags=top_tags)