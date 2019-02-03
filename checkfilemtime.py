# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 19:57
# @Author  : Mifyang
# @Email   : mifyang@126.com
# @File    : 指定层级递归.py
# @Software: PyCharm

import os
import datetime
path = "D:/Users/mianfeng.yang.PUB/Documents/工作文件/"
print(os.listdir(path))
level = 1
def PrintDir(filepath,path_dep):
    f = open("filecheck.txt",'a+',)
    for file in os.listdir(filepath):
        child_dir = filepath + file + "/"
        file_mtime = os.stat(filepath + file).st_mtime
        f_mtime = datetime.datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d')
        if os.path.isfile(filepath + file):
            print("%s%s 文件 \n最后修改时间是: %s" % (filepath, file, f_mtime))
            f.writelines("%s%s 文件 \n最后修改时间是: %s\n" % (filepath, file, f_mtime))
        if os.path.isdir(child_dir):
            print("%s 文件夹 \n最后修改时间是: %s" % (child_dir, f_mtime))
            f.write("%s 文件夹 \n最后修改时间是: %s\n" % (child_dir, f_mtime))
            PrintDir(child_dir)

    f.close()
PrintDir(path)