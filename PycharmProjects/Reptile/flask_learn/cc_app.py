from flask import Flask,url_for,escape,request,render_template,g,Markup,make_response,redirect,abort
from flask import session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello, World'

# 首先我们导入了 Flask 类。 该类的实例将会成为我们的 WSGI 应用。

# 接着我们创建一个该类的实例。第一个参数是应用模块或者包的名称。
# 如果你使用 一个单一模块（就像本例），那么应当使用 __name__ ，因为名称会根据这个 模块是按应用方式使用还是作为一个模块导入而发生变化（可能是 ‘__main__’ ， 也可能是实际导入的名称）。
# 这个参数是必需的，这样 Flask 才能知道在哪里可以 找到模板和静态文件等东西。更多内容详见 Flask 文档。

# 然后我们使用 route() 装饰器来告诉 Flask 触发函数的 URL 。

# 函数名称被用于生成相关联的 URL 。函数最后返回需要在用户浏览器中显示的信息。

# 把它保存为 hello.py 或其他类似名称。请不要使用 flask.py 作为应用名称，这会与 Flask 本身发生冲突。


# app.route添加网址映射，等效于方法app.add_url_rule()。app.add_url_rule()存储了url映射。
@app.route('/')
def index():
    return 'Index Page test autoload'

# 使用 route() 装饰器来把函数绑定到 URL: 可以动态变化 URL 的某些部分， 还可以为一个函数指定多个规则

# 使用url_for动态构建指定函数的 URL

@app.route('/login111')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

# HTTP 方法
@app.route('/login22', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        return 'post'
    else:
        return 'get'

# 渲染模板
# 使用 render_template() 方法可以渲染模板，你只要提供模板名称和需要 作为参数传递给模板的变量就行了
@app.route('/hello/')
@app.route('/hello/<name>')
def hello1(name=None):
    return render_template('hello.html', name=name)

# 请求对象 request，通过使用 method 属性可以操作当前请求方法，通过使用 form 属性处理表单数据
# 操作 URL （如 ?key=value ）中提交的参数可以使用 args 属性:

@app.route('/login33',methods=['POST','GET'])
def login2():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return render_template('login.html',password=password,username=username)
    elif request.method == 'GET':
        username = request.args.get('username','')
        password = request.args.get('password','')
        return render_template('login.html',password=password,username=username)
    else:
        error = 'Invalid username/password'
    return render_template('login.html',error=error)

# 文件上传 request.file,
# 已上传的文件被储存在内存或文件系统的临时位置。你可以通过请求对象 files 属性来访问上传的文件。每个上传的文件都储存在这个 字典型属性中。
# 通过save方法保存到服务器系统， 

@app.route('/update',methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file_key']
        f.save('lujing/a.txt' + secure_filename(f.filename))

# Cookies
# 要访问 cookies ，可以使用 cookies 属性。可以使用响应 对象 的 set_cookie 方法来设置 cookies 。
# 请求对象的 cookies 属性是一个包含了客户端传输的所有 cookies 的字典。在 Flask 中，如果使用 会话 ，那么就不要直接使用 cookies ，因为 会话 比较安全一些。

@app.route('/cookies')
def get_cookies():
    username_cookie = request.cookies.get('username')
    return username_cookie

# 可以添加头的字典作为第3个参数，但是很少使用。另外也可以返回Response对象。
# make_response()接纳1-3个参数，适用于视图函数定制响应，比如：
@app.route('/cookies')
def set_cookie():
    response = make_response(render_template(''))
    response.set_cookie('username','username_cookie')
    return response


# 关于响应
# 视图函数的返回值会自动转换为一个响应对象。如果返回值是一个字符串，那么会被 转换为一个包含作为响应体的字符串、一个 200 OK 出错代码 和一个 text/html 类型的响应对象。如果返回值是一个字典，那么会调用 jsonify() 来产生一个响应。以下是转换的规则：

# 如果视图返回的是一个响应对象，那么就直接返回它。

# 如果返回的是一个字符串，那么根据这个字符串和缺省参数生成一个用于返回的 响应对象。

# 如果返回的是一个字典，那么调用 jsonify 创建一个响应对象。

# 如果返回的是一个元组，那么元组中的项目可以提供额外的信息。元组中必须至少 包含一个项目，且项目应当由 (response, status) 、 (response, headers) 或者 (response, status, headers) 组成。 status 的值会重载状态代码， headers 是一个由额外头部值组成的列表 或字典。

# 如果以上都不是，那么 Flask 会假定返回值是一个有效的 WSGI 应用并把它转换为 一个响应对象。

# 如果想要在视图内部掌控响应对象的结果，那么可以使用 make_response() 函数。



# 重定向和错误
@app.route('/redirect')
def t_redirect():
    return redirect(url_for('login3'))

@app.route('/login3')
def login3():
    abort(401)
    return 'this is never excute'

# 使用 errorhandler() 装饰器可以定制出错页面    # 
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
# 注意 render_template() 后面的 404 ，这表示页面对应的出错 代码是 404 ，即页面不存在
# 默认返回状态码200，可以修改






# Session
#  session 的对象，允许你在不同请求 之间储存信息,相当于用密钥签名加密的 cookie 

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.secret_key = os.urandom(16)

@app.route('/index')
def index3():
    if 'username' in session:
        return 'login in as %s' % escape(session['username'])
    return 'not logind'

@app.route('/login',methods=['GET','POST'])
def login4():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return ''' <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>'''

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

# 日志
# app.logger.debug('A value for debugging')
# app.logger.warning('A warning occurred (%d apples)', 42)
# app.logger.error('An error occurred')


if __name__ == "__main__":
    # 使用调试选项debug=True即可。当代码改变时，它会自动重新加载应用程序
    # app.run(debug=True)
    pass