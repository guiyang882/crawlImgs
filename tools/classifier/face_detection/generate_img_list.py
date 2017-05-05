# coding: utf-8
import os
import csv
img_dir = "/Users/hezheng/Downloads/img/"
with open("img_list.csv", "w", newline="") as datacsv:
    csvwriter = csv.writer(datacsv, dialect=("excel"))
    g = os.walk(img_dir)
    for path,d,filelist in g:
        for filename in filelist:
            if filename.endswith('jpg'):
                f = os.path.join(path, filename)
                csvwriter.writerow ([f])

# with open('thefile.txt', 'w') as file_object:
#     x = []
#     g = os.walk(img_dir)
#     for path,d,filelist in g:
#         for filename in filelist:
#             if filename.endswith('jpg'):
#                 f = os.path.join(path, filename)
#                 f = f + '\n'
#                 x.append(f)
#     print(x)
#     file_object.writelines(x)
# file_object.close()

# with open('thefile.txt', 'r') as file_object:
#     lines = file_object.readlines()
#     for line in lines:
#         filename = line.split('\n')
#         print(filename[0])
