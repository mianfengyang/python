#coding=utf-8

"""
=============================================================
#   project: python
#      file: py03-类的继承.py
#    author: mianfeng.yang
#      date: 2019-08-12 15:48:31
=============================================================
"""
class Person:
    def __init__(self, name, gender, height, age, mobile, email):
        self.name = name
        self.gender = gender
        self.height = height
        self.age = age
        self.mobile = mobile
        self.email = email

    def run(self):
        print("===走路===")

    def eat(self):
        print("===吃饭===")

    def sleep(self):
        print("===睡觉===")


class Japanese(Person):
    def __init__(self, name, gender, height, age, mobile, email):
        Person.__init__(self, name, gender, height, age, mobile, email)

    def say(self):
        print("===欢迎来到中国===")
def main():
    pass


if __name__ == '__main__':
    main()