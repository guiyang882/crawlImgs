# coding: utf-8
from PIL import Image
import face_recognition
import csv
img_dir = "/Users/hezheng/Downloads/img/"
imagelist = "/home/guiyang/Downloads/spider-2017-03-31/image.list"
with open(imagelist , "r", encoding="utf-8") as csvfile:
    read = csv.reader(csvfile)
    true_datacsv = open("true_img_list.csv","w")
    false_datacsv = open("false_img_list.csv","w")
    for i in read:
        image = face_recognition.load_image_file(i[0])
        face_locations = face_recognition.face_locations(image)
        if len(face_locations) > 0:
            print("{} face(s) in {}.".format(len(face_locations),i[0]))
            true_datacsv = open("true_img_list.csv", "a", newline="")
            csvwriter = csv.writer(true_datacsv, dialect=("excel"))
            csvwriter.writerow(i)
        else:
            false_datacsv = open("false_img_list.csv", "a", newline="")
            csvwriter = csv.writer(false_datacsv, dialect=("excel"))
            csvwriter.writerow(i)
    true_datacsv.close()
    false_datacsv.close()

# image = face_recognition.load_image_file(img_dir+img_name)

# Find all the faces in the image
# face_locations = face_recognition.face_locations(image)
#
# print("I found {} face(s) in this photograph.".format(len(face_locations)))

# for face_location in face_locations:
#
#     # Print the location of each face in this image
#     top, right, bottom, left = face_location
#     print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
#
#     # You can access the actual face itself like this:
#     face_image = image[top:bottom, left:right]
#     pil_image = Image.fromarray(face_image)
#     pil_image.show()
