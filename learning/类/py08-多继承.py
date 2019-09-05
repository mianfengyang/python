#coding=utf-8

"""
=============================================================
#   project: python
#      file: py08-多继承.py
#    author: mianfeng.yang
#      date: 2019-09-05 11:57:54
=============================================================

1. 所谓多继承 就是一个类同时继承了多个父类
2. 语法：class 类名(父类1，父类2)
3. 注意：当一个类有多个父类的时候，默认使用第一个父类 的同名的属性和方法

"""


def main():
    """多继承"""
    class Master(object):
        def __init__(self):
            self.kongfu = '[古法煎饼果子配方]'

        def make_cake(self):
            print(f'运用{self.kongfu} 制作煎饼果子')

    class School(object):
        def __init__(self):
            self.kongfu = '[黑马煎饼果子配方]'

        def make_cake(self):
            print(f'运用 {self.kongfu} 制作煎饼果子')

    class Prentice(School, Master):
        pass

    daqiu = Prentice()
    print(daqiu.kongfu)
    daqiu.make_cake()


if __name__ == '__main__':
    main()