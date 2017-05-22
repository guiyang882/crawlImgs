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
from bs4 import BeautifulSoup
import hashlib
from scrapy.utils.python import to_bytes

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
        if not os.path.exists("./already.user.id"):
            raise IOError("./already.user.id not found !")
        alreadyUser = []
        with codecs.open(filename="./already.user.id", mode='r', encoding='utf8') as reader:
            for line in reader.readlines():
                line = line.strip()
                alreadyUser.append(line)

        subfix = ".lofter.com/rss"
        urllist = []
        with codecs.open(filename=filename, mode='r', encoding='utf8') as reader:
            for line in reader.readlines():
                line = line.strip()
                if line in alreadyUser:
                    continue
                urllist.append("http://"+line + subfix)
                alreadyUser.append(line)
        with codecs.open(filename="./already.user.id", mode='w', encoding='utf8') as writer:
            for line in alreadyUser:
                writer.write(line)
                writer.write('\n')
                self.urllist = urllist

    def fetchXML(self):
        strDate = "20170522"
        def _downloadImg(imgUrl):
            savePrefix = "/root/SPIDERIMAGESDB/DATASOURCE/Lofter/" + strDate + "/"
            if not os.path.isdir(savePrefix):
                os.makedirs(savePrefix)
            image_guid = hashlib.sha1(to_bytes(imgUrl)).hexdigest()
            image_name = None
            if ".jpg" in imgUrl:
                image_name = image_guid + ".jpg"
            if ".png" in imgUrl:
                image_name = image_guid + ".png"
            if ".jpeg" in imgUrl:
                image_name = image_guid + ".jpeg"
            if image_name == None:
                return
            try:
                with open(savePrefix+image_name, "wb") as writer:
                    writer.write(urllib.request.urlopen(imgUrl).read())
            except Exception as es:
                print(es)
            with codecs.open("./download" + strDate + ".csv", mode='a', encoding='utf8') as writer:
                writer.write(imgUrl+',Lofter/'+strDate+'/'+image_name)
                writer.write('\n')
                print(imgUrl, image_name)

        for urlitem in self.urllist:
            feed = feedparser.parse(urlitem)
            for post in feed.entries:
                imgurl = post["links"][0]["href"]
                try:
                    data = urllib.request.urlopen(imgurl).read().decode("utf8")
                except Exception as es:
                    print(es)
                soup = BeautifulSoup(data, "lxml")
                imglist = soup.find_all('img')
                for img in imglist:
                    if "class" in img.attrs.keys() and img.attrs["class"][0] == 'avatar':
                        continue
                    tmpUrl = img.attrs["src"]
                    _downloadImg(tmpUrl)

if __name__ == '__main__':
    filename = "./users.50.160.id"
    obj = SpiderLofter()
    obj.loadUrls(filename)
    obj.fetchXML()
