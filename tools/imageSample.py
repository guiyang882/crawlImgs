# -*- coding: utf-8 -*-
# @Time    : 2017/5/7 17:03
# @Author  : liuguiyangnwpu@gmail.com
# @File    : imageSample.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function

import os
import shutil
import codecs
import random

"""该文件主要是将数据库中采样出数据，提供给外部进行处理"""
def mainSample():
    def _isEnglish(keyWord):
        for c in keyWord:
            if not ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')):
                return False
        return True

    filelist = "./res.list"

    def _fromScene(isChinese=False):
        scene_list = []
        with codecs.open(filelist, 'r', 'utf8') as handle:
            for line in handle.readlines():
                imgClass = line.strip().split('/')[-2]
                if '+' in imgClass:
                    print(imgClass.split('+')[0], imgClass.split('+')[0].isalpha())
                    if isChinese == False:
                        scene_list.append(line.strip())
                    elif _isEnglish(imgClass.split('+')[0]) == False:
                        scene_list.append(line.strip())

        res_list = []
        random.shuffle(scene_list)
        print(len(scene_list))
        a = random.sample(scene_list, 1200)
        res_list.extend(a)
        return res_list

    def _load_sceneMap():
        filepath = "./scene.map"
        scene_map = {}
        with codecs.open(filepath, 'r', 'utf-8') as handle:
            for line in handle.readlines():
                line = line.strip().split(',')
                key = line[0]
                for cell in line:
                    scene_map[cell] = key
        return scene_map

    saveDir = "./sampleImgs"
    res_list = _fromScene(isChinese=True)
    scene_map = _load_sceneMap()

    for item in res_list:
        if '+' in item.strip().split('/')[-2]:
            keyWord = item.strip().split('/')[-2].split('+')[0]
        else:
            keyWord = item.strip().split('/')[-2]
        if keyWord in scene_map.keys():
            keyWord = scene_map[keyWord]
        if os.path.isdir(saveDir + "/" + keyWord) == False:
            os.makedirs(saveDir + "/" + keyWord)
        savepath = saveDir + "/" + keyWord + "/" + item.strip().split('/')[-1]
        print(savepath)
        shutil.copy(item, savepath)

if __name__ == '__main__':
    mainSample()