#coding=utf-8

"""
=============================================================
#   project: python
#      file: py01-requests-1.py
#    author: mianfeng.yang
#      date: 2019-09-27 17:30:58
=============================================================
"""
import requests

req = requests.request(method='Get', url='https://www.jihaoba.com/haoduan/139/nanjing.htm')
req.


if __name__ == '__main__':
    print(req)