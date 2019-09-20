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
        self.child_list = set()

    def run(self):
        res = self.get_child_dir(self.filepath, self.depth)
        # print(res)

        res = sorted(res, key=lambda s: s[1])[-1]
        res_queue.put(res)


    def get_child_dir(self, filepath, depth):
        # child_list.clear()
        depth -= 1

        self.child_list.add((filepath, os.stat(filepath).st_mtime))
        for file in os.listdir(filepath):
            childpath = filepath + file + "/"
            # 如果超出最大深度，不再往下遍历
            if depth <= 0:
                continue
            # 如果有子目录则递归遍历子目录child_list
            if os.path.isdir(childpath):
                self.get_child_dir(childpath, depth)
        # 返回所有子目录列表
        return self.child_list

    def get_dir_mtime(self, filepath):
        dir_mtime = os.stat(filepath).st_mtime
        return dir_mtime

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
        t1.join()
        # print(t1.get_rest(i, depth))

    t2 = Consumer(res_queue)
    t2.start()