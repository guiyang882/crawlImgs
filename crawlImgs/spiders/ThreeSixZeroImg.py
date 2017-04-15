# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
import os
import urllib
import json
import codecs
import datetime
from pprint import pprint
from crawlImgs.items import CrawlimgsItem
from crawlImgs.spiders.utils import getPartLabel 

def getURL(pagenum, word):
    return 'http://image.so.com/j?src=srp&correct=%E5%8A%A8%E7%89%A9&sn=60&pn=' + str(pagenum) +  '&q=' + word

class ThreesixzeroimgSpider(scrapy.Spider):
    name = "ThreeSixZeroImg"
    allowed_domains = ["image.so.com"]

    def __init__(self, keywordjson=None, category=None, *args, **kwargs):
        super(ThreesixzeroimgSpider, self).__init__(*args,**kwargs)
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
        label = str(response.url).strip().split("q=")[-1]
        for site in sites["list"]:
            image = CrawlimgsItem()
            image["image_urls"] = [site["img"]]
            image["image_label"] = self.getName(label)
            image["image_fromURL"] = site["link"]
            image["image_height"] = site["height"]
            image["image_width"] = site["width"]
            image["image_fromURLHost"] = site["dspurl"]
            image["image_crawDateTime"] = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
            yield image
