# 装饰器函数带参数
def arg_func(arg):
    def func1(func):
        def add_func():
            if arg == 'aaa':
                print('aaa')
            if arg == 'bbb':
                print('bbb')
            return func()
        return add_func
    return func1

@arg_func('aaa')
def test():
    print('is aaa')

test()

def cached(timeout=5 * 60, key='view_%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            value = cache.get(cache_key)
            if value is None:
                value = f(*args, **kwargs)
                cache.set(cache_key, value, timeout=timeout)
            return value
        return decorated_function
    return decorator

# @app.route('/hello')
# @app.route('/hello/<name>')
# @cached()
# def hello(name=None):
#     print 'view hello called'
#     return render_template('hello.html', name=name)