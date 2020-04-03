iso = [0, 100, 160, 200, 250, 320, 400, 500, 640, 800]  # 0 is auto ISO
shutterSpeed = [0, 600000]  # not actually the list I'm going to use, just a range for ref.
whiteBalance = ["auto", "sunlight", "cloudy", "shade", "tungsten", "fluorescent", "incandescent", "flash", "horizon"]
# in whiteBalance, "off" is an option, but I am not including it in the list now because it disables the preview
fileFormat = ["jpeg", "png"]  # #format can be 'jpg', 'png', 'yuv', 'rgb', 'rgba', 'bgr', 'bgra'.
displayInfo = True

isoIndex = 0  # type: int
shutterSpeedIndex = 0 # type: int
whiteBalanceIndex = 0 # type: int
fileformatIndex = 0 #type: int

settings = ["iso", "shutterSpeed", "whiteBalance", "displayInfo", "fileformat"]
currentSettingIndexInt = 0  # saves the current editable setting

overlayString = 'ISO: ' + str(iso[isoIndex]) + " || speed: " + str(shutterSpeed[shutterSpeedIndex]) + " || WB: " + str(whiteBalance[whiteBalanceIndex]) + " || format: " + str(fileFormat[fileformatIndex]) + " || info: " + str(displayInfo)
if 0 <= currentSettingIndexInt <= 4:
    global overlayString
    if currentSettingIndexInt == 0:
        overlayString = '[ISO: ' + str(iso[isoIndex]) + "] || speed: " + str(shutterSpeed[shutterSpeedIndex]) + " || WB: " + str(whiteBalance[whiteBalanceIndex]) + " || format: " + str(fileFormat[fileformatIndex]) + " || info: " + str(displayInfo)
    elif currentSettingIndexInt == 1:
        overlayString = 'ISO: ' + str(iso[isoIndex]) + " || [speed: " + str(shutterSpeed[shutterSpeedIndex]) + "] || WB: " + str(whiteBalance[whiteBalanceIndex]) + " || format: " + str(fileFormat[fileformatIndex]) + " || info: " + str(displayInfo)
    elif currentSettingIndexInt == 2:
        overlayString = 'ISO: ' + str(iso[isoIndex]) + " || speed: " + str(shutterSpeed[shutterSpeedIndex]) + " || [WB: " + str(whiteBalance[whiteBalanceIndex]) + "] || format: " + str(fileFormat[fileformatIndex]) + " || info: " + str(displayInfo)
    elif currentSettingIndexInt == 3:
        overlayString = 'ISO: ' + str(iso[isoIndex]) + " || speed: " + str(shutterSpeed[shutterSpeedIndex]) + " || WB: " + str(whiteBalance[whiteBalanceIndex]) + " || [format: " + str(fileFormat[fileformatIndex]) + "] || info: " + str(displayInfo)
    elif currentSettingIndexInt == 4:
        currentSettingIndexInt = 'ISO: ' + str(iso[isoIndex]) + " || speed: " + str(shutterSpeed[shutterSpeedIndex]) + " || WB: " + str(whiteBalance[whiteBalanceIndex]) + " || format: " + str(fileFormat[fileformatIndex]) + " || [info: " + str(displayInfo) + "]"
    else:
        print("error: current setting index is out of defined range")

print(overlayString)
