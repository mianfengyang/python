# coding=utf-8

"""
==============================================================
# @Time    : 2019/9/20 19:52
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : mthread_checkfile
# @Software: PyCharm
==============================================================
('c:/windows/appcompat/appraiser/AltData/', 1569149779.8340926)
('c:/windows/apppatch/zh-CN/', 1563119805.6274726)
('C:/Windows/Help/mui/', 1537027433.8218148)



"""
import os
from threading import Thread
from datetime import datetime
from queue import  Queue

depth = 4
path = r'c:/windows/'
a  = ['c:/windows/appcompat/', 'c:/windows/apppatch/', 'C:/Windows/Help/']

class Producer(Thread):
    def __init__(self, filepath, depth, res_queue):
        super().__init__()
        self.filepath = filepath
        self.depth = depth
        self.res_queue = res_queue
        self.child_list = set()
        self.result = []

    def run(self):
        # 1. 获取用户根目录
        udir = self.get_user_path(self.filepath)
        self.result.append(udir)

        # 2. 找到用户目录里最新的mtime目录及mtime
        ndir_mtime = self.get_child_dir_mtime(self.filepath, self.depth)
        ndir, umtime = sorted(ndir_mtime, key=lambda s: s[1])[-1]
        self.result.append(ndir)
        self.result.append(datetime.fromtimestamp(umtime).strftime('%Y-%m-%d %H:%M'))

        # 3. 返回用户目录的使用者
        user = self.get_user(self.filepath)
        self.result.append(user)

        # 4. 将完整列表放进队列
        res_queue.put(self.result)


    def get_user_path(self,filepath):
        return filepath

    def get_child_dir_mtime(self, filepath, depth):

        depth -= 1
        self.child_list.add((filepath, os.stat(filepath).st_mtime))
        for file in os.listdir(filepath):
            childpath = filepath + file + "/"
            # 如果超出最大深度，不再往下遍历
            if depth <= 0:
                continue
            # 如果有子目录则递归遍历子目录child_list
            if os.path.isdir(childpath):
                self.get_child_dir_mtime(childpath, depth)
        # 返回所有子目录集合，利用了集合自动去重功能
        return self.child_list

    def get_user(self,filepath):
        if "appcompat" in filepath:
            return "appcompat"
        if "apppatch" in filepath:
            return "apppatch"
        if "Help" in filepath:
            return "Help"

class WriteToExcel:
    def __init__(self,  res_queue):
        self.res_queue = res_queue

    def get_udir_umtime(self):

        return self.res_queue.get()

if __name__ == '__main__':
    res_queue = Queue()
    for i in a:
        t1 = Producer(i, depth, res_queue)
        t1.start()
        t1.join()


    get_res1 = WriteToExcel(res_queue)

    while True:

        print(get_res1.get_udir_umtime())

        # result.append(datetime.fromtimestamp(a[1]).strftime("%Y-%m-%d %H:%M:%S"))
        # # print(a,datetime.fromtimestamp(b).strftime("%Y-%m-%d %H:%M:%S"))
        if res_queue.empty():
            break
    # print(result)

