#coding=utf-8

# origin auther: garsonbb
# by garson blog garnote.top
import sys, getopt
import time
from gevent.queue import Queue
from gevent.threadpool import ThreadPool
import gevent
from gevent import monkey
import requests

from detect import *
monkey.patch_all(thread=False, ssl=False, socket=True)

pool = ThreadPool(3)
q = Queue()

rin = 'task.txt'
output = 'replace'
timeout = 1
parallels = 20
hostname = 'google.com'
mod = True
ips = []
passip = []

times = 0
n = 1
stop = False
port = 8118


def printx (text = '',type = 0):
    global times ,n
    p = int((times/n)*30)
    t1 = '##############################' #30
    t2 = '                              ' #30
    if type == 1:
        sys.stdout.write('                                                      \r')
        sys.stdout.flush()
        print(text)
    else:
        sys.stdout.write('[' + t1[0:p] + t2 [0:30-p] + ']' + '\r')
        sys.stdout.flush()


def worker(port):

    while not q.empty():
        global times ,n ,passip,stop
        ip = q.get_nowait()
        port = 8118 if port is None else str(port)
        if detect(ip, timeout, hostname, port) and req_test(ip, port) == True:
            passip.append(ip)
            printx ('√   '+ip , 1)
        times += 1
        printx()

        global output
        #print ('√   finish  ' + 'This time seem'+ str(times) +' ip,'+'SNI_IP '+ str(len(passip)) +' s。')
        print (times)
        print (passip)

def req_test(ip, port):
    testUrl = 'http://www.douban.com'
    timeout = 3
    proxies = {"http":"http://"+ip+":"+port,"https":"http://"+ip+":"+port
    }
    headers = {
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0',
           'Referer': 'http://www.zhihu.com/',
           
    }
    try:
        content=requests.get(testUrl,proxies=proxies,timeout=timeout, headers=headers).text.encode('UTF-8')
    except Exception as e:
        print (e)
        print ("NetWork Error...")
        return False
    return True


def caller(ips ,port):
    print 
    requests = []
    n = len(ips)
    for item in ips:
        q.put(item)

    gevent.joinall([
    gevent.spawn(worker,port),
    gevent.spawn(worker,port)
    ])


def main():
    try:
        opts ,args = getopt.getopt(sys.argv[1:],'i:o:t:p:n:h',['in','out','timeout','parallels','hostname'])
    except getopt.GetoptError as err:
        usage()
        print(err)
        sys.exit('parameter error')
    global rin ,output ,timeout ,parallels ,ips ,mod ,hostname
    for o, a in opts:
        if o in ('-i','--in'):
            rin = a
        elif o in ('-o','--out'):
            output = a
        elif o in ('-h','--help'):
            usage()
            sys.exit()
        elif o in ('-t','--timeout'):
            timeout = int(a)
        elif o in ('-n' , '--hostname'):
            hostname = a

    file_obj = open(rin)
    try:
        txt = file_obj.read()
        ips = gen_ip(txt)
        print('读入了'+ str(len(ips)) +'个ip')
        caller(ips, port)
    finally:
        file_obj.close()

if __name__ == '__main__':
    main()



