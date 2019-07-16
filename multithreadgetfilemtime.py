#coding=utf-8

"""
=============================================================
#   project: python
#      file: multithreadgetfilemtime.py
#    author: mianfeng.yang
#      date: 2019-07-09 15:35:06
=============================================================
"""
import threading
import datetime
import os
from queue import Queue
import collections


bpath1 = r'//192.168.1.11/pubin/'
bpath10 = r'//192.168.10.11/devin/'
bpathtest = r'D:/soft/'
depth = 5
user = ""
checklist10 = ['huoguangxin', '吉利', 'libin', 'liujunwei', 'yuanjun', '张建红', 'zhanglili', '张永辉', 'hw.liu']
checklist1 = ["huoguangxin", 'jianhong.zhang', 'jili', 'libin',
              'liujunwei', 'yuanjun', 'zhangyonghui', '杨绵峰', 'zhanglili', 'hw.liu', '汤宝云']
testlist = ['google', 'Ghelper_1.4.6.beta', 'X220_Drivers', 'Xmanager Enterprise 5 Build 0987', 'xmind-8-update7-windows']

userpath_queue = Queue(100)
userdir_queue = Queue(100)
userdir = {}
userpaths = []

for i in checklist1:
    userpaths.append(bpath1 + i + '/')
# for i in checklist10:
#     userpaths.append(bpath10 + i + '/')


def FindChildDir(path, depth, userdir):
    depth -= 1
    for i in os.listdir(path):
        if depth <= 0:
            continue
        if os.path.isfile(path + i):
            childpath = path + i
            childpath_mtime = datetime.datetime.fromtimestamp(os.stat(childpath).st_mtime).strftime('%Y-%m-%d %H:%M')
            userdir[childpath] = childpath_mtime

        if os.path.isdir(path + i):
            childpath = path + i + '/'
            childpath_mtime = datetime.datetime.fromtimestamp(os.stat(childpath).st_mtime).strftime('%Y-%m-%d %H:%M')
            userdir[childpath] = childpath_mtime
            FindChildDir(childpath, depth, userdir)
    res = sorted(userdir.items(), key=lambda d: d[1])[-1]
    return res

def GetLatestFile(path):
    latestfile = FindChildDir(path,depth,userdir={})
    print(latestfile)

def main():
    print("%s主线程开始……" % threading.current_thread().name)
    start_time = datetime.datetime.now()
    print("开始时间：{}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    print()

    for path in userpaths:
        t = threading.Thread(target=GetLatestFile,args=(path,))
        t.start()

    end_time = datetime.datetime.now()
    print()
    print("结束时间：{}\n总共耗时：{}".format(end_time.strftime("%Y-%m-%d %H:%M:%S"), end_time - start_time))
    print("%s主线程结束……" % threading.current_thread().name)

if __name__ == '__main__':
    main()