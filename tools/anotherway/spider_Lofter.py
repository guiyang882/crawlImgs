# -*- coding: utf-8 -*-
# @Time    : 2017/5/11 18:00
# @Author  : liuguiyangnwpu@gmail.com
# @File    : spider_Lofter.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function

import os
import codecs
import urllib.request
import feedparser

"""主要是用来抓取网易lofter的xml文件数据"""

class SpiderLofter():
    def __init__(self):
        self.urllist = []
        pass

    def __del__(self):
        pass

    def loadUrls(self, filename):
        """filename formate:
        userid
        """
        if not os.path.exists(filename):
            raise IOError(filename + " Not Found !")
        subfix = ".lofter.com/rss"
        urllist = []
        with codecs.open(filename=filename, mode='r', encoding='utf8') as reader:
            for line in reader.readlines():
                line = line.strip()
                urllist.append("http://"+line + subfix)
        self.urllist = urllist

    def fetchXML(self):
        for urlitem in self.urllist:
            feed = feedparser.parse(urlitem)
            for post in feed.entries:
                imgurl = post["links"][0]["href"]
                data = urllib.request.urlopen(imgurl).read().decode("utf8")
                print(data)
                break

if __name__ == '__main__':
    filename = "./users.id"
    obj = SpiderLofter()
    obj.loadUrls(filename)
    obj.fetchXML()
