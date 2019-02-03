import os
import datetime

basepath1 = "//192.168.1.11/pubin/杨绵峰/"
checklist1 = ['huoguangxin', 'hw.liu', 'jianhong.zhang', 'jili', 'libin', 'liujunwei', 'yuanjun', 'zhanglili', 'zhangyonghui', '杨绵峰']
basepath10 = "//192.168.10.11/devin/"
checklist10 = ['huoguangxin', 'hw.liu', 'libin', 'liujunwei', 'yuanjun', 'zhanglili', '张建红']



def newmtime(filepath):
    dict = {}
    filelists = os.listdir(filepath)
    filelists.sort(key=lambda fn: os.path.getmtime(filepath  + fn))
    print(filelists)
    print(len(filelists))
    print(filelists[-1])
    filenew = filepath + filelists[-1]
    filemtime = datetime.datetime.fromtimestamp(os.stat(filenew).st_mtime).strftime('%Y-%m-%d')
    print(filenew,filemtime)
    dict[filenew] = filemtime
    return dict


result = newmtime(basepath1)
print(result)