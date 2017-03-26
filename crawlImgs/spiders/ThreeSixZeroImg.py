# -*- coding: utf-8 -*-
import scrapy
import os
import urllib
import json
from crawlImgs.items import CrawlimgsItem

totalPage = 5

def getURL(pagenum, word):
    return 'http://image.so.com/j?src=srp&correct=%E5%8A%A8%E7%89%A9&sn=60&pn=' + str(pagenum) +  '&q=' + word

def getWordList(file_path):
    wordList = []
    with open(file_path, "r") as handle:
        for line in handle.readlines():
            line = line.strip().split(',')
            wordList.append((line[0], line[1]))
    return wordList

def getPartLabel(partID):
    partID = int(partID)
    wordList = []
    if os.path.exists("./labels.csv"):
        with open("./labels.csv", "r") as handle:
            cnt = 0
            for line in handle.readlines():
                cnt += 1
                if int(cnt / 20) == partID:
                    line = line.strip().split(",")
                    wordList.extend([item for item in line if len(item) > 0])
    return wordList

class ThreesixzeroimgSpider(scrapy.Spider):
    name = "ThreeSixZeroImg"
    allowed_domains = ["image.so.com"]
    start_urls = ['http://image.so.com/']

    def __init__(self, category=None, *args, **kwargs):
        super(ThreesixzeroimgSpider, self).__init__(*args,**kwargs)
        self.start_urls = []
        self.wordList = getPartLabel(category)
        for cell in self.wordList:
            for pagenum in range(int(totalPage)):
                self.start_urls.append(getURL(pagenum * 60, cell))
        print(self.start_urls)

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
            yield image
