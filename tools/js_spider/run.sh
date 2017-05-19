#!/bin/bash
for ind in $(seq 81 90)
do
	echo $ind
    casperjs main.js $ind &
done
