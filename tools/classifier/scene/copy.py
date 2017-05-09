# -*- coding: utf-8 -*-
# @Time    : 2017/5/9 15:32
# @Author  : liuguiyangnwpu@gmail.com
# @File    : copy.py.py
# @Software: PyCharm

from __future__ import absolute_import
from __future__ import print_function
import os
import shutil
import codecs
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    filelog = "./res.csv"
    srcprefix = "/home/store-1-img/SPIDERIMAGESDB/部分结果/第三批测试图像37431张.05.07/"
    destprefix = "./存储的目录/"
    with codecs.open(filename=filelog, 'r', 'utf8') as handle:
        for line in handle.readlines():
            line = line.strip().split(' ')
            if os.path.exists(srcprefix + line[0]):
                t = destprefix+line[-1]
                if not os.path.isdir(t):
                    os.makedirs(t)
                savepath = t + "/" + line[0].split('/')[-1]
                shutil.move(srcprefix+line[0], savepath)

if __name__ == '__main__':
    main()