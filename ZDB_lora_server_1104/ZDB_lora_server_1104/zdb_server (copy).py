#!/usr/bin/env python3
# coding=utf-8
' ZDB server module (20200713)'
__author__ = 'nluo@dspsemi.com'

import os 
import sys
import configparser
import threading
import time
import datetime
import platform
#if(platform.system()=='Windows'):
#    import console
import queue
import random
import MySQLdb
import pymysql
import cv2
import struct
import zlib
import arpreq
from meterreader import Mreader as mr
from DBUtils.PooledDB import PooledDB
from socket import *

#时分秒字符串转成当天秒数
def t2s(t):
    h,m,s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

### 获取当前时间
def gettm():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[0:-4]

def gettm_ms():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:-4]

def gettm_t2s():
    return t2s(datetime.datetime.now().strftime('%H:%M:%S'))

def gettm_ymd():
    return datetime.datetime.now().strftime('%Y%m%d')


def cal_crc32(file_path):
    """
    计算文件 crc32 hash 值
    """
    with open(file_path, 'rb') as fh:
        hash = 0
        while True:
            s = fh.read(65536)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)

def to_ascii(h):
    list_s = []
    for i in range(0, len(h), 2):
        list_s.append(chr(int(h[i:i+2], 16)))
    return ''.join(list_s)
        
### 定义不打印的类
class print_null:
    def write(self,string):
        pass
		#do something you wanna do

### 下行协议类
class pro_tx_data:
    def __init__(self):
        self.gw_id = '00000000';
        self.node_ver = '01';
        self.node_type  = '01';
        self.node_id = '01010000';
        self.node_sid = '0000';
        self.pro_cont_data = '';
        self.pro_cont_data_len  = '00';
        self.pro_cont_data_crc  = '0000';

    def pack_data(self):
        return self.gw_id + self.node_ver + self.node_type\
               + self.node_sid + self.pro_cont_data_len \
               + self.pro_cont_data + self.pro_cont_data_crc

### 上行协议类          
class pro_rx_data:
    def __init__(self):
        self.pro_ver='01';
        self.pro_id='00';
        self.gw_id = '00000000';
        self.node_id = '01010000';
        self.node_sid = '0000';
        self.node_ch = '02';
        self.node_snr = '00';
        self.node_rssi = '0000';
        self.node_nc = '0000';
        self.node_timestap = '00000000';
        self.node_nr = '00';
        self.node_alive_n = '0000';
        self.pro_data_len = '0000';
        self.pro_data  = '';

### 这个服务器的类
class ZDB_Server(object):
    """GatewayAPI Tcp服务器"""
    def __init__(self):
        """初始化对象"""
        self.code_mode = "utf-8" 
        self.conf = configparser.ConfigParser()
        ### 读取配置文件
        self.conf.read('server.ini', encoding='utf-8')
        print('Version: {}  Build date: {}  Author: {}\n'.format(self.conf.get('DEFAULT', 'version'),\
                self.conf.get('DEFAULT', 'build_date'),self.conf.get('DEFAULT', 'author')))

        ### 与集中器网关交互的socket配置
        self.server_port = self.conf.getint('Server', 'port')
        self.server_socket = socket(AF_INET, SOCK_STREAM) #创建socket               
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)   #设置端口复用
        self.server_socket.bind(('', self.server_port))#绑定IP和Port
        self.server_socket.listen(100)
        print('当前主机时间为：%s'%gettm())
        # 查看当前主机名
        print('当前主机名称为: ' + gethostname())
        # 根据主机名称获取当前IP
        s = socket(AF_INET, SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 53))
        except Exception as e:
            pass
        print('当前主机的IP为: {}'.format(s.getsockname()[0]))
        s.close()
        #for ip in gethostbyname_ex(gethostname())[2]:
        #    print('%s '%ip)
        print("Server监听端口: %d"%self.server_port)
        #设置webCtl的连接参数
        self.webmsgq_in = queue.Queue(1)
        self.webmsgq_out = queue.Queue(1) 
        self.webctl_port=int(self.conf.get('WebCtl', 'port'))
        self.webctl_socket = socket(AF_INET, SOCK_STREAM)               #创建socket
        self.webctl_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)   #设置端口复用
        self.webctl_socket.bind(("", self.webctl_port)) #绑定IP和Port
        self.webctl_socket.listen(10)                   #设置为被动socket
        print("WebCtl监听端口: %d"%self.webctl_port)
        #字典配置
        self.gwnd_socket_dict = {}
        self.gwnd_status_dict = {}
        self.gwnd_cycle_end_dict = {}
        self.gateway_status_dict = {}
        self.gwnd_autowork_dict = {}
        self.gwnd_piccnt_dict = {}
        self.gwnd_rxqueue_dict = {}
        self.gwnd_wakeupInterval_dict = {}
        #白名单
        self.white_list = []
        self.own_devices_dict = self.read_own_devices()
        for gateway_id in list(self.own_devices_dict.keys()):
            for node_id in self.own_devices_dict[gateway_id]:
                self.white_list.append(gateway_id+node_id)
                self.gwnd_autowork_dict[gateway_id+node_id] = 1
        #print('预设的白名单字典:',self.own_devices_dict)
        print('预设的白名单:',self.white_list)
        ### 指针表/数字表

        ### 维护升级配置
        self.maintain_start_t = t2s(self.conf.get('Maintenance','time_start'))
        self.maintain_end_t = t2s(self.conf.get('Maintenance', 'time_end'))
        self.upgrade_start_t = t2s(self.conf.get('Maintenance','upgrade_start'))
        self.upgrade_end_t = t2s(self.conf.get('Maintenance', 'upgrade_end'))
        self.upgrade_wait = self.conf.getint('Maintenance', 'upgrade_wait')

        #print('m_start={}, m_end={}, now={}'.format(self.maintain_start_t, self.maintain_end_t, gettm_t2s()))
        self.gwid_lastBN_dict = {}
        self.gwid_lastBF_dict = {}
        self.fw_debug_flag = 0
        ### 节点相关配置
        self.white_list_enable = self.conf.getint('Node', 'white_list_enable')  #白名单功能
        self.allow_auto_reg = self.conf.getint('Node', 'allow_auto_reg')  #自动发现注册
        self.cycle_interval = self.conf.getint('Node', 'cycle_interval') #循环周期(秒),比如300秒
        print('每个集中器的轮询周期：{}秒'.format(self.cycle_interval))
        self.random_delay_max = self.conf.getint('Node', 'random_delay_max') #随机延时
        self.RTO_max = self.conf.getint('Node', 'RTO_max') #响应超时
        self.mindelay_in_imgframes = self.conf.getint('Node', 'mindelay_in_imgframes') #帧间最小延时
        self.upload_mode = self.conf.getint('Node', 'upload_mode') #0 传识别结果和图， 1 只传识别结果
        self.lowpower_wakeup_enable = self.conf.getint('Node', 'lowpower_wakeup_enable')
        self.wakeup_interval = self.conf.getint('Node', 'wakeup_interval')  #终端唤醒周期(分钟)
        if self.wakeup_interval > 255:
            self.wakeup_interval = 255
        elif self.wakeup_interval < 0:
            self.wakeup_interval = 0
        self.RTO_fail_exit = self.conf.getint('Node', 'RTO_fail_exit')  #终端唤醒周期(分钟)

        ### thread lock
        self.socket_txlock_dict = {}
        self.socket_status_dict = {}
        self.file_lock = threading.Lock()
        ### 485的虚拟集中器地址和实际地址映射
        self.vgw_rgw_dict = {}
        ### 485 注册回应延迟ms
        self.reg_resp_delay = self.conf.getint('Node', 'reg_resp_delay')
        self.data_recv_delay = self.conf.getint('Node', 'data_recv_delay')
        ### 设置mysql的连接参数
        self.mysql_enable=self.conf.getboolean('Mysql', 'enable')
        self.mysql_tlock_enable = 0
        if self.mysql_enable:
            self.mysql_lock=threading.Lock()
            mysql_host=self.conf.get('Mysql', 'host')
            mysql_port=self.conf.getint('Mysql', 'port')
            mysql_user=self.conf.get('Mysql', 'user')
            mysql_passwd=self.conf.get('Mysql', 'password')
            mysql_db=self.conf.get('Mysql', 'database')
            self.mysql_lock_enable=self.conf.getboolean('Mysql', 'conn_lock_enable')
            conn_max=self.conf.getint('Mysql', 'conn_max')
            conn_mincached=self.conf.getint('Mysql', 'conn_mincached')
            conn_maxcached=self.conf.getint('Mysql', 'conn_maxcached')
            conn_maxusage=self.conf.getint('Mysql', 'conn_maxusage')
            self.mysql_pool = PooledDB(creator=pymysql,
                                    maxconnections=conn_max,   # 连接池允许的最大连接数，0和None表示不限制连接数（0）
                                    mincached=conn_mincached,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建（4）
                                    maxcached=conn_maxcached,  # 链接池中最多闲置的链接，0和None不限制
                                    maxusage=conn_maxusage,    # 一个链接最多被重复使用的次数，None表示无限制
                                    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                                    host=mysql_host,
                                    user=mysql_user,
                                    passwd=mysql_passwd,
                                    db=mysql_db,
                                    port=mysql_port)       
        self.save_root_dir = self.conf.get('Save', 'save_root_dir')
        self.img_relative_dir_f = self.conf.get('Save', 'img_relative_dir_f')
        self.img_relative_dir_b = self.conf.get('Save', 'img_relative_dir_b')
        self.model_relative_dir = self.conf.get('Save', 'model_relative_dir')
        
        self.createDir(self.save_root_dir+'/'+self.img_relative_dir_f)
        self.createDir(self.save_root_dir+'/'+self.img_relative_dir_b)
        self.createDir(self.save_root_dir+'/'+self.model_relative_dir)

        self.fw_dir = self.conf.get('Maintenance', 'fw_dir')
        self.createDir(self.fw_dir)
        self.broadcast_interval = self.conf.getint('Maintenance', 'broadcast_interval')
        self.start_to_fw_upgrade = 0
        self.fw_upgrade_para=[]
        
        #输出信息重定向
        self.log_dir = self.conf.get('Debug', 'log_dir')
        self.createDir(self.log_dir)
        print('运行中...')
        self.debug_level = self.conf.getint('Debug', 'level')
        if self.debug_level == 0:
            self.stdout_bak = sys.stdout
            sys.stdout = print_null()
        if self.debug_level > 1:
            self.log_file = self.log_dir+'/log_'+datetime.datetime.now().strftime('%Y%m%d%H%M')+'.txt'
            print('日志保存中：{} ...'.format(self.log_file))
            self.stdout_bak = sys.stdout
            sys.stdout.close()
            sys.stdout = open(self.log_file,'w')

    # 返回更新节点数
    def update_devices_autowork(self, dict, msg):
        op = msg[0:3]
        flag = 0
        if(op != 'STA' and  op != 'STP'):
            print('update_devices_autowork(): msg error!')
            flag = -1
            return
        g_list = msg[3:].split('{')[1].split('}')[0].split('|')
        for g in g_list:
            gw, nodes = g.split(":")
            node_list = nodes.split(',')
            node_list = list(set(node_list))
            node_list.sort()
            if op == 'STA':
                for nd in  node_list:
                    dict[gw+nd] = 1
                    flag = flag + 1
            elif op == 'STP':
                for nd in  node_list:
                    dict[gw+nd] = 0
                    flag = flag + 1
        return flag

    # 统计所有设备的信息，dict为更新对象字典， msg以ADD/DEL开头，
    # 如'ADD{5D000001:000001,000002,000003|5D000002:000001,000002}'
    # 更新后dict如：{'5D000001': ['000001', '000002', '000003'], '5D000002': ['000001', '000002']}
    def update_own_devices(self, dict, msg):
        op = msg[0:3]
        if(op != 'ADD' and  op != 'DEL'):
            print('update_own_devices(): msg error!')
            return
        g_list = msg[3:].split('{')[1].split('}')[0].split('|')
        for g in g_list:
            gw, nodes = g.split(":")
            node_list = nodes.split(',')
            node_list = list(set(node_list))
            node_list.sort()
            if op == 'ADD':
                if gw not in dict:
                    dict[gw] = node_list
                else:
                    dict[gw].extend(node_list)
                dict[gw]=list(set(dict[gw]))
            elif op == 'DEL':
                if gw in list(dict.keys()):
                    for i in  node_list:
                        if i in dict[gw]:          
                            dict[gw].remove(i)
                    if len(dict[gw]) == 0:
                        dict.pop(gw)

    def save_own_devices(self, dict):
        #保存
        with open('own_devices.ini','w') as f:
            f.write(str(dict))
            print('保存own devices完成！')


    def read_own_devices(self):
        #读取
        dict = {}
        with open('own_devices.ini','r') as f:
            a = f.read()
            dict = eval(a)
            #print(dict)
        return dict

    def test_own_devices(self):
        devies_dict = {}
        # 增加
        msg = 'ADD{5D000001:000005,000002,000001,000004,000003|5D000002:000006,000002,000004,000001,000005}'
        self.update_own_devices(devies_dict, msg)
        msg = 'ADD{5D000033:000020,000021,000022,000023}'
        self.update_own_devices(devies_dict, msg)
        # 删除
        msg = 'DEL{5D000002:000002,000004,000001,000005}'
        self.update_own_devices(devies_dict, msg)
        # 保存
        self.save_own_devices(devies_dict)
        # 读取
        read_dict = {}
        read_dict = self.read_own_devices()

    def createDir(self, path):
        if os.path.exists(path):
            #print('新建文件夹：%s已存在'%path)
            pass
        else:
            try:
                os.mkdir(path)
                print('新建文件夹：%s'%path)
            except Exception as e:
                os.makedirs(path)
                print('新建多层文件夹：%s' % path)

    ### 输入字节流，输出大端的crc16字符串(4个字符)
    def crc16_xmodem_be(self, dat):
        wcrc = 0
        for i in dat:
            c = i
            for j in range(8):
                treat = c & 0x80
                c <<= 1
                bcrc = (wcrc >> 8) & 0x80
                wcrc <<= 1
                wcrc = wcrc & 0xffff
                if (treat != bcrc):
                    wcrc ^= 0x1021
        return "%02X%02X"%((wcrc & 0x00ff),wcrc>>8)

    ### 字节列表以16进制格式打印数据，发送显示绿色，接收显示红色
    def print_hex(self, data, isTx, tag):
        lin = ['%02X'.ljust(4) % i for i in data]
        if isTx == 1:
            print('|gateway id | node id   |L1|T2|L2|V2..|.crc16| [{},{}]'.format(gettm(),tag))
            print('\033[1;31;40m',' '.join(lin),'\033[0m')
        else:
            print('|vr|id|gateway id | node id   |s-id |ch|snr|rssi| nc  | timestap  |nr|alive| len |valid data .. [{} {}]'.format(gettm(),tag))
            print('\033[1;32;40m',' '.join(lin),'\033[0m')

    ### web发来命令放入queue里面给回复使用
    def webctl_rx(self):   
        while True:
            ###等待客户端连接
            self.webctl_client, self.webctl_addr = self.webctl_socket.accept()
            print('Web服务的连接：{},{}'.format(self.webctl_client, self.webctl_addr))
            while True:
                try:
                    rcv = self.webctl_client.recv(1024) 
                    if rcv:
                        print('[%s]: from web server:%s'%(gettm(),rcv.decode('utf8',errors='ignore')))
                        self.webmsgq_in.put(rcv)
                        self.webctl_client.send(rcv)
                    else: 	### 客户端断开连接
                        print("{} offline".format(self.webctl_addr))
                        self.webctl_client.close()
                        break
                except error:
                    break
                    #print("{} socket close/timeout.".format(self.webctl_addr))
            self.webctl_client.close()
            time.sleep(1)
        self.webctl_socket.close()

    ### 执行web发来的命令，结果返回给web
    def webctl_tx(self):
        while True:
            try:
                data = self.webmsgq_in.get_nowait()
                data_str = data.decode('utf8',errors='ignore')
            except queue.Empty:
                ##print('webmsgq_out empty!')
                time.sleep(0.1)
            else:
                err = 0
                op=''
                op_id=''
                target=''
                act=''
                data=''
                recg_period=0
                img_upload_period=0
                img_upload_time=0,0
                flag = 0
                print('web:',data_str)
                if not data_str.endswith('end'):
                    resp='WebCtl:Not ends with [end]:{}'.format(data_str)
                    print(resp)
                    self.webctl_client.send(str.encode(resp))
                    continue
                if not (data_str.startswith('get') or data_str.startswith('set') or data_str.startswith('cfg')):
                    resp='WebCtl:Not starts with [get/set/cfg]:{}'.format(data_str)
                    print(resp)
                    self.webctl_client.send(str.encode(resp))
                    continue
                strlist = data_str.split(';')
                for nv in strlist:
                    if nv == 'end':
                        continue
                    nvlist = nv.split('=')
                    if len(nvlist) !=2:
                        err = -1
                        break
                    print(nvlist[0],nvlist[1])
                    if nvlist[0]=='get' or nvlist[0]=='set' or nvlist[0]=='cfg':
                        op = nvlist[0]
                        op_id = nvlist[1]
                    elif nvlist[0]=='target':
                        target = nvlist[1]
                    elif nvlist[0]=='act':
                        act = nvlist[1]
                    elif nvlist[0]=='data':
                        data = nvlist[1]
                    elif nvlist[0]=='recg_period':
                        recg_period_val = nvlist[1]
                    elif nvlist[0]=='img_upload_period':
                        img_upload_period = nvlist[1]    
                    elif nvlist[0]=='img_upload_time':
                        img_upload_time = nvlist[1]     
                print('WebCtl: Parse Result:op_id=[{}],target=[{}],act=[{}],recg_period=[{}],img_upload_period=[{}],img_upload_time=[{}],data=[{}]'.format(op_id,target,act,\
                        recg_period,img_upload_period,img_upload_time,data))
                #print('gateway_id:',gateway_id,'node_id:',node_id)
                if err != 0:
                    print('WebCtl: error ({})!'.format(err))
                    continue

                if (op == 'get' or op == 'set'):
                    if target == '':
                        resp='WebCtl: target empty!{}:{}'.format(target, err)
                        print(resp)
                        self.webctl_client.send(str.encode(resp))
                        continue
                    gwnd = target
                    
                    if (op == 'set') and (act =='1201'):
                        ### 广播固件，查找socket
                        find_socket = 0
                        socket = 0
                        for gwnd_i, socket_i in list(self.gwnd_socket_dict.items()):
                            if gwnd_i[0:8] == gwnd[0:8]:
                                find_socket = 1
                                socket = socket_i
                        if find_socket != 1 or socket == 0:
                            print('WebCtl: socket invalid,({})!'.format(gwnd))
                            continue
                    else:
                        if gwnd not in self.gwnd_socket_dict:
                            print('WebCtl: socket not found,({})!'.format(gwnd))
                            continue
                        socket = self.gwnd_socket_dict[gwnd]

                        if socket == 0:
                            print('WebCtl: socket invalid,({})!'.format(gwnd))
                            continue

                        if gwnd not in self.gwnd_autowork_dict:
                            resp='WebCtl: {} not found!'.format(gwnd)
                            print(resp)
                            self.webctl_client.send(str.encode(resp))
                            continue
                    auto_flag = 0 #非自动控制
                    #备份并设置自动工作停止标识
                    if not ((op == 'set') and (act =='1201')):
                        autowork_restore = self.gwnd_autowork_dict[gwnd]
                        self.gwnd_autowork_dict[gwnd] = 0
                    lmiId=''
                    print(op, act)
                    if op == 'get' and act[0:2] =='01':
                        (cont_id,cont_cmd) = (act[0:2],act[2:])
                        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
                        print('WebCtl: 查询状态',flag,res.hex().upper())
                        if flag == 1:
                            resp='{}:{}'.format(op_id, 'OK')
                        else:
                            resp='{}:{}'.format(op_id, 'ERR')
                        print(resp)
                        self.webctl_client.send(str.encode(resp))
                    elif op == 'set' and ( act[0:4] =='0201' or act[0:4] =='0202' ):
                        (cont_id,cont_cmd) = (act[0:2],act[2:])
                        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
                        print('WebCtl: 单点控制',flag,res.hex().upper())
                        if flag == 1:
                            resp='{}:{}'.format(op_id, 'OK')
                        else:
                            resp='{}:{}'.format(op_id, 'ERR')
                        print(resp)
                        self.webctl_client.send(str.encode(resp))
                    elif op == 'set' and act =='020300':
                        print('WebCtl: 开始图像识别(拍照+获取识别结果)')
                        flag,res = self.do_a_task_02(auto_flag, gwnd, socket)
                        if flag == 1:
                            flag,res = self.do_a_task_03(auto_flag, gwnd, socket)
                        if flag == 1:
                            flag,res = self.do_a_task_04(auto_flag, gwnd, socket)
                        if flag == 1:
                            flag,res = self.do_a_task_05(auto_flag, gwnd, socket)
                        if flag == 1:
                            flag,res,lmiId = self.do_a_task_06(auto_flag, gwnd, socket)
                        print('WebCtl: 完成图像识别(拍照+获取识别结果)',flag,res.hex().upper())
                        if flag == 1:
                            resp='{}:{}'.format(op_id, 'OK')
                        else:
                            resp='{}:{}'.format(op_id, 'ERR')
                        print(resp)
                        self.webctl_client.send(str.encode(resp))
                    elif op == 'set' and act =='041400':
                        print('WebCtl: 开始上传参考图(拍照+获取识别结果+图像上传)')
                        flag,res = self.do_a_task_02(auto_flag, gwnd, socket)
                        if flag == 1:
                            flag,res = self.do_a_task_03(auto_flag, gwnd, socket)
                        if flag == 1:
                            flag,res = self.do_a_task_04(auto_flag, gwnd, socket)
                        if flag == 1:
                            flag,res = self.do_a_task_05(auto_flag, gwnd, socket)
                        if flag == 1:
                            flag,res,lmiId = self.do_a_task_06(auto_flag, gwnd, socket)
                        if flag == 1:
                            flag,res = self.do_a_task_07(auto_flag, gwnd, socket, res, lmiId)
                        print('WebCtl: 完成上传标准图(拍照+获取识别结果+图像上传)',flag,res.hex().upper())
                        if flag == 1:
                            resp='{}:{}'.format(op_id, 'OK')
                        else:
                            resp='{}:{}'.format(op_id, 'ERR')
                        print(resp)
                        self.webctl_client.send(str.encode(resp))
                    elif op == 'set' and act =='0304':
                        print('WebCtl: 开始下发模板')
                        md_str_len = 96 * 2
                        if len(data) == 0 or len(data) > md_str_len:
                            resp='WebCtl: data is invalid, length={}(expect:192), node={}'.format(len(data), gwnd)
                            print(resp)
                            self.webctl_client.send(str.encode(resp))
                        elif len(data) < md_str_len:
                            pad_data = ['0' for i in range(md_str_len - len(data))]
                            pad_str = ''.join(pad_data) 
                            data = data + pad_str
                        flag,res = self.do_a_task_08(auto_flag, gwnd, data, socket)
                        print('WebCtl: 完成下发模板',flag, res.hex().upper())
                        if flag == 1:
                            resp='{}:{}'.format(op_id, 'OK')
                        else:
                            resp='{}:{}'.format(op_id, 'ERR')
                        print(resp)
                        self.webctl_client.send(str.encode(resp))
                    elif op == 'set' and act =='1201':
                        target = target[0:8] + '0000FFFF'  # 广播
                        self.fw_upgrade_para=[auto_flag,target, data, socket]
                        if self.start_to_fw_upgrade == 0:
                            resp='{}:{}'.format(op_id, 'OK')
                        else:
                            resp='{}:{}'.format(op_id, 'ERR')
                        print(resp)
                        self.start_to_fw_upgrade = 1
                        self.webctl_client.send(str.encode(resp))
                        #self.do_upgrade(auto_flag, target, data, socket)
                    elif op == 'set' and act =='0204':
                        self.gwnd_wakeupInterval_dict[gwnd] = int(data)
                        print('Assign value:{}'.format(self.gwnd_wakeupInterval_dict[gwnd]))
                        resp='{}:{}'.format(op_id, 'OK')
                        print(resp)
                        self.webctl_client.send(str.encode(resp))
                        
                    #恢复自动工作标识
                    if not ((op == 'set') and (act =='1201')):
                        self.gwnd_autowork_dict[gwnd] = autowork_restore
                elif op == 'cfg': 
                    if act[0:3] == 'ADD' or act[0:3] == 'DEL':
                        print('update_own_devices()!')
                        self.update_own_devices(self.own_devices_dict, act)
                        self.save_own_devices(self.own_devices_dict)
                        self.own_devices_dict = self.read_own_devices()     
                        for gateway_id in list(self.own_devices_dict.keys()):
                            for node_id in self.own_devices_dict[gateway_id]:
                                gwnd = gateway_id+node_id
                                if act[0:3] == 'ADD':
                                    self.white_list.append(gwnd)
                                    self.gwnd_autowork_dict[gwnd] = 1
                                else:
                                    if gwnd in self.white_list:
                                        self.white_list.remove(gwnd)
                                    self.gwnd_autowork_dict[gwnd] = 0
                        self.white_list = list(set(self.white_list))
                        print('self.white_list:',self.white_list)
                        print('self.gwnd_autowork_dict:',self.gwnd_autowork_dict)
                        resp='{}:{}'.format(op_id, 'OK')
                        print(resp)
                        self.webctl_client.send(str.encode(resp))
                    if act[0:3] == 'STA' or act[0:3] == 'STP':
                        print('{},update_devices_autowork()!'.format(act[0:3]))
                        flag = self.update_devices_autowork(self.gwnd_autowork_dict, act)
                        print('self.gwnd_autowork_dict:',self.gwnd_autowork_dict)
                        if flag > 0:
                            resp='{}:{}'.format(op_id, 'OK')
                        else:
                            resp='{}:{}'.format(op_id, 'ERR')
                        print(resp)
                        self.webctl_client.send(str.encode(resp))

    def thread_helper(self):
        (timer1, timer2) = (0, 0)
        while True:
            ##定期输出图片数：
            time.sleep(10)
            timer1 = timer1 + 10
            timer2 = timer2 + 10
            if timer1 >= 120:
                print('---------------------------------------------')
                print('当前({})共上传图片数统计如下：'.format(gettm()))
                i = 0
                total = 0
                for gwnd in self.gwnd_piccnt_dict:
                    i = i + 1
                    total = total + self.gwnd_piccnt_dict[gwnd]
                    print('[{}]终端{}上传了{}张图片。(状态: {})'.format('%03d'%i, gwnd, \
                            '%04d'%self.gwnd_piccnt_dict[gwnd],self.gwnd_status_dict[gwnd]))
                print('总计：{}张。'.format(total))
                print('---------------------------------------------')
                timer1 = 0
            ### 日志每3小时新建文件
            if timer2 >= 10800:
                if self.debug_level > 1:
                    self.log_file = self.log_dir+'/log_'+datetime.datetime.now().strftime('%Y%m%d%H%M')+'.txt'
                    print('日志保存中：{} ...'.format(self.log_file))
                    self.stdout_bak = sys.stdout
                    sys.stdout.close()
                    sys.stdout = open(self.log_file,'w')
                timer2 = 0
                
            ### web 更新FW
            if self.start_to_fw_upgrade == 1:
                self.start_to_fw_upgrade = 2
                print('固件升级参数：')
                print(*self.fw_upgrade_para)
                self.do_upgrade(*self.fw_upgrade_para)
                self.start_to_fw_upgrade = 0

    ### 入库操作，访问很频繁，这里使用mysql pool，线程安全，提升系统性能
    def mysql_excute(self, mysql):
        result=''
        if self.mysql_enable:
            try:
                conn = self.mysql_pool.connection()
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                result = cursor.execute(mysql)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print('mysql excute err!',e)
                print('sql [{}] -> result:[{}]'.format(mysql, result))
            return result

    ### 开始工作了
    def run(self):
        """运行"""
        ### 开启webctl接口线程
        tr = threading.Thread(target=self.webctl_rx, args=())
        tr.start()
        ts = threading.Thread(target=self.webctl_tx, args=())
        ts.start()
        td = threading.Thread(target=self.thread_helper, args=())
        td.start()        
        while True:
            ### 等待集中器连接
            client_socket, client_addr = self.server_socket.accept()
            if client_socket in list(self.socket_status_dict.values()):
                print('socket {}已存在,不创建线程!'.format(client_socket))
                continue
            client_socket.settimeout(1800)
            print("\n集中器上线通知: 时间：[{}], socket：[{}]！".format(gettm(), client_socket))          
            self.socket_txlock_dict[client_socket] = threading.Lock()
            self.socket_status_dict[client_socket] = 1
            ### socket TX线程
            ts = threading.Thread(target=self.thread_send_to_gateway, args=(client_socket,))
            ts.start()
            ### socket RX线程
            tr = threading.Thread(target=self.thread_recv_from_gateway, args=(client_socket,))
            tr.start()
        self.server_socket.close()

    ### 接收线程，处理网关来的数据
    def thread_recv_from_gateway(self, client_socket):
        while True:
            try:
                rx_data = client_socket.recv(1024)
                self.print_hex(rx_data, 0, ' ')
                #print('rx_data=',rx_data.hex().upper())
                if rx_data:
                    rx_data_hex=rx_data.hex().upper()
                    if len(rx_data_hex) <= 54:
                        cont_data=b''
                    else:
                        cont_data=rx_data_hex[54:]
                        ### 上行数据，检查crc16是否正确,不匹配则忽略该条数据
                        cont_crc16 = cont_data[-4:]  #自带的crc16
                        calc_crc16 = self.crc16_xmodem_be(bytes.fromhex(cont_data[0:-4]))  #计算的crc16
                        if cont_crc16 != calc_crc16:
                            print('丢弃: CRC16错误, 收到:',cont_crc16,'计算:',calc_crc16)
                            continue

                    ### 除了网关心跳包外，从集中器收到的来自节点的数据都缓存到queue里面给发送线程用
                    gwnd = rx_data[2:10].hex().upper()
                    ### 包类型判断
                    if rx_data[0:2].hex().upper() == '0101': #注册包
                        self.gwnd_socket_dict[gwnd] = client_socket
                        print("注册包来自节点:",gwnd)
                        if gwnd not in list(self.gwnd_status_dict.keys()):
                            self.gwnd_cycle_end_dict[gwnd] = datetime.datetime.now()  # cycle结束赋初值
                        if gwnd not in list(self.gwnd_status_dict.keys()) or self.gwnd_status_dict[gwnd] == 'OFF':
                            self.gwnd_status_dict[gwnd] = 'REG'
                            ### 对于485透传，若node id第一位是FF，修改gwnd前4字节为MAC地址的后4字节
                            if gwnd[8:10] == 'FF':
                                print('get MAC info..')
                                arp_info = ''
                                arp_info = arpreq.arpreq(client_socket.getpeername()[0])
                                mac_4B = '00000000'
                                #MAC地址17字节显示
                                if len(arp_info) == 17:
                                    mac_4B = (arp_info[6:8] + arp_info[9:11] + arp_info[12:14] + arp_info[15:17]).upper()
                                    print('RS485终端：MAC (4B)：', mac_4B)
                                    gw = gwnd[0:8]
                                    self.vgw_rgw_dict[gw] = mac_4B
                                else:
                                    print('Invalid MAC info:' + arp_info)
                        if gwnd[8:10] == 'FF':
                            ### 对于485透传，回应注册包:集中器ID+节点ID+长度(5)+命令(6)+内容长度(1)+内容(1)+CRC16
                            calc_crc16 = self.crc16_xmodem_be(bytes.fromhex('060101'))
                            response =  rx_data[2:10]+ bytes.fromhex('05060101') + bytes.fromhex(calc_crc16)
                            print('回应注册包：{}, 延时{}ms..'.format(response.hex().upper(),self.reg_resp_delay))
                            if self.reg_resp_delay > 0:
                                time.sleep(self.reg_resp_delay/1000)
                            client_socket.send(response)
                        self.gateway_status_dict[gwnd[0:8]] = 1      
                    elif rx_data[0:2].hex().upper() == '0103': #数据包
                        #self.socket_rxqueue_dict[client_socket].put(rx_data)
                        if self.data_recv_delay > 0:
                            print('接收数据包,延时处理{}ms..'.format(self.data_recv_delay))
                            time.sleep(self.data_recv_delay/1000)
                        if gwnd in list(self.gwnd_rxqueue_dict):
                            self.gwnd_rxqueue_dict[gwnd].put(rx_data)

                    if self.mysql_enable:
                        now_ms = gettm_ms()
                        now = gettm()
                        if rx_data_hex[30:32] == '00':
                            rssi = 0 - int(rx_data_hex[28:30],16)
                        else:
                            rssi = int(rx_data_hex[28:30],16)
                        if gwnd[0:8] in list(self.vgw_rgw_dict):
                            print('转换成功:{}->{}.'.format(gwnd, self.vgw_rgw_dict[gwnd[0:8]] + gwnd[8:16]))
                            gwnd = self.vgw_rgw_dict[gwnd[0:8]] + gwnd[8:16]
                        gateway_url = 'http://'+ client_socket.getpeername()[0]
                        mysql='UPDATE lora_terminal SET networkType=\'{}\',meterType=\'{}\',channelId=\'{}\',snr=\'{}\',rssi=\'{}\',runStatus=\'{}\',status=\'{}\',modifierId=\'{}\',modifier=\'{}\',modifyTime=\'{}\' where gatewayId=\'{}\' and terminalId=\'{}\';'.format('2',gwnd[10:12],int(rx_data_hex[24:26],16), int(rx_data_hex[26:28],16), rssi, '1', '0',now_ms, 'server',now, gwnd[0:8],gwnd[8:16])
                        #print('[{}]\n'.format(mysql))
                        result = self.mysql_excute(mysql)
                        if result == 0 or result == '':
                            mysql='INSERT INTO `lora_terminal` VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format(now_ms,gwnd[0:8],gwnd[8:16],'2', gwnd[10:12],int(rx_data_hex[24:26],16),int(rx_data_hex[26:28],16),rssi,'','','1','0','','智能抄表终端',now_ms,'server',now,now_ms,'server',now)
                            result = self.mysql_excute(mysql)
                        mysql='UPDATE lora_gateway SET runStatus=\'{}\', modifierId=\'{}\', modifier=\'{}\', modifyTime=\'{}\' where gatewayId=\'{}\';'.format('1', now_ms, 'server', now, gwnd[0:8])
                        result = self.mysql_excute(mysql)
                        if result == 0 or result == '':
                            mysql='INSERT INTO `lora_gateway` VALUES (\'{}\',\'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format(now_ms, gwnd[0:8], '', client_socket.getpeername()[0], client_socket.getpeername()[1],'1', gateway_url, 'LoRa集中器','1', '0', now_ms, 'server', now,now_ms,'server', now)
                            result = self.mysql_excute(mysql)

                    
                    ###数据入库,调试才使用
                    if self.mysql_enable == 2:
                            mysql="insert into tb_report (record_time, protocol_ver,protocol_id,gateway_id,node_id,node_sid,node_channel,node_snr,node_rssi,node_nc,node_timestap,node_normal,node_alive_num,node_data_len,node_data) values (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"%(gettm_ms(),rx_data_hex[0:2],rx_data_hex[2:4],rx_data_hex[4:12],rx_data_hex[12:20],rx_data_hex[20:24],rx_data_hex[24:26],rx_data_hex[26:28],rx_data_hex[28:32],rx_data_hex[32:36],rx_data_hex[36:44],rx_data_hex[44:46],rx_data_hex[46:50],rx_data_hex[50:54],cont_data)
                            #result=self.db.executedata(mysql_inset)
                            if self.mysql_lock_enable:
                                with self.mysql_lock:
                                    result = self.mysql_excute(mysql)
                            else:
                                result = self.mysql_excute(mysql)
                else:
                    ### 客户端断开连接
                    now_ms = gettm_ms()
                    now = gettm()
                    geteway = ''
                    print("\n集中器掉线通知：{}, {}！".format(client_socket, now_ms))
                    self.socket_status_dict[client_socket] = 0
                    client_socket.close()
                    ### 状态切换为OFF
                    for gwnd_val, socket_val in list(self.gwnd_socket_dict.items()):
                        if socket_val == client_socket:
                            print('Offline,1:',gwnd_val)
                            self.gwnd_socket_dict[gwnd_val] = 0
                            self.gwnd_status_dict[gwnd_val] = 'OFF'
                            geteway = gwnd_val[0:8]
                    mysql='UPDATE lora_gateway SET runStatus=\'{}\', modifierId=\'{}\', modifier=\'{}\', modifyTime=\'{}\' where gatewayId=\'{}\';'.format('0', now_ms, 'server', now, geteway)
                    result = self.mysql_excute(mysql)
                    break
            except error:
                ### 状态切换为OFF
                geteway = ''
                for gwnd_val, socket_val in list(self.gwnd_socket_dict.items()):
                    if socket_val == client_socket:
                        print('Offline,2:',gwnd_val,socket_val)
                        self.gwnd_socket_dict[gwnd_val] = 0
                        self.gwnd_status_dict[gwnd_val] = 'OFF'
                        geteway = gwnd_val[0:8]
                print("集中器断开:socket recv() close/timeout:{}".format(client_socket))
                now_ms = gettm_ms()
                now = gettm()
                mysql='UPDATE lora_gateway SET runStatus=\'{}\', modifierId=\'{}\', modifier=\'{}\', modifyTime=\'{}\' where gatewayId=\'{}\';'.format('0', now_ms, 'server', now, geteway)
                result = self.mysql_excute(mysql)
                self.socket_status_dict[client_socket] = 0
                client_socket.close()
                break    


    ### 下发命令回应
    def cmd_response(self, gwnd):
        n = 0
        response = b''
        ### 获取不到节点返回，超时（200x10ms为2秒）
        while n < self.RTO_max:
            try:
                #socket = self.gwnd_socket_dict[gwnd]
                #if socket != 0:
                #    response = self.socket_rxqueue_dict[socket].get_nowait()
                if gwnd in list(self.gwnd_rxqueue_dict):
                    response = self.gwnd_rxqueue_dict[gwnd].get_nowait()
            except :# self.socket_rxqueue_dict[socket].Empty:
                #print('socket_rxqueue_dict empty!')
                time.sleep(0.01)
                n = n + 1
            else:
                #print('** Response Detect!')
                if len(response) > 0:
                    if response[0] == '0x01' and response[1] == '0x01':
                        ### 过滤心跳包
                        continue
                    else:
                        #print('got:',response)
                        #time.sleep(0.01)
                        break
                else:
                    break
        return response

    ### 下发命令(socket)
    def cmd_dispatch(self, gwnd, socket, data):
        flag = 0
        try:
            self.print_hex(data, 1, gwnd)
            if socket != 0:
                socket.send(data)
        except error:
            flag = -1
            if socket in self.socket_status_dict:
                self.socket_status_dict[socket] = 0
            if socket != 0:
                socket.close()
            print('ERROR: socket send() error: gwnd={},data={}'.format(gwnd, data.hex().upper()))
        #print(gettm(),': send to ',client_addr)
        #time.sleep(5) #测试用
        return flag


    ### 下发命令，等待回应，返回状态（-1：网络错误（终端不回），
    ### 0：无响应（终端不回），1：完成（终端回），2：忙（终端回），3:异常（终端回））和数据
    def send_no_wait(self, gwnd, socket, tx_array):
        flag = 0
        result = b''
        ###socket = self.gwnd_socket_dict[gwnd]
        if socket in list(self.socket_txlock_dict.keys()):
            self.socket_txlock_dict[socket].acquire()    #加锁
        else:
            print("send_wait(): The socket lock for the node not found:[{}],[{}],[{}]".format(gwnd,socket,self.socket_txlock_dict))
            flag = -1
            return flag,result
        if self.cmd_dispatch(gwnd, socket, tx_array) == 0:
            flag = 1
        if socket in list(self.socket_txlock_dict.keys()):
            self.socket_txlock_dict[socket].release()
        return flag,result

    def broadcast_common(self, auto_flag, gwnd, socket, cont_id, cont_cmd):
        flag = 0
        result = b''
        #print(cont_id, cont_cmd)
        tx = pro_tx_data()
        tx.gw_id = gwnd[0:8]                                          #如:'25A88D03'
        tx.node_id = gwnd[8:16]
        tx.node_ver = tx.node_id[0:2]
        tx.node_type = tx.node_id[2:4]
        tx.node_sid = tx.node_id[4:8]                                 #如:'0001'
        tx.pro_cont_data_id = cont_id
        tx.pro_cont_data = tx.pro_cont_data_id+'%02X'%(len(cont_cmd)>>1)+ cont_cmd  #如：单点查询 01 01 01
        tx.pro_cont_data_crc = self.crc16_xmodem_be(bytes.fromhex(tx.pro_cont_data))
        #print(len(tx.pro_cont_data+tx.pro_cont_data_crc)>>1)
        tx.pro_cont_data_len = '%02X'%(len(tx.pro_cont_data+tx.pro_cont_data_crc)>>1)
        l=tx.pro_cont_data_len
        #print(tx.pro_cont_data+tx.pro_cont_data_crc)
        if l != '05' and l != '06' and l != '07' and l != '09' and l != 'BE':
            print('tx data error! len:', l)
            return flag,result
        tx_hex=tx.pack_data()
        tx_array=bytes().fromhex(tx_hex)
        flag,result = self.send_no_wait(gwnd, socket, tx_array)
        return flag, result


    ### 下发命令，等待回应，返回状态（-1：网络错误（终端不回），
    ### 0：无响应（终端不回），1：完成（终端回），2：忙（终端回），3:异常（终端回））和数据
    def send_wait(self, gwnd, socket, tx_array):
        flag = 0
        result = b''
        ###socket = self.gwnd_socket_dict[gwnd]
        if socket in list(self.socket_txlock_dict.keys()):
            self.socket_txlock_dict[socket].acquire()    #加锁
        else:
            print("send_wait(): The socket lock for the node not found:[{}],[{}],[{}]".format(gwnd,socket,self.socket_txlock_dict))
            flag = -1
            return flag,result
        if self.cmd_dispatch(gwnd, socket, tx_array) == 0:
            result=self.cmd_response(gwnd)
            #print(result,' 27->',result[27],' 29->',result[29],' 30->',result[30])
            #print(tx_array,' 9->',tx_array[9]+0x80,' 11->',tx_array[11])
            ### (1)匹配应用协议类型ID 和 内容ID
            if result != b'' and len(result)>30 and result[27]==(tx_array[9]+0x80) and result[29]==tx_array[11]:
                #一般情况下，状态读取这个数据
                flag = result[30] #状态
                ### (2)例外，对于补光灯控制，都是完成
                if result[27]== 0x82 and result[29] == 0x01:
                    #print('warning: 8201')
                    flag = 1
                ### (3)例外，对于实时拍照回复, 0x01和0x11都是应答
                if result[27]== 0x82 and result[29] == 0x02:
                    if result[28] == 0x01 or result[28] == 0x11:
                        flag = 1
                        #print('warning: 8202')
                ### (4)例外，对于单点数据回复,都是应答
                if result[27]== 0x84:
                    #print('warning: 84')
                    flag = 1
                #print('cmd_response OK.');
            else:
                if result == b'':
                    print('[{}]:{} no response.'.format(gettm(),gwnd))
                elif len(result) <=30:
                    print('丢弃:length less 30')
                else:
                    print('result=',result.hex().upper())
                    print('丢弃:'+'%02X'%(result[27]),'应为','%02X'%(tx_array[9]+0x80), \
                            'or', '%02X'%(result[29]),'应为','%02X'%(tx_array[11]))
                result = b''  #丢弃此包
                flag = 0     #无响应
        else:
            print('发送失败')
            flag = -1  #发送,Socket失败

        if socket in list(self.socket_txlock_dict.keys()):
            self.socket_txlock_dict[socket].release()    #解锁
        #print('send_wait:',flag,result)
        return flag,result

    def unicast_common(self, auto_flag, gwnd, socket, cont_id, cont_cmd):
        flag = 0
        result = b''
        #维护时，不自动管理
        if auto_flag == 1 and self.gwnd_autowork_dict[gwnd] != 1:
            flag = -2
            return flag,result
        if self.gwnd_status_dict[gwnd] == 'OFF':
            flag = -1
            return flag,result
        #print(cont_id, cont_cmd)
        tx = pro_tx_data()
        tx.gw_id = gwnd[0:8]                                          #如:'25A88D03'
        tx.node_id = gwnd[8:16]
        tx.node_ver = tx.node_id[0:2]
        tx.node_type = tx.node_id[2:4]
        tx.node_sid = tx.node_id[4:8]                                 #如:'0001'
        tx.pro_cont_data_id = cont_id
        tx.pro_cont_data = tx.pro_cont_data_id+'%02X'%(len(cont_cmd)>>1)+ cont_cmd  #如：单点查询 01 01 01
        tx.pro_cont_data_crc = self.crc16_xmodem_be(bytes.fromhex(tx.pro_cont_data))
        #print(len(tx.pro_cont_data+tx.pro_cont_data_crc)>>1)
        tx.pro_cont_data_len = '%02X'%(len(tx.pro_cont_data+tx.pro_cont_data_crc)>>1)
        l=tx.pro_cont_data_len
        #print(tx.pro_cont_data+tx.pro_cont_data_crc)
        if l != '05' and l != '06'  and l != '07' and l != '09' and l != 'BE':
            print('tx data error! len:',tx.pro_cont_data_len)
            return flag,result
        tx_hex=tx.pack_data()
        tx_array=bytes().fromhex(tx_hex)
        flag,result = self.send_wait(gwnd, socket, tx_array)
        #重试5次(加上第一次共6次)
        retry = 0
        sleep_n = 1
        for i in range(1,6):
            #维护时，不自动管理
            if auto_flag == 1 and self.gwnd_autowork_dict[gwnd] != 1:
                flag = -2
                break
            #print('result={},flag={}'.format(result,flag))
            if result == b'' and flag != -1:
                retry = retry + 1
                sleep_n = sleep_n * 2
                time.sleep(sleep_n)
                print('{}: send_wait() retry {} (slept {}s)...'.format(gwnd,i,sleep_n))
                flag,result = self.send_wait(gwnd, socket, tx_array)
            else:
                break
        if result == b'':
            if retry == 5:
                if self.RTO_fail_exit == 1:
                    flag = -1
                    print('{}: reconnection failed 5 times, exit!'.format(gwnd))
                else:
                    flag = 0
                    print('{}: reconnection failed 5 times, continue!'.format(gwnd))
            print('{}: send_wait() timeout.'.format(gwnd))
        return flag, result


    def do_a_task_01_old(self, auto_flag, gwnd, socket):
        print('【1】系统状态查询',gwnd)
        (cont_id,cont_cmd) = ('01','01')
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('系统状态查询:终止，err={},节点{}。'.format(flag, gwnd))
        return flag,res

    def do_a_task_01(self, auto_flag, gwnd, socket):
        print('【1】系统信息查询',gwnd)
        (cont_id,cont_cmd) = ('04','1000000001')
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag == 1:
            VAL_OFFSET=35
            # 描述信息
            ver_desc = to_ascii(res[VAL_OFFSET:VAL_OFFSET+32].hex())
            print('{}:版本信息:[{}]'.format(gwnd, ver_desc))
            # 电池信息
            temp = int().from_bytes(res[VAL_OFFSET+53:VAL_OFFSET+54], byteorder='big')/100
            if temp > 0:
                battery = '%0.2fV'%round(2 + temp, 2)
            else:
                battery = ''
            if self.lowpower_wakeup_enable == 1:
                print('电池电压:{}.'.format(battery))
            wakeup_interval_r = int().from_bytes(res[VAL_OFFSET+54:VAL_OFFSET+55], byteorder='big')
            if(wakeup_interval_r > 200):
                wakeup_interval_txt = '{}分钟'.format(wakeup_interval_r-200)
            elif(wakeup_interval_r >0):
                wakeup_interval_txt = '{}天'.format(wakeup_interval_r)
            else:
                wakeup_interval_txt = ''

            if self.lowpower_wakeup_enable == 1:
                print('低功耗唤醒周期:{},即[{}]。'.format(wakeup_interval_r, wakeup_interval_txt))
            now_ms = gettm_ms()
            now = gettm()
            if self.lowpower_wakeup_enable == 1:
                mysql='UPDATE lora_terminal SET `describe`=\'{}\',version=\'{}\', battery=\'{}\', wakeupInterval=\'{}\', modifierId=\'{}\',modifier=\'{}\',modifyTime=\'{}\' where gatewayId=\'{}\' and terminalId=\'{}\';'.format('智能抄表终端', ver_desc, battery, wakeup_interval_txt, now_ms, 'server',now, gwnd[0:8],gwnd[8:16])
            else:
                mysql='UPDATE lora_terminal SET `describe`=\'{}\' modifierId=\'{}\',modifier=\'{}\',modifyTime=\'{}\' where gatewayId=\'{}\' and terminalId=\'{}\';'.format('终端'+ver_desc, now_ms, 'server',now, gwnd[0:8],gwnd[8:16])
            result = self.mysql_excute(mysql)
            print(mysql,'result:',result)
        else:
            print('系统状态查询:终止，err={},节点{}。'.format(flag, gwnd))
        return flag,res

    def do_a_task_02(self, auto_flag, gwnd, socket):
        # pass
        print('【2】开始拍照',gwnd)
        (cont_id,cont_cmd) = ('02','0201')
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('开始拍照:终止，err={},节点{}。'.format(flag, gwnd))
        return flag,res

    def do_a_task_03(self, auto_flag, gwnd, socket):
        # pass
        time.sleep(5)#等待拍照执行
        print('【3】查询拍照',gwnd)
        (cont_id,cont_cmd) = ('01','02')
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('查询拍照:终止，err={},节点{}。'.format(flag, gwnd))
        return flag,res

    def do_a_task_04(self, auto_flag, gwnd, socket):
        # pass
        print('【4】开始识别',gwnd)
        (cont_id,cont_cmd) = ('02','0300')
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('开始识别:终止，err={},节点{}。'.format(flag, gwnd))
        return flag,res
                
    def do_a_task_05(self, auto_flag, gwnd, socket):
        # pass
        time.sleep(15)#等待识别执行,给20s时间
        print('【5】查询识别结束',gwnd)
        (cont_id,cont_cmd) = ('01','03')
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('查询识别结束:终止，err={},节点{}。'.format(flag, gwnd))
        return flag,res


    def do_a_task_06(self, auto_flag, gwnd, socket):
        print('【6】获取识别结果',gwnd)
        lmiId = ''
        outer_result = '?'
        inner_result = '?'
        (cont_id,cont_cmd) = ('04','1200000001')
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('获取识别结果:终止，err={},节点{}。'.format(flag, gwnd))
        else:
            img_reg_flag = int.from_bytes(res[47:48], byteorder='big', signed=False) 
            algVer =  int.from_bytes(res[56:58], byteorder='big', signed=False) 
            modVer =  int.from_bytes(res[58:60], byteorder='big', signed=False)
            #水表类型：01 指针表， 02 数字表
            meter_type = gwnd[10:12]
            #print('meter_type={}'.format(meter_type))
            if meter_type == '01':
                outer_bytes = res[60:64]
                inner_bytes = res[64:68]
                outer_result = round(struct.unpack('>f', struct.pack('4B', *outer_bytes))[0], 2)
                inner_result = round(struct.unpack('>f', struct.pack('4B', *inner_bytes))[0], 2)
            elif meter_type == '02':
                num_len = int(res[60:61].hex(),16)
                #print("num_len={},{},{}".format(num_len,res[60:61], res[61:61+num_len]))
                if num_len > 0 and num_len < 10:
                    outer_result = res[61:61+num_len].decode("utf-8")
                    inner_result = outer_result
            log = '{}: 节点：{}, 识别标记：{}, 算法版本：{}, 模型版本：{}, 外圈读数：{}, 内圈读数：{}。\n'.format(gettm(),\
            gwnd, img_reg_flag, algVer, modVer, outer_result, inner_result)
            print(log)
            with self.file_lock:
                with open(self.log_dir + '/'+'识别结果.log', "a") as f:
                    f.write(log)
            if self.mysql_enable:
                lmiId = gettm_ms()
                now = gettm()
                mysql='INSERT INTO `lora_meter_identify` VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format(lmiId,\
                gwnd[0:8], gwnd[8:16], img_reg_flag, inner_result, outer_result, modVer, '0', now)
                result = self.mysql_excute(mysql)
        return flag,res,lmiId

    def do_a_task_07(self, auto_flag, gwnd, socket, res, lmiId):
        print('【7】获取参考图',gwnd)
        #<1B>(查询数据ID,29-30) + <4B>(帧序号，此时为1,30-34) + <1B>(len=31,34-35) 
        #+ <180B>(31字节摘要信息 + 149字节补0)；
        #摘要:<8B>(时间35-43)+<4B>(大小43-47) + <1B>(识别标记：0不用，1未识别，2已识别47-48)
        #+ <4B>(总帧数48-52) + <4B>(CRC32(文件内容)52-65) + <10B>(识别结果内容，若无补0x00)
        N_VAL_OFFSET=48
        n=int(res[N_VAL_OFFSET:N_VAL_OFFSET+4].hex(),16)
        #gwnd=res[2:10].hex().upper()
        TIME_VAL_OFFSET = 35
        SIZE_VAL_OFFSET = 43
        file_timestap=res[TIME_VAL_OFFSET:TIME_VAL_OFFSET + 8].hex().upper()
        file_size=int(res[SIZE_VAL_OFFSET:SIZE_VAL_OFFSET + 4].hex().upper(), 16)
        print('file_size:',file_size)
        file_data=b''
        i = 2
        img_type = 1
        flag = 0
        retry_c = 0
        while i <= n:
            (cont_id,cont_cmd) = ('04','12%08X'%i)
            flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
            if flag != 1:
                print('获取参考图:终止，err={},节点{}。'.format(flag, gwnd))
                break
            FRAME_LEN=217
            if len(res) != FRAME_LEN:
                flag = 0  #非1，重新开始
                print('图片帧长度{}错误！'.format(len(res)))
                break
            FRAME_NO_VAL_OFFSET = 30
            frame_no = int(res[FRAME_NO_VAL_OFFSET:FRAME_NO_VAL_OFFSET + 4].hex().upper(), 16)
            #print('frame no:', res[FRAME_NO_VAL_OFFSET:FRAME_NO_VAL_OFFSET + 4].hex().upper())
            if frame_no != i :
                retry_c += 1
                if retry_c < 3:
                    print("图片帧序号{}错误{}次，重传。".format(frame_no, retry_c))
                    continue
                else:
                    flag = 0 #非1，重新开始
                    print("图片帧序号{}错误{}次，中断。".format(frame_no, retry_c))
                    break
            retry_c = 0
            print('{}:正在获取第{}张参考图，完成：{}/{}。'.format(gwnd,self.gwnd_piccnt_dict[gwnd]+1,i,n))
            IMG_DATA_LEN = 180
            LEN_VAL_OFFSET = 34
            IMG_DATA_OFFSET = 35
            data_len = IMG_DATA_LEN
            if res[LEN_VAL_OFFSET] < IMG_DATA_LEN:
                data_len=res[LEN_VAL_OFFSET]
            #print('图片有效数据：',res[35:-2])
            file_data = file_data + res[IMG_DATA_OFFSET:IMG_DATA_OFFSET + data_len]
            if i == n:
                if file_size != len(file_data):
                    flag = 0 #非1，重新开始
                    print("接收图片数据长度错误,，中断。({}/{})".format(len(file_data),file_size))
                    break
                img_id = gettm_ms()
                ymd_str = gettm_ymd()
                img_name_ref = img_id + '.jpg'
                # front-end img
                img_relative_dir_f = self.img_relative_dir_f + '/' + ymd_str + '/' + gwnd
                self.createDir(self.save_root_dir + '/' + img_relative_dir_f)
                img_path_f = self.save_root_dir + '/' + img_relative_dir_f + '/' + img_name_ref
                img_path_f_for_web = img_relative_dir_f + '/'+img_name_ref
                # back-end img
                img_relative_dir_b = self.img_relative_dir_b + '/' + ymd_str + '/' + gwnd
                self.createDir(self.save_root_dir + '/' + img_relative_dir_b)
                img_path_b = self.save_root_dir + '/' + img_relative_dir_b + '/' + img_name_ref
                img_path_b_for_web = img_relative_dir_b + '/' + img_name_ref

                with open(img_path_f, "wb") as f:
                    f.write(file_data)
                    self.gwnd_piccnt_dict[gwnd] = self.gwnd_piccnt_dict[gwnd] + 1
                    print('{}:[{}]第{}张参考图保存在：{}.'.format(gwnd, gettm_ms(),self.gwnd_piccnt_dict[gwnd], img_path_f))
                #md_txt = './base/default_model.txt'
                #md_jpg = './base/default_model.jpg'
                
                md_txt = self.save_root_dir + '/' + self.model_relative_dir + '/base_' + gwnd + '.txt'
                md_jpg = self.save_root_dir + '/' + self.model_relative_dir + '/base_' + gwnd + '.jpg'
                (err_flag, outer_result, inner_result, IMG) = (0, 0, 0, '')
                if os.path.exists(md_txt) and os.path.exists(md_jpg) and os.path.exists(img_path_f):
                    try:
                        err_flag,outer_result,inner_result,IMG = mr.meter_reader_now(md_txt, md_jpg, img_path_f)
                        print('后台识别：Mark [{}], err_flag=[{}], outer=[{}], inner=[{}], img_path_b =[{}]'.format(img_path_f,err_flag,outer_result,inner_result, img_path_b))
                        cv2.imwrite(img_path_b, IMG)
                    except Exception as e:
                        print('后台识别：错误, err={}'.format(e))
                else:
                    print('后台识别：未识别，模型文件或者待识别图片不存在！[{},{},{}]'.format(md_txt, md_jpg, img_path_f))
                    img_path_b_for_web = ' '
                ###数据入库
                if self.mysql_enable:
                    now_ms = gettm_ms()
                    now = gettm()
                    mysql='INSERT INTO `lora_img_identify` VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', null, \'{}\', \'{}\');'.format(now_ms, gwnd[0:8], gwnd[8:16], img_name_ref, img_path_f_for_web, img_type, img_path_b_for_web, inner_result, outer_result, '1', lmiId, now)
                    result = self.mysql_excute(mysql)
            i = i + 1
            if self.mindelay_in_imgframes > 0:
                time.sleep(self.mindelay_in_imgframes)  #休息1s再获取下一帧
        return flag,res

    def do_a_task_08(self, auto_flag, gwnd, md_96B_data, socket):
        print('【8】下发模板',gwnd)
        #cont_cmd：03 00000001 60 <96B模板数据：如下AA代替> <84个00>
        cont_id = '03'
        pad_data = ['00' for i in range(84)]
        pad_str = ''.join(pad_data) 
        cont_cmd = '040000000160' + md_96B_data + pad_str
        flag, res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('下发模板:终止，err={},节点{}。'.format(flag, gwnd))
        print('下发模板成功,',gwnd)
        return flag,res

    def do_a_task_09(self, auto_flag, gwnd, fw_path, socket, frame_no, cmd_id_no):
        if frame_no == 0xFFFF:
            print('【9】升级固件:',gwnd, cmd_id_no)
        else:
            print('广播遗失帧：{} {} {}'.format(frame_no,gwnd,cmd_id_no))
        # cmd_id_no=1,2,3
        #【1】<1B>(0x01：下发程序，0x02：下发模型one；0x03：下发模型all；) + <4B>(帧序号,此处为1) + #<1B>(有效数据长度，此时为13) + <180B>(13字节摘要信息 + 167字节补0)；
        #其中摘要信息定义为：<1B>(版本号,从1开始) + <4B>(模型字节数) + <4B>(总帧数) + <4B>(CRC32(文件内容))；
        #【2】<1B>(0x01：下发程序;0x02：下发模型one；0x03：下发模型all；) + <4B>(帧序号,从2到N) + #<1B>(有效数据长度，1~180) + <180B>(帧数据)
        #其中N的计算方法：第一帧中有文件大小信息，文件大小按照180字节分拆分的帧数+1。
        if not os.path.exists(fw_path):
            print(fw_path, 'is not exist!')
            return -1,''
        ### 判断是否过了维护期
        if (auto_flag == 1) and (gettm_t2s() >= self.upgrade_end_t):
            print('{}:{} 维护期结束，停止广播。'.format(gettm_ms(),gwnd))
            return -2,''
        flag = 0
        res = ''
        DAT_SIZE = 180
        cont_id = '12'
        pad_167_data = ['00' for i in range(167)]
        pad_167_str = ''.join(pad_167_data)
        fw_size = os.path.getsize(fw_path)
        fw_size_str = '%08X'%fw_size
        N= (fw_size + DAT_SIZE - 1)//DAT_SIZE + 1
        N_str = '%08X'%N
        crc32_str = cal_crc32(fw_path)
        fw_name = os.path.basename(fw_path)
        vi = fw_name.index('V')
        ver = fw_name[vi+1:vi+3]
        cmd_id = '%02X'%cmd_id_no
        print('FW size:{}, N:{}, CRC32:{}.'.format(fw_size, N, crc32_str))
        # 发送摘要信息
        cont_cmd = cmd_id+'00000001'+'0D' + ver + fw_size_str + N_str + crc32_str + pad_167_str
        print(cont_cmd)
        if frame_no == 0xFFFF:
            for i in range(3):
                print('摘要信息发送第{}次：'.format(i+1,fw_path))
                flag, res = self.broadcast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
                time.sleep(2)
        # 发送FW信息
        gwid = gwnd[0:8]
        count_n = 2
        if auto_flag == 0:
            self.gwid_lastBN_dict[gwid] = 0
            self.gwid_lastBF_dict[gwid] = ''
        with open(fw_path, 'rb') as f:
            while True:
                ### 判断是否过了维护期
                if (auto_flag == 1) and (gettm_t2s() >= self.upgrade_end_t):
                    print('{}:{}维护期结束，停止广播。'.format(gettm_ms(),gwnd))
                    break
                buf = f.read(DAT_SIZE)
                if len(buf) == 0:
                    print('{}:{}广播完成 {}。'.format(gettm_ms(), gwnd, fw_path))
                    self.gwid_lastBN_dict[gwid] = 0
                    self.gwid_lastBF_dict[gwid] = ''
                    break
                cmd_id = '%02X'%cmd_id_no
                cont_cmd = cmd_id + '%08X'%count_n + '%02X'%len(buf) + buf.hex().upper()
                if len(buf) != DAT_SIZE:
                    pad_data = ['00' for i in range(DAT_SIZE-len(buf))]
                    pad_str = ''.join(pad_data)
                    cont_cmd = cont_cmd + pad_str
                if (frame_no == 0xFFFF) and (fw_path == self.gwid_lastBF_dict[gwid]) and (count_n < self.gwid_lastBN_dict[gwid] - 500) :
                    pass
                else:
                    if (self.fw_debug_flag == 1) and (count_n == 30):
                        self.fw_debug_flag = 0
                        socket.close()
                    #if (count_n > 800 and count_n < 810) or count_n > 830:
                    if frame_no == 0xFFFF or frame_no == count_n:
                        flag, res = self.broadcast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
                        if flag != 1:
                            if frame_no == 0xFFFF:
                                # 记住上一次发送失败的帧数和文件
                                self.gwid_lastBN_dict[gwid] = count_n
                                self.gwid_lastBF_dict[gwid] = fw_path
                            break
                        time.sleep(self.broadcast_interval/1000)
                        print('完成{}/{}: 当前{}字节,{}, flag={}。'.format(count_n, N, len(buf),fw_path, flag))
                count_n += 1
        if frame_no == 0xFFFF:
            print('{}:{}升级结束。'.format(gettm_ms(),gwnd))
        return flag,res

    #查询完整性
    def do_a_task_10(self, auto_flag, gwnd, socket, type):
        if type != 0x15 and type != 0x16 and type != 0x17:
            print('参数错误：type={}'.format(type))
            return -1,''
        time.sleep(5)#等待执行
        print('【10】查询完整性',gwnd)
        (cont_id,cont_cmd) = ('04', '%02X'%type+'0001')
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('查询完整性:终止，err={},节点{}。'.format(flag, gwnd))
        #print(flag,res.hex().upper());
        return flag,res

    def do_a_task_11(self, auto_flag, gwnd, socket):
        print('【11】设置唤醒周期',gwnd)
        # 有配置用配置的，无配置用默认的
        if gwnd in self.gwnd_wakeupInterval_dict:
            value = self.gwnd_wakeupInterval_dict[gwnd]
            print('配置周期:{}'.format(value))
        else:
            value = self.wakeup_interval##############################################################唤醒周期   value 为int型
        print('终端唤醒周期:{}。(1~180：天；203~255：3~55分钟)'.format(value))
        (cont_id,cont_cmd) = ('02','04'+'%02X'%value)
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('设置唤醒周期:终止，err={},节点{}。'.format(flag, gwnd))
        return flag,res
        # time.sleep(15)

    def do_a_task_12(self, auto_flag, gwnd, socket):
        print('【12】重启终端',gwnd)
        (cont_id,cont_cmd) = ('02','0500')
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('重启终端:终止，err={},节点{}。'.format(flag, gwnd))
        return flag,res

    def do_a_task_13(self, auto_flag, gwnd, socket):
        print('【13】设置终端低功耗',gwnd)
        (cont_id,cont_cmd) = ('02','0600')
        flag,res = self.unicast_common(auto_flag, gwnd, socket, cont_id, cont_cmd)
        if flag != 1:
            print('设置终端低功耗:终止，err={},节点{}。'.format(flag, gwnd))
        return flag,res

    def do_upgrade(self, auto_flag, target, fw_path, socket):
        frame_no = 0xFFFF
        cmd_id_no = 0
        query_type = 0
        gwid = target[0:8]
        file = os.path.basename(fw_path)
        (flag, res) = (0, '')
        if file.endswith('.sbm.cc') or file.endswith('.bin.cc'):
            if (auto_flag == 1) and (self.gwid_lastBN_dict[gwid] > 0) and (fw_path != self.gwid_lastBF_dict[gwid]):
                print('忽略[{}]: 未完成 [{}] [{}(-500)].'.format(fw_path, self.gwid_lastBF_dict[gwid], self.gwid_lastBN_dict[gwid]))
                return flag
        if file.endswith('.sbm.cc'):
            # 查找程序.sbm.cc文件
            cmd_id_no = 0x01
            query_type = 0x15
            print('{}:{}升级程序【{}】...'.format(gettm_ms(),gwid, fw_path))
        elif file.endswith('.bin.cc') and file.find('ssdone') > 0 :
            # 查找程序.bin.cc文件的ssdone模型
            cmd_id_no = 0x02
            query_type = 0x16
            print('{}:{}升级模型【{}】...'.format(gettm_ms(),gwid, fw_path))
        elif file.endswith('.bin.cc') and file.find('ssdall') > 0 :
            # 查找程序.bin.cc文件的ssdall模型
            cmd_id_no = 0x03
            query_type = 0x17
            print('{}:{}升级模型【{}】...'.format(gettm_ms(),gwid, fw_path))
        else:
            print('固件文件名错误[{}]!'.format(file))
        if cmd_id_no > 0:
            # 根据类型广播固件
            print('--------------------------------[{}]--------------------------------------'.format(cmd_id_no))
            #升级
            flag, res = self.do_a_task_09(auto_flag, target, fw_path, socket, frame_no, cmd_id_no)
            if flag != 1:
                print('升级退出,file:{},flag:{}.'.format(fw_path, flag))
                return flag

            # 对所挂的节点进行完整性查询
            for gwnd_i, socket_i in list(self.gwnd_socket_dict.items()):
                ### 判断是否过了维护期
                if (auto_flag == 1) and (gettm_t2s() >= self.upgrade_end_t):
                    break
                if gwnd_i[0:8] == gwid:
                    ### 查询完整性3次，即最多重传45*3个丢包
                    for retry in range(3):
                        if (auto_flag == 1) and (gettm_t2s() >= self.upgrade_end_t):
                            break
                        print('{}/{}:查询{}接收固件(type={})的完整性：'.format(retry+1, 3, gwnd_i,'%02X'%query_type))
                        flag, res = self.do_a_task_10(auto_flag, gwnd_i, socket_i, query_type)
                        FRAME_NUM_OFFSET = 30
                        if flag != 1:
                            break
                        #print(res.hex().upper())
                        #print(res[FRAME_NUM_OFFSET:FRAME_NUM_OFFSET+9].hex().upper())
                        if len(res) < 0xBA:
                            continue
                        lost_frame_flag = int(res[FRAME_NUM_OFFSET:FRAME_NUM_OFFSET+4].hex(),16)
                        FRAME_LOST_NUM_OFFSET = 34
                        lost_frame_num = int(res[FRAME_LOST_NUM_OFFSET:FRAME_LOST_NUM_OFFSET+1].hex(),16)//4
                        if(lost_frame_flag != 0x1):
                            print('invalid lost_frame_flag：{}.'.format(lost_frame_flag))
                            continue
                        print('查询结果:{}遗失{}帧。'.format(gwnd_i,lost_frame_num))
                        if lost_frame_num == 0:
                            break
                        VAL_OFFSET = 35
                        for idx in range(lost_frame_num) : 
                            lost_frame_no = int(res[VAL_OFFSET+idx*4:VAL_OFFSET+idx*4+4].hex(),16)
                            print('重传:{}遗失的第{}帧，帧号:{}.'.format(gwid, idx, lost_frame_no))
                            tmp_flag, tmp_res = self.do_a_task_09(auto_flag, target, fw_path, socket, lost_frame_no, cmd_id_no)
                            if tmp_flag != 1:
                                break
                if flag != 1:
                    break
            # 广播完固件等待烧录重启

            print('{}升级中..{}秒后继续。{},flag:{}.'.format(file, self.upgrade_wait,gettm_ms(),  flag))
            #time.sleep(300)
            time.sleep(self.upgrade_wait)
            # 对所挂的节点进行版本查询
            for gwnd_i, socket_i in list(self.gwnd_socket_dict.items()):
                # 重启命令
                flag, res = self.do_a_task_12(auto_flag, gwnd_i, socket_i)
                # 版本查询
                flag, res = self.do_a_task_01(auto_flag, gwnd_i, socket_i)
        return flag

    def do_automitic_task(self, gwnd, socket):
        flag = 0
        mould_flag = 0 # 1:表示调试模板下发功能
        auto_flag = 1  # 1:表示自动工作模式
        lmiId=''
        flag, res = self.do_a_task_01(auto_flag, gwnd, socket)
        # NOT RUN BELOW
        while True:
            #设置唤醒周期
            if self.lowpower_wakeup_enable == 1:
                if flag == 1:
                    flag,res = self.do_a_task_11(auto_flag, gwnd, socket)
                    time.sleep(15)
            # if flag == 1:
            #     flag,res = self.do_a_task_02(auto_flag, gwnd, socket)
            # if flag == 1:
            #     flag,res = self.do_a_task_03(auto_flag, gwnd, socket)
            # if flag == 1:
            #     flag,res = self.do_a_task_04(auto_flag, gwnd, socket)
            # if flag == 1:
            #     flag,res = self.do_a_task_05(auto_flag, gwnd, socket)
            if flag == 1:
                flag,res,lmiId = self.do_a_task_06(auto_flag, gwnd, socket)
                time_start = time.time()
                while flag != 1 :#################################################超时退出循环
                    print('do_a_task_06 err')
                    flag, res, lmiId = self.do_a_task_06(auto_flag, gwnd, socket)
                    time_end = time.time()
                    time_c = time_end - time_start
                    print('do_a_task_06')
                    if time_c == 10:
                        print(time_c)
                        break

            if (flag == 1) and (self.upload_mode == 0):
                flag,res = self.do_a_task_07(auto_flag, gwnd, socket, res, lmiId)
            if self.lowpower_wakeup_enable == 1:
                if flag == 1:
                    flag,res = self.do_a_task_01(auto_flag, gwnd, socket)
            if flag == -1:
                self.gwnd_status_dict[gwnd] = 'OFF'
                break
            elif flag != 1:
                print('New cycle starts 15s later. (flag={})'.format(flag))
                time.sleep(15)
                break
            #设置重启
            if self.lowpower_wakeup_enable == 1:
                if flag == 1:
                    flag,res = self.do_a_task_13(auto_flag, gwnd, socket)
                    flag = -1
                    self.gwnd_status_dict[gwnd] = 'OFF'
                    print('=Done=')
                    break
            if mould_flag == 1:
                md_96B_data = '3F800000412000003E4CCCCD40000000'\
                        +'0000000000000000000000B00000005C'\
                        +'0000007500000094000000F000000091'\
                        +'000000EC0000008C0000006000000059'\
                        +'000000630000005A0000000000000000'\
                        +'000000000000000090003F6C4002FD78'
                flag,res = self.do_a_task_08(auto_flag, gwnd, md_96B_data, socket)
                mould_flag = 0
            ### 完成任务，跳出
            break
        #执行一遍退出
        return flag

    def thread_send_to_node(self, gwnd, socket):
        rand_delay = round(random.uniform(0.5, self.random_delay_max * 1.0), 2)
        print('节点{}随机延时为:{}秒。'.format(gwnd, rand_delay))
        if gwnd not in self.gwnd_piccnt_dict:
            self.gwnd_piccnt_dict[gwnd] = 0
        if gwnd not in list(self.gwnd_rxqueue_dict):
            self.gwnd_rxqueue_dict[gwnd] = queue.Queue(10)
        ### 大的周期循环
        break_case = 0
        while True:
            ### 若服务器不在线退出
            if self.gwnd_socket_dict[gwnd] == 0:
                break_case = 1
                break
            ### 刚开始检查一下是否有上次没完成的休息
            while datetime.datetime.now() < self.gwnd_cycle_end_dict[gwnd]:
                if self.gwnd_status_dict[gwnd] == 'OFF':
                    break_case = 3
                    break
                time.sleep(1)  
            if break_case == 3:
                break
            ### 维护时间
            while (gettm_t2s() >= self.maintain_start_t) and  (gettm_t2s() < self.maintain_end_t):
                print('{}：{} is being maintained.'.format(gettm(),gwnd))
                time.sleep(60)
            ### 周期工作
            cycle_start = datetime.datetime.now()  # 计时开始
            cycle_delta = datetime.timedelta(seconds=int(self.cycle_interval))
            cycle_expect_end = cycle_start + cycle_delta  # 计时结束
            self.gwnd_cycle_end_dict[gwnd] = cycle_expect_end
            print('{} start to work from 【{}】 to 【{}】.'.format(gwnd, cycle_start, cycle_expect_end))
            time.sleep(rand_delay)
            ### 这里做一次任务
            status = self.do_automitic_task(gwnd, socket)
            #status = 1
            if (status != 1) and (status != -1):
                time.sleep(5)
                continue
            elif status == -1:
                break_case = 2
                break
            ### sleep至设定的周期cycle_interval。
            work_seconds = (datetime.datetime.now() - cycle_start).seconds
            sleep_seconds = self.cycle_interval - work_seconds
            print('[{}] {} from:[{}],worked: [{}]s, will sleep: [{}]s, to:[{}].'.format(gettm(),\
                gwnd,cycle_start, work_seconds,sleep_seconds, cycle_expect_end))
            while datetime.datetime.now() < cycle_expect_end:
                if self.gwnd_status_dict[gwnd] == 'OFF':
                    break_case = 3
                    break
                time.sleep(1)
            if break_case == 3:
                break
        print('{}: {}单个tx线程退出(break case = {})!'.format(gettm(),gwnd, break_case))
        #print('{} finish cycle, now:{}, expect:{}.'.format(gwnd, datetime.datetime.now(), cycle_expect_end))

    def thread_send_to_gateway(self, client_socket):
        gwid = ''
        while True:
            #遍历连接上的所有节点
            for gwnd, socket in list(self.gwnd_socket_dict.items()):
                #排除不属于当前连接的集中器的socket
                if socket != client_socket:
                    continue
                #排除不属于注册的节点
                if gwnd in self.gwnd_status_dict and self.gwnd_status_dict[gwnd] != 'REG':
                    continue
                #属于未加入白名单的节点
                if gwnd not in self.white_list:
                    #配置了自动注册
                    if self.allow_auto_reg == 1:
                        ###print('self.white_list (before) = ', self.white_list)
                        self.white_list.append(gwnd)
                        self.gwnd_autowork_dict[gwnd] = 1
                        print('add gwnd = ', gwnd)
                        ###print('self.white_list (after) = ', self.white_list)
                        # 如'ADD{5D000001:000001,000002,000003|5D000002:000001,000002}'
                        msg='ADD{{{}:{}}}'.format(gwnd[0:8],gwnd[8:16])
                        print('msg=',msg)
                        #可能有多个socket同时修改配置文件，加锁
                        with self.file_lock:
                            ###print('保存前：',self.own_devices_dict)
                            self.update_own_devices(self.own_devices_dict, msg)
                            self.save_own_devices(self.own_devices_dict)
                            self.own_devices_dict = self.read_own_devices()
                            ###print('保存后：',self.own_devices_dict)
                    else:
                        print('Warning: device',gwnd,'is not in the white list!')
                        #print('self.gwnd_status_dict = ', self.gwnd_status_dict)
                        continue
                #排除在自动工作列表里面，但是禁止工作的
                if gwnd in list(self.gwnd_autowork_dict) and self.gwnd_autowork_dict[gwnd] != 1:
                    continue
                gwid = gwnd[0:8]
                #注册通过，分配发送线程
                t = threading.Thread(target=self.thread_send_to_node, args=(gwnd, socket))
                t.start()
                self.gwnd_status_dict[gwnd] = 'RUN'
                print('{}: {}线程开启：'.format(gettm(),gwnd))
            # 接收线程显示为断连，退出
            if self.socket_status_dict[client_socket] == 0:
                print('{}集中器掉线通知：{},退出tx线程。'.format(gettm(),client_socket))
                break
            if (gwid != '') and (gettm_t2s() >= self.upgrade_start_t) and (gettm_t2s() < self.upgrade_end_t):
                print('{}: {}进入升级状态。'.format(gettm(),gwid))
                # 升级程序，模型
                filelist = os.listdir(self.fw_dir)
                if not gwid in self.gwid_lastBN_dict:
                    self.gwid_lastBN_dict[gwid] = 0
                    #self.gwid_lastBN_dict[gwid] = 100
                if not gwid in self.gwid_lastBF_dict:
                    self.gwid_lastBF_dict[gwid] = ''
                    #self.gwid_lastBF_dict[gwid] = './FW/25AB8D0E_ZDB_V99_A99_LD2_200710.sbm.cc'
                
                for file in sorted(filelist) :
                    ### 判断是否过了维护期
                    if gettm_t2s() >= self.upgrade_end_t:
                        break
                    vgwid = ''
                    for vgw_i, rgw_i in list(self.vgw_rgw_dict.items()):
                        if rgw_i == gwid:
                            vgwid = vgw_i
                            print('升级 {} (vgwid: {})'.format(gwid, vgwid))
                    if file.startswith(gwid.upper()) or file.startswith(gwid.lower()) or file.startswith(vgwid.upper()) or file.startswith(vgwid.lower()):
                        auto_flag = 1  # 1:表示自动工作模式
                        target = gwid + '0000FFFF'  # 广播
                        fw_path = os.path.join(self.fw_dir, file)
                        flag=self.do_upgrade(auto_flag, target, fw_path, socket)
                        if flag == -1:
                            break
            time.sleep(3)
        
