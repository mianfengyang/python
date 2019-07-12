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
bpathtest = r'D:/soft/'
depth = 5
user = ""
checklist10 = ['huoguangxin', '吉利', 'libin', 'liujunwei', 'yuanjun', '张建红', 'zhanglili', '张永辉', 'hw.liu']
checklist1 = ["huoguangxin", 'jianhong.zhang', 'jili', 'libin',
              'liujunwei', 'yuanjun', 'zhangyonghui', '杨绵峰', 'zhanglili', 'hw.liu', '汤宝云']
testlist = ['google', 'Ghelper_1.4.6.beta', 'X220_Drivers', 'Xmanager Enterprise 5 Build 0987', 'xmind-8-update7-windows']

userpath_queue = Queue(100)
userdir_queue = Queue(100)
userdir = []
userpaths = []

for i in checklist1:
    userpaths.append(bpath1 + i + '/')
# for i in checklist10:
#     userpaths.append(bpath10 + i + '/')

class Producer(threading.Thread):
    def run(self):

        while True:

            userpath = userpath_queue.get()
            ud = self.FindChildDir(userpath, depth, userdir = [])
            print(ud)
            userdir_queue.put(ud)
            if ud == None and userpath_queue.empty():
                break



    def FindChildDir(self, path, depth, userdir):
        depth -= 1
        for i in os.listdir(path):
            if depth <= 0:
                continue
            if os.path.isfile(path + i):
                childpath = path + i
                userdir.append(childpath)

            if os.path.isdir(path + i):
                childpath = path + i + '/'
                userdir.append(childpath)
                self.FindChildDir(childpath, depth, userdir)
        return userdir


class Consumer(threading.Thread):
    def run(self):

        while True:
            if userpath_queue.empty() and userdir_queue.empty():
                break
            resultuserdir = userdir_queue.get()
            print(threading.current_thread().name, resultuserdir)


def main():
    print("%s主线程开始……" % threading.current_thread().name)
    start_time = datetime.datetime.now()
    print("开始时间：{}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    print()

    for path in userpaths:
        userpath_queue.put(path)

    thread_list = []
    for x in range(3):
        t1 = Producer()
        thread_list.append(t1)
        t2 = Consumer()
        thread_list.append(t2)

    for t in thread_list:
        t.start()
        t.join()


    end_time = datetime.datetime.now()
    print()
    print("结束时间：{}\n总共耗时：{}".format(end_time.strftime("%Y-%m-%d %H:%M:%S"), end_time - start_time))
    print("%s主线程结束……" % threading.current_thread().name)

if __name__ == '__main__':
    main()