from flask import Flask, request, render_template, session, flash, redirect, url_for
from celery import Celery
from flask_mail import Mail, Message

app = Flask(__name__)

# celery配置
app.config["CELERY_BROKER_URL"] = "redis://127.0.0.1:6379/0"  # 消息代理的连接url
app.config["CELERY_RESULT_BACKEND"] = "redis://127.0.0.1:6379/0"  # 存储状态后运行结果
app.config["CELERY_TASK_SERIALIZER"] = "pickle"  # 默认是json序列化，设置为pickle
app.config["CELERY_ACCEPT_CONTENT"] = ["pickle"]  # 设置反序列化为pickle
app.config["CELERY_RESULT_SERIALIZER"] = "pickle"


# 163邮箱配置
app.config["MAIL_SERVER"] = "smtp.163.com"  # 电子邮箱的服务器的主机名和ip地址
app.config["MAIL_PORT"] = 25  # 电子邮箱的服务器的端口
app.config["MAIL_USE_TLS"] = True  # 启用传输层安全协议
app.config["MAIL_USERNAME"] = "qq1516442017@163.com"  # 邮箱账户用户名
app.config["MAIL_PASSWORD"] = "qq545699233"  # 邮件账户的密码

app.config["SECRET_KEY"] = "sdfghjklfghjk"

# 创建一个celery对象，传入应用名和消息代理的连接url
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery的其他任何配置可以直接使用celery.conf.update（）通过Flask的配置直接传递
celery.conf.update(app.config)

# 创建一个email对象
mail = Mail(app)


# 定义一个异步任务，这里传参是Message的实例对象，因为设置了pickle序列化，可以直接传递自定义的实例，程序出错
@celery.task
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


# 当使用json序列化时，需要在任务中创建实例
@celery.task
def send_async_email2():
    msg = Message(
        "Hello from flask",
        sender='qq1516442017@163.com',
        recipients=["545699233@qq.com"]
    )
    msg.body = "This is a test email sent from a background Celery task."
    with app.app_context():
        mail.send(msg)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("celeryapp.html", email=session.get("email", ""))
    email = request.form.get("content")
    session['email'] = email

    # 发送邮件（使用自定义的实例）
    # msg = Message(
    #     "Hello from flask",
    #     sender='xxxx@163.com',
    #     recipients=[request.form.get("email")]
    # )
    # msg.body = "This is a test email sent from a background Celery task."
    if request.form['submit'] == 'Send':
        # 立即发送（使用自定义的实例）
        # send_async_email.delay(msg)
        # 未设置pickle序列化时，需在任务中创建实例，执行异步任务如下：
        send_async_email2.delay()
        flash(f"Sending email to {email}")
    else:
        # 一分钟后发送（使用自定义的实例）
        # send_async_email.apply_async(args=[msg], countdown=60)
        # 未设置pickle序列化时，需在任务中创建实例，执行异步任务如下：
        send_async_email2.apply_async(countdown=2)
        flash(f'An email will be sent to {email} in one minute')
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)