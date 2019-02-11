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
import os

basep = r'//192.168.1.11/pubin/'
checklist = ['huoguangxin', 'hw.liu', 'jianhong.zhang', 'jili', 'libin', 'liujunwei', 'yuanjun', 'zhanglili', 'zhangyonghui', '杨绵峰']
paths = []
for i in checklist:
    path = basep + i +'/'
    paths.append(path)
print(paths)