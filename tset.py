import os
import datetime
path = "D:/Users/mianfeng.yang.PUB/Documents/工作文件/基础信息/Route_Switch/"
path1 = "//192.168.1.11/pubin/zhanglili/"
ignore_file = ['Thumbs.db']
def newmtime(filepath,new = {}):
    filelists = os.listdir(filepath)
    filelists.sort(key=lambda fn: os.path.getmtime(filepath + "/" + fn))
    filenew = filepath + filelists[-1]
    filemtime = datetime.datetime.fromtimestamp(os.stat(filenew).st_mtime).strftime('%Y-%m-%d')
    print(filenew, filemtime)
    new[filenew] = filemtime
    #print(new)
    return new

def FindFileMtime(filepath,dirdepth):

    #print("当前目录：{} 递归层级：{}".format(filepath, dirdepth))
    dirdepth -= 1

    result = newmtime(filepath)


    for file in os.listdir(filepath):

        if dirdepth <= 0:
            continue
        if os.path.isdir(filepath + file):
            childpath = filepath + file + "/"
            FindFileMtime(childpath,dirdepth)
    #newestlist.append(result)
    return result

p = FindFileMtime(path1,3)

print(sorted(p.values())[-1])