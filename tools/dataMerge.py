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
import multiprocessing

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

def removeInvalidItem(itemlist, pid):
    """去除数据库中无效的item，主要的判别依据是去除不在文件系统中的item"""
    mc = MongoClient(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
    spiderdb = mc[settings["MONGODB_DB"]]
    dbtable = spiderdb[settings["MONGODB_COLLECTION"]]

    srcprefix = "/root/SPIDERIMAGESDB/DATASOURCE/"
    for item in itemlist:
        partpath = item["imagepath"]
        filepath = srcprefix + partpath
        if not os.path.exists(filepath):
            print(item["_id"], pid)
            dbtable.remove(item)

def addSpecificInfo2Item(itemlist, pid):
    """将DB中，缺少关键字 imagename 进行添加"""
    mc = MongoClient(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
    spiderdb = mc[settings["MONGODB_DB"]]
    dbtable = spiderdb[settings["MONGODB_COLLECTION"]]
    # itemlist = list(dbtable.find({"imagename": {"$exists": False}}))
    for item in itemlist:
        partpath = item["imagepath"]
        imgname = partpath.split("/")[-1]
        print(item["_id"])
        dbtable.update({"_id": item["_id"]}, {"$set": {"imagename": imgname}})

if __name__ == '__main__':
    mc = MongoClient(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
    spiderdb = mc[settings["MONGODB_DB"]]
    dbtable = spiderdb[settings["MONGODB_COLLECTION"]]
    itemlist = list(dbtable.find())
    totalLen = len(itemlist)
    nthreads = 8
    pool = multiprocessing.Pool(processes=nthreads)
    singlepart = totalLen // nthreads
    start = 0
    for ind in range(nthreads + 1):
        if start < totalLen:
            partItem = itemlist[start:start + singlepart]
            start += singlepart
            pool.apply_async(removeInvalidItem, (partItem, ind + 1,))
    pool.close()
    pool.join()