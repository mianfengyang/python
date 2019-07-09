#coding=utf-8

"""
=============================================================
project: python
   file: 02-线程加锁LOCK生产者消费者模式.py
 author: mianfeng.yang
   date: 2019-07-08 14:30:47
=============================================================
"""

import threading
import random


gMoney = 0
gLock = threading.Lock()
gTimes = 0
gTotoalTimes = 10

class Producer(threading.Thread):
    def run(self):
        global gMoney
        global gTimes
        while True:
            money = random.randint(100,1000)
            gLock.acquire()
            if gTimes >= gTotoalTimes:
                gLock.release()
                break
            gMoney += money
            print("%s 生产了 %d 元钱 总额 %d 元钱" % (threading.current_thread(), money, gMoney))
            gTimes += 1
            gLock.release()


class Consumer(threading.Thread):


    def run(self):
        global gMoney
        global gTimes
        while True:
            money = random.randint(100,1000)
            gLock.acquire()
            if gMoney > money:
                gMoney -= money
                print("%s消费了 %d 元钱 剩余 %d 元钱" % (threading.current_thread(), money, gMoney))
            else:
                # if gTimes >= gTotoalTimes:
                #     gLock.release()
                #     break
                print("%s共有 %d 元钱 准备消费 %d 元钱 余额不足……" % (threading.current_thread(), gMoney, money))
                gLock.release()
                break
            gLock.release()


def main():

    for x in range(3):
        t1 = Producer(name="生产者 %d" % x)
        t2 = Consumer(name="消费者 %d" % x)
        t1.start()
        t2.start()


if __name__ == '__main__':
    main()