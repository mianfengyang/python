#coding=utf-8

"""
=============================================================
#   project: python
#      file: py05-__del__().py
#    author: mianfeng.yang
#      date: 2019-09-04 13:39:54
=============================================================

当删除对象时，python解释器也会默认调用__del__()方法
"""


def main():
    """函数说明文档 写在这里"""
    class Washer():
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def __del__(self):
            print(f"{self}对象已经被删除")


    haier1 = Washer(100, 200)
    print(haier1)

if __name__ == '__main__':
    main()