# coding=utf-8

"""
==============================================================
# @Time    : 2019/9/18 20:08
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : tsServer.py
# @Software: PyCharm
==============================================================
"""
from socket import *

HOST = '0.0.0.0'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpServer = socket(AF_INET, SOCK_STREAM)
tcpServer.bind(ADDR)
tcpServer.listen()
sock, addr = tcpServer.accept()

while True:
    # 这里需要注意的是：从键盘接收数据后应该紧接着就发送，不然发送不过去，服务端也接收不到
    recv_data = sock.recv(BUFSIZE)
    print("FROM:{}\nDATA:{}".format(addr, recv_data.decode('utf-8')))
    if recv_data.decode('utf-8') == 'exit':
        break
    send_data = input('> ')
    sock.send(send_data.encode('utf8'))
    if send_data == 'exit':
        break
sock.close()
tcpServer.close()

