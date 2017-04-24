#!/bin/bash

if [ $# != 1 ];then
    echo "Input Format Error script keyword.json path"
else
    for ind in $(seq 0 20)
    do
        scrapy crawl BaiduImg -a keywordjson=$1 -a category=$ind > run.log 2>&1 &
    done
    sleep 6h
    for ind in $(seq 0 20)
    do
        scrapy crawl ThreeSixZeroImg -a keywordjson=$1 -a category=$ind > run.log 2>&1 &
    done
    sleep 6h
    for ind in $(seq 0 20)
    do
        scrapy crawl BingSearchImg -a keywordjson=$1 -a category=$ind > run.log 2>&1 &
    done
fi

