#!/usr/bin/env python
# coding=utf-8
from pymongo import MongoClient
import pymongo
settings = {
    "MONGODB_SERVER":"10.18.103.154",
    "MONGODB_PORT":27017,
    "MONGODB_DB":"spiderdb",
    "MONGODB_COLLECTION":"imagetable"
}

class DataManager():
    def __init__(self):
        mc = MongoClient(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
        spiderdb = mc[settings["MONGODB_DB"]]
        self._collection = spiderdb[settings["MONGODB_COLLECTION"]]
        self._saveImgList = []
    
    def __del__(self):
        if len(self._saveImgList) > 0:
            self.flush2MongoDB()

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
dataObj.updateByDistinct()
