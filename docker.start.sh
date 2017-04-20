#!/bin/bash

pid=`docker ps -a | grep "scrapy" | awk -F' ' '{print $1}'`
if [ ! ${pid} ];then
    echo "Not found the pid about the scrapy docker !"
else
    docker rm -f ${pid}
fi
docker run -it \
    -m 8G \
    --cpuset-cpus="0,1,2,3" \
    -v /home/ai-i-liuguiyang/proj/crawlImgs:/root/crawlImgs \
    -v /home/store-1-img/SPIDERIMAGESDB:/root/SPIDERIMAGESDB \
    --name scrapy \
    ubuntu:scrapy /bin/bash
