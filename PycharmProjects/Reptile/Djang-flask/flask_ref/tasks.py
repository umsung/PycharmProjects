from celery import Celery
import os

celery = Celery('tasks', backend='redis://localhost:6379/2', broker='redis://localhost:6379/1')

from kombu import serialization
serialization.registry._decoders.pop("application/x-python-serialize")

# if os.name != "nt":
#     # Mac and Centos
#     celery.conf.update(
#         CELERY_ACCEPT_CONTENT = ['application/json', ],
#         CELERY_TASK_SERIALIZER = 'json',
#     )
# else:
#     celery.conf.update(
#         # result_expires=3600,
#         # task_serializer='pickle',
#         CELERY_ACCEPT_CONTENT = ['pickle', ],
#         CELERY_TASK_SERIALIZER = 'pickle',
#         # CELERY_RESULT_SERIALIZER = 'pickle'
#     )


@celery.task
def send_email(msg):
    with app.app_context():
        mail.send(msg)


@celery.task
def add(x, y):
    return x + y
'''
创建了一个Celery实例app，名称为tasks；
中间人用RabbitMQ，URL为amqp://guest@localhost//；
存储用Redis，URL为redis://localhost:6379/0。
同时我们定义了一个Celery任务add，可以返回两个参数的和。
当函数使用@app.task修饰后，即为可被Celery调度的任务。
'''

'''
启动后台职程,职程会监听消息中间人队列并等待任务调度，启动命令为：
$ celery worker -A tasks --loglevel=info --concurrency=5
参数”-A”指定了Celery实例的位置，本例是在”tasks.py”中，celery命令会自动在该文件中寻找Celery对象实例。不过我更建议你指定Celery对象名称，如”-A tasks.app”。
参数”loglevel”指定了日志等级，也可以不加，默认为warning。
参数”concurrency”指定最大并发数，默认为CPU核数。
任务的并发默认采用多进程方式，Celery也支持”gevent”或者”eventlet”协程并发。
方法是在启动职程时使用”-P”参数
celery -A tasks worker --pool=solo -l info
'''

if __name__ == "__main__":
    add.delay(4,4)