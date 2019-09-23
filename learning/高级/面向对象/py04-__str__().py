#coding=utf-8

"""
=============================================================
#   project: python
#      file: py04-__str__().py
#    author: mianfeng.yang
#      date: 2019-09-04 13:27:41
=============================================================
当使用print输出对象的时候，默认打印对象的内存地址。如果类定义了__str__方法，那么就会打印从在这个方法中return的数据
"""


def main():
    """函数说明文档 写在这里"""
    class Washer():
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def __str__(self):
            return "解释说明：类的说明或对象状态的说明"

    haier1 = Washer(100, 200)
    print(haier1)

if __name__ == '__main__':
    main()