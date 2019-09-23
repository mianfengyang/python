#!/usr/bin/python36
#encoding:utf-8

from socket import *

HOST = '127.0.0.1'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    # 这里需要注意的是：从键盘接收数据后应该紧接着就发送，不然发送不过去，服务端也接收不到
    send_data = input('> ')
    tcpCliSock.send(send_data.encode('utf-8'))
    if send_data == 'exit':
        break
    recv_data = tcpCliSock.recv(BUFSIZ)
    print("FROM:{}\nDATA:{}".format(HOST, recv_data.decode('utf-8')))
    if recv_data.decode('utf-8') == 'exit':
        break
tcpCliSock.close()
