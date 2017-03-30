#!/usr/bin/env python
# coding=utf-8

import os
import sys
import csv

def convert():
    filepath = "./labels.csv"
    if os.path.exists(filepath) == False:
        raise IOError("labels.csv not exists !")
    with open("standard_list_withPerson.csv", "w") as writer:
        csv_writer = csv.writer(writer)
        with open(filepath, 'r') as handle:
            for line in handle.readlines():
                line = line.strip().split(' ')
                keylist = []
                for item in line:
                    try:
                        num = int(item)
                    except Exception as ex:
                        keyword = [key.replace('_', '+') for key in item.split('/') if len(key) > 1]
                        keylist.extend(keyword)
                if len(keylist) == 0:
                    continue
                withPerson = []
                for key in keylist:
                    if (key[0] >= 'a' and key[0] <= 'z') or (key[0] >= 'A' and key[0] <= 'Z'):
                        key += "+person"
                        withPerson.append(key)
                    else:
                        key += "+人"
                        withPerson.append(key)
                csv_writer.writerow(withPerson)
                print(keylist)

if __name__ == "__main__":
    convert()
