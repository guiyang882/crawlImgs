#!/bin/bash

for ind in $(seq 0 12)
do
    echo $ind
    scrapy crawl BaiduImg -a category=$ind > run.log 2>&1 &
    scrapy crawl ThreeSixZeroImg -a category=$ind > run.log 2>&1 &
done
