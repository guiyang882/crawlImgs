# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import scrapy
import urllib
import json
import datetime
import codecs
from pprint import pprint
from crawlImgs.items import CrawlimgsItem
from crawlImgs.spiders.utils import getPartLabel

def getURL(pagenum, word):
    return 'https://image.baidu.com/search/avatarjson?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1488547724906_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1488547724907%5E00_1002X1024&rn=200&pn=' + str(pagenum) +  '&word=' + word

class BaiduimgSpider(scrapy.Spider):
    name = "BaiduImg"
    allowed_domains = ["baidu.com"]

    def __init__(self, keywordjson=None, category=None, *args, **kwargs):
        super(BaiduimgSpider, self).__init__(*args,**kwargs)
        self.totalPage = 5
        self.start_urls = []
        self.wordList, self.totalPage = getPartLabel(keywordjson, category)
        for cell in self.wordList:
            for pagenum in range(self.totalPage):
                self.start_urls.append(getURL(pagenum * 60, cell))

    def getName(self, word):
        try:
            ret_word = urllib.unquote(word).decode('utf-8')
        except Exception as ex:
            ret_word = urllib.parse.unquote(word)
        return ret_word

    def parse(self, response):
        sites = json.loads(response.body_as_unicode())
        label = str(response.url).strip().split("word=")[-1]
        for site in sites["imgs"]:
            image = CrawlimgsItem()
            image["image_urls"] = [site["objURL"]]
            image["image_label"] = self.getName(label)
            image["image_fromURL"] = site["fromURL"]
            image["image_fromURLHost"] = site["fromURLHost"]
            image["image_height"] = site["height"]
            image["image_width"] = site["width"]
            image["image_crawDateTime"] = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
            yield image
