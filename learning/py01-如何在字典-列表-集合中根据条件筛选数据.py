# coding=utf-8

"""
==============================================================
# @Time    : 2019/8/6 19:36
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : py01-如何在字典-列表-集合中根据条件筛选数据
# @Software: PyCharm
==============================================================
"""
from random import  randint
import timeit

def main():
    data = [randint(-10, 10) for _ in range(10)]
    res = filter(lambda x: x >= 0, data)
    print(res.__next__())

    res1 = [x for x in data if x >= 0]
    print(res1)



if __name__ == '__main__':
    main()