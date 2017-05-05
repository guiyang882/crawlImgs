#!/bin/bash

pid=`docker ps -a | grep "face" | awk -F' ' '{print $1}'`
if [ ! ${pid} ];then
    echo "Not found the pid about the scrapy docker !"
else
    docker rm -f ${pid}
fi
docker run -it \
    -v /home/ai-i-liuguiyang/proj/crawlImgs:/root/crawlImgs \
    -v /home/store-1-img/SPIDERIMAGESDB:/root/SPIDERIMAGESDB \
    --name face \
    ubuntu:face /bin/bash
