from PIL import Image
import os

# settings
count = 0
filename = "icon.png"
directory = r"C:\Users\phile\PycharmProjects\OpenMosseCam\Raspberry Pi programs\app_icons\button_icons_no_transparency"
basewidth = 60

# create and fill filePathList
savedFilePathList = []
for path in os.listdir(directory):
    savedFilePathList.append(os.path.join(directory, path))

for path in savedFilePathList:
    print("starting step " + str(count) +" out of " + str(len(savedFilePathList)))
    img = Image.open(path)

    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)

    img.save(os.path.join(directory, (os.listdir(directory)[count])), quality=100)
    count += 1
    print("finished step " + str(count-1) +" out of " + str(len(savedFilePathList)))

