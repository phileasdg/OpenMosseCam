import os
import glob
from PIL import Image
from PIL.ExifTags import TAGS
import time

def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

os.chdir(r"C:\Users\phile\OneDrive\Bureau\Classes @COA\Spring 2020\Human Ecology core course\Jodi and Sarah\Framing")

files = glob.glob("*.JPG")

for file in files:
    print(file)
    time = get_exif(file)["DateTimeOriginal"]

    time = time.replace(":", "")
    time = time.replace(" ", "_")
    number = 0
    new_name = time+".jpg"
    # new_name = time+"_additional_information.jpg"
    if new_name == file:
        print(new_name, "already ok")
        continue
    while os.path.exists(new_name):
        number += 1
        new_name = time+"_"+str(number)+".jpg"
        # new_name = time+"_"+str(number)+"_additional_information.jpg"
    os.rename(file, new_name)
