#!/bin/bash

for ind in $(seq 0 12)
do
    scrapy crawl BaiduImg -a category=$ind > run.log 2>&1 &
done

sleep 120m

for ind in $(seq 0 12)
do
    scrapy crawl ThreeSixZeroImg -a category=$ind > run.log 2>&1 &
done
