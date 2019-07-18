#coding=utf-8

"""
=============================================================
#   project: python
#      file: multithreadgetfilemtime.py
#    author: mianfeng.yang
#      date: 2019-07-09 15:35:06
=============================================================
"""
from multiprocessing import Process
import datetime
import os
from queue import Queue
import collections
import time

bpath1 = r'//192.168.1.11/pubin/'
bpath10 = r'//192.168.10.11/devin/'
bpathtest = r'D:/soft/'
depth = 4
user = ""
checklist10 = ['huoguangxin', '吉利', 'libin', 'liujunwei', 'yuanjun', '张建红', 'zhanglili', '张永辉', 'hw.liu']
checklist1 = ["huoguangxin", 'jianhong.zhang', 'jili', 'libin',
              'liujunwei', 'yuanjun', 'zhangyonghui', '杨绵峰', 'zhanglili', 'hw.liu', '汤宝云']
testlist = ['google', 'Ghelper_1.4.6.beta', 'X220_Drivers', 'Xmanager Enterprise 5 Build 0987', 'xmind-8-update7-windows']

userdir = {}
userpaths = []

for i in checklist1:
    userpaths.append(bpath1 + i + '/')
# for i in checklist10:
#     userpaths.append(bpath10 + i + '/')


def FindChildDir(path, depth, userdir={}):
    depth -= 1
    for i in os.listdir(path):
        if depth <= 0:
            continue
        if os.path.isfile(path + i):
            childpath = path + i
            childpath_mtime =os.stat(childpath).st_mtime
            s_time = "2019-07-01"
            s_time = time.mktime(time.strptime(s_time,"%Y-%m-%d"))
            if childpath_mtime.__ge__(s_time):
                userdir[childpath] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(childpath_mtime))
            # else:
            #     print("未备份")
        else:
            childpath = path + i + '/'
            FindChildDir(childpath, depth, userdir)
    return userdir

def GetLatestFile(path):

    latestfile = FindChildDir(path,depth,userdir={})
    if  latestfile:
        res = sorted(latestfile.items(),key=lambda s: s[1])[-1]
        print(res)

def main():
    print("%s主线程开始……" % Process.name)
    start_time = datetime.datetime.now()
    print("开始时间：{}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))
    print()


    pro_list = []
    for x in userpaths:
        t = Process(target=GetLatestFile,args=(x,))
        pro_list.append(t)

    for x in pro_list:
        x.start()

    for x in pro_list:
        x.join()


    end_time = datetime.datetime.now()
    print()
    print("结束时间：{}\n总共耗时：{}".format(end_time.strftime("%Y-%m-%d %H:%M:%S"), end_time - start_time))
    print("%s主线程结束……" % Process.name)

    # for path in userpaths:
    #     GetLatestFile(path)

if __name__ == '__main__':

    main()