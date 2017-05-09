# -*- coding: utf-8 -*-

import scrapy
import urllib
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
import datetime
import pickle
import codecs
import os
import pymongo
from pymongo import MongoClient
from scrapy.conf import settings
from scrapy.exceptions import DropItem

is_Save2Mongo = True
if settings["MONGODB_ON"] == "False":
    is_Save2Mongo = False

class DataManager():
    def __init__(self):
        mc = MongoClient(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
        spiderdb = mc[settings["MONGODB_DB"]]
        self._collection = spiderdb[settings["MONGODB_COLLECTION"]]
        self._saveImgList = []
    
    def __del__(self):
        if len(self._saveImgList) > 0:
            self.flush2MongoDB()
        #self.updateByDistinct()

    def insertSpiderItem(self, item, isBatch = False):
        '''
        如果参数选择的是isBatch, 
        那么需要调用 flush2MongoDB() 将数据直接写入到DB中
        '''
        imageItem = [{
            "imageurls":item["image_urls"][0],
            "imagepath":item["image_paths"],
            "imagelabel":item["image_label"],
            "imagefromurl":item["image_fromURL"],
            "imagefromurlhost":item["image_fromURLHost"],
            "imageheight":item["image_height"],
            "imagewidth":item["image_width"],
            "imagecrawdatetime":item["image_crawDateTime"]
        }]
        if isBatch == False:
            self._collection.insert_many(imageItem)
        else:
            self._saveImgList.extend(imageItem)
    
    def flush2MongoDB(self):
        if len(self._saveImgList) > 0:
            self._collection.insert_many(self._saveImgList)
            self._saveImgList = []

    def getCachedItemSize(self):
        return len(self._saveImgList)

    def updateByDistinct(self):
        itemlist = list(self._collection.distinct("imagepath"))
        for item in itemlist:
            tmplist = list(self._collection.find({"imagepath":item}).sort([
                                ("imagecrawdatetime", pymongo.ASCENDING)
                            ]))
            if len(tmplist) > 1:
                for i in range(1, len(tmplist)):
                    self._collection.delete_many(tmplist[i])

dataObj = DataManager()

class MyImagesPipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super(MyImagesPipeline, self).__init__(store_uri, download_func, settings)
        print("######## pipelines #####")

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
                    with codecs.open("image_infos.csv", 'a', 'utf-8') as handle:
                        #handle.write(item['image_label'] + "," + item['image_paths'] + "," + item['image_urls'][0] + "\n")
                        handle.write(
                            item['image_label'] + "," + item['image_paths'] + "," + item['image_urls'][0] + "," + item["image_crawDateTime"]+ "\n")
                    print("is_Save2Mongo ", is_Save2Mongo)
                    if is_Save2Mongo == True:
                        dataObj.insertSpiderItem(item, isBatch=True)
                        print("get Cached ItemSize is ", dataObj.getCachedItemSize())
                        if dataObj.getCachedItemSize() > 100:
                            dataObj.flush2MongoDB()
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
