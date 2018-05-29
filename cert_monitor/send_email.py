# -*- coding:utf-8 -*-

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


#sender_qq为发件人的qq号码
sender_qq = '511452239'
#pwd为qq邮箱的授权码
pwd = 'mdqekbifknxqbibd'
#收件人邮箱receiver
receiver= ['moruikang@youmi.net']
#邮件的正文内容
mail_content = '你好，测试'
#邮件标题
mail_title = '测试邮件'

def send_mail(receiver=[],mail_title='',mail_content=''):

    # qq邮箱smtp服务器
    sender_qq = '511452239'
    pwd = 'mdqekbifknxqbibd'
    host_server = 'smtp.qq.com'
    sender_qq_mail = sender_qq+'@qq.com'

    #ssl登录
    smtp = SMTP_SSL(host_server)
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = str(receiver)
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()

if __name__ == "__main__":
    send_mail(receiver=receiver,mail_title=mail_title,\
    mail_content=mail_content)
