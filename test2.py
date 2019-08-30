
#coding:utf-8

import queue
list1 = ['aa', 'bb', 'cc', 'dd']
list2 = ['11', '22', '33', '44']
a = [1, 2, 3, 4]
b = {}
q = queue.Queue()

def add_value():
    q.put(list1)
    q.put(list2)

def get_value():
    while not q.empty():
        print(q.get())


def main():
    # add_value()
    # get_value()
    global b
    for i in range(len(a) - 1):
        if a[i] > a[i+1]:
            b['tt'] = a[i]
        else:
            b['tt'] = a[i+1]
    print(b)

if __name__ == "__main__":
    main()