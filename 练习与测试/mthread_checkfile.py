# coding=utf-8

"""
==============================================================
# @Time    : 2019/9/20 19:52
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : mthread_checkfile
# @Software: PyCharm
==============================================================
"""
import os
from threading import Thread
from datetime import datetime
from queue import  Queue

depth = 9
path = r'c:/windows/'
a  = ['c:/windows/appcompat/', 'c:/windows/apppatch/', 'C:/Windows/Help/']

class Producer(Thread):
    def __init__(self, filepath, depth, res_queue):
        super().__init__()
        self.filepath = filepath
        self.depth = depth
        self.res_queue = res_queue

    def run(self):
        res = self.get_rest(self.filepath, self.depth)
        self.res_queue.put(res)

    def get_rest(self, filepath, depth, child_list = []):

        depth -= 1
        child_list.append(filepath)
        for file in os.listdir(filepath):
            childpath = filepath + file + "/"
            # 如果超出最大深度，不再往下遍历
            if depth <= 0:
                continue
            # 如果有子目录则递归遍历子目录
            if os.path.isdir(childpath):
                self.get_rest(childpath, depth)
        # 返回所有子目录列表
        return child_list

class Consumer(Thread):
    def __init__(self,  res_queue):
        super().__init__()
        self.res_queue = res_queue

    def run(self):
        while True:
            print(self.res_queue.get())
            if self.res_queue.empty():
                break

if __name__ == '__main__':
    res_queue = Queue()
    for i in a:
        t1 = Producer(i, depth, res_queue)
        t1.start()
        # print(t1.get_rest(i, depth))

    t2 = Consumer(res_queue)
    t2.start()