#coding=utf-8

"""
=============================================================
project: python
   file: 03-线程加锁condition版.py
 author: mianfeng.yang
   date: 2019-07-08 16:27:13
=============================================================
"""

import threading
import random

gMoney = 0
gCondition = threading.Condition()
gTotoalTimes = 20
gTimes = 0

class Producer(threading.Thread):
    def run(self):
        global gMoney
        global gTimes
        while True:
            money = random.randint(100, 1000)
            gCondition.acquire()
            if gTimes >= gTotoalTimes:
                gCondition.release()
                break
            gMoney += money
            print("%s生产了 %d 元钱，总额为 %d 元钱" % (threading.current_thread(), money, gMoney))
            gTimes += 1
            gCondition.notify_all()
            gCondition.release()

class Consumer(threading.Thread):
    def run(self):
        global gMoney
        while True:
            money = random.randint(100, 1000)
            gCondition.acquire()
            while gMoney < money:
                if gTimes >= gTotoalTimes:
                    gCondition.release()
                    return
                print("%s 当前余额 %d 元钱 准备消费 %d 元钱 余额不足……" % (threading.current_thread(), gMoney, money,))
                gCondition.wait()
            gMoney -= money
            print('%s消费了 %d 元钱，余额 %d 元钱' %(threading.current_thread(), money, gMoney))
            gCondition.release()


def main():
    for i in range(3):
        t1 = Producer(name="生产者%d" % i)
        t2 = Consumer(name="消费者%d" % i)
        t1.start()
        t2.start()


if __name__ == '__main__':
    main()