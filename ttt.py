import smtplib # 发送邮件
from email.mime.text import MIMEText  # 创建邮件的文本内容
from email.mime.multipart import MIMEMultipart  # 构建多组件的邮件（比如邮件里面包含文本和附件）
from email.mime.application import MIMEApplication  # 添加附件

