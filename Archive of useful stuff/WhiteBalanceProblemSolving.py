#TODO: THIS CODE WORKS!!!!! NOW IMPLEMENT IT WITHIN THE MOSSECAM V1.
# imports
from picamera import PiCamera, Color
from time import sleep
from gpiozero import Button
import time
import os

# variables (initial values)

camera = PiCamera()
vidFileName = 'image_' + str(time.ctime())  # + '.jpg'

# Settings lists

whiteBalanceGainRED = 0.1  # type: float #TODO
whiteBalanceGainBLUE = 0.1 # type: float #TODO

# List of settings and List of settings recorder
settings = ["WB RED gains", "WB BLUE gains"]
currentSettingIndexInt = 0  # saves the current editable setting

# Buttons
button1 = Button(17)  # used as shutter button, runs capture function
button2 = Button(22)  # used as "next/up" button, moves setting to the previous option in settings list
button3 = Button(23)  # used as "previous/down" button, moves setting to the next option in settings list
button4 = Button(27)  # used as setting toggle button, runs settingSwitch function (changes the setting that b2 and b3


# functions
def shutter_button_press():
    global vidFileName
    imgFileName = 'image_' + str(time.ctime())  # + '.jpg'
    camera.capture(os.path.join('/home/pi/Pictures/MosseCam/', imgFileName, '.jpg'))
    camera.stop_preview()
    camera.start_preview(alpha=200)  # last 2 lines provide visual feedback for image capture
    return


def make_overlaystring_with_WB():
    global currentSettingIndexInt
    global overlayString

    if currentSettingIndexInt == 0:
        overlayString = "[RED gain: " + str(whiteBalanceGainRED)+"]" + "\n  ||  BLUE gain: " + str(whiteBalanceGainBLUE) + "  ||"  # TODO
    elif currentSettingIndexInt == 1:
        overlayString = "RED gain: " + str(whiteBalanceGainRED)+" " + "\n  || [BLUE gain: " + str(whiteBalanceGainBLUE) + "] ||"  # TODO
    else:
        print("error: current setting index is out of defined range")


def update_settings_overlay_display():
    global currentSettingIndexInt
    global overlayString
    make_overlaystring_with_WB()

    camera.annotate_text_size = 160
    camera.annotate_foreground = Color('black')
    camera.annotate_background = Color('white')
    camera.annotate_text = overlayString


def setting_toggle_button_press():
    global currentSettingIndexInt
    i = currentSettingIndexInt
    if 0 <= i < 1:
        i += 1
    elif i >= 1:
        i = 0
    else:
        print("error: current setting index outside of list range")
    currentSettingIndexInt = i

    print(currentSettingIndexInt)
    print(settings[currentSettingIndexInt])
    sleep(0.3)
    update_settings_overlay_display()
    return currentSettingIndexInt


def next_up_button_press():
    global currentSettingIndexInt
    global whiteBalanceGainRED
    global whiteBalanceGainBLUE
    i = currentSettingIndexInt
    if 0 <= i <= 1:
        if i == 0:
            if 0.1 <= whiteBalanceGainRED < 8:
                whiteBalanceGainRED += 0.1
                camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
                sleep(0.3)
            elif whiteBalanceGainRED >= 8:
                whiteBalanceGainRED = 0
                camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
        if i == 1:
            if 0.1 <= whiteBalanceGainBLUE < 8:
                whiteBalanceGainBLUE += 0.1
                camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
                sleep(0.3)
            elif whiteBalanceGainBLUE >= 8:
                whiteBalanceGainBLUE = 0
                camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
    else:
        print("error: the current setting value is outside of the defined range")
    update_settings_overlay_display()
    print(str(whiteBalanceGainRED), str(whiteBalanceGainBLUE))


def previous_down_button_press():
    global currentSettingIndexInt
    global whiteBalanceGainRED
    global whiteBalanceGainBLUE
    i = currentSettingIndexInt
    if 0 <= i <= 1:
        if i == 0:
            if 0.1 < whiteBalanceGainRED <=8:
                whiteBalanceGainRED -= 0.1
                camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
            elif whiteBalanceGainRED <= 0.1:
                whiteBalanceGainRED = 8
                camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
                sleep(0.3)
        if i == 1:
            if 0.1 < whiteBalanceGainBLUE <=8:
                whiteBalanceGainBLUE -= 0.1
                camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
            elif whiteBalanceGainBLUE <= 0.1:
                whiteBalanceGainBLUE = 8
                camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
            sleep(0.3)
    else:
        print("error: the current setting value is outside of the defined range")
    update_settings_overlay_display()
    print(str(whiteBalanceGainRED), str(whiteBalanceGainBLUE))


# software code
print(currentSettingIndexInt)
print(settings[currentSettingIndexInt])

camera.rotation = -90
camera.resolution = (3280, 2464)
camera.start_preview() # (alpha=200) to add transparency)
update_settings_overlay_display()

camera.iso = 0
camera.shutter_speed = 0
camera.awb_mode = "off"

sleep(3)
# ^we can make the warm up period as short as two seconds, any less and camera does not have time to set ISO and shtr

while True:
    button1.when_pressed = shutter_button_press  # don't call the function with (), leave parentheses out
    button4.when_pressed = setting_toggle_button_press  # changes the editable setting
    button2.when_pressed = next_up_button_press  # next on editable setting
    button3.when_pressed = previous_down_button_press  # previous on editable setting

    if currentSettingIndexInt != 3:
        displayInfo = True
