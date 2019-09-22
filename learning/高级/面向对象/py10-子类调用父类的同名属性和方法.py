#coding=utf-8

"""
=============================================================
#   project: python
#      file: py10-子类调用父类的同名属性和方法.py
#    author: mianfeng.yang
#      date: 2019-09-05 12:20:08
=============================================================
"""


def main():
    """子类调用父类同名属性和方法"""
    class Master(object):
        def __init__(self):
            self.kongfu = '[古法煎饼果子配方]'

        def make_cake(self):
            print(f'运用 {self.kongfu} 制作煎饼果子')

    class School(object):
        def __init__(self):
            self.kongfu = '[黑马煎饼果子配方]'

        def make_cake(self):
            print(f'运用 {self.kongfu} 制作煎饼果子')

    class Prentice(School, Master):
        def __init__(self):
            self.kongfu = '[独创煎饼果子配方]'

        def make_cake(self):
            # 加自已的初始化原因: 如果不加，则会自动调用上一次调用过的父类同名属性
            self.__init__()
            print(f'运用 {self.kongfu} 制作煎饼果子')

        def Master_make_cake(self):
            Master.__init__(self)
            Master.make_cake(self)

        def School_make_cake(self):
            School.__init__(self)
            School.make_cake(self)

    daqiu = Prentice()
    print(daqiu.kongfu)
    daqiu.make_cake()
    daqiu.Master_make_cake()
    daqiu.School_make_cake()
    daqiu.make_cake()

if __name__ == '__main__':
    main()