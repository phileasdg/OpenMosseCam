ISOsetting = "100"
shutterSetting = "1/100"
modeSetting = "photo"  # or video
effectSetting = "none"
formatSetting = "png"
resolutionSetting = "1920x1080"
AWBmodeSetting = "greyworld"
REDwhiteBalanceGain = "0.0"
BluewhiteBalanceGain = "0.0"

settingsDictionary = {
    "ISO": ISOsetting,
    "Shutter": shutterSetting,
    "Mode": modeSetting,
    "Effect": effectSetting,
    "Format": formatSetting,
    "Resolution": resolutionSetting,
    "AWB": AWBmodeSetting,
    "Red:": REDwhiteBalanceGain,
    "Blue:": BluewhiteBalanceGain
}

for k, v in settingsDictionary.items():

    print(k, v)
    k = fontObj.render(v), True, GREEN)  # text, anti-aliasing, text colour, bg colour
    textRectObj = k.get_rect()
    textRectObj.topleft = (a, a)
