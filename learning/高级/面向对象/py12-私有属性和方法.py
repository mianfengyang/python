#coding=utf-8

"""
=============================================================
#   project: python
#      file: py12-私有属性和方法.py
#    author: mianfeng.yang
#      date: 2019-09-05 13:15:58
=============================================================

1. 私有属性和方法不继承给子类
2. 写法：属性或方法名前加2个_
3. 私有属性和方法 可以在类里面设置和修改

"""


def main():
    """私有属性和方法"""

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

            # 定义私有属性 私有变量前加2个_
            self.__money = 2000000

        def get_money(self):
            return self.__money

        def set_money(self, money):
            self.__money = money

        def __info_print(self):
            print("这是私有方法")

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

    class Tusun(Prentice):
        pass

    xiaoqiu = Tusun()
    xiaoqiu.get_money()
    xiaoqiu.set_money(10000000000)
    print(xiaoqiu.get_money())

if __name__ == '__main__':
    main()