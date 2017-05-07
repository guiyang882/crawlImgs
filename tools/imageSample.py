# -*- coding: utf-8 -*-
# @Time    : 2017/5/7 17:03
# @Author  : liuguiyangnwpu@gmail.com
# @File    : imageSample.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function
import os
import codecs
from pymongo import MongoClient
import multiprocessing
import shutil
import random

settings = {
    "MONGODB_SERVER": "10.18.103.205",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "spiderdb",
    "MONGODB_COLLECTION": "imagetable"
}

"""该文件主要是将数据库中采样出数据，提供给外部进行处理"""
def extractPersonImageFromDB_tagFlag():
    mc = MongoClient(settings["MONGODB_SERVER"], settings["MONGODB_PORT"])
    spiderdb = mc[settings["MONGODB_DB"]]
    dbtable = spiderdb[settings["MONGODB_COLLECTION"]]
    # 找到所有含有人的但是还没有进行采样的数据进行数据的提取
    itemlist = list(dbtable.find({"exists_person":1, "fetched": {"$exists": False}}))
    print(len(itemlist))
    for item in itemlist:
        partpath = item["imagepath"]
        print(partpath)
        dbtable.update({"_id": item["_id"]}, {"$set": {"fetched": 1}})

def copyImage():
    """该函数主要是将数据中导出的列表数据从制定的目录中读取出来，并储存到制定的目录中去"""
    srcprefix = "/root/SPIDERIMAGESDB/DATASOURCE/"
    saveDir = "/root/SPIDERIMAGESDB/部分结果/第三批测试图像39649张.05.07/"
    filename = "/root/SPIDERIMAGESDB/部分结果/第三批提取数据的日志2017.05.07.csv"
    if not os.path.exists(filename):
        raise IOError(filename + " not Exists !")
    with codecs.open(filename, 'r', 'utf8') as handle:
        for line in handle.readlines():
            line = line.strip()
            absfilepath = srcprefix + line
            if not os.path.exists(absfilepath):
                continue
            dirname = line.split("/")[-2]
            if "+" in dirname:
                dirname = dirname.split("+")[0]
            if not os.path.isdir(saveDir + dirname):
                os.makedirs(saveDir + dirname)
            saveabspath = saveDir + dirname + "/" + line.split("/")[-1]
            shutil.copy(absfilepath, saveabspath)
            print(saveabspath)

if __name__ == '__main__':
    copyImage()
