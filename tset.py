import os
import datetime
path = r'D:/Users/mianfeng.yang.PUB/Documents/工作文件/基础信息/Route_Switch/'
path1 = r'//192.168.1.11/pubin/zhanglili/'
path2 = r'd:/soft/'
path3 = r'e:/电子书/2/'
def newmtime(filepath,new = {}):
    filelists = os.listdir(filepath)
    filelists.sort(key=lambda fn: os.path.getmtime(filepath + fn))
    print(filelists)
    filenew = filepath + filelists[-1]
    filemtime = datetime.datetime.fromtimestamp(os.stat(filenew).st_mtime).strftime('%Y-%m-%d')
    print(filenew, filemtime)
    new[filenew] = filemtime
    #print(new)
    return new

print(newmtime(path3))
# def FindFileMtime(filepath,dirdepth):
#
#     #print("当前目录：{} 递归层级：{}".format(filepath, dirdepth))
#     dirdepth -= 1
#
#     result = newmtime(filepath)
#     for file in os.listdir(filepath):
#         childpath = filepath + file + "/"
#         if dirdepth <= 0:
#             continue
#         if os.path.isdir(childpath):
#
#             FindFileMtime(childpath,dirdepth)
#     #newestlist.append(result)
#     return result

#p = FindFileMtime(path3,3)

