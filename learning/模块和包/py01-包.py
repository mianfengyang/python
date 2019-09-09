#coding=utf-8

"""
=============================================================
#   project: python
#      file: py01-包.py
#    author: mianfeng.yang
#      date: 2019-09-09 10:13:07
=============================================================

1. 包将有联系的模块组织在一起，即放到同一个文件夹下，并且在这个文件夹创建一个名字为__init__.py文件，那么这个文件夹就称之为包。
2. 导入包
    方法1：import 包名.模块名
          包名.模块名.目标
    方法2：from 包名 import *
          模块名.目标
    注意：使用方法2时，必须在__ini__.py文件中添加__all__ = [],控制允许导入的模块列表
3.
"""
import mypackage.mymodule1

mypackage.mymodule1.info_print1()

from mypackage import *
mymodule2.info_print()
mymodule1.info_print1()


def main():
    """函数说明文档 写在这里"""
    pass


if __name__ == '__main__':
    main()