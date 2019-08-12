# coding=utf-8

"""
==============================================================
# @Time    : 2019/7/8 19:41
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : 04-Queue队列
# @Software: PyCharm
==============================================================
"""

import queue
import threading
import time


def set_value(q):
    index = 0
    while True:
        q.put(index)
        index += 1
        time.sleep(2)


def get_value(q):
    while True:
        print(q.get())


def main():
    q = queue.Queue(4)
    t1 = threading.Thread(target=set_value, args=[q])
    t2 = threading.Thread(target=get_value, args=[q])
    t1.start()
    t2.start()

if __name__ == '__main__':
    main()