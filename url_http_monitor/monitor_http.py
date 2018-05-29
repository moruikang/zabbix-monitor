#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import sys

def monitor_http(url):

    response = None
    try:
        response = urllib2.urlopen(url,timeout=5)
        #print response.info() # header
        print response.getcode()
    except urllib2.URLError as e:

        if hasattr(e, 'code'):
            print e.code
        elif hasattr(e, 'reason'):
            print e.reason
    finally:
       if response:
           response.close()

def discovery_web():

    print '{'
    print '\t"data":['
    with open("/opt/scripts/WEB.txt", "r") as f:

        line_num = len(f.readlines())
        f.seek (0)
        i = 1
        for line in f.readlines():
            line.strip("\n")
            lines = line.split()
            if i != line_num:
                if len(lines) == 1:
                    print '\t\t{"{#SITENAME}":"%s","{#PROXYIP}":""},' % lines[0]
                elif len(lines) == 2:
                    print '\t\t{"{#SITENAME}":"%s","{#PROXYIP}":"%s"},' % (lines[0],lines[1])
            else:
                if len(lines) == 1:
                    print '\t\t{"{#SITENAME}":"%s","{#PROXYIP}":""}' % lines[0]
                elif len(lines) == 2:
                    print '\t\t{"{#SITENAME}":"%s","{#PROXYIP}":"%s"}' % (lines[0],lines[1])
            i += 1
    print '\t]'
    print '}'

def main():

    if len(sys.argv) ==2 and sys.argv[1] == "discovery_web":
        discovery_web()
    elif len(sys.argv) ==3 and sys.argv[1] == "monitor_http":
        url = sys.argv[2]
        monitor_http(url)
    else:
        print "Usage:python %s discovery_web|monitor_http [URL]" % sys.argv[0]

if __name__ == "__main__":
    main()
