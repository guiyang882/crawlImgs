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

baseurl = "https://api-cn.faceplusplus.com/facepp/v3/detect"
api_key = "JPGuSbXGIBVCCRsMM4aon3eAefwTChwd"
api_secret = "Kr4REbUec1lh-64mYAYvNLExw4qCmjEN"
return_landmark = 0

def buildPOSTRequest(imagefile):
    def getImageBase64(imagefile):
        if not os.path.exists(imagefile):
            raise IOError(imagefile + " not found !")

        def convert_image():
            # Picture ==> base64 encode
            with open(imagefile, 'rb') as fin:
                image_data = fin.read()
                base64_data = base64.b64encode(image_data)
                return base64_data.decode()

        return convert_image()

    data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "image_base64": getImageBase64(imagefile),
        "return_landmark": return_landmark
    }
    postdata = urllib.parse.urlencode(data)
    req = urllib.request.Request(baseurl, data=postdata)
    page = urllib.request.urlopen(req).read()
    detect_res = json.loads(page)
    print(detect_res)

def main():
    rootDir = ""
    if not os.path.isdir(rootDir):
        raise IOError(rootDir + " not found !")
    imagelist = os.listdir(rootDir)
    for imagefile in imagelist:
        print(imagefile)

if __name__ == '__main__':
    main()

