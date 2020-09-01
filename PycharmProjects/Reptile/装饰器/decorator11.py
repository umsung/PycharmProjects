import functools

def log(parm):
    if isinstance(parm, str):
        def decorator(func):
            @functools.wraps(func)
            def wapper(*args, **kw):
                print('%s,%s' %(parm, func.__name__))
                return func(*args, **kw)
            return wapper
        return decorator
    else:
        @functools.wraps(parm)
        def wapper(*args, **kw):
            instance = args[0]
            print(instance.duation)
            print(args[1:])
            print('%s' % parm.__name__)
            return parm(*args, **kw)
        return wapper

class logger(object):
    def __init__(self, duation, func):
        self.duation = duation
        self.func = func

    def __call__(self, *args, **kw):
        print('wait %s S' % self.duation)
        return self.func(*args, **kw)

    @log
    def test(self, p1,a,b,c):
        print(f'this is {p1}')


l = logger(1,2)

l.test('p111',5,6,9)

