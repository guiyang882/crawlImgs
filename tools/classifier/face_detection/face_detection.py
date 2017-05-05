# -*- coding: utf-8 -*-
# @Time    : 2017/5/5 15:54
# @Author  : liuguiyangnwpu@gmail.com
# @File    : face_detection.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function

import os
import face_recognition

from pymongo import MongoClient

DBSETTINGS = {
    "MONGODB_SERVER":"10.18.103.205",
    "MONGODB_PORT":27017,
    "MONGODB_DB":"spiderdb",
    "MONGODB_COLLECTION":"imagetable"
}

mc = MongoClient(DBSETTINGS["MONGODB_SERVER"], DBSETTINGS["MONGODB_PORT"])
spiderdb = mc[DBSETTINGS["MONGODB_DB"]]
dbtable = spiderdb[DBSETTINGS["MONGODB_COLLECTION"]]

def main():
    itemlist = list(dbtable.find({'exists_person': {'$exists': False}}))
    print(len(itemlist))
    srcprefix = "/root/SPIDERIMAGESDB/DATASOURCE/"
    for item in itemlist:
        partpath = item["imagepath"]
        filepath = srcprefix + partpath
        if not os.path.exists(filepath):
            continue
        try:
            image = face_recognition.load_image_file(filepath)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) > 0:
                dbtable.update({"_id": item["_id"]}, {'$set': {"exists_person": 1}})
            else:
                dbtable.update({"_id": item["_id"]}, {'$set': {"exists_person": 0}})
            print(item["_id"])
        except Exception as es:
            print(es)

if __name__ == '__main__':
    main()
