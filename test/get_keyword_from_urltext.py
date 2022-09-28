from lib2to3.pgen2.literals import evalString
import re
import os

from lxml import etree

def get_keyword():
    text = etree.parse('file/h3cie-rs+.html', etree.HTMLParser())
    keywords = text.xpath('//table[@id="ctl00_ContentBody_ProGdCert"]/tr/td[3]/text()')
    print(keywords)



if __name__ == "__main__":
    get_keyword()