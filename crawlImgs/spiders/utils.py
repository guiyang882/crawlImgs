#!/usr/bin/env python
# coding=utf-8
import os
import json
import codecs

def parseClassificationTemplate(fetchKeyWords):
    wordlist = []
    if isinstance(fetchKeyWords, dict):
        for key in fetchKeyWords.keys():
            val = fetchKeyWords[key]
            tmplist = [key]
            for item in val:
                tmplist.append(key + "+" + item)
            wordlist.append(tmplist)
    return wordlist

def parseSceneTemplate(fetchKeyWords):
    wordlist = []
    if isinstance(fetchKeyWords, dict):
        for scene in fetchKeyWords.keys():
            scenedict = fetchKeyWords[scene]
            if isinstance(scenedict, dict):
                for sceneKernal in scenedict.keys():
                    tmplist = [sceneKernal]
                    val = scenedict[sceneKernal]
                    for item in val:
                        tmplist.append(sceneKernal + "+" + item)
                    wordlist.append(tmplist)
    return wordlist

def parseJsonTemplate(wordjson):
    if "fetchPageNums" not in wordjson.keys():
        wordjson["fetchPageNums"] = 5
    if "taskName" not in wordjson.keys():
        raise IOError("taskName not in " + keywordfile + " !")
    if wordjson["taskName"] not in ["CLASSIFICATION", "DETECTION", "SCENE", "OTHERS"]:
        raise IOError("In " + keywordfile + " Not Contain the taskName " + wordjson["taskName"])
    if "fetchKeyWords" not in wordjson.keys():
        raise IOError("Not found the fetch Keywords !")

    wordlist = []
    if wordjson["taskName"] == "CLASSIFICATION":
        wordlist = parseClassificationTemplate(wordjson["fetchKeyWords"])
    elif wordjson["taskName"] == "DETECTION":
        wordlist = parseClassificationTemplate(wordjson["fetchKeyWords"])
    elif wordjson["taskName"] == "OTHERS":
        wordlist = parseClassificationTemplate(wordjson["fetchKeyWords"])
    elif wordjson["taskName"] == "SCENE":
        wordlist = parseSceneTemplate(wordjson["fetchKeyWords"])
    else:
        pass
    return wordlist

def getPartLabel(keywordfile, partID):
    if isinstance(partID, str):
        partID = int(partID)

    wordlist, totalPage = [], 5
    if os.path.exists(keywordfile) == False:
        raise IOError(keywordfile + " not exists !")
    with codecs.open(keywordfile, 'r', 'utf-8') as handle:
        wordjson = json.load(handle)
        tmplist = parseJsonTemplate(wordjson)
        cnt = 0
        for line in tmplist:
            cnt += 1
            if int(cnt / 20) == partID:
                wordlist.extend(line)
        totalPage = wordjson["fetchPageNums"]
        if isinstance(totalPage, str):
            totalPage = int(totalPage)
    return wordlist, totalPage
