# -*- coding: utf-8 -*-
# @Time    : 2017/5/15 15:20
# @Author  : liuguiyangnwpu@gmail.com
# @File    : demo.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function

import urllib.request
from bs4 import BeautifulSoup
import re

loft_sitemap = "http://www.lofter.com/sitemap.xml"
siteMap = urllib.request.urlopen(loft_sitemap).read().decode("ascii")
# print(siteMap)
regUrl = re.compile(r'<loc>(http://www.lofter.com/.+)</loc>')
targetUrl = regUrl.findall(siteMap)
for item in targetUrl:
    print(item)
    page = urllib.request.urlopen(item).read().decode("utf8")
    soup = BeautifulSoup(page, "lxml")
    print(soup.find_all("div", {"class": "m-info f-cb"}))
    break