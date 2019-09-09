#coding=utf-8

"""
=============================================================
#   project: python
#      file: py07-单继承.py
#    author: mianfeng.yang
#      date: 2019-09-04 17:35:04
=============================================================

1. 单个子类继承单个父类，叫单继承
"""


def main():
    """函数说明文档 写在这里"""
    class Master(object):
        def __init__(self):
            self.kongfu = '[古法制作煎饼果子配方]'

        def make_cake(self):
            print(f'运用 {self.kongfu} 制作煎饼果子')

    class Prentice(Master):
        pass

    daqiu = Prentice()
    print(daqiu.kongfu)
    daqiu.make_cake()

if __name__ == '__main__':
    main()