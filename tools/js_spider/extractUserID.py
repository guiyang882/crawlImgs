# coding:utf8

# 从网页中提取出制定的用户的ID
import re
import codecs
import os
prefixPath = "./html/"
filelist = os.listdir("./html")

htmlid = [str(i) + ".html" for i in range(50, 161)]

userIDs = []
for filepath in filelist:
    if filepath not in htmlid:
        continue
    # print(filepath)
    with codecs.open(prefixPath + filepath, 'r', 'utf8') as handle:
        regMatch = re.compile(r'http:\/\/([a-zA-Z0-9]{3,20})\.lofter.com\"')
        for line in handle.readlines():
            res = regMatch.findall(line)
            if len(res) == 0:
                continue
            for item in res:
                if item == 'www':
                    continue
                if item not in userIDs:
                    userIDs.append(item)

for uid in userIDs:
    print(uid)