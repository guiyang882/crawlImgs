# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import urllib
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
import datetime
import pickle
import os
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class DataManager():
    def __init__(self):
        connection = pymongo.Connection(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
        spiderdb = connection[settings["MONGODB_DB"]]
        self._collection = spiderdb[settings["MONGODB_COLLECTION"]]
        self._saveImgList = []

    def insertSpiderItemBySingle(self, item, isBatch = False):

        pass

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        url = item['image_urls'][0]
        try:
            request = scrapy.Request(url)
        except Exception as es:
            print(es)
            request = None
        if request != None:
            request.meta['word'] = item['image_label']
            yield request

    def item_completed(self, results, item, info):
        if results != None:
            for ok, x in results:
                if ok:
                    image_path = x['path']
                    item['image_paths'] = image_path
                    # print(item["image_label"] + "," + item["image_paths"] + "," + item["image_urls"][0] + "\n")
                    with open("image_infos.csv", 'a') as handle:
                        handle.write(item['image_label'] + "," + item['image_paths'] + "," + item['image_urls'][0] + "\n")

                    return item

    def file_path(self, request, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url
        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        word = str(request.meta['word']).split('word=')[-1]
        try:
            word = urllib.unquote(word).decode('utf-8')
        except Exception as ex:
            word = urllib.parse.unquote(word)
        print(word + "/%s.jpg" % image_guid)
        return word + '/%s.jpg' % (image_guid)
