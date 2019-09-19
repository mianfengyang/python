#coding=utf-8

"""
=============================================================
#   project: python
#      file: student.py
#    author: mianfeng.yang
#      date: 2019-09-09 11:07:37
=============================================================
"""


class Student(object):
    def __init__(self, name, gender, tel):
        self.name = name
        self.gender = gender
        self.tel = tel

    def __str__(self):
        return f'{self.name}, {self.gender}, {self.tel}'

if __name__ == '__main__':
    pass