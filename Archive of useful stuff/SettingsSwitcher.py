from gpiozero import Button
from time import sleep

# variables (initial values)

iso = [0, 100, 160, 200, 250, 320, 400, 500, 640, 800] # 0 is auto ISO
shutterSpeed = [0, 600000] #not actually the list I'm going to use, just a range for ref.
whiteBalance = ["off", "auto", "sunlight", "cloudy", "shade", "tungsten", "fluorescent", "incandescent", "flash", "horizon"]
displayInfo = True

isoIndex = 0
shutterSpeedIndex = 0
whiteBalanceIndex = 1

settings = ["iso", "shutterSpeed", "whiteBalance", "displayInfo"]
currentSettingIndexInt = 0
# saves the current editable setting

button4 = Button(27)
button2 = Button(22)  # used as "next/up" button, moves setting to the previous option in settings list

# functions

def setting_toggle_button_press():
    global currentSettingIndexInt
    i = currentSettingIndexInt
    if 0 <= i < 3:
        i += 1
    elif i >= 3:
        i = 0
    else:
        print ("error: current setting index outside of list range")
    currentSettingIndexInt = i

    print (currentSettingIndexInt)
    print (settings[currentSettingIndexInt])
    sleep(0.3)
    return currentSettingIndexInt

def next_up_button_press():
    global currentSettingIndexInt
    i = currentSettingIndexInt
    if 0 <= i <= 3:
        if i == 0: # ISO index + 1
            global isoIndex
            isoi = isoIndex
            if 0 <= isoi < 9:
                isoi += 1
            elif isoi >= 9:
                isoi = 0
            else:
                print ("error: iso index is out of list range")
            isoIndex = isoi
        if i == 1: #shutter speed index + 1 (TODO: Change when I update the shutter speed list)
            global shutterSpeedIndex
            sh = shutterSpeedIndex
            if 0 <= sh < 1:
                sh += 1
            elif sh >= 1:
                sh = 0
            else:
                print ("error: iso index is out of list range")
            shutterSpeedIndex = sh
        if i == 2: # white balance index + 1
            global whiteBalanceIndex
            wb = whiteBalanceIndex
            if 0 <= wb < 9:
                wb += 1
            elif wb >= 9:
                wb = 0
            else:
                print ("error: iso index is out of list range")
            whiteBalanceIndex = wb
        if i == 3: # display info boolean switch
            global displayInfo
            info = not displayInfo
            displayInfo = info
    else:
        print ("error: the current setting value is outside of the 0-3 range")

    print ("iso: ", iso[isoIndex])
    print ("shutterspeed: ", shutterSpeed[shutterSpeedIndex])
    print ("white balance:", whiteBalance[whiteBalanceIndex])
    print ("display info ", displayInfo)


# software code
print (currentSettingIndexInt)
print (settings[currentSettingIndexInt])

button4.when_pressed = setting_toggle_button_press
button2.when_pressed = next_up_button_press



