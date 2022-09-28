#coding=utf-8

"""
=============================================================
#   project: python
#      file: bs_test.py
#    author: mianfeng.yang
#      date: 2019-11-05 10:02:11
=============================================================
"""
import requests
from bs4 import BeautifulSoup
res = requests.get("http://epubw.com")
print(res.status_code)
print(res.encoding)
# print(res_baidu.text)
bs = BeautifulSoup(res.text,"html.parser")
title_tag = bs.title
print(title_tag.string)
div_tag = bs.find("div", {"class":"col-xs-4 col-sm-3 card-1"})
print(div_tag)

if __name__ == '__main__':
    pass