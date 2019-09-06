#coding=utf-8

"""
=============================================================
#   project: python
#      file: py08-文件操作.py
#    author: mianfeng.yang
#      date: 2019-08-30 16:56:23
=============================================================
1. 打开: open(path, mod)
    path:文件的路径
    mod: 以何种模式打开，主要有：r,w,a,rb,wb,r+,w+,rb+,wb+,ab,a+,ab+
    带 b 的都是二进制方式，带 + 号的表示可读可写
    r,w 模式文件指针在开头
    a 模式文件指针在末尾
2. 读：read()
3. 写: write()
4. 关闭： close()
"""


def main():
    """r+ w+ a+区别"""
    f1 = open('test.txt', 'r+')

    # w+: 没有文件则创建，文件指针在开头，用新内容覆盖原内容
    f2 = open('test.txt', 'w+')
    f2.write('456\n')
    # a+ 没有文件则创建，文件指针在末尾，无法读取数据（文件指针后面没有数据）
    f3 = open('test.txt', 'a+')
    f3.write('789')
    con1 = f1.read()
    con2 = f2.read()
    con3 = f3.read()
    print(con1)
    print(con2)
    print(con3)

    f1.close()
    f2.close()
    f3.close()


if __name__ == '__main__':
    main()