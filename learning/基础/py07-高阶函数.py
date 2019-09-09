#coding=utf-8

"""
=============================================================
#   project: python
#      file: py07-高阶函数.py
#    author: mianfeng.yang
#      date: 2019-08-30 15:57:11
=============================================================

1. 高阶函数可以简化代码,具有灵活性高
2. 调用高阶函数时可以将一个函数名传递到原函数中，这样的函数叫高阶函数
3. 内置高阶函数：map(),reduce,filter(),
    map: map(func, lst) python3中返回迭代器
    reduce(func, lst),func必须有2个参数，功能函数计算的序列的下一个数据做累计计算
    filter(func, lst),过虑功能
"""
import functools


def main():
    """函数说明文档 写在这里"""

    # 高阶函数定义，其中f参数是将要传入进来的函数名称
    def add_num(a, b, f):
        return f(a) + f(b)
    res = add_num(1, -10, abs)
    print(res)
    res1 = add_num(1.2, 2.9, round)
    print(res1)

    # map 用法：
    list1 = [1, 2, 3, 4]
    def func1(x):
        return x ** 2
    r1 = map(func1, list1)
    r2 = map(lambda x: x ** 2, list1)
    print(r1)
    print(list(r1))
    print(list(r2))

    # reduce 用法
    list2 = [1, 2, 3, 4, 5]
    def func2(a, b):
        return a + b
    r3 = functools.reduce(func2, list2)
    r4 = functools.reduce(lambda a, b: a + b, list2)
    print(r3)
    print(r4)

    # filter 用法
    list3 = [1,2,3,4,5,6,7,8,9,10]
    def func3(x):
        return x % 2 == 0

    r5 = filter(func3, list3)
    print(list(r5))

if __name__ == '__main__':
    main()