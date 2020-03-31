from uuid import uuid4
from os import path
from datetime import datetime

from flask import render_template, Blueprint,redirect,url_for,abort
from sqlalchemy import func,desc

from jmilkfansblog.models import db, User, Post, Tag, Comment, posts_tags
from jmilkfansblog.forms import CommentForm,PostForm
from flask_login import login_required,current_user
from jmilkfansblog.extensions import *
from flask_principal import Permission,Principal,RoleNeed,UserNeed


bp = Blueprint(
    'blog',  # 定义一个名为blog的蓝图
    __name__,
    # path.pardir ==> ..
    template_folder=path.join(path.pardir, 'templates', 'blog'),
    # Prefix of Route URL 
    url_prefix='/blog')


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
        ).group_by(Tag).order_by(desc('total')).limit(5).all()
    # select tag.name,count(p.post_id) from Tag tag join posts_tags p on tag.id = p.tag_id group_by tag.name order_by count(p.post_id) limit 5
    return recent,top_tags

@bp.route('/')
@bp.route('/<int:page>')
def home(page=1):
    """View function for home page"""

    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).paginate(page, 3)

    recent,top_tags= sidebar_data()

    return render_template('home.html',
                           posts=posts,
                           top_tags=top_tags,
                           recent=recent)


@bp.route('/post/<string:post_id>',methods=['GET','POST'])
def post(post_id):
    """View function for post page"""
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(form.name.data)
        comment.text = form.text.data
        comment.date = datetime.now()
        comment.post_id = post_id
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blog.home'))

    post = db.session.query(Post).get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('post.html',
                           post=post,
                           tags=tags,
                           comments=comments,
                           recent=recent,
                           form=form,
                           top_tags=top_tags)


@bp.route('/new',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if not current_user:
        return redirect(url_for('main.login'))

    if form.validate_on_submit():
        new_post = Post('newPostTitle')
        # new_post.id = 11
        new_post.text = form.text.data
        new_post.title = form.title.data
        new_post.publish_date = datetime.now()
        new_post.users = current_user
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog.home'))
    return render_template('blog/new_post.html',form=form)

@bp.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def edit_post(id):
    """View function for edit_post."""

    post = Post.query.get_or_404(id)
    form = PostForm()
    # Ensure the user logged in.
    if not current_user:
        return redirect(url_for('main.login'))

    # Only the post onwer can be edit this post.
    if current_user != post.users:
        # return redirect(url_for('blog.post', post_id=id))
        abort(401,'have not pre')

    # 当 user 是 poster 或者 admin 时, 才能够编辑文章
    # Admin can be edit the post.
    permission = Permission(UserNeed(post.users.id))
    if permission.can() or admin_permission.can():
        

        #   if current_user != post.users:
        #    abort(403)

        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.now()

            # Update the post
            db.session.add(post)
            db.session.commit()

            return redirect(url_for('blog.post', post_id=post.id))
    else:
        abort(403)

    # Still retain the original content, if validate is false.
    form.title.data = post.title
    form.text.data = post.text
    return render_template('blog/edit_post.html', form=form, post=post)





@bp.route('/tag/<string:tag_name>')
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


@bp.route('/user/<string:username>')
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