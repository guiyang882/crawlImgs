# -*- coding: utf-8 -*-
# @Time    : 2017/5/9 16:16
# @Author  : liuguiyangnwpu@gmail.com
# @File    : ToutiaoImg.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function

import os
import scrapy
import urllib
import json
import datetime
from crawlImgs.items import CrawlimgsItem
import _datetime
import time

def getURL(index):
    atnow = _datetime.datetime.now()
    delta = _datetime.timedelta(minutes=30*index)
    val = atnow - delta
    val = int(time.mktime(val.timetuple()))
    val = str(val)
    a = "http://www.toutiao.com/api/pc/feed/?category=gallery_detail&utm_source=toutiao&max_behot_time="+val+"&as=A135C9A18147C24&cp=5911578C32C41E1",
    b = "http://www.toutiao.com/api/pc/feed/?category=gallery_old_picture&utm_source=toutiao&max_behot_time="+val+"&as=A165B9E121980C4&cp=5911F8304C641E1",
    c = "http://www.toutiao.com/api/pc/feed/?category=gallery_story&utm_source=toutiao&max_behot_time="+val+"&as=A1B599C1E1B80E7&cp=5911C8A06E776E1",
    d = "http://www.toutiao.com/api/pc/feed/?category=gallery_photograthy&utm_source=toutiao&max_behot_time="+val+"&as=A135F931B128116&cp=591168C14166DE1"
    tmp = [a,b,c,d]
    return tmp

class ToutiaoSpider(scrapy.Spider):
    name = "ToutiaoImg"
    allowed_domains = ["toutiao.com"]

    def __init__(self, keywordjson=None, category=None, *args, **kwargs):
        super(ToutiaoSpider, self).__init__(*args,**kwargs)
        self.totalPage = 48 * 6 * 30
        self.start_urls = [
            "http://www.toutiao.com/api/pc/feed/?category=gallery_detail&utm_source=toutiao&max_behot_time=0&as=A135C9A18147C24&cp=5911578C32C41E1",
            "http://www.toutiao.com/api/pc/feed/?category=gallery_old_picture&utm_source=toutiao&max_behot_time=0&as=A165B9E121980C4&cp=5911F8304C641E1",
            "http://www.toutiao.com/api/pc/feed/?category=gallery_story&utm_source=toutiao&max_behot_time=1494314535&as=A1B599C1E1B80E7&cp=5911C8A06E776E1",
            "http://www.toutiao.com/api/pc/feed/?category=gallery_photograthy&utm_source=toutiao&max_behot_time=0&as=A135F931B128116&cp=591168C14166DE1"
        ]
        for i in range(1, self.totalPage):
            self.start_urls.extend(getURL(i))

    def parse(self, response):
        sites = json.loads(response.body_as_unicode())
        itemlist = sites["data"]
        for item in itemlist:
            image_list = item["image_list"]
            for imgdict in image_list:
                imgItem = CrawlimgsItem()
                info = imgdict["url"]
                rect = info.strip().split("/")[-2].split("x")
                imgItem["image_urls"] = [imgdict["url"]]
                imgItem["image_label"] = item["chinese_tag"]
                imgItem["image_fromURL"] = item["url"]
                imgItem["image_fromURLHost"] = item["url"]
                imgItem["image_height"] = int(rect[1])
                imgItem["image_width"] = int(rect[0])
                imgItem["image_crawDateTime"] = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
                yield imgItem
