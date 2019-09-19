#coding=utf-8

"""
=============================================================
#   project: python
#      file: py02-class-1.py
#    author: mianfeng.yang
#      date: 2019-08-08 16:04:15
=============================================================
"""
class Cat:
    def say(self):
        print("I am a cat")

class Dog:
    def say(self):
        print("I am a dog")

class Duck:
    def say(self):
        print("I am a duck")


def main():
    # animal = Cat()
    # animal.say()
    animal_list = [Cat, Dog, Duck]
    for ani in animal_list:
        ani().say()

    a = ['a', 'b']
    b = ['c', 'd']
    name_tuple = ['e', 'f']
    name_set = set()
    name_set.add('g')
    name_set.add('h')
    a.extend(b)

    a.extend(name_tuple)
    print(a)
    print(name_tuple)


if __name__ == '__main__':
    main()