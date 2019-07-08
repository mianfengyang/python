#coding=utf-8

"""
=============================================================
project: python
   file: 01-线程加锁LOCK.py
 author: mianfeng.yang
   date: 2019-07-08 13:13:04
=============================================================
"""

import threading

gNum = 0
gNumLock = threading.Lock()

def add_value():
    global gNum
    gNumLock.acquire()
    for i in range(1000000):
        gNum += 1
    gNumLock.release()
    print(gNum)

def main():
    for i in range(6):
        t1 = threading.Thread(target=add_value)
        t1.start()

if __name__ == '__main__':
    main()

