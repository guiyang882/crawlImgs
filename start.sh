#!/bin/bash

for ind in $(seq 0 12)
do
    echo $ind
    scrapy crawl BaiduImg -a category=$ind &
done
