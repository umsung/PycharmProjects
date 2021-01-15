import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(subject='subject', content='content'):
    # mail server
    mail_host = 'smtp.sina.com'
    mail_port = 25
    mail_user = ''     # 账号
    mail_pwd = ''       # 密码

    # mail message
    # email模块 负责构造邮件
    # 三个参数：第一个为邮件正文文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = subject  # 邮件的主题
    message['From'] = ''   # 发送者    填写发送邮箱者地址
    message['To'] = ''   # 接收者      填写接收邮箱者地址, #收件人为多个收件人,通过join将列表转换为以;为间隔的字符串

    # send mail
    # smtplib模块负责发送邮件，是一个发送邮件的动作
    try:
        # 实例化SMTP()
        smtp_obj = smtplib.SMTP()

        # 实例化SMTP(),连接邮箱服务器, mail_host是邮箱服务器地址，mail_port是端口，
        # 新浪邮箱：smtp.sina.com,
        # 新浪VIP：smtp.vip.sina.com,
        # 搜狐邮箱：smtp.sohu.com，
        # 126邮箱：smtp.126.com,
        # 139邮箱：smtp.139.com,
        # 163网易邮箱：smtp.163.com。
        smtp_obj.connect(mail_host, mail_port)  # SMTP协议默认端口是25
        smtp_obj.login(mail_user, mail_pwd)
        # as_string()message(MIMEText对象或者MIMEMultipart对象)变为str
        smtp_obj.sendmail(message['From'], message['To'], message.as_string())
        smtp_obj.quit()
    except smtplib.SMTPException as e:
        print(e)


def send_mail_withFile(sender, psw, receiver, smtpserver, report_file):
    '''发送最新的测试报告内容，发送可带附件的邮件'''
    # 读取测试报告的内容
    with open(report_file, "rb") as f:
        mail_body = f.read()
    # 定义邮件内容
    msg = MIMEMultipart()   # 模块MIMEMultipart发送可带附件, MIMEText只能发送正文
    body = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    msg['Subject'] = u"自动化测试报告"
    msg["from"] = sender
    msg["to"] = psw
    # 加上时间戳
    # msg["date"] = time.strftime('%a, %d %b %Y %H_%M_%S %z')
    msg.attach(body)
    # 添加附件
    att = MIMEText(mail_body, "base64", "utf-8")
    # att = MIMEText(open(report_file, "rb").read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment; filename= "report.html"'
    msg.attach(att)

    # --- 发送邮件 兼容163和qq邮箱--
    try:
        # 登录邮箱
        smtp = smtplib.SMTP()
        # 连接邮箱服务器
        smtp.connect(smtpserver)
        # 用户名密码
        smtp.login(sender, psw)
    except:
        smtp = smtplib.SMTP_SSL(smtpserver, port)
        smtp.login(sender, psw)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('test report email has send out !')


s = 'Please study hard'
c = 'My name is Teacher hou, I teach python'
send_mail(subject=s, content=c)
