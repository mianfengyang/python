#coding=utf-8

"""
=============================================================
#   project: python
#      file: py04-拆包和解包.py
#    author: mianfeng.yang
#      date: 2019-08-29 13:22:21
=============================================================
"""


def main():
    """元组拆包"""
    return  100, 200


if __name__ == '__main__':
    n1,n2 = main()
    print(n1)
    print(n2)
    dict1 = {'name': 'tom', 'age':25}
    # 字典拆包
    name,age = dict1
    print(name)
    print(age)
    print(dict1[name])
    print(dict1[age])