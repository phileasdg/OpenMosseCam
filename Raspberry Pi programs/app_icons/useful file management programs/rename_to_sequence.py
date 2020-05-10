import os
import glob
from PIL import Image
from PIL.ExifTags import TAGS
import time

os.chdir(r"C:\Users\phile\OneDrive\Bureau\Classes @COA\Spring 2020\Human Ecology core course\Jodi and Sarah\Framing")

files = glob.glob("*.JPG")
number = 0

for file in files:
    print(file)
    new_name = str(number)+".jpg"
    if new_name == file:
        print(new_name, "already ok")
        continue
    number += 1
    os.rename(file, new_name)
