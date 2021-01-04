# coding=utf-8

"""
==============================================================
# @Time    : 2020/12/2 14:25
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : test
# @Software: PyCharm
==============================================================
"""
import os
file = open( "E:/a.txt", "a+" )
file_add = open("E:/a.txt","r")
content = file.read()
content_add = file_add.read()
pos = content.find( "buildTypes")
if pos != -1:
	content = content[:pos] + content_add + content[pos:]
	file = open( "E:/a.txt", "w" )
	file.write( content )
	file.close()
	file_add.close()
