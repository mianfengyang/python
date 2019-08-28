#coding=utf-8

"""
=============================================================
#   project: python
#      file: 07-列表时间复杂度.py
#    author: mianfeng.yang
#      date: 2019-07-18 15:02:23
=============================================================
"""

import timeit


def t1():
    li = []
    for i in range(10000):
        li.append(i)


def t2():
    li = []
    for i in range(10000):
        li = li + [i]


def t3():
    li = [i for i in range(10000) ]


def t4():
    li = []
    for i in range(10000):
        li.extend([i])


def t5():
    li = list(range(10000))


def main():
    time1 = timeit.Timer("t1()","from __main__ import t1")
    print("append %d" % time1.timeit(1000))

    time3 = timeit.Timer("t3()", "from __main__ import t3")
    print("i for i in  %d" % time3.timeit(1000))
    time4 = timeit.Timer("t4()", "from __main__ import t4")
    print("extend %d" % time4.timeit(1000))
    time5 = timeit.Timer("t5()", "from __main__ import t5")
    print("list %d" % time5.timeit(1000))
    time2 = timeit.Timer("t2()", "from __main__ import t2")
    print("+ %d" % time2.timeit(1000))

if __name__ == '__main__':
    main()