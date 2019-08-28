#coding=utf-8

"""
=============================================================
#   project: python
#      file: py02-推导式.py
#    author: mianfeng.yang
#      date: 2019-08-28 13:52:33
=============================================================
"""
from random import randint


# 只有列表，字典，集合 才有推导式

def main():
    # 列表推导式
    list1 = [i for i in range(10) if i % 2 == 0]
    list2 = [i for i in range(0, 10, 2)]
    print(list1)
    print(list2)


    # 合并2个列表组合成1个字典
    list3 = ['name', 'age', 'gender']
    list4 = ['Tom', 20, '男']
    dict_list = {list3[i]: list4[i] for i in range(len(list3))}
    print(dict_list)


    # 字典推导式
    dict1 = {k: randint(60,100) for k in ["Tom", "Bob", "Frank"] }
    print(dict1)


    # 提取字典中目标数据
    counts = {'MBP':268, 'HP': 125, 'DELL': 201, 'LENNOVO':199, 'ACER': 99}
    count1 = {key: value for key, value in counts.items() if value > 200}
    print(count1)

    # 集合推导式
    # 集合有自动去重功能
    list5 = [1, 2, 1, 3]
    set1 = {i ** 2 for i in list5}

    # 当变量不需要被引用或无关紧要时，可用下划线等符号表示，下面这条语句就是创建一个包含5个随机数的集合
    set2 = {randint(60, 100) for _ in range(5)}
    print(set1)
    print(set2)


if __name__ == '__main__':
    main()