import functools
from hashlib import md5
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import functools
from flaskr.db import get_db

# 验证蓝图
# 把相关视图和代码注册到蓝图，然后再把蓝图注册到工厂函数的实例中
# 创建了一个名称为 'auth' 的 Blueprint 。
# 和应用对象一样， 蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数。 url_prefix 会添加到所有与该蓝图关联的 URL 前面。
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif len(username) < 6 or len(password)<6:
            error = 'length must be more than six'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'already registered.'
# fetchone() 根据查询返回一个记录行(一维元组)。 如果查询没有结果，则返回 None 。fetchall() ，它返回包括所有结果的列表。
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, md5(password.encode('utf-8')).hexdigest())   # generate_password_hash(password)
            )
            db.commit()
            return redirect(url_for('auth.login'))
            # return render_template('auth/login.html', messages='Regiester Success!')

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        # print('password', password)
        # print('user',user[0],user[1],user[2],user['password'])
        if not username:
            error = 'username cant not null'
        elif not password:
            error = 'password can not null'
        elif db.execute('select * from user where username=?',(username,)).fetchone() is None:
            error = 'username is error'
        elif md5(password.encode('utf-8')).hexdigest() != user['password']:
            error = 'password is error'
        if error == None:
            session.clear() # 防止在登陆状态下，再去登陆其他账号，导致session有多个账号信息
            session['user_id'] = db.cursor().execute('select id from user where username=?' ,(username,)).fetchone()[0]
            print("sessionid", session['user_id'])
            return redirect(url_for('blog.index'))
        else:
            flash(error)
            # 如果验证失败，那么会向用户显示一个出错信息。 flash() 用于储存在渲染模块时可以调用的信息。
    return render_template('auth/login.html')

# hook适用于一些通用性的操作。
# 目前有before_first_request、before_request、after_request（有异常不会执行）、teardown_request（有异常也会执行）。hook和视图函数之前可以使用全局变量g传递参数。
# bp.before_app_request() 注册一个 在视图函数之前运行的函数,不论其 URL 是什么。验证是否已经登陆
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('select*from user where id=?',(user_id,)).fetchone()

# 注销的时候需要把用户 id 从 session 中移除。
@bp.route('/logout')
def logout():
    # session.pop(key)。
    # del session[key]。
    # session.clear()：删除session中所有的值。
    # 设置session的有效期：如果没有设置session的有效期。那么默认就是浏览器关闭后过期。如果设置session.permanent=True，那么就会默认在31天后过期。如果不想在31天后过期，那么可以设置app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hour=2)在两个小时后过期
    # session.pop(key, None)
    session.clear()
    return redirect(url_for('blog.index'))

# @bp.route('/a')
# def index():
#     # return 'welcome'
#     return render_template('auth/index.html')

def logind_require(view):
    @functools.wraps(view)
    def warppen_view(*args,**kw):
        if g.user == None:
            return redirect(url_for('auth.login'))
        return view(*args,**kw)
    return warppen_view

@bp.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('auth/page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
 
# @bp.errorhandler(404)
# def page_not_found(error):
#     return render_template('auth/page_not_found.html'), 404
# # 注意 render_template() 后面的 404 ，这表示页面对应的出错 代码是 404 ，即页面不存在
# 默认返回状态码200，可以修改
# 可以添加头的字典作为第3个参数，但是很少使用。另外也可以返回Response对象。
# make_response()接纳1-3个参数，适用于视图函数定制响应，比如：