# Copyright (c) 2009 IW.
# All rights reserved.
#
# Author: liuguiyang <liuguiyang@interns.chuangxin.com>
# Date:   2017/5/19

"""
主要是将数据推送到阿里云服务器
"""
import os
import oss2
auth = oss2.Auth('LTAIUyqFtCCwOFlG', 'KM19zPQabzSbNsYmXVJYBYVgLUtXP5')
bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'tolabel')
prefix = "./Lofter/"
for image in os.listdir(prefix):
    filepath = prefix + image
    try:
        print(filepath)
        print(bucket.put_object_from_file('chuangxin/20170519/' + image, filepath))
    except Exception as es:
        print(es)