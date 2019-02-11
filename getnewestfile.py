import os
import datetime
path1 = r'd:/soft/'
path2 = r'e:/电子书/'
path3 = r'd:/Users/frank/'
bpath = r'//192.168.1.11/pubin/'
def findfiles(filepath, child_list = []):
    '''
    递归遍历当前目录，返回当前目录下所有子目录列表
    参数 filepath为传入路径参数，child_list列表用于保存传入路径中每个子目录
    :param filepath:
    :param child_list:
    :return: child_list
    '''
    child_list.append(filepath)
    for file in os.listdir(filepath):
        childpath = filepath + file + "/"
        # 如果有子目录则递归遍历子目录
        if os.path.isdir(childpath):
            findfiles(childpath)
    #返回所有子目录列表
    return child_list


def getmaxdepth(dirlist,cdirdepth):
    '''
    找出当前目录子目录的最大深度并返回
    :param dirlist:
    :param cdirdepth:
    :param dpath:
    :return: maxdpath
    '''
    dpath_dict = {}
    dpath = []
    for i in dirlist:
        dpath.append(i.count("/"))
    maxdpath = max(dpath) - cdirdepth
    lpath = sorted(dirlist,key=lambda s: s.count("/"))[-1]
    dpath_dict[maxdpath] = lpath
    dirlist.clear()
    return dpath_dict


def getmtime(dir):
    '''
    获取当前目录的修改时间并返回
    :param dir:
    :return: filemtime
    '''
    filemtime = datetime.datetime.fromtimestamp(os.stat(dir).st_mtime).strftime('%Y-%m-%d %H:%M')
    return filemtime



def Pt(filepath, newestdir = {}):
    '''
    打印输出当目录及子目录和目录深度,返回目录及对应修改时间的字典,再把字典按时间排序取出最新一个
    :param filepath1:
    :param newestdir:
    :return: newestdir
    '''
    newestdir.clear()

    dirlist = findfiles(filepath)
    #dirlist.pop(0)
    print("当前目录：{}".format(filepath))
    for cdir in dirlist:
        #print("\t包含子目录：{}\t最新修改时间：{}".format(cdir, getmtime(cdir)))
        newestdir[cdir] = getmtime(cdir)
    result_dpath = getmaxdepth(dirlist, filepath.count("/"))
    print("当前目录最大深度：{}".format(result_dpath))
    dirlist.clear()
    return newestdir

checklist = ['huoguangxin', 'hw.liu', 'jianhong.zhang', 'jili', 'libin',
             'liujunwei', 'yuanjun', 'zhanglili', 'zhangyonghui', '杨绵峰']
for p in checklist:
    path = bpath + p + "/"
    print("当前目录下最新修改的目录为是：{}\n".format(sorted(Pt(path).items(),key=lambda d:d[1])[-1]))