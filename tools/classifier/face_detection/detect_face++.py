# Copyright (c) 2009 IW.
# All rights reserved.
#
# Author: liuguiyang <liuguiyang@interns.chuangxin.com>
# Date:   2017/5/19

import urllib.request
import urllib.parse
import base64
import os
import json
import math
import cv2

baseurl = "https://api-cn.faceplusplus.com/facepp/v3/detect"
api_key = "JPGuSbXGIBVCCRsMM4aon3eAefwTChwd"
api_secret = "Kr4REbUec1lh-64mYAYvNLExw4qCmjEN"
return_landmark = 0

def fetchDetectInfo(imagefile):
    def getImageBase64(imagefile):
        if not os.path.exists(imagefile):
            raise IOError(imagefile + " not found !")

        def convert_image():
            # Picture ==> base64 encode
            with open(imagefile, 'rb') as fin:
                image_data = fin.read()
                if (len(image_data) / 1024 / 1024) <= 2:
                    base64_data = base64.b64encode(image_data)
                    return base64_data.decode()
                else:
                    K = (len(image_data) / 1024 / 1024 / 2) + 1
                    a = 1 / math.sqrt(K)
                    img = cv2.imread(imagefile)
                    h, w = img.shape[0:2]
                    new_img = cv2.resize(img, (int(a * w), int(a * h)))
                    cv2.imwrite("/tmp/" + imagefile.split("/")[-1], new_img)
                    with open("/tmp/" + imagefile.split("/")[-1], 'rb') as f:
                        image_data = f.read()
                        print(len(image_data))
                        base64_data = base64.b64encode(new_img)
                        return base64_data.decode()



        return convert_image()

    data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "image_base64": getImageBase64(imagefile),
        "return_landmark": return_landmark
    }
    postdata = urllib.parse.urlencode(data).encode(encoding="UTF8")
    req = urllib.request.Request(baseurl, data=postdata)
    page = urllib.request.urlopen(req).read().decode(encoding="UTF8")
    detect_res = json.loads(page)
    print(detect_res)

def main():
    rootDir = "/root/SPIDERIMAGESDB/DATASOURCE/Lofter/"
    if not os.path.isdir(rootDir):
        raise IOError(rootDir + " not found !")
    imagelist = os.listdir(rootDir)
    for imagefile in imagelist:
        imagefile = "6c6d454bf5b1301a8aac7f3b060a04fa1aefc0ac.jpg"
        filepath = rootDir + imagefile
        print(filepath)
        fetchDetectInfo(filepath)
        break


if __name__ == '__main__':
    main()

