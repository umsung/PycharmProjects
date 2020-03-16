# 一个完整的Celery分布式队列架构应该包含一下几个模块：

# 消息中间人 Broker
# 消息中间人，就是任务调度队列，通常以独立服务形式出现。
# 它是一个生产者消费者模式，即主程序将任务放入队列中，而后台职程则会从队列中取出任务并执行。
# 任务可以按顺序调度，也可以按计划时间调度。Celery组件本身并不提供队列服务，你需要集成第三方消息中间件。
# Celery推荐的有RabbitMQ和Rsedis，另外也支持MongoDB、SQLAlchemy、Memcached等，但不推荐。

# 任务执行单元 Worker，也叫职程
# 即执行任务的程序，可以有多个并发。它实时监控消息队列，获取队列中调度的任务，并执行它。

# 执行结果存储 Backend
# 由于任务的执行同主程序分开，如果主程序想获取任务执行的结果，就必须通过中间件存储。
# 同消息中间人一样，存储也可以使用RabbitMQ、Redis、MongoDB、SQLAlchemy、Memcached等，建议使用带持久化功能的存储中间件。另外，并非所有的任务执行都需要保存结果，这个模块可以不配置。

from celery import Celery

app = Celery('tasks',
             broker='amqp://guest@localhost//',
             backend='redis://localhost:6379/0')

@app.task
def add(x, y):
    return x + y

#  celery worker -A tasks --loglevel=info --concurrency=5