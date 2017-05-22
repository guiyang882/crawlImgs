#!/bin/bash
for ind in $(seq 161 180)
do
	echo $ind
    casperjs main.js $ind &
done
