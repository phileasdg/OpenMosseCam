# Settings lists
iso = [0, 100, 160, 200, 250, 320, 400, 500, 640, 800]  # 0 is auto ISO
shutterSpeed = [0, 125, 156, 200, 250, 312, 400, 500, 625, 800, 1000, 1250, 1562, 2000, 2500, 3125, 4000, 5000, 6250,
                8000, 10000, 12500, 16666, 20000, 25000, 33333, 40000, 50000, 66666, 76923, 100000, 125000, 166666,
                200000, 250000, 300000, 400000, 500000, 600000, 800000, 1000000, 1300000, 1600000, 2000000, 2500000,
                3200000, 4000000, 5000000, 6000000]
shutterSpeedTranslation = ["auto", "1/8000", "1/6400", "1/5000", "1/4000", "1/3200", "1/2500", "1/2000", "1/1600",
                           "1/1250", "1/1000", "1/800", "1/640", "1/500", "1/400", "1/320", "1/250", "1/200", "1/160",
                           "1/125", "1/100", "1/80", "1/60", "1/50", "1/40", "1/30", "1/25", "1/20", "1/15", "1/13",
                           "1/10", "1/8", "1/6", "1/5", "1/4", "0.3", "0.4", "0.5", "0.6", "0.8", "1", "1.3", "1.6",
                           "2",
                           "2.5", "3.2", "4", "5", "6"]
whiteBalance = ["off", "greyworld", "auto", "sunlight", "cloudy", "shade", "tungsten", "fluorescent", "incandescent",
                "flash", "horizon"]
# in whiteBalance, "off" is an option, but I am not including it in the list now because it disables the preview
displayInfo = True
fileFormat = ["jpeg", "png"]  # #format can be 'jpg', 'png', 'yuv', 'rgb', 'rgba', 'bgr', 'bgra'.
imageEffect = ['none', 'negative', 'solarize', 'hatch', 'gpen', 'film', 'colorswap', 'washedout',
               'colorbalance', 'cartoon']
# effects availablee: 'none', 'negative', 'solarize', 'sketch', 'denoise', 'emboss', 'oilpaint', 'hatch', 'gpen',
# 'pastel', 'watercolor', 'film', 'blur', 'saturation', 'colorswap', 'washedout', 'posterise', 'colorpoint',
# 'colorbalance', 'cartoon', 'deinterlace1', 'deinterlace2'


# Settings lists index recorders and reference
isoIndex = 0  # type: int
shutterSpeedIndex = 0  # type: int
whiteBalanceIndex = 1  # type: int
fileformatIndex = 0  # type: int
imageEffectIndex = 0  # type: int

whiteBalanceGainRED = 0.9
whiteBalanceGainBLUE = 0.9

# List of settings and List of settings recorder
settings = ["iso", "shutterSpeed", "whiteBalance", "displayInfo", "fileFormat", "imageEffect", "WB RED gains",
            "WB BLUE gains"]

# ignore the bits above

currentSettingIndexInt: int = 7  # saves the current editable setting
highlightBracketList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]

for i in range(16):
    if currentSettingIndexInt * 2 == i:
        highlightBracketList[i] = "["
    elif currentSettingIndexInt * 2 + 1 == i:
        highlightBracketList[i] = "]"
    else:
        highlightBracketList[i] = " "

    print(highlightBracketList[i])

overlayString = " || " + highlightBracketList[0] + "ISO: " + str(iso[isoIndex]) + highlightBracketList[1] + \
         " || \n || " + highlightBracketList[2] + "speed: " + str(shutterSpeedTranslation[shutterSpeedIndex]) + highlightBracketList[3] +\
         " || \n || " + highlightBracketList[4] + "AWB: " + str(whiteBalance[whiteBalanceIndex]) + highlightBracketList[5] +\
         " || \n || " + highlightBracketList[6] + "info: " + str(displayInfo) + highlightBracketList[7] +\
         " || \n || " + highlightBracketList[8] + "format: " + str(fileFormat[fileformatIndex]) + highlightBracketList[9] + \
         " || \n || " + highlightBracketList[10] + "effect: " + str(imageEffect[imageEffectIndex]) + highlightBracketList[11] +\
         " || \n || " + highlightBracketList[12] + "RED gain: " + str(round(whiteBalanceGainRED, 2)) + highlightBracketList[13] +\
         " || \n || " + highlightBracketList[14] + "BLUE gain: " + str(round(whiteBalanceGainBLUE, 2)) + highlightBracketList[15] +\
         "  ||"

print(overlayString)

