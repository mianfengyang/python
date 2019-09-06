#coding=utf-8

"""
=============================================================
#   project: python
#      file: py01-异常语语法.py
#    author: mianfeng.yang
#      date: 2019-09-06 14:21:32
=============================================================

1. 语法：
        try:
            可能发生错误的代码
        except:
            如果出现异常执行的代码

2. 捕获指定异常
        try:
            可能发生错误的代码
        except 异常类型:
            如果捕获到异常执行的代码

3. 捕获多个指定异常
        try:
            可能发生错误的代码
        except (异常类型1, 异常类型2):
            如果捕获到异常执行的代码

4. 捕获异常描述信息
        try:
            可能发生错误的代码
        except (异常类型1, 异常类型2) as result:
            print(result)

5. 捕获所有异常
        try:
            可能发生错误的代码
        except Exception as result:
            print(result)

6. 注意：一般try下方只放一行尝试执行的代码


"""


def main():
    """异常语法"""
    try:
        f = open('test.txt', 'r')
    except:
        f = open('test.txt', 'w')


if __name__ == '__main__':
    main()