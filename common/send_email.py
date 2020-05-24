"""
通过邮件发送测试报告
报告作为邮件附件的形式进行发送

"""


def send_msg(file_path):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication

    # 第一步：连接到smtp服务器
    smtp = smtplib.SMTP_SSL(host="smtp.qq.com", port=465)

    # 第二步：登录服务器
    smtp.login("musen_nmb@qq.com", "algmmzptupjccbab")

    # 第三步：准备邮件
    # 1、准备内容
    from_user = "musen_nmb@qq.com"
    to_user = "3247119728@qq.com"
    subject = "发送测试报告"
    content = "2019-11-27上课的测试报告"
    # 读取报告文件中的内容
    file_content = open(file_path, "rb").read()

    # 2、构造邮件
    # (1)、构造一封多组件的邮件
    msg = MIMEMultipart()

    # (2)往多组件邮件中加入文本内容
    text_msg = MIMEText(content, _subtype='plain', _charset="utf8")
    msg.attach(text_msg)

    # (3)往多组件邮件中加入文件附件
    file_msg = MIMEApplication(file_content)
    file_msg.add_header('content-disposition', 'attachment', filename='python.html')
    msg.attach(file_msg)

    # (4)添加发件人，收件人，邮件主题
    msg["From"] = from_user
    msg["To"] = to_user
    msg["Subject"] = subject

    # print(msg)
    # 第四步： 发送邮件
    smtp.send_message(msg, from_addr="musen_nmb@qq.com", to_addrs="942582599@qq.com")
