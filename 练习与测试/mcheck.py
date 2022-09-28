#coding=utf-8

"""
=============================================================
#   project: python
#      file: mcheck.py
#    author: mianfeng.yang
#      date: 2019-09-20 17:17:15
=============================================================
"""
import os
from datetime import datetime
from threading import Thread
from queue import Queue
from openpyxl import Workbook

bpath1 = r'//192.168.1.11/pubin/'
bpath10 = r'//192.168.10.11/devin/'
depth = 4

checklist10 = ['huoguangxin', '吉利', 'libin', 'liujunwei', 'yuanjun', '张建红', 'zhanglili', '张永辉', 'hw.liu']
checklist1 = ["huoguangxin", 'jianhong.zhang', 'jili', 'libin',
              'liujunwei', 'yuanjun', 'zhangyonghui', '杨绵峰', 'zhanglili', 'hw.liu', '汤宝云', '严建锋', '惠梦月']
userlist = ['//192.168.1.11/pubin/huoguangxin/', '//192.168.1.11/pubin/jianhong.zhang/', '//192.168.1.11/pubin/jili/', '//192.168.1.11/pubin/libin/', '//192.168.1.11/pubin/liujunwei/', '//192.168.1.11/pubin/yuanjun/', '//192.168.1.11/pubin/zhangyonghui/', '//192.168.1.11/pubin/杨绵峰/', '//192.168.1.11/pubin/zhanglili/', '//192.168.1.11/pubin/hw.liu/', '//192.168.1.11/pubin/汤宝云/', '//192.168.1.11/pubin/严建锋/', '//192.168.1.11/pubin/惠梦月/', '//192.168.10.11/devin/huoguangxin/', '//192.168.10.11/devin/吉利/', '//192.168.10.11/devin/libin/', '//192.168.10.11/devin/liujunwei/', '//192.168.10.11/devin/yuanjun/', '//192.168.10.11/devin/张建红/', '//192.168.10.11/devin/zhanglili/', '//192.168.10.11/devin/张永辉/', '//192.168.10.11/devin/hw.liu/']

# for i in checklist1:
#     userlist.append(bpath1 + i + '/')
# for j in checklist10:
#     userlist.append(bpath10 + j + "/")
# print(userlist)

class Producer(Thread):
    def __init__(self, filepath, depth, res_queue):
        super().__init__()
        self.res_queue = res_queue
        self.filepath = filepath
        self.depth = depth

    def run(self):
        res = self.GetResult(self.filepath)
        res_queue.put(res)

    def GetResult(self, filepath):
        userdir_dirtime = []
        res = self.find_child_dir(self.filepath, self.depth)
        for i in res:
            userdir_dirtime.append(i)
        # print(userdir_dirtime)
        newestdir = sorted(userdir_dirtime, key=lambda s: s[1])[-1]
        userdir_ndir_mtime_user = (
        self.filepath, newestdir[0], datetime.fromtimestamp(newestdir[1]).strftime('%Y-%m-%d %H:%M'), self.GetUser(self.filepath))
        return userdir_ndir_mtime_user

    def find_child_dir(self, filepath, depth):
        '''
        递归遍历当前目录，返回当前目录下所有子目录列表
        参数 filepath为传入路径参数，child_list列表用于保存传入路径中每个子目录
        :param filepath:        传递一个路径
        :param depth            传递一个最大遍历目录的深度
        :yield: 利用生成器函数返回子目录列表
        '''
        self.depth -= 1
        yield self.filepath, os.stat(self.filepath).st_mtime
        for file in os.listdir(self.filepath):
            childpath = self.filepath + file + "/"
            # print(childpath)
            # 如果超出最大深度，不再往下遍历
            if self.depth <= 0:
                continue
            # 如果有子目录则递归遍历子目录
            if os.path.isdir(childpath):
                yield from self.find_child_dir(childpath, self.depth)


    def GetUser(self, filepath):
        """
        根据用户目录名返回中文用户名
        :return: user
        """
        user = ''
        if ("huoguangxin" in self.filepath) or ("霍广新" in self.filepath):
            user = "霍广新"
        if ("hw.liu" in self.filepath) or ("刘宏伟" in self.filepath):
            user = "刘宏伟"
        if ("jianhong.zhang" in self.filepath) or ("张建红" in self.filepath):
            user = "张建红"
        if ("jili" in self.filepath) or ("吉利" in self.filepath):
            user = "吉利"
        if ("libin" in self.filepath) or ("李宾" in self.filepath):
            user = "李宾"
        if ("liujunwei" in self.filepath) or ("刘军伟" in self.filepath):
            user = "刘军伟"
        if ("yuanjun" in self.filepath) or ("袁君" in self.filepath):
            user = "袁君"
        if ("zhangyonghui" in self.filepath) or ("张永辉" in self.filepath):
            user = "张永辉"
        if ("zhanglili" in self.filepath) or ("张丽丽" in self.filepath):
            user = "张丽丽"
        if ("杨绵峰" in self.filepath):
            user = "杨绵峰"
        if ("汤宝云" in self.filepath):
            user = "汤宝云"
        if ("惠梦月" in self.filepath):
            user = "惠梦月"
        if ("严建锋" in self.filepath):
            user = "严建锋"
        return user


class Consumer(Thread):
    def __init__(self, res_queue):
        super().__init__()
        self.res_queue = res_queue

    def run(self):
        while True:

            print(self.res_queue.get())
            # if self.res_queue.empty():
            #     break



if __name__ == '__main__':
    start_time = datetime.now()
    print("开始时间：{}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    res_queue = Queue()
    for i in userlist:
        t = Producer(i, 4, res_queue)
        t.start()
        # t.join()
    myconsumer = Consumer(res_queue)
    myconsumer.start()
    # myconsumer.join()
    # print(res_queue.get())
    # print(res_queue.get())
    # print(res_queue.get())
    # print(res_queue.get())
    # print(res_queue.get())
    # pass

    end_time = datetime.now()
    print("结束时间：{}\n总共耗时：{}".format(end_time.strftime("%Y-%m-%d %H:%M:%S"), end_time - start_time))