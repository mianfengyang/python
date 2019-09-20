
#encoding:utf-8

from socket import *
import threading
HOST = '127.0.0.1'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

def send_data():
    while True:
        send_data = input('> ')
        tcpCliSock.send(send_data.encode('utf-8'))
        if  send_data == "exit":
            break
    tcpCliSock.close()

def recv_data():
    while True:
        recv_data = tcpCliSock.recv(BUFSIZ)
        print(recv_data.decode('utf-8'))
        if recv_data == "exit":
            break
    tcpCliSock.close()


if __name__ == '__main__':

    t1 = threading.Thread(target=send_data)
    t2 = threading.Thread(target=recv_data)
    t1.start()
    t2.start()