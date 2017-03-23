# -*- coding: utf-8 -*-
import scrapy
import urllib
import json

from crawlImgs.items import CrawlimgsItem

totalPage = 10

def getURL(pagenum, word):
    return 'https://image.baidu.com/search/avatarjson?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1488547724906_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1488547724907%5E00_1002X1024&rn=200&pn=' + str(pagenum) +  '&word=' + word

def getWordList(file_path):
    wordList = []
    with open(file_path, "r") as handle:
        for line in handle.readlines():
            line = line.strip().split(',')
            wordList.append((line[0], line[1]))
    return wordList

class BaiduimgSpider(scrapy.Spider):
    name = "BaiduImg"
    allowed_domains = ["baidu.com"]
    start_urls = []
    wordList = getWordList("./labels.csv")
    for cell in wordList:
        for pagenum in range(int(totalPage)):
            start_urls.append(getURL(pagenum * 60, cell[0]))
            start_urls.append(getURL(pagenum * 60, cell[1]))

    def getName(self, word):
        ret_word = urllib.unquote(word).decode('utf-8')
        return ret_word

    def parse(self, response):
        sites = json.loads(response.body_as_unicode())
        label = str(response.url).strip().split("word=1")[-1]
        for site in sites["imgs"]:
            image = CrawlimgsItem()
            image["image_urls"] = [site["objURL"]]
            image["image_label"] = self.getName(label)
            yield image