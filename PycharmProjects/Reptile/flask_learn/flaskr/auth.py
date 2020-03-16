import functools
from hashlib import md5
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response,jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
import functools
from flaskr.db import get_db
import time
from werkzeug.contrib.cache import MemcachedCache
from werkzeug.contrib.cache import SimpleCache
from functools import wraps
from flaskr import cache
# from flask.ext.cache import Cache
# 验证蓝图
# 把相关视图和代码注册到蓝图，然后再把蓝图注册到工厂函数的实例中
# 创建了一个名称为 'auth' 的 Blueprint 。
# 和应用对象一样， 蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数。 url_prefix 会添加到所有与该蓝图关联的 URL 前面。
bp = Blueprint('auth', __name__, url_prefix='/auth')
cache = SimpleCache()
# cache = MemcachedCache(['127.0.0.1:11211'])


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
            # session.clear() # 防止在登陆状态下，再去登陆其他账号，导致session有多个账号信息
            session.pop('user_id',None)
            session['user_id'] = db.cursor().execute('select id from user where username=?' ,(username,)).fetchone()[0]
            # print("sessionid", session['user_id'])
            # res = session.get('redirect')
            # if res:
            #     return redirect(res)
            if session.get('returnurl'):  
                return redirect(session.get('returnurl'))
            return redirect(url_for('blog.index'))
        else:
            flash(error)
            # 如果验证失败，那么会向用户显示一个出错信息。 flash() 用于储存在渲染模块时可以调用的信息。
    returnurl = request.args.get('returnurl')
    # session.pop('returnurl',None)
    session['returnurl'] = returnurl
    return render_template('auth/login.html')

# 钩子函数 hook适用于一些通用性的操作。
# 目前有before_first_request、before_request、after_request（有异常不会执行）、teardown_request（有异常也会执行）。hook和视图函数之前可以使用全局变量g传递参数。
# bp.before_app_request() 注册一个 在视图函数之前运行的函数,不论其 URL 是什么。验证是否已经登陆
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if request.method == 'POST':
        cache.clear()
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
    # session.clear()
    # session['redirect'] = request.referrer
    session.pop('user_id',None)
    # print(request.referrer,request.url,request.base_url,request.path)
    return redirect(request.referrer)

def logind_require(view):
    @functools.wraps(view)
    def warppen_view(*args,**kw):
        if g.user == None:
            # session['redirect'] = request.referrer
            # print(request.referrer)
            return redirect(url_for('auth.login',returnurl=request.url))
        return view(*args,**kw)
    return warppen_view

# @bp.errorhandler(404)
# def page_not_found(error):
#     return render_template('auth/page_not_found.html'), 404
# # 注意 render_template() 后面的 404 ，这表示页面对应的出错 代码是 404 ，即页面不存在
# 默认返回状态码200，可以修改
# 可以添加头的字典作为第3个参数，但是很少使用。另外也可以返回Response对象。
# make_response()接纳1-3个参数，适用于视图函数定制响应，比如：
@bp.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('auth/page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

@bp.route('/account/center')
@logind_require
def account_center():
    return render_template('auth/accontCenter.html')

@bp.route('/account/center/info',methods=['GET','POST'])
@logind_require
def accountCenterInfo():
    # db = get_db()
    # post = db.execute('select p.id, author_id,created,title,body,username'
    # ' from post p join user u on p.author_id=u.id where p.id=?',(id,)).fetchone()
    # if post is None:
    #     abort(404, "Post id {} is Not exist.".format(id))

    # if post['author_id'] != g.user['id']:
    #     abort(403)

    if request.method == 'POST':
        oldPwd = request.form['OldPwd']
        print(oldPwd)
        md5_oldpwd = md5(oldPwd.encode('utf-8')).hexdigest()
        newPwd = request.form['NewPwd']
        md5_newPwd = md5(newPwd.encode('utf-8')).hexdigest()
        rePwd = request.form['rePwd']
        md5_rePwd= md5(rePwd.encode('utf-8')).hexdigest()
        db = get_db()
        error = None
        if not oldPwd:
            error = '旧密码不能为空！'
        elif not newPwd:
            error = '新密码不能为空！'
        elif not rePwd:
            error = '二次确认密码不能为空！'
        elif db.execute('select * from user where id=? and password =?',(g.user['id'],md5_oldpwd)).fetchone() is None:
            error = '原密码不正确！'
        elif len(newPwd) < 6:
            error = '新密码长度不能小于6位！'
        elif md5_rePwd != md5_newPwd:
            error = '两次输入的密码不一致！'
        if error is None:
            db.execute("update user set password=? where id=?",(md5_newPwd,g.user['id']))
            db.commit()
            session.clear()
            return redirect(url_for('auth.login'))
        else:
            flash(error)
    return render_template('auth/rePassword.html')

@bp.route('/update/success')
def update_success():
    time.sleep(2)
    return redirect(url_for('auth.login'))

@bp.route('/check_name',methods=['POST'])
def register_check_name():
    # false = False
    username = request.form['username']
    db = get_db()
    s_name=db.execute(
        'select username from user where username=?',(username,)
    ).fetchone()
    if s_name:
        response = make_response(jsonify({'result':'1', 'msg':'账号存在，false'}))
    else:
        response = make_response(jsonify({'result':'2','msg':'账号不存在，ture'}))
    return response

# @bp.route('/check_pwd',methods=['POST'])
# def check_pwd():
#     # false = False
#     username = request.form['password']
#     db = get_db()
#     s_name=db.execute(
#         'select username from user where username=?',(username,)
#     ).fetchone()
#     if s_name:
#         response = make_response(jsonify({'result':'1', 'msg':'账号存在，false'}))
#     else:
#         response = make_response(jsonify({'result':'2','msg':'账号不存在，ture'}))
#     return response


# cache对象的set(key, value, timeout)和get(key)方法来存取缓存项了。
# 注意set()方法的第三个参数timeout是缓存过期时间，默认为0，也就是永不过期。
# 缓存项键值的前缀，默认是view_,
# SimpleCache将缓存项存放在Python解释器的内存中
def cached(timeout=5*60,key='view_%s'):
    def decorator(func):
        @wraps(func)
        def wappern(*args,**kw):
            cache_key = key % request.path
            value = cache.get(cache_key)
            if value is None:
                value = func(*args,**kw)
                cache.set(cache_key, value, timeout=timeout)
            return value
        return wappern
    return decorator