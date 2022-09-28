import os
import re
from tkinter import Tk

try:
    # 获取剪切板内容
    t=Tk()
    s = t.clipboard_get()

    # 正则替换
    pat = re.compile(r'(true,)|(false,)|(null,)|(null)')
    r = pat.sub('"a",', s)
    # 将剪切板内容作为字典输入
    cookie_list = eval(r)
    result_list = []

    for dic in cookie_list:
        s = dic.get('name') + '=' + dic.get('value') + ';'
        result_list.append(s)

    result = ''.join(result_list)
    # 将cookie复制到剪切板
    t.clipboard_append(result)
    t.update()
    t.destroy()
    print('生成cookie成功！')
except Exception as e:
    print(e)
    print('生成cookie失败，请重新复制cookie')
