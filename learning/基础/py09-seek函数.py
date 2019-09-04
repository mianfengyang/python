#coding=utf-8

"""
=============================================================
#   project: python
#      file: py09-seek函数.py
#    author: mianfeng.yang
#      date: 2019-09-03 15:30:27
=============================================================

语法：文件对象.seek(偏移量，起始位置）
     偏移量： 偏移的字节数
     起始位置： 0-开头 1-当前 2-结尾
"""


def main():
    """seek()函数使用：用来移动改变文件指针位置"""
    f = open('test.txt', 'r+')
    f.seek(2,0)
    f.write('aaa')
    f.seek(0,0)
    conf = f.read()

    print(conf)
    f.close()


if __name__ == '__main__':
    main()