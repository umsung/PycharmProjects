class Dict(dict):

    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


d=Dict(a=1,b=2)
print(d.a)
print(d['b'])
d.key='value'
assert d['key'] != 'value'
print(d['key'] == 'value')