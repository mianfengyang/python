
#encoding:utf-8

from socket import *
import threading
HOST = '127.0.0.1'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

def chat_cli():
    """当发送和接收写在一个函数当中时，此时的通信是半双工模式，不能连续发送信息，只有等对方也发送数据过来并接收到了，
      才能再次发送。
      要想实现全双工模式通信，则可以将发送和接收分开，并使用多线程
    """



# 发送数据线程
# def send_data():
#     while True:
#         send_data = input('> ')
#         tcpCliSock.send(send_data.encode('utf-8'))
#         if  send_data == "exit":
#             break

# 接收数据线程
# def recv_data():
#     while True:
#         recv_data = tcpCliSock.recv(BUFSIZ)
#         print("\nFROM:{}\nDATA:{}".format(HOST, recv_data.decode('utf-8')))
#         if recv_data.decode('utf8') == "exit":
#             break
    # tcpCliSock.close()




if __name__ == '__main__':


    t1 = threading.Thread(target=chat_cli)
    # t1 = threading.Thread(target=send_data)
    # t2 = threading.Thread(target=recv_data)


    t1.start()
    #t2.start()
    t1.join()
    #t2.join()
    tcpCliSock.close()
