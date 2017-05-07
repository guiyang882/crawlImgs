# -*- coding: utf-8 -*-
# @Time    : 2017/5/7 18:13
# @Author  : liuguiyangnwpu@gmail.com
# @File    : dataMerge.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function
import os
import codecs
from pymongo import MongoClient

settings = {
    "MONGODB_SERVER":"10.18.103.205",
    "MONGODB_PORT":27017,
    "MONGODB_DB":"spiderdb",
    "MONGODB_COLLECTION":"imagetable"
}

def flagItem(filename):
    """主要是用来标记哪些图像的数据是被标记的"""
    mc = MongoClient(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
    spiderdb = mc[settings["MONGODB_DB"]]
    dbtable = spiderdb[settings["MONGODB_COLLECTION"]]
    if not os.path.exists(filename):
        raise IOError(filename + " not Found !")
    with codecs.open(filename, 'r', 'utf8') as handle:
        for line in handle.readlines():
            subfix = line.strip().split('.')[-1]
            if subfix not in ["png", "bmp", "jpg", "JPG", "PNG", "jpeg", "JPEG"]:
                continue
            imagename = line.strip().split('/')[-1]
            itemlist = list(dbtable.find({"imagename":imagename}))
            for item in itemlist:
                dbtable.update({"_id": item["_id"]}, {"$set": {"fetched": 1}})
if __name__ == '__main__':
    filename = ""
    flagItem(filename)