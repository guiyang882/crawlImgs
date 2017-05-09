# -*- coding: utf-8 -*-
# @Time    : 2017/5/9 14:42
# @Author  : liuguiyangnwpu@gmail.com
# @File    : scene.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function
import json
from copy import deepcopy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

with open('scenes.json', 'r') as f:
    data = json.load(f)

log_file = "nohup.log"
sougou_list = 'sougou_list.txt'

def search(query):
    pre1 = '_'
    pre2 = '-'
    af = ' '
    query2 = query.replace(pre1, af)
    query1 = query2.replace(pre2, af)
    for scene in data.keys():
        for keyword in data[scene]:
            if query1 in data[scene][keyword]:
                return scene
    return "not found"

with open(log_file, 'r') as reader:
    samples = []
    for line in reader.readlines():
        line = line.strip().split(' ')
        samples.append(deepcopy(line))
    samples = sorted(samples, key=lambda x:x[0])

    def _showRes(singleItem):
        val = singleItem[2]
        word = search(val)
        if word == "not found":
            print(singleItem[0], "Others")
        else:
            print(singleItem[0], word)

    size = len(samples)
    for index in range(size):
        if '/' not in samples[index][0]:
            continue
        if len(samples[index]) != 4:
            continue
        rank = int(float(samples[index][1]))
        _showRes(samples[index])
