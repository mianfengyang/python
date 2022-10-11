#coding=utf-8

"""
=============================================================
#   project: python
#      file: test.py
#    author: mianfeng.yang
#      date: 2019-09-24 15:19:12
=============================================================
"""
import os
str1 = 'hello world'
print(str1)
print(repr(str1))

str2 = r"let's like you"
print(str2)
str3 = r'c:\windows'
print(str3)
str4 = r"let's make love"
print(str4)

# 2个单引号就是2个字串，会自动拼接
str5 = r'Good Morning''\\'
print(str5)

# 字符串方法及魔法函数
# print(dir(str))
"""
['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
"""

str6 = "this is frank, nice to meet you"

print(str6.title())
print(str6.upper())

str7 = "   前面有3个空格  再来2个  又来2个，结尾4个    "
# strip()不带参数表示删除前后空白，也可以带参数（子字串）表示删除前后子串
print(str7.strip())
# lstrip()不带参数表示删除左侧空白
print(str7.lstrip())
# rstrip()不带参数表示删除右侧空白
print(str7.rstrip())

# 查找、替换
str8 = "I am a worker hard work, hornet man a funny boy"
print(str8.startswith("i"))
print(str8.startswith("I"))
print(str8.endswith("man"))
print(str8.find("man"))
print(str8.index("man"))
print(str8.replace("a", "A", 1))

# 分割、连接
str9 = "crazyit.org is a good site"
print(str9.split())
print(str9.split(None, 2))
print(str9.split("."))
str10 = r"\\192.168.1.11\pubin\mifyang"
print(str10.split("\\")[-1])
print("{|}".join(str10.split("\\")).lstrip("{|}"))

list1 = [i for i in os.listdir(str3) if os.path.isdir(str3 + "\\" + i) ]
# print(list1)


if __name__ == '__main__':
    pass