# -*- coding: utf-8 -*-
# @Time    : 2017/5/8 19:59
# @Author  : liuguiyangnwpu@gmail.com
# @File    : NetEaseSpider.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function

from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
import datetime
import re
import scrapy
from crawlImgs.items import CrawlimgsItem
from bs4 import BeautifulSoup

class NetEaseSpider(scrapy.Spider):
    name = "NetEaseImg"
    allowed_domains = ["www.163.com"]

    start_urls = [
        "http://news.163.com/photo/#Insight",
        "http://news.163.com/photo/#Current",
        "http://news.163.com/photo/#Week",
        "http://news.163.com/photo/#Special",
        "http://news.163.com/photo/#War",
        "http://news.163.com/photo/#Hk",
        "http://news.163.com/photo/#Discovery",
        "http://news.163.com/photo/#Paper"
    ]
    rules = [
        Rule(
            SgmlLinkExtractor(allow=(r"http://news.163.com/photoview/[0-9a-zA-Z]{6,8}/[0-9]{6,9}.html\?from\=ph_ss#p=[0-9A-Z]{10,18}")),
             callback="parse_item_yield"
        ),
    ]

    def parse_item(self, response):
        soup = BeautifulSoup(response.body)
        for item in soup.findAll("a"):
            if item.has_attr("href"):
                head_url_list = re.findall(self.head_re, item["href"])
                detail_url_list = re.findall(self.detail_re, item["href"])
                if head_url_list is None:
                    for tmp in head_url_list:
                        yield Request(tmp, callback=self.parse_item_yield)
                if detail_url_list is None:
                    for tmp in detail_url_list:
                        yield Request(tmp, callback=self.parse_item_yield)

    def parse_item_yield(self, response):
        soup = BeautifulSoup(response.body)
        image = CrawlimgsItem()

        image["image_urls"] = [site["objURL"]]
        image["image_label"] = self.getName(label)
        image["image_fromURL"] = response.url
        image["image_fromURLHost"] = response.url
        image["image_crawDateTime"] = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        yield image
        news_item["news_title"] = u"网易新闻"
        if type(soup.find("title")) != types.NoneType:
            news_item["news_title"] = soup.find("title").string
        new_date_list = soup.findAll("div",{"class":["ep-time-soure cDGray","pub_time"]})
        news_date_re = re.findall(r"\d{2}/\d{4}/\d{2}",response.url)[0].split("/")
        news_item["news_date"] = "20" + news_date_re[0] + "-" + news_date_re[1][:2] + "-" + news_date_re[1][-2:] + " " + news_date_re[2]
        if len(new_date_list) != 0:
            news_item["news_date"] = new_date_list[0].string[:19]
        tmp_news_source = soup.find("a",{"id":"ne_article_source"})
        if tmp_news_source != None:
            news_item["news_source"] = tmp_news_source.string
        else:
            news_item["news_source"] = "NetEase"
        data = soup.findAll("div",{"id":"endText"})[0]
        data_list = data.findAll("p",{"class":""})
        contents = ""
        for item in data_list:
            if type(item.string) != types.NoneType:
                test = item.string.encode("utf-8")
                contents = contents + test
        news_item["news_content"] = contents
        key_map = {}
        for x,w in jieba.analyse.extract_tags(contents,withWeight=True):
            key_map[x] = w
        news_item["news_key"] = json.dumps(key_map)
        yield news_item

        for item in soup.findAll("a"):
            if item.has_attr("href"):
                head_url_list = re.findall(self.head_re,item["href"])
                detail_url_list = re.findall(self.detail_re,item["href"])
                if type(head_url_list) != types.NoneType:
                    for tmp in head_url_list:
                        if tmp not in SAVED_URL:
                            yield Request(tmp,callback=self.parse_item_yield)
                if type(detail_url_list) != types.NoneType:
                    for tmp in detail_url_list:
                        if tmp not in SAVED_URL:
                            yield Request(tmp,callback=self.parse_item_yield)