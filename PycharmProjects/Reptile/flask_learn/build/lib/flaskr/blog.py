import functools
from hashlib import md5
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,abort
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.auth import logind_require
from flaskr.db import get_db
from datetime import datetime, timedelta

# 验证蓝图

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
     'SELECT p.id, title, body, created, updated, author_id,username'
     ' FROM post p JOIN user u ON p.author_id = u.id'
     ' order by created desc'
     ).fetchall()
    
    # t_times = posts['created'] + timedelta(hours=8)
    return render_template('blog/index.html', posts = posts)

@bp.route('/create', methods=['GET','POST'])
@logind_require
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required'
        if not body:
            error = 'Body is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('insert into post (title,body,author_id) values(?,?,?)',(title,body,g.user['id']))
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_post(id,check_author=True):
    db = get_db()
    post = db.execute('select p.id, author_id,created,title,body,username'
    ' from post p join user u on p.author_id=u.id where p.id=?',(id,)).fetchone()

    if post is None:
        abort(404, "Post id {} is Not exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post
    # abort也是特殊响应，用于错误处理。它直接产生异常，把控制交给web server。
    # abort() 会引发一个特殊的异常，返回一个 HTTP 状态码。
    # 它有一个可选参数， 用于显示出错信息，若不使用该参数则返回缺省出错信息。 
    # 404 表示“未找到”， 403 代表“禁止访问”。（ 401 表示“未授权”


@bp.route('/<int:id>/update', methods=['GET','POST'])
@logind_require
def update(id):
    db = get_db()
    post = db.execute(
        'select p.id ,author_id,created,title,body,username'
    ' from post p join user u on p.author_id=u.id where p.id=?',(id,)).fetchone()
    if post is None:
        abort(404, "Post id {} is Not exist.".format(id))

    if post['author_id'] != g.user['id']:
        abort(403)
    # post = db.execute('select * from post where id=?',(id,)).fetchall()
    # post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required'
        if not body:
            error = 'Body is required'
        if error is not None:
            flash(error)
        else:
            db.execute('update post set title=?,body=? where id=?',(title,body,id))
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html',post=post)


@bp.route('/<int:id>/delete', methods=['POST'])
@logind_require
def delete(id):
    get_post(id)
    # db = get_db()
    # post = db.execute(
    #     'select p.id ,author_id,created,title,body,username'
    # ' from post p join user u on p.author_id=u.id where p.id=?',(id,)).fetchone()
    # if post is None:
    #     abort(404, "Post id {} is Not exist.".format(id))

    # if post['author_id'] != g.user['id']:
    #     abort(403)
    db = get_db()
    db.execute('delete from post where id=?',(id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/detail')
def detail(id):
    db = get_db()
    post = db.execute(
     'SELECT p.id, title, body, created, updated, author_id, username'
     ' FROM post p JOIN user u ON p.author_id = u.id'
     ' where p.id=?',(id,)).fetchone()
    t_times = post['created'] + timedelta(hours=8)
    return render_template('blog/detail.html',post=post, t=t_times)