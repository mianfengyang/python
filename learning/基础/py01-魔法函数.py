#coding=utf-8

"""
=============================================================
#   project: python
#      file: py01-魔法函数.py
#    author: mianfeng.yang
#      date: 2019-08-08 15:17:42
=============================================================
"""

# 什么是魔法函数？
# 以双下划线开头和结尾的函数都是魔法函数
# 不用自己定义魔法函数，用的是python里提供的就可以，可以用FOR循环遍历


class Commpany():
    def __init__(self, employee_list):
        self.employee = employee_list

    def __getitem__(self, item):
        return self.employee[item]



def main():
    company = Commpany(["tom", "bob", "jane"])

    for em in company:
        print(em)


if __name__ == '__main__':
    main()