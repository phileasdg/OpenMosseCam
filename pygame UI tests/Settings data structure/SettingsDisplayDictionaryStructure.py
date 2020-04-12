ISOsetting = "100"
shutterSetting = "1/100"
modeSetting = "photo"  # or video
effectSetting = "none"
formatSetting = "png"
resolutionSetting = "1920x1080"
AWBmodeSetting = "greyworld"
REDwhiteBalanceGain = "0.0"
BluewhiteBalanceGain = "0.0"

settingsFetcherDictionary = {
    "ISO": ISOsetting, # v can be a list
    "Shutter": shutterSetting,
    "Mode": modeSetting,
    "Effect": effectSetting,
    "Format": formatSetting,
    "Resolution": resolutionSetting,
    "AWB": AWBmodeSetting,
    "Red:": REDwhiteBalanceGain,
    "Blue:": BluewhiteBalanceGain
}

settingsList = ["ISO", "Shutter", "Mode", "Effect", "Format", "Resolution", "AWB", "Red:", "Blue:"]
for i in settingsList:
    print(settingsFetcherDictionary[i])

# for k, v in settingsDictionary.items():
#     print(k, v)
