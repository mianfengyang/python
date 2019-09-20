#coding=utf-8

"""
=============================================================
#   project: python
#      file: tsServer.py
#    author: mianfeng.yang
#      date: 2019-09-20 11:39:43
=============================================================
"""
from socket import *
import threading

HOST = '0.0.0.0'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen()
sock, addr = tcpSerSock.accept()

def recv_data():
    while True:
        recv_data = sock.recv(BUFSIZ)
        print("FROM:{}\nDATA:{}".format(addr, recv_data.decode('utf8')))
        if recv_data == "exit":
            break
    sock.close()
    tcpSerSock.close()

def send_data():
    while True:
        send_data = input('>')
        sock.send(send_data.encode('utf8'))
        if  send_data == "exit":
            break
    sock.close()
    tcpSerSock.close()

if __name__ == '__main__':

    t1 = threading.Thread(target=recv_data)
    t2 = threading.Thread(target=send_data)

    t1.start()
    t2.start()