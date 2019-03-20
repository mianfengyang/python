# coding=utf-8

"""
==============================================================
# @Time    : 2019/2/10 0010
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : test
# @Software: PyCharm
==============================================================
"""
import os
import datetime
import threading
import openpyxl
path1 = r'd:/soft/'
path2 = r'e:/'
path3 = r'd:/Users/frank/'
bpath1 = r'//192.168.1.11/pubin/'
bpath10 = r'//192.168.10.11/devin/'
depth = 4
result_list = []


def findfiles(filepath, depth, child_list = []):
    '''
    递归遍历当前目录，返回当前目录下所有子目录列表
    参数 filepath为传入路径参数，child_list列表用于保存传入路径中每个子目录
    :param filepath:        传递一个路径
    :param depth            传递一个最大遍历目录的深度
    :param child_list:      用来保存子目录的列表
    :return: child_list     返回子目录列表
    '''
    depth -= 1
    child_list.append(filepath)
    for file in os.listdir(filepath):
        childpath = filepath + file + "/"
        # 如果超出最大深度，不再往下遍历
        if depth <= 0:
            continue
        # 如果有子目录则递归遍历子目录
        if os.path.isdir(childpath):
            findfiles(childpath, depth)
    #返回所有子目录列表
    return child_list


def getmaxdepth(dirlist,cdirdepth):
    '''
    找出当前目录子目录的最大深度并以字典的形式返回
    :param dirlist:     传递一个目录列表
    :param cdirdepth:   用于计算给定初始路径的 ”/“ 的个数
    :param dpath:       用于存放子目录的 ”/“ 的个数的列表
    :return: maxdpath   用于计算子目录的深度（"/"的个数）
    '''
    dpath_dict = {}
    dpath = []
    for i in dirlist:
        dpath.append(i.count("/"))
    maxdpath = max(dpath) - cdirdepth
    #将目录列表按”/“出现的个数进行排序，取出最后一个，也就是拥有最大目录深度的那个
    lpath = sorted(dirlist,key=lambda s: s.count("/"))[-1]
    #将目录的最大深度值，最大深度的目录存入字典
    dpath_dict[maxdpath] = lpath
    #由于函数是递归调用，所以再次调用时要清空字典，这样不会影响下次的值
    dirlist.clear()
    return dpath_dict


def getmtime(dir):
    '''
    获取当前目录的修改时间并返回
    :param dir:         传递一个目录
    :return: filemtime  返回目录的修改时间
    '''
    filemtime = datetime.datetime.fromtimestamp(os.stat(dir).st_mtime).strftime('%Y-%m-%d %H:%M')
    return filemtime



def Pt(filepath, newestdir = {}):
    '''
    打印输出当目录及子目录和目录深度,返回目录及对应修改时间的字典,再把字典按时间排序取出最新一个
    :param filepath:        传递一个路径
    :param newestdir:       初始化一个空字典，用来保存最新修改的目录和对应的修改时间
    :return: newestdir
    '''

    #每次调用函数时清空字典
    newestdir.clear()
    dirlist = findfiles(filepath, depth)
    #print("当前目录：{}".format(filepath))

    for cdir in dirlist:
        #print("\t包含子目录：{}\t最新修改时间：{}".format(cdir, getmtime(cdir)))
        newestdir[cdir] = getmtime(cdir)
    #result_dpath = getmaxdepth(dirlist, filepath.count("/"))
    # for k, v in result_dpath.items():
    #     print("当前目录最大递归深度:{}\n最大深度目录：{}".format(k, v))
    #清空子目录列表，主要是不影响下次调用
    dirlist.clear()
    return newestdir


def get_fullpath_1(p):
    """
    根据传入的子目录名，生成完整路径
    :param p:       传入子目录列表中的一个元素
    :return:
    """
    path = bpath1 + p + "/"
    result = sorted(Pt(path).items(),key=lambda d:d[1])[-1]
    print("当前目录下最新修改的目录是：{}\n".format(result))
    #print(path)


def get_fullpath_10(p):
    """
       根据传入的子目录名，生成完整路径
       :param p:       传入子目录列表中的一个元素
       :return:
    """
    path = bpath10 + p + "/"
    result = sorted(Pt(path).items(), key=lambda d: d[1])[-1]
    print("当前目录下最新修改的目录是：{}\n".format(result))
    #print(path)

def get_result_1(checklist1):
    for i in checklist1:
        t1 = threading.Thread(target=get_fullpath_1, args=(i, ))
        t1.start()
        t1.join()

def get_result_10(checklist10):
    for i in checklist10:
        t10 = threading.Thread(target=get_fullpath_10, args=(i, ))
        t10.start()
        t10.join()

checklist10 = ['huoguangxin', 'hw.liu', '吉利', 'libin', 'liujunwei', 'yuanjun', '张建红', 'zhanglili']
checklist1 = ["huoguangxin", 'hw.liu', 'jianhong.zhang', 'jili', 'libin',
              'liujunwei', 'yuanjun', 'zhangyonghui', '杨绵峰', 'zhanglili']

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    get_result_1(checklist1)
    get_result_10(checklist10)
    end_time = datetime.datetime.now()
    print("开始时间：{}\n结束时间：{}\n总共耗时：{}".format(start_time.strftime("%Y-%m-%d %H:%M:%S"),
                                             end_time.strftime("%Y-%m-%d %H:%M:%S"), end_time - start_time))

