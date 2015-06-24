#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import sys,re
from Queue import Queue
from threading import Thread

'''
    批量扫描mongodb未授权验证的数据库，并列出数据库名字
    需要安装的模块有pymongo 
    方式easy_install pymongo
'''

result = []

'''
    线程函数
    通过Queue获取ip地址.ip地址列表通过读取文件获取
'''
def loop():
    while True:
        ip = q.get()
        try:
            #链接mongodb 服务器
            client = MongoClient(ip,27017,connectTimeoutMS=1000,socketTimeoutMS=1000,waitQueueTimeoutMS=1000)
            #serverInfo = client.server_info()
            try:
                #获取mongodb服务器信息
                serverInfo = client.server_info()
                print "[-] " + ip
                for keys in serverInfo:
                    if(keys=="sysInfo"):
                        print "[-] "+(keys)+":"+str(serverInfo[keys])
                try:
                    #获取mongodb服务器的数据名，如果成功获取，则表明不用验证即可查看
                    dbList = client.database_names()
                    print "[-] " + ip
                    for i in dbList:
                        print "[-] "+i 
                    print "\n"
                    #保存结果
                    result.append(ip)
                except:
                    pass
            except:
                pass
            client.close()
            
        except KeyboardInterrupt:
            print "[-] Interrupted by user. Exiting..."
            exit()
        except:
            pass
    q.task_done()


if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print "[-] Usage: %s NumberOfThreads IpListFile"%(sys.argv[0])
        exit()
    
    threadNum = int(sys.argv[1])   #线程数
    fp = sys.argv[2]               #ip地址列表文件名 
    isExit = False
    q=Queue()
    #创建线程
    for i in range(threadNum):
        t = Thread(target=loop)
        #t.daemon=True
        t.setDaemon(True)
        t.start()
    #载入队列
    with open(fp) as f:
        if (isExit!=False):
            sys.exit()
        for line in f:
            pw = line.strip()
            q.put(pw)
    f.close()
    q.join()