#coding=utf-8

"""
=============================================================
#   project: python
#      file: py11-super()方法.py
#    author: mianfeng.yang
#      date: 2019-09-05 12:35:52
=============================================================

1. super 调用父类时使用
2. 语法：
    a. 带参数  super(类名，self).__init__() super(当前类名，self).方法名
    b. 不带参数 super().__init__() super().方法名
"""


def main():
    """super()属性和方法"""
    class Master(object):
        def __init__(self):
            self.kongfu = '[古法煎饼果子配方]'

        def make_cake(self):
            print(f'运用 {self.kongfu} 制作煎饼果子')

    class School(Master):

        def __init__(self):
            super().__init__()
            self.kongfu = '[黑马煎饼果子配方]'

        def make_cake(self):
            print(f'运用 {self.kongfu} 制作煎饼果子')

            # 带参数写法
            # super(School,self).__init__()
            # super(School, self).make_cake()

            # 不带参数的写法
            super().__init__()
            super().make_cake()

    class Prentice(School):
        def __init__(self):
            super().__init__()
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

        def make_old_cake(self):
            super().__init__()
            super().make_cake()

    daqiu = Prentice()
    # print(daqiu.kongfu)
    # daqiu.make_cake()
    # daqiu.Master_make_cake()
    # daqiu.School_make_cake()
    daqiu.make_old_cake()
    daqiu.make_cake()


if __name__ == '__main__':
    main()