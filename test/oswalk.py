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
import multiprocessing
import time
import os
import datetime


bpath1 = r'//192.168.1.11/pubin/'
bpath10 = r'//192.168.10.11/devin/'
bpathtest = r'D:/soft/'
depth = 5
user = ""
checklist10 = ['huoguangxin', '吉利', 'libin', 'liujunwei', 'yuanjun', '张建红', 'zhanglili', '张永辉', 'hw.liu']
checklist1 = ["huoguangxin", 'jianhong.zhang', 'jili', 'libin',
              'liujunwei', 'yuanjun', 'zhangyonghui', '杨绵峰', 'zhanglili', 'hw.liu', '汤宝云']
testlist = ['google', 'Ghelper_1.4.6.beta', 'X220_Drivers', 'Xmanager Enterprise 5 Build 0987', 'xmind-8-update7-windows']

userdir = {}
userpaths = []

for i in checklist1:
    userpaths.append(bpath1 + i + '/')
# for i in checklist10:
#     userpaths.append(bpath10 + i + '/')

def iter_files(rootDir):
    #遍历根目录
    for root,dirs,files in os.walk(rootDir):
        dirdict = {}
        for file in files:
            childpath = root + dirs
            childpath_mtime = datetime.datetime.fromtimestamp(os.stat(file).st_mtime).strftime('%Y-%m-%d %H:%M')
            dirdict[file] = childpath_mtime
        print(dirdict)

def main():

    for path in userpaths:
        s = iter_files(path)
        for i in s:
            print(i)


if __name__ == '__main__':
    main()
