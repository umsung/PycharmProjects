import functools
from hashlib import md5
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,abort,jsonify,current_app,make_response
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.auth import logind_require,cached
from flaskr.db import get_db
from datetime import datetime, timedelta
import os,time
from werkzeug.utils import secure_filename
import math
# from flaskr import cache
import re

# 验证蓝图
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
bp = Blueprint('blog', __name__)

# 用户输入名字后提交表单,然后点击浏览器的刷新按钮,会看到一个莫名其妙的警告,要求在再次提交表单之前进行确认。之所以出现这种情况,是因为刷新页面时浏览器会重新发送之前已经发送过的最后一个请求。如果这个请求是一个包含表单数据的 POST 请求,刷新页面后会再次提交表单。

# 基于这个原因,最好别让 Web 程序把 POST 请求作为浏览器发送的最后一个请求。这种需求的实现方式是,使用重定向作为 POST 请求的响应,而不是使用常规响应。

# 重定向的相应内容是URL而不是html页面（重定向响应）。浏览器收到POST消息返回的响应时,会向重定向的 URL 发起 GET 请求,显示页面的内容。这个页面的加载可能要多花几微秒,因为要先把第二个请求发给服务器。这个技巧称为Post/重定向/Get 模式。

# 但这种方法会带来另一个问题。程序处理 POST 请求时,使用 form.name.data 获取用户输入的名字,可是一旦这个请求结束,数据也就丢失了。

# 程序可以把数据存储在用户会话中,在请求之间“记住”数据。它是请求上下文中的变量session

def make_cache_key(*args,**kw):
    path = request.path  # 返回请求url，不带域名和参数
    if request.method == 'GET':
        agrs = str(hash(frozenset(request.args.items())))
        return path+agrs
    if request.method == 'POST':
        form = str(hash(frozenset(request.form.items())))
        return path+form

# 使用Flask-SQLAlchemy提供的pagination()方法。页数是pagination()方法的第一个参数，也是唯一必须的参数。
# 可选参数per_page用来指定每页显示的记录数。
# @bp.route('/')
# def index():
#     db = get_db()
#     posts = db.execute(
#      'SELECT p.id, title, body, created, updated, author_id,username,img'
#      ' FROM post p JOIN user u ON p.author_id = u.id'
#      ' order by created desc'
#      ).fetchall()

#     # t_times = posts['created'] + timedelta(hours=8)
#     # return render_template('blog/index.html', posts = posts)
    
#     return redirect(url_for('blog.index1', page_id=1))

@bp.route('/')
@bp.route('/<int:page_id>')
def index1(page_id=1):
    # if not page_id:
    #     page_id = 1
    db = get_db()
    session.pop('pageindex',None)
    pageindex = request.args.get('key')
    if pageindex:
        pageindex1 = pageindex.replace(" ","")
        pageindex1 = re.sub('\W+','',pageindex1)
        session['pageindex'] = pageindex
        posts = db.execute(
            "SELECT p.id,ifnull(c.count_id,0) as num, title, body, created, updated, author_id,username,img,click"
            " FROM post p JOIN user u ON p.author_id = u.id" 
            " LEFT JOIN (select post_id,count(id) as count_id from comment group by post_id) as c ON p.id = c.post_id"
            " where title like ?"
            " order by created desc",('%'+pageindex1+'%',)
            ).fetchall()
    else:
        posts = db.execute(
            'SELECT p.id, ifnull(c.count_id,0) as num, title, body, created, updated, p.author_id,username,img,click'
            ' FROM post p  JOIN user u ON p.author_id = u.id LEFT JOIN (select post_id,count(id) as count_id from comment group by post_id) as c ON p.id = c.post_id'
            ' order by created desc'
            ).fetchall()
    p=[]
    if posts:
        for index,post in enumerate(posts):
            if (index+1)<=page_id*3 and (index+1)>=(page_id*3)-2:
                p.append((index+1,post))

    if page_id < 1:
        return render_template('auth/page_not_found.html'), 404

    if int(len(posts))%3 == 0 and int(len(posts)) !=0:
        if page_id > int(len(posts))//3:
            return render_template('auth/page_not_found.html'), 404

    if int(len(posts))%3 != 0:
        if page_id > int(len(posts))//3 +1:
            return render_template('auth/page_not_found.html'), 404
   
    return render_template('blog/index.html', posts = p, posts_len=int(len(posts)), page_id=page_id,pageindex=pageindex)
    # elif page_id == 1 and not p:
    #     return redirect(url_for('blog.index1', page_id=1))
    # else:
    #     return render_template('auth/page_not_found.html'), 404

def allow_file(filename):
    return '.' in filename and filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS
        

def file_path(f, path='flaskr/static/img/'):

    sys_img_path, db_img_path,error = None,None,None
    if not(f and allow_file(f.filename)):
        # return jsonify({'Error':1001,'msg':'请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp、gif'})
        error = '请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp'
        return sys_img_path, db_img_path,error
    img_name = secure_filename(f.filename)
    print(img_name)
    md5_img_name = md5(img_name.encode('utf-8')).hexdigest()
    img_type = img_name.rsplit('.')[1].lower()
    if not os.path.exists(path):
        os.mkdir(path)
    current_app.config['UPLOAD_FOLDER'] = path
    real_file_name = md5_img_name+'.'+img_type
    sys_img_path = os.path.join(current_app.config['UPLOAD_FOLDER'],real_file_name)
    db_img_path = 'img/'+real_file_name
    return sys_img_path, db_img_path,error


@bp.route('/create', methods=['GET','POST'])
@logind_require
def create():
    if request.method == 'POST':
        error = None
        title = request.form['title']
        body = request.form['body']
        f = request.files['file']
        print('f',f,'name',f.name,'filename',f.filename)
        db_img_path = ''
        sys_img_path=''
        if  f.filename is not None and f.filename != '':            
            # if not(f and allow_file(f.filename)):
            #     return jsonify({'Error':1001,'msg':'请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp、gif'})
            #     # error = '请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp'
            # img_name = secure_filename(f.filename)
            # print(img_name)
            # md5_img_name = md5(img_name.encode('utf-8')).hexdigest()
            # img_type = img_name.rsplit('.')[1].lower()
            # file_path = 'flaskr/static/img/' 
            # current_app.config['UPLOAD_FOLDER'] = file_path
            # real_file_name = md5_img_name+'.'+img_type
            # sys_img_path = os.path.join(current_app.config['UPLOAD_FOLDER'],real_file_name)
            # db_img_path = 'img/'+real_file_name
            # # img_path = file_path + md5_img_name+'.'+img_type
            
            sys_img_path,db_img_path ,error= file_path(f)
            # f.save(sys_img_path)

        if not title:
            error = 'Title is required'
        if not body:
            error = 'Body is required'
        if error is not None:
            flash(error)
        else:
            if sys_img_path:
                f.save(sys_img_path)
            db = get_db()
            db.execute('insert into post (title,body,author_id,img) values(?,?,?,?)',(title,body,g.user['id'],db_img_path))
            db.commit()
            return redirect(url_for('blog.index1'))
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
        'select p.id ,author_id,created,title,body,username,img'
    ' from post p join user u on p.author_id=u.id where p.id=?',(id,)).fetchone()
    
    limit_post = db.execute(
        'select p.id ,author_id,created,title,body,username,img'
    ' from post p join user u on p.author_id=u.id where p.id>=?',(id,)).fetchall()

    if post is None or limit_post is None:
        abort(404, "Post id {} is Not exist.".format(id))
        return False

    if post['author_id'] != g.user['id']:
        abort(403,"当前账号无权限删除他人博客")
        return False
    # post = db.execute('select * from post where id=?',(id,)).fetchall()
    # post = get_post(id)
    # request.args.get('')获取get请求参数
    if request.method == 'POST':
        error = None
        db_img_path = ''
        sys_img_path=''
        title = request.form['title']
        body = request.form['body']
        if 'file' not in request.files:
            db_img_path = post['img']
        else:
            f = request.files['file']
            # f_name = secure_filename(f.filename)
            # if not(f and allow_file(f.filename)):
            #     return jsonify({'Error':1001,'msg':'请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp、gif'})
            # md5_f_name = md5(f_name.encode('utf-8')).hexdigest()
            # f_type = f_name.rsplit('.')[1].lower()
            # db_f_path = 'img/'+ md5_f_name +'.'+ f_type
            # f.save('flaskr/static/'+db_f_path)
            sys_img_path,db_img_path ,error= file_path(f)
            
        if not title:
            error = 'Title is required'
        if not body:
            error = 'Body is required'
        if len(title) > 20:
            error = 'Title length can not more than 20'
        if len(body) > 20000:
            error = 'Title length can not more than 20000'
        if error is not None:
            flash(error)
        else:
            if sys_img_path:
                f.save(sys_img_path)
            db.execute('update post set title=?,body=?,img=?,updated=? where id=?',(title,body,db_img_path,datetime.now().strftime('%Y-%m-%d %H:%M:%S'),id))
            db.commit()
            if len(limit_post) % 3 == 0:
                return redirect(url_for('blog.index1',page_id=len(limit_post)/3))
            else:
                return redirect(url_for('blog.index1',page_id=(len(limit_post)//3)+1))
    return render_template('blog/update.html',post=post)


@bp.route('/<int:id>/delete', methods=['POST'])
@logind_require
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('delete from post where id=?',(id,))
    db.commit()
    limit_post = db.execute(
        'select p.id ,author_id,created,title,body,username,img'
    ' from post p join user u on p.author_id=u.id where p.id>=?',(id,)).fetchall()
    if len(limit_post) != 0:
        if len(limit_post) % 3 == 0:
            return redirect(url_for('blog.index1',page_id=int(len(limit_post)//3)))
        else:
            return redirect(url_for('blog.index1',page_id=int(math.ceil(len(limit_post)/3))))
    else:
        return redirect(url_for('blog.index1',page_id=1))


@bp.route('/<int:id>/deleteApi', methods=['POST'])
def deleteApi(id):
    if g.user is None:
        return make_response(jsonify({'result':'false','ErrorInfo':'nologin'}))
    get_post(id)
    db = get_db()
    try:
        db.execute('delete from comment where post_id=?',(id,))
        db.execute('delete from post where id=?',(id,))
        #  sqlite不支持以下关联删除
        # db.execute('delete p,c from post p left join comment c on c.post_id = p.id where p.id=?',(id,))
    except Exception as e:
        db.rollback()
        return make_response(jsonify({'result':'false','msg':'删除未成功'}))
    db.commit()
    limit_post = db.execute(
        'select p.id ,author_id,created,title,body,username,img'
    ' from post p join user u on p.author_id=u.id where p.id=?',(id,)).fetchall()
    if limit_post is None:
        response = make_response(jsonify({'result':'true','msg':'删除失败'}))
    else:
        response = make_response(jsonify({'result':'false','msg':'删除成功'}))
    return response


def timeViwe(dtime):
    dtime = str(dtime)
    year = int(dtime.split('-')[0].strip())
    month = int(dtime.split('-')[1].strip())
    day = int(dtime.split(' ')[0].split('-')[-1].strip())
    hour = int(dtime.split(' ')[1].split(':')[0].strip())
    minute =int(dtime.split(' ')[1].split(':')[1].strip())
    second = int(dtime.split(' ')[1].split(':')[2].strip())
    if datetime.now().year < year:
        return '{}年前'.format(datetime.now().year-year)
    elif year == datetime.now().year and  datetime.now().month > month:
        return '{}月前'.format(datetime.now().month-month)
    elif  year == datetime.now().year and  datetime.now().month == month and datetime.now().day > day:
        return '{}天前'.format(datetime.now().day-day)
    elif datetime.now().hour>hour :
        return '{}小时前'.format(datetime.now().hour-hour)
    elif datetime.now().minute>minute :
        return '{}分钟前'.format(datetime.now().minute-minute)
    elif datetime.now().second>second :
        return '{}秒前'.format(datetime.now().second-second)
    elif datetime.now().second == second :
        return '刚刚'
    else:
        return '时间错误'


@bp.route('/<int:id>/detail',methods=['GET','POST'])
def detail(id):
    print ('view hello called')
    db = get_db()
    if request.method =='POST':
        if g.user == None:
            session['redirect'] = request.referrer
            # print(request.referrer)
            return redirect(url_for('auth.login',returnurl=request.url))
        title = request.form['title']
        content = request.form['body']
        error =None
        if not content or not title:
            error = '未输入内容'

        if len(title) > 10:
            error = '标题长度不能大于10'

        if error is not None:
            flash(error)
        else:
            try:
                db.execute('insert into comment (author_id,post_id,commentator,ctitle,content) values(?,?,?,?,?)',(g.user['id'],id,g.user['username'],title,content))
            except Exception as e:
                db.rollback()
                return jsonify({'result':'false','msg':'发布失败'})
            db.commit()
            
        return redirect(url_for('blog.detail', id=id))

    commentDatas = db.execute(
     'SELECT c.*,username'
     ' FROM comment c JOIN post P ON c.post_id = p.id JOIN user u ON c.author_id=u.id'
     ' where p.id=? order by c.comment_time desc',(id,)).fetchall()

    post = db.execute(
        'select p.id, title, body, p.created, p.updated, p.author_id, username,img, islike,click'
        ' from user u,post p'
        ' where u.id=P.author_id AND p.id=?',(id,)).fetchone()

    db.execute('update post set click=click+1 where id=?',(id,))
    db.commit()

    if g.user:
        up = db.execute(
            'select p.id, u.id, islike'
            ' from user u,post p'
            ' where u.id=P.author_id AND u.id=? AND p.id=?',(g.user['id'],id)).fetchone()
        return render_template('blog/detail.html',post=post,up=up, commentDatas=commentDatas,formTime = timeViwe)

    # t_times = post['created'] + timedelta(hours=8)
    return render_template('blog/detail.html',post=post,up=None,commentDatas=commentDatas,formTime = timeViwe)

@bp.route('/detail/likeSign',methods=['POST'])
def likeSign():
    pid = request.form['pid']
    db = get_db()
    post = db.execute(
        'select p.id, title, body, p.created, p.updated, p.author_id, username,img, islike'
        ' from user u,post p'
        ' where u.id=P.author_id AND p.id=?',(pid,)).fetchone()
    # Post.query.join(User).filter(Post.id=pid).one() 

    if g.user is None:
        return make_response(jsonify({'ErrorInfo':'nologin'}))  
    
    if post is None:
        return make_response(jsonify({'msg':'页面不存在'}))    

    if post['islike'] == '1':
        try:
            db.execute('update post set islike=0 where id=?',(pid,))
        except Exception as e:
            db.rollback()
            return make_response(jsonify({'msg':'取消标记失败'}))
        db.commit()
        return make_response(jsonify({'result':'true','state':'signed','msg':'取消标记成功'}))
    if post['islike'] == '0':
        try:
            db.execute('update post set islike=1 where id=?',(pid,))
        except Exception as e:
            db.rollback()
            return make_response(jsonify({'msg':'标记失败'}))
        db.commit()
        return make_response(jsonify({'result':'true','state':'unsign','msg':'标记成功'}))

def get_comment(id):
    db = get_db()
    comment = db.execute('select * from comment where id=?',(id,)).fetchone()
    if comment is None:
        # abort(404, 'comment id {} is not exists'.format(id))
        return make_response(jsonify({'result':'false','msg':'404，评论不存在'}))
    if comment['author_id'] != g.user['id']:
        # abort(403,'jujue')
        return make_response(jsonify({'result':'false','msg':'403，无权限，请检查当前账号是否为评论账号'}))
    return comment


@bp.route('/<int:id>/deleteCommentApi', methods=['POST'])
def deleteCommentApi(id):
    db = get_db()
    comment = db.execute('select * from comment where id=?',(id,)).fetchone()
    if g.user is None:
        return make_response(jsonify({'ErrorInfo':'nologin','msg':'请先登录!'}))
    if comment is None:
        # abort(404, 'comment id {} is not exists'.format(id))
        return make_response(jsonify({'result':'false','msg':'404，评论不存在'}))
    if comment['author_id'] != g.user['id']:
        # abort(403,'jujue')
        return make_response(jsonify({'result':'false','msg':'403，无权限，请检查当前账号是否为评论账号'}))
    
    md5_id = request.form['md5_id']
    if md5_id != md5(str(id).encode('utf-8')).hexdigest():
        return make_response(jsonify({'result':'false','msg':'删除未成功'}))
    
    # db = get_db()
    try:
        db.execute('delete from comment where id=?',(id,))
    except Exception as e:
        db.rollback()
        return make_response(jsonify({'result':'false','msg':'删除未成功'}))
    db.commit()
    limit_post = db.execute(
        'select *'
    ' from comment where id=?',(id,)).fetchall()
    if limit_post is None:
        response = make_response(jsonify({'result':'false','msg':'删除成功'}))
    else:
        response = make_response(jsonify({'result':'true','msg':'删除失败'}))
    return response


@bp.route('/upload',methods=['GET','POST'])
def upload():
    is_upload = False
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        print(f,filename)
        filename_type = f.filename.rsplit('.')[1].lower()
        md5_img_file = md5(filename.encode('utf-8')).hexdigest()
        if not (f and allow_file(filename)):
            return jsonify({'Error':1001,'msg':'请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp'})
        file_path = 'flaskr/static/img' 
        current_app.config['UPLOAD_FOLDER'] = file_path
        real_filename = md5_img_file+'.'+filename_type

        # for i in iter(f):
        #     md5().update(i)
        # md5_f = md5().hexdigest()
        # r = md5_f+'.'+filename_type
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'],real_filename))
        is_upload=True
        return render_template('blog/upload.html',is_upload=is_upload, filename=real_filename)
    return render_template('blog/upload.html')

# 这个方法的缺点是在导入时无法在蓝图中使用应用对象。但是你可以在一个请求中使用它。 
# 如何通过配置来访问应用？使用 current_app:
@bp.route('/test')
@cached()
def cache_test():
    print('test')
    return render_template('blog/t.html')

# @bp.route('/test11')
# @cache.memoize(timeout=300)
# def cache_test11():
#     print('test11')
#     return render_template('blog/t1.html')

# @bp.before_request
# def handle_before():
#     # 从缓存里查询请求次数
#     count = cache.get('count') or 1
#     # 如果次数大于10,直接不让用户再继续了
#     if count > 10:
#         # return '5秒钟以内只能刷新十次'
#         abort(403,'操作次数频繁')
#     count +=1
#     # 该缓存5秒过期
#     cache.set('count',count,5)
#     if not request.user_agent:
#         return '求你带个头'


