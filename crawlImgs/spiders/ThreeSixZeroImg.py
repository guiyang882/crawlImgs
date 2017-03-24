# -*- coding: utf-8 -*-
import scrapy

totalPage = 10

def getURL(pagenum, word):
    return 'http://image.so.com/j?src=srp&correct=%E5%8A%A8%E7%89%A9&sn=60&pn=' + str(pagenum) +  '&q=' + word

class ThreesixzeroimgSpider(scrapy.Spider):
    name = "ThreeSixZeroImg"
    allowed_domains = ["image.so.com"]
    start_urls = ['http://image.so.com/']

    def parse(self, response):
        pass
