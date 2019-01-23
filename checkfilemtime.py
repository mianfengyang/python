# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 19:57
# @Author  : Mifyang
# @Email   : mifyang@126.com
# @File    : 指定层级递归.py
# @Software: PyCharm

import os
import datetime
path = "e:/电子书/"
print(os.listdir(path))
level = 1
def PrintDir(filepath,level):
    for p_file_or_dir in os.listdir(filepath):
        child_dir = filepath + p_file_or_dir + "/"
        file_mtime = os.stat(filepath + p_file_or_dir).st_mtime
        f_mtime = datetime.datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d')
        if os.path.isfile(filepath + p_file_or_dir):
            print("%s 文件 最后修改时间是: %s" % (p_file_or_dir, f_mtime))
        if os.path.isdir(child_dir):
            level += 1
            print("%s 文件夹 最后修改时间是: %s" % (child_dir, f_mtime))
            if level <= 4:
                PrintDir(child_dir,level)
PrintDir(path,level)