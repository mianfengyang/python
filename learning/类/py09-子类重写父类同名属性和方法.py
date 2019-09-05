#coding=utf-8

"""
=============================================================
#   project: python
#      file: py09-子类重写父类同名属性和方法.py
#    author: mianfeng.yang
#      date: 2019-09-05 12:07:37
=============================================================
"""


def main():
    """子类重写父类同名属性和方法"""
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
        def __init__(self):
            self.kongfu = '[独创煎饼果子配方]'
        def make_cake(self):
            print(f'运用 {self.kongfu} 制作煎饼果子')


    daqiu = Prentice()
    print(daqiu.kongfu)
    daqiu.make_cake()

    # 查看子类继承了哪些父类
    print(Prentice.__mro__)



if __name__ == '__main__':
    main()