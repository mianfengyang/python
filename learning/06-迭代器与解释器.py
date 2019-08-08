#coding=utf-8

"""
=============================================================
#   project: python
#      file: 06-迭代器与解释器.py
#    author: mianfeng.yang
#      date: 2019-07-12 18:29:51
=============================================================
"""
import random

def main():
    l1 = [random.randint(10, 20) for i in range(10)]
    l2 = {x:random.randint(-5, 20) for x in range(10) }
    print(l1)
    print(l2)
    l3 = sorted(l2.items(), key=lambda s: s[1] )
    print(l3)

if __name__ == '__main__':
    main()