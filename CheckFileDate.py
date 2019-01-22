import os
import time,datetime
path = "e:/"
dirlist = os.listdir(path)
print(dirlist)
for file in dirlist:
    file_mtime = os.stat(path + file).st_mtime
    f_mtime = datetime.datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d')
    if os.path.isdir(path + file):
        print("%s 文件夹\n最后修改时间是: %s" %(file, f_mtime))
    if os.path.isfile(path + file):
        print("%s 文件\n最后修改时间是: %s" %(file, f_mtime))
