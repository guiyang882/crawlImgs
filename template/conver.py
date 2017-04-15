#!/usr/bin/env python
# coding=utf-8
import json
import codecs
from pprint import pprint

filepath = "./template.SCENE.json"
with open(filepath, 'r') as handle:
    data = json.load(handle)
    data = data["fetchKeyWords"]
    destData = {}
    for key in data.keys():
        val = data[key]
        destData[key] = {}
        for item in val:
            for kk in item.keys():
                destData[key][kk] = item[kk]
    with open("./tmp.json", 'w') as handle:
        json.dump(destData, handle)

