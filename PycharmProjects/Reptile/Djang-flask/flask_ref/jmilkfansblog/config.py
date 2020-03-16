class Config(object):
    """Base config class."""
    SECRET_KEY = '123456'
    RECAPTCHA_PUBLIC_KEY = "<your public key>"
    RECAPTCHA_PRIVATE_KEY = "<your private key>"
   


class ProdConfig(Config):
    """Production config class."""
    pass

class DevConfig(Config):
    """Development config class."""
    DEBUG = True
    # MySQL connection
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:fanguiju@127.0.0.1:3306/myblog?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///E:/Pscrapy/PycharmProjects/Reptile/Djang-flask/flask_ref/jmilkfansblog/data.sqlite'
    # SQLALCHEMY_MIGRATE_REPO = 'dp.repository'
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CACHE_TYPE = 'simple'  # 使用本地python字典进行存储，线程非安全

    # CACHE_TYPE = 'filesystem' # 使用文件系统来存储缓存的值
    # CACHE_DIR = "" # 文件目录

    # CACHE_TYPE = 'memcached' # 使用memcached服务器缓存
    # CACHE_KEY_PREFIX # 设置cache_key的前缀
    # CAHCE_MEMCACHED_SERVERS # 服务器地址的列表或元组
    # CACHE_MEMCACHED_USERNAME # 用户名
    # CACHE_MEMCACHED_PASSWORD # 密码

    # CACHE_TYPE = 'uwsgi' # 使用uwsgi服务器作为缓存
    # CACHE_UWSGI_NAME # 要连接的uwsgi缓存实例的名称

    # CACHE_TYPE = 'redis' # 使用redis作为缓存
    # CACHE_KEY_PREFIX # 设置cache_key的前缀
    # CACHE_REDIS_HOST  # redis地址
    # CACHE_REDIS_PORT  # redis端口
    # CACHE_REDIS_PASSWORD # redis密码
    # CACHE_REDIS_DB # 使用哪个数据库
    # # 也可以一键配置
    # CACHE_REDIS_URL 连接到Redis服务器的URL。示例redis://user:password@localhost:6379/2