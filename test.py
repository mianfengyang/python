# coding=utf-8

"""
==============================================================
# @Time    : 2019/2/10 0010
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : test
# @Software: PyCharm
==============================================================
"""
import threading
import time

def sing():
    for i in range(5):
        print("唱歌……%d" % i)
        time.sleep(0.2)

def dance():
    for i in range(5):
        print("跳舞……%d" % i)
        time.sleep(0.2)


def main():

    t1 = threading.Thread(target=sing)
    t2 = threading.Thread(target=dance)
    t1.start()
    t2.start()

if __name__ == '__main__':
    main()
