#coding=utf-8

"""
=============================================================
#   project: python
#      file: py13-多态.py
#    author: mianfeng.yang
#      date: 2019-09-05 13:42:54
=============================================================

1. 多态指的是一类事物有多种形态，（一个抽象类有多个子类，因而多态的概念依赖于继承）
2. 定义 ：
    多态是一种使用对象的方式， 子类重写父类方法，调用不同子类对象的相同父类方法，可以产生不同的执行结果
3. 好处：
    调用灵活，有了多态，更容易编写出通用的代码，做出通用的编程，以适应需求的不断变化
4. 实现步骤：
    定义父类，并提供公共方法
    定义子类，并重写父类方法
    传递子类对象给调用者，可以看到不同子类执行效果不同

"""


def main():
    """多态"""
    class Dog(object):
        def work(self):
            print('指哪打哪……')

    class ArmyDog(Dog):
        def work(self):
            print('追击敌人……')

    class DrugDog(Dog):
        def work(self):
            print('追查毒品……')

    class Person(object):
        # 传入不同的对象，得到不同的结果(dog)
        def work_with_dog(self, dog):
            dog.work()

    ab = Dog()
    ad = ArmyDog()
    dd = DrugDog()

    daqiu = Person()
    daqiu.work_with_dog(ab)
    daqiu.work_with_dog(ad)
    daqiu.work_with_dog(dd)


if __name__ == '__main__':
    main()