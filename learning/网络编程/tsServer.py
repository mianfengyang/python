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

def chat_ser():
    """当发送和接收写在一个函数当中时，此时的通信是半双工模式，不能连续发送信息，只有等对方也发送数据过来并接收到了，
    才能再次发送。
    要想实现全双工模式通信，则可以将发送和接收分开，并使用多线程
    """
    while True:
        recv_data = sock.recv(BUFSIZ)
        print("\nFROM:{}\nDATA:{}".format(addr, recv_data.decode('utf8')))
        if recv_data.decode('utf8') == "exit":
            break

        send_data = input('>')
        sock.send(send_data.encode('utf8'))
        if send_data == "exit":
            break
    # sock.close()
    # tcpSerSock.close()


# def recv_data():
#     while True:
#         recv_data = sock.recv(BUFSIZ)
#         print("\nFROM:{}\nDATA:{}".format(addr, recv_data.decode('utf8')))
#         if recv_data.decode('utf8') == "exit":
#             break

# def send_data():
#
#     while True:
#         send_data = input('>')
#         sock.send(send_data.encode('utf8'))
#         if  send_data == "exit":
#             break
    # sock.close()
    # tcpSerSock.close()

if __name__ == '__main__':

    t1 = threading.Thread(target=chat_ser)
    # t1 = threading.Thread(target=recv_data)
    # t2 = threading.Thread(target=send_data)

    t1.start()
    # t2.start()
    t1.join()
    # t2.join()

    sock.close()
    tcpSerSock.close()