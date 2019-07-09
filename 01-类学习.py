# coding=utf-8

"""
==============================================================
# @Time    : 2019/7/7 21:13
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : 01-类学习
# @Software: PyCharm
==============================================================
"""
class Restaurant():
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        print(self.restaurant_name, self.cuisine_type)

    def open_restaurant(self):
        print("%s正在营业……！" % self.restaurant_name)

myRestaurant = Restaurant("疯之夜", "民营")
myRestaurant.describe_restaurant()
myRestaurant.open_restaurant()