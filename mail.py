import smtplib
from email.mime.text import MIMEText

def sendEmail(email,subject,content):
    # 发送邮件
    sender='TheSenderEmail@example.com'
    password='NEJP*****IAKPG'
    receiver = email
    message = MIMEText(content, "html", "utf-8")
    message['Subject'] = subject
    message['To'] = receiver
    message['From'] = sender
    try:
        smtp = smtplib.SMTP_SSL("smtp.163.com", 994)  # 实例化smtp服务器
        smtp.login(sender, password)
        smtp.sendmail(sender, [receiver], message.as_string())
        print("发送成功!")
    except:
        print("发送失败！")
        
        
