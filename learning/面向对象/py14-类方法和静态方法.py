#coding=utf-8

"""
=============================================================
#   project: python
#      file: py14-类方法和静态方法.py
#    author: mianfeng.yang
#      date: 2019-09-06 13:54:50
=============================================================

1. 类方法：
    需要用装饰器@classmethod 来标识其为类方法，对于类方法，第一个参数必须是类对象，一般以cls作为第一个参数

    使用场景：
    当方法中需要使用类对象（如访问私有类属性等）时，定义类方法
    类方法一般和类属性配合使用

2. 静态方法：
    需要使用装饰器@staticmethod来装饰，静态方法既不需要传递类对象也不需要传递实例对象（形参没有self/cls)
    静态方法也可以通过 实例对象 和 类对象 去访问

    使用场景：
    当方法中既不需要使用实例对象（如实例对象，实例属性），也不需要使用类对象（如类属性，类方法，创建实例等）时，定义静态方法
    取消不需要的参数传递，有利于 减少不必要的内存占用和性能消耗
"""


def main():
    """函数说明文档 写在这里"""
    # 定义类：私有类属性，类方法获取这个私有类属性
    class Dog(object):
        __tooth = 10

        # 定义类方法
        @classmethod
        def get_tooth(cls):
            return cls.__tooth

    # 静态方法定义
    class Cat(object):
        @staticmethod
        def info_print():
            print('这是一个静态方法')

    wangcai = Dog()
    result = wangcai.get_tooth()
    print(result)

    xiaojun = Cat()
    xiaojun.info_print()
    Cat.info_print()

if __name__ == '__main__':
    main()