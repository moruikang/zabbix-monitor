#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import time
import ssl
import socket 
import time
import smtplib
from email.mime.text import MIMEText
import json
from send_email import send_mail as sm


#url = sys.argv[1]
socket.setdefaulttimeout(2)

def get_ip_by_domain(url):
    ip = socket.gethostbyname(url)
    return ip

def get_ssl_expired_time(url):

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()

    s = socket.socket()
    s = context.wrap_socket(s, server_hostname=url)
    try:
        s.connect((url, 443))
        s.do_handshake()
    except Exception, e:
        print e
        print "This website don't have domain certificate"
        exit(0)
    
    cert = s.getpeercert()

    expire = ssl.cert_time_to_seconds(cert['notAfter'])

    tl = time.localtime(expire)
    expired_time = time.strftime("%Y-%m-%d %H:%M:%S", tl)
    remain = expire - time.time()
    if remain < 0:
        print 'certification expired'
        return -1, format_time
    else:
        expired_day = int(remain / 86400)
        print "certification will be expired in %d days" % expired_day
        return expired_day, expired_time

#def send_email(mail_list, sub, content):
#
#    mail_host = "smtp.qq.com" #"smtp.126.com"
#    mail_user = "511452239" #"wanty23"
#    mail_pass = "mrkhwjl821" #"8529293"
#    mail_postfix = "qq.com" #"126.com"
#    
#    me = "domain name expired support" + "<" + mail_user +"@" + mail_postfix + ">"
#    msg = MIMEText(content, _subtype="plain", _charset="gb2312")
#    msg["Subject"] = sub
#    msg["From"] = me
#    msg["To"] = str(mail_list)
   
#    try:
#        server = smtplib.SMTP()
#        server.connect(mail_host)
#        server.login(mail_user,mail_pass)
#        server.sendmail(me, mail_list, msg.as_string())
#        server.close()
#        return True
#    except Exception, e:
#        print str(e)
#        return False

def record_msg(url ,ip, expired_day, expired_time):

    msg = dict()
    msg[url] = dict()
    msg[url]['ip'] = ip
    msg[url]['expired_day'] = expired_day
    msg[url]['expired_time'] = expired_time
    url_file = "url.json"
    with open("url.json","a") as f:
        json.dump(msg, f)
        f.write("\n")


if __name__ == "__main__":

    url = sys.argv[1]
    ip =  get_ip_by_domain(url)
    expired_day, expired_time = get_ssl_expired_time(url)
    print ip, expired_day, expired_time
    if expired_day < 200:
       sub = "证书即将于%s过期，剩余%d天" % (str(expired_time), expired_day)
       content = "证书即将于%s过期，剩余%d天" % (expired_time, expired_day)
       sm("moruikang@youmi.net", sub, content)
    record_msg(url, ip, expired_day, expired_time)
