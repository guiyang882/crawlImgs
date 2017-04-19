#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
import os
import scrapy
import urllib
import json
import datetime
import codecs
from bs4 import BeautifulSoup
from pprint import pprint
from crawlImgs.items import CrawlimgsItem
from crawlImgs.spiders.utils import getPartLabel

def getURL(pagenum, word):
    urlbase = "http://cn.bing.com/images/async"
    queryparam = {
        "q":word,
        "first":pagenum*36,
        "count":35,
        "relp":35,
        "lostate":"r",
        "mmasync":1,
        "dgState":"x*737_y*1394_h*167_c*3_i*36_r*9",
        "IG":"68A0CBB3A3764BC581E625B675C2C6D4",
        "SFX":2,
        "iid":"images.5727"
    }
    if queryparam["first"] == 0:
        queryparam["first"] = 1
    paramdata = urllib.parse.urlencode(queryparam)
    urlpath = urlbase + "?" + paramdata
    return urlpath

class BingSearchSpider(scrapy.Spider):
    name = "BingSearchImg"
    allowed_domains = ["cn.bing.com"]

    def __init__(self, keywordjson=None, category=None, *args, **kwargs):
        super(BingSearchSpider, self).__init__(*args,**kwargs)
        self.totalPage = 5
        self.start_urls = []
        self.wordList, self.totalPage = getPartLabel(keywordjson, category)
        for cell in self.wordList:
            for pagenum in range(self.totalPage):
                self.start_urls.append(getURL(pagenum, cell))

    def getName(self, word):
        try:
            ret_word = urllib.unquote(word).decode('utf-8')
        except Exception as ex:
            ret_word = urllib.parse.unquote(word)
        return ret_word

    def parse(self, response):
        label = str(response.url).strip().split("q=")[-1].split("&")[0]
        soup = BeautifulSoup(response.body_as_unicode(), "html.parser")
        for site in soup.find_all("img", attrs={"class":"mimg"}):
            site.attrs["src"]
            image = CrawlimgsItem()
            image["image_urls"] = [site.attrs["src"]]
            image["image_label"] = self.getName(label)
            image["image_fromURL"] = site.attrs["src"]
            image["image_fromURLHost"] = site.attrs["src"]
            image["image_height"] = site["height"]
            image["image_width"] = site["width"]
            image["image_crawDateTime"] = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
            yield image
