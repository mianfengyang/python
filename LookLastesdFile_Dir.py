#coding:utf-8
import os
import time,datetime
path_1 = "//192.168.1.11/pubin/"
path_10 = "//192.168.10.11/devin/"
checklist_1 = ['huoguangxin', 'hw.liu', '张建红',
             'jili', 'libin', 'liujunwei', 'yuanjun',
             'zhanglili', 'zhangyonghui', '杨绵峰']
level = 1
for userdir in checklist_1:
    #列出目录下所有的文件
    list = os.listdir(path_1 + userdir)
    #对文件修改时间进行升序排列
    list.sort(key=lambda fn:os.path.getmtime(path_1 + userdir + '/' + fn))
    #获取最新修改时间的文件
    filetime = datetime.datetime.fromtimestamp(os.path.getmtime(path_1 + userdir + list[-1]))
    #获取文件所在目录
    filepath = os.path.join(path_1 + userdir,list[-1])
    print("最新修改的文件(夹)："+ list[-1])
    print("时间："+filetime.strftime('%Y-%m-%d'))

