#coding=utf-8

"""
=============================================================
project: python
   file: 04-queue学习.py
 author: mianfeng.yang
   date: 2019-07-09 15:22:41
=============================================================
"""


#coding:utf-8

import queue
list1 = ['aa', 'bb', 'cc', 'dd']
list2 = ['11', '22', '33', '44']
q = queue.Queue()

def add_value():
    q.put(list1)
    q.put(list2)

def get_value():
    while not q.empty():
        print(q.get())


def main():
    add_value()
    get_value()

if __name__ == "__main__":
    main()