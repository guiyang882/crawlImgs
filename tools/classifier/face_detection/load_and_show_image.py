import scipy.misc
from PIL import Image
import csv
import numpy as np
def load_image_file(filename, mode='RGB'):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array
    :param filename: image file to load
    :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
    :return: image contents as numpy array
    """
    return scipy.misc.imread(filename, mode=mode)

img_num = 245
csv_list = "false_img_list.csv"
with open(csv_list, "r", encoding="utf-8") as csvfile:
    read = csv.reader(csvfile)
    name_list = []
    for i in read:
        filename = i[0]
        name_list.append(filename)
print(name_list[img_num])
face_image = load_image_file(name_list[img_num])
pil_image = Image.fromarray(face_image)
pil_image.show()