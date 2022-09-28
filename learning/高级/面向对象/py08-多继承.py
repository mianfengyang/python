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

    class TuSun(Prentice):
        pass

    xiaoqiu = TuSun()
    xiaoqiu.make_cake()
    xiaoqiu.Master_make_cake()
    xiaoqiu.School_make_cake()
    xiaoqiu.make_cake()


if __name__ == '__main__':
    main()