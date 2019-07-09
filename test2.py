
#coding:utf-8
import threading
import time
import random
import queue

g_money = 0
q = queue.Queue()
glogk = threading.Lock()
class producer(threading.Thread):

    def run(self):
        global g_money
        for i in range(5):
            money = random.randint(100, 500)
            g_money += money
            q.put(g_money)
            print("%s正在生产钱 %d 元,总共有 %d 元钱" % (threading.current_thread(), money, g_money))
            time.sleep(0.2)

class xiaofeize(threading.Thread):

    def run(self):
        global g_money
        for i in range(5):
            q.get(g_money)
            xmoney = random.randint(100, 500)
            print("%s共有 %d 元钱，正在消费 %d 元钱，剩余 %d 元钱" % (threading.current_thread(), g_money, xmoney, g_money - xmoney))
            g_money -= xmoney
            if g_money <= 0 or g_money < xmoney:
                print("共有 %d 元钱，正在消费 %d 元钱 余额不足……" % (g_money, xmoney))
                

            time.sleep(0.2)

def main():
    p1 = producer()
    # p1.func1()
    p1.start()
    p2 = xiaofeize()
    p2.start()


if __name__ == "__main__":
    main()