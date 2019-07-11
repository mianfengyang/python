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


bpath1 = r'//192.168.1.11/pubin/'
bpath10 = r'//192.168.10.11/devin/'
depth = 5
user = ""
checklist10 = ['huoguangxin', '吉利', 'libin', 'liujunwei', 'yuanjun', '张建红', 'zhanglili', '张永辉', 'hw.liu']
checklist1 = ["huoguangxin", 'jianhong.zhang', 'jili', 'libin',
              'liujunwei', 'yuanjun', 'zhangyonghui', '杨绵峰', 'zhanglili', 'hw.liu', '汤宝云']


userdir_queue = Queue(100)


userpaths = []

for i in checklist1:
    userpaths.append(bpath1 + i + '/')
# for i in checklist10:
#     userpaths.append(bpath10 + i + '/')




def FindChildDir(path, depth, clist):
    depth -= 1
    #clist.append(path)
    for i in os.listdir(path):
        if depth <= 0:
            continue
        childpath = path + i + '/'
        clist.append(childpath)
        if os.path.isdir(childpath):
            FindChildDir(childpath, depth, clist)
    return clist


clist = []
def getuserdir():
    for path in userpaths:
        clist.clear()
        userdir = FindChildDir(path, depth, clist)
        userdir_queue.put(userdir)


def main():
    start_time = datetime.datetime.now()
    print("开始时间：{}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))


    for x in range(5):
        t = threading.Thread(target=getuserdir)
        t.start()

    while True:
        if userdir_queue.empty():
            break
        print(userdir_queue.get())
    end_time = datetime.datetime.now()
    print("结束时间：{}\n总共耗时：{}".format(end_time.strftime("%Y-%m-%d %H:%M:%S"), end_time - start_time))

if __name__ == '__main__':
    main()