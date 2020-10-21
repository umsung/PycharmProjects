import os
import unittest
import time
import HTMLTestRunner
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


cur_path = os.path.dirname(os.path.realpath(__path__))


def add_case(caseName="case", rule="test_*.py"):
    case_path = os.path.join(cur_path, caseName)

    if not os.path.exists(case_path): os.mkdir(case_path)
    print('case path: ', case_path)
    suite = unittest.defaultTestLoader.discover(case_path, pattern=rule, top_level_dir=None)
    print(suite)
    return suite


def run_case(all_case, reportName="report"):
    now = time.strftime("%Y-%m-%d_%H_%M_%S")
    report_folder_path = os.path.join(cur_path, reportName)

    if os.path.exists(report_folder_path): os.mkdir(report_folder_path)

    report_real_path = os.path.join(report_folder_path, now+'.html')
    print(report_folder_path)

    fp = open(report_real_path, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='接口测试报告标题', description="用例执行情况")
    runner.run(all_case)
    fp.close()


def get_report_file(report_folder_path):
    lists = os.listdir(report_folder_path)
    lists = sorted(lists, key=lambda x: os.path.getmtime(os.path.join(report_folder_path, x)))
    report_file = os.path.join(report_folder_path, lists[-1])
    return report_file


def send_email(report_file, sender, receiver, stmpserver, port, username, pwd):
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 定义邮件内容
    msg = MIMEMultipart()
    body = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['subject'] = u"测试报告标题"
    msg['from'] = sender
    msg['to'] = receiver
    msg.attach(body)

    # 添加邮件附件
    att = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')
    att['Content-Type'] = 'application/octet-stream'
    att['Content-Disposition'] = 'attachment; filename = "report.html"'
    msg.attach(att)

    try:
        try:
            # 像QQ邮箱这种ssl加密的就走SMTP_SSL，用授权码登录
            # 其它邮箱就正常账号密码登录，走SMTP
            smtp = smtplib.SMTP_SSL(stmpserver, port)
        except:
            stmp = smtplib.SMTP()
            stmp.connect(stmpserver, port)

        stmp.login(username, pwd)
        stmp.send_message(sender, receiver, msg.as_string())
        print('success')
    except:
        print('email send error')



if __name__ == '__main__':
    all_case = add_case()
    run_case(all_case)
    report_folder_path = os.path.join(cur_path, 'report')
    report_file = get_report_file()
    from API_Auto_yoyo.config import readConfig
    sender = readConfig.sender
    receiver = readConfig.receiver
    stmpserver =readConfig.stmp_server
    port = readConfig.port
    pwd = readConfig.pwd
    send_email(report_file,sender, receiver, stmpserver, port, pwd)


