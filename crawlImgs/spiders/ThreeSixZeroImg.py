# -*- coding: utf-8 -*-
import scrapy
import os
import urllib
import json
import codecs
import datetime
from pprint import pprint
from crawlImgs.items import CrawlimgsItem

totalPage = 5

def getURL(pagenum, word):
    return 'http://image.so.com/j?src=srp&correct=%E5%8A%A8%E7%89%A9&sn=60&pn=' + str(pagenum) +  '&q=' + word

def getWordList(file_path):
    wordList = []
    with codecs.open(file_path, "r", 'utf-8') as handle:
        for line in handle.readlines():
            line = line.strip().split(',')
            wordList.append((line[0], line[1]))
    return wordList

def getPartLabel(partID):
    partID = int(partID)
    wordList = []
    if os.path.exists("./labels.csv"):
        with codecs.open("./labels.csv", "r", 'utf-8') as handle:
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

    def __init__(self, category=None, *args, **kwargs):
        super(ThreesixzeroimgSpider, self).__init__(*args,**kwargs)
        self.start_urls = []
        self.wordList = getPartLabel(category)
        for cell in self.wordList:
            for pagenum in range(int(totalPage)):
                self.start_urls.append(getURL(pagenum * 60, cell))
        #print(self.start_urls)

    def getName(self, word):
        try:
            ret_word = urllib.unquote(word).decode('utf-8')
        except Exception as ex:
            ret_word = urllib.parse.unquote(word)
        return ret_word

    def parse(self, response):
        sites = json.loads(response.body_as_unicode())
        label = str(response.url).strip().split("q=")[-1]
        #pprint(sites)
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
