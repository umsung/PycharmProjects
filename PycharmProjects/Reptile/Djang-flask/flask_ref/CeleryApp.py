from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from tasks import send_email,celery

app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'hard to guess string',
    MAIL_SERVER = 'smtp.163.com',
    MAIL_DEFAULT_SENDER = 'qq1516442017@163.com',
    MAIL_USERNAME = 'qq1516442017@163.com',
    MAIL_PASSWORD = 'qq545699233'
)

# app.config["CELERY_TASK_SERIALIZER"] = "pickle"  # 默认是json序列化，设置为pickle
# app.config["CELERY_ACCEPT_CONTENT"] = ["pickle"]  # 设置反序列化为pickle
# app.config["CELERY_RESULT_SERIALIZER"] = "pickle"


mail = Mail(app)

@app.route('/celeryapp',methods=['GET','POST'])
def celeryapp():
    if request.method == 'GET':
        return render_template('celeryapp.html')

    address = request.form['address']
    msg = Message('Hello Celery',
                  recipients=[address])
    msg.body = request.form['content']
    # mail.send(msg)
    # send_email.delay(msg)
    send_email.delay(msg)

    flash('Sending email to %s' % address)
    return redirect(url_for('celeryapp'))


if __name__ == "__main__":
    app.run(debug=True)