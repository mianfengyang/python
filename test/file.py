"""
按行遍历文件，根据正则表达式来匹配每行内容，匹配到则不写入文件，没匹配到写入文件。
这里是以a+的方式打开文件，默认文件指针在文件尾，所以要用seek(0)方法将指针定位到
文件首行。
"""
import os
import re

filepath = "/home/frank/a.txt"
url = ["frank","hello"]
f = open(filepath,"a+")
f.seek(0)
size = os.path.getsize(filepath)
# print(size)
pn = re.compile(r'frank')
while 1:
    line = f.readline()
    # print(line + "===")
    if size == 0:
        # print("-0-")
        f.write(url[0] + "\n")
        break
    if re.match(pn,line):
        # print("-1-")
        break
    elif line:
        # print("-2-")
        continue
    else:
        # print("-3-")
        f.write(url[0] + "\n")
        break
    
f.close()