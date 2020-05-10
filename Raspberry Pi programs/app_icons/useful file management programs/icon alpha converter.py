from PIL import Image
import os

# settings
count = 0
filename = "icon.png"
directory = r"C:\Users\phile\PycharmProjects\OpenMosseCam\Raspberry Pi programs\app_icons\button_icons_no_transparency"

# create and fill filePathList
savedFilePathList = []
for path in os.listdir(directory):
    savedFilePathList.append(os.path.join(directory, path))

for path in savedFilePathList:
    print("starting step " + str(count) +" out of " + str(len(savedFilePathList)))
    img = Image.open(path)

    # remove alpha
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:  # choose colour to be alpha
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(os.path.join(directory, (os.listdir(directory)[count])), quality=100)
    count += 1
    print("finished step " + str(count-1) +" out of " + str(len(savedFilePathList)))
