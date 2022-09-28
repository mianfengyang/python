#coding=utf-8

"""
=============================================================
#   project: python
#      file: py06-lambda.py
#    author: mianfeng.yang
#      date: 2019-08-30 13:07:45
=============================================================
lambda也是匿名函数
1. lambda可以简化代码
2. 语法：lambda 参数列表：表达式
3. 参数可有可无，能够接收任何数量的参数但只能返回一个表达式的值
4. 参数使用及写法同函数的参数
    1个参数
    多个参数
    无参数
    *args   lambda *args: args           返回元组
    **kwargs    lambda **kwargs: kwargs  返回字典
5. 带判断的lambda
    lambda a, b: a if a > b else b
"""

def main():
    """函数说明文档 写在这里"""
    f2 = lambda : 100
    # 直接打印 lambda表达式 输出的是内存地址
    print(f2)
    # 打印函数调用
    print(f2())

    f3 = lambda a, b: a + b
    print(f3(4,5))

    f4 = lambda a,b: a if a > b else b
    print(f4(100,300))

if __name__ == '__main__':
    main()