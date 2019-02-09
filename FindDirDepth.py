import os
import datetime
path1 = r'd:/soft/'
path2 = r'e:/电子书/'


# 递归遍历当前目录，返回当前目录子目录列表
def FindDpath(filepath, dirlist = []):


    dirlist.append(filepath)
    for file in os.listdir(filepath):
        childpath = filepath + file + "/"
        #childpath = os.path.join(filepath,file)
        if os.path.isdir(childpath):
            FindDpath(childpath)
        # else:
        #     print(filepath + file)
    return dirlist



#找出当前目录子目录的最大深度
def FindMaxDirPath(dirlist,cdirdepth,dpath = []):


    for i in dirlist:
        dpath.append(i.count("/"))
    maxdpath = max(dpath) - cdirdepth
    return maxdpath

#找出当前目录下最新的文件或目录
def newmtime(dir):
    # filelists = os.listdir(filepath)
    # filelists.sort(key=lambda fn: os.path.getmtime(filepath + fn))
    # #print(filelists)
    # filenew = filelists[-1]
    filemtime = datetime.datetime.fromtimestamp(os.stat(dir).st_mtime).strftime('%Y-%m-%d')
    #print(filenew, filemtime)
    #new[filenew] = filemtime
    #print(new)
    return filemtime


#打印输出当目录及子目录和目录深度
def Pt(filepath1, newestdir = {}):


    dirlist = FindDpath(filepath1)
    dirlist.pop(0)
    print("当前目录：{}".format(filepath1))
    for cdir in dirlist:
        print("\t包含子目录：{}\t最新修改时间：{}".format(cdir, newmtime(cdir)))
        newestdir[cdir] = newmtime(cdir)
    print("当前目录最大深度：%s" % FindMaxDirPath(dirlist,filepath1.count("/")))
    return newestdir


print(sorted(Pt(path1).items(),key=lambda d:d[1])[-1])