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
from domain import State


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
        #print e
        #print "This website don't have domain certificate"
        exit(0)
    
    cert = s.getpeercert()

    subject = cert['subject']
    expire = ssl.cert_time_to_seconds(cert['notAfter'])

    tl = time.localtime(expire)
    expired_time = time.strftime("%Y-%m-%d %H:%M:%S", tl)
    remain = expire - time.time()
    if remain < 0:
        #print 'certification expired'
        return -1, format_time
    else:
        expired_day = int(remain / 86400)
        #print "certification will be expired in %d days" % expired_day
        return expired_day, expired_time, subject


def record_msg(url ,ip, expired_day, expired_time, subject):

    domain = State()
    if url not in domain['data']:
        msg = {}
        msg['ip'] = ip
        msg['expired_day'] = expired_day
        msg['expired_time'] = expired_time
        msg['subject'] = subject
        domain['data'][url] = msg
    else:
        domain['data'][url]['ip'] = ip
        domain['data'][url]['expired_day'] = expired_day
        domain['data'][url]['expired_time'] = expired_time
        domain['data'][url]['subject'] = subject 
    domain.save()
        
def discovery_website():

    print '{'
    print '\t"data":['
    with open("/opt/scripts/website.txt", "r") as f:

        line_num = len(f.readlines())
        f.seek (0)
        i = 1
        for line in f.readlines():
            line.strip("\n")
            lines = line.split()
            if i != line_num:
                if len(lines) == 1:
                    print '\t\t{"{#WEBSITENAME}":"%s"},' % lines[0]
                else:
                    print 'Bad configuration in file website.txt'
                    exit(0)
            else:
                if len(lines) == 1:
                    print '\t\t{"{#WEBSITENAME}":"%s"}' % lines[0]
                elif len(lines) == 2:
                    print 'Bad configuration in file website.txt'
                    exit(0)
            i += 1
    print '\t]'
    print '}'

def main():
    
    if len(sys.argv) ==2 and sys.argv[1] == "discovery_website":
        discovery_website()
    elif len(sys.argv) ==3 and sys.argv[1] == "monitor_sslcert":
        url = sys.argv[2]
        ip =  get_ip_by_domain(url)
        expired_day, expired_time, subject = get_ssl_expired_time(url)
        print expired_day
        record_msg(url, ip, expired_day, expired_time, subject)
    else:
        print "Usage:python %s discovery_website|monitor_sslcert [URL]" % sys.argv[0]


if __name__ == "__main__":

    main()
