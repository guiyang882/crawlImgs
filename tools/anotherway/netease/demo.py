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
for url in targetUrl:
    try:
        response = urllib.request.urlopen(url)
        if response.status in [200]:
            if 'gif' not in response.url:
                print(response.url)
    except Exception as es:
        pass