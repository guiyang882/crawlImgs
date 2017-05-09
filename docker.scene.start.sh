#!/bin/bash

pid=`docker ps -a | grep "scene" | awk -F' ' '{print $1}'`
if [ ! ${pid} ];then
    echo "Not found the pid about the scrapy docker !"
else
    docker rm -f ${pid}
fi
docker run -it \
    -v /home/store-1-img/SPIDERIMAGESDB/部分结果/第三批测试图像37431张.05.07:/root/caffe/sougou \
    --name scene \
    ubuntu:scene /bin/bash
