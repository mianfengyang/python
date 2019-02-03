import os
import time,datetime
basepath1 = "//192.168.1.11/pubin/"
checklist1 = ['huoguangxin', 'hw.liu', 'jianhong.zhang', 'jili', 'libin', 'liujunwei', 'yuanjun', 'zhanglili', 'zhangyonghui', '杨绵峰']
basepath10 = "//192.168.10.11/devin/"
checklist10 = ['huoguangxin', 'hw.liu', 'libin', 'liujunwei', 'yuanjun', 'zhanglili', '张建红']
#print(os.listdir(basepath10))
#dirlist = os.listdir(path)
#print(dirlist)
level = 1
def GetFileMtime(path,checklist):

    for file in checklist:
        file_mtime = os.stat(path + file).st_mtime
        f_mtime = datetime.datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d')
        if os.path.isfile(path + file):
            print("%s%s 文件\n最后修改时间是: %s" %(path,file, f_mtime))
        if os.path.isdir(path + file):
            childdir = path + file + "/"
            childlist = os.listdir(childdir)
            print("%s%s 文件夹\n最后修改时间是: %s" %(path,file, f_mtime))
            GetFileMtime(childdir,childlist)

GetFileMtime(basepath1,checklist1)