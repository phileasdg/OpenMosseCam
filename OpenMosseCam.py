# CHANGES FROM V1.0:
# Starts awb mode: greyworld.
# picamera has been modified to include the greyworld awb setting.
# When awb mode == 'off', default values for R&B gains are 9.0, 9.0

# TODO: implement touch screen and overlays using PyGame or PyOpenGL or NumPy or OpenCV or Pietro's recommendation.
# TODO: MAKE IT POSSIBLE TO CHANGE GAINS TO SECOND DECIMAL POINT

# TODO : implement RAW + Jpeg save option (also, figure out how raw files work with PiCam)

# TODO: Make the default wb 0.9,0.9
# TODO: Make the white balance controlable from outside the camera
# TODO: Make the camera take external commands and return information

# TODO: find way of synchronising shutter between DSLR and MosseCam

# TODO : MAKE camera write settings to file so that the settings save from one session to the next
# TODO: DEBUGGING PROBLEM : FIGURE OUT WHY OTHER FORMATS CAUSE ERROR (PROBABLY MEMORY ISSUE)

# TODO: Look at options for in camera colour editing
# TODO: RAW DNG integration on MosseCam

# TODO: make on off power switch and connect it to the pi and battery so that I can turn power on and off.

# MosseCam User instructions:
# 1)
# // to take a picture, press button 1 (17).
# 2)
# // Navigate the menu using button 4 (27) to toggle between settings and buttons 2 and 3 to change the setting
# // currently selected.
# 3)
# // The following settings are customisable: ISO, shutterSpeed, AWB mode, displayInfo (on, off), fileFormat,
# imageEffect, WB RED gains, WB BLUE gains (WB gains are only available when the AWB mode is "off").
# 4)
# // To exit the camera, press and hold buttons 2 and 3 (22, 23).
# 5)
# //To turn off the Raspberry Pi, disable displayInfo in the menu and hold buttons 2 and 3 (22, 23).

# imports
import picamera
from picamera import Color, mmal
import ctypes as ct
from time import sleep
from gpiozero import Button
import time
import os
import sys


class userCamera(picamera.PiCamera):
    AWB_MODES = {
        'off':           mmal.MMAL_PARAM_AWBMODE_OFF,
        'auto':          mmal.MMAL_PARAM_AWBMODE_AUTO,
        'sunlight':      mmal.MMAL_PARAM_AWBMODE_SUNLIGHT,
        'cloudy':        mmal.MMAL_PARAM_AWBMODE_CLOUDY,
        'shade':         mmal.MMAL_PARAM_AWBMODE_SHADE,
        'tungsten':      mmal.MMAL_PARAM_AWBMODE_TUNGSTEN,
        'fluorescent':   mmal.MMAL_PARAM_AWBMODE_FLUORESCENT,
        'incandescent':  mmal.MMAL_PARAM_AWBMODE_INCANDESCENT,
        'flash':         mmal.MMAL_PARAM_AWBMODE_FLASH,
        'horizon':       mmal.MMAL_PARAM_AWBMODE_HORIZON,
        'greyworld':     ct.c_uint32(10)
        }


# variables (initial values)

camera = userCamera()
imgFileName = 'image_' + str(time.ctime()) + '.jpg'  # or any initial format

# Settings lists
iso = [0, 100, 160, 200, 250, 320, 400, 500, 640, 800]  # 0 is auto ISO

shutterSpeed = [0, 125, 156, 200, 250, 312, 400, 500, 625, 800, 1000, 1250, 1562, 2000, 2500, 3125, 4000, 5000, 6250,
                8000, 10000, 12500, 16666, 20000, 25000, 33333, 40000, 50000, 66666, 76923, 100000, 125000, 166666,
                200000, 250000, 300000, 400000, 500000, 600000, 800000, 1000000, 1300000, 1600000, 2000000, 2500000,
                3200000, 4000000, 5000000, 6000000]
shutterSpeedTranslation = ["auto", "1/8000", "1/6400", "1/5000", "1/4000", "1/3200", "1/2500", "1/2000", "1/1600",
                           "1/1250", "1/1000", "1/800", "1/640", "1/500", "1/400", "1/320", "1/250", "1/200", "1/160",
                           "1/125", "1/100", "1/80", "1/60", "1/50", "1/40", "1/30", "1/25", "1/20", "1/15", "1/13",
                           "1/10", "1/8", "1/6", "1/5", "1/4", "0.3", "0.4", "0.5", "0.6", "0.8", "1", "1.3", "1.6", "2",
                           "2.5", "3.2", "4", "5", "6"]
whiteBalance = ["off", "greyworld", "auto", "sunlight", "cloudy", "shade", "tungsten", "fluorescent", "incandescent", "flash", "horizon"]  # TODO: Add greyworld
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
settings = ["iso", "shutterSpeed", "whiteBalance", "displayInfo", "fileFormat", "imageEffect", "WB RED gains", "WB BLUE gains"]
currentSettingIndexInt = 0  # saves the current editable setting

# Buttons
button1 = Button(17)  # used as shutter button, runs capture function
button2 = Button(22)  # used as "next/up" button, moves setting to the previous option in settings list
button3 = Button(23)  # used as "previous/down" button, moves setting to the next option in settings list
button4 = Button(27)  # used as setting toggle button, runs settingSwitch function (changes the setting that b2 and b3


# functions
def shutter_button_press():
    global imgFileName
    imgFileName = 'image_' + str(time.ctime()) + "." + str(fileFormat[fileformatIndex])
    disable_display()
    camera.capture(os.path.join('/home/pi/Desktop/MosseCam/Pictures', imgFileName), format=fileFormat[fileformatIndex])
    camera.stop_preview()
    camera.start_preview() # (alpha=200) to enable transparency
    # last 2 lines provide visual feedback for image capture
    update_settings_overlay_display()
    return


def make_overlaystring_with_WB():
    global currentSettingIndexInt
    global overlayString

    if currentSettingIndexInt == 0:
        overlayString = '|| [ISO: ' + str(iso[isoIndex]) + "] || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n ||  info: " + str(
            displayInfo) + "  || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||" + "\n||  RED gain: " + str(round(whiteBalanceGainRED, 2)) + "  ||\n  ||  BLUE gain: " + str(round(whiteBalanceGainBLUE, 2)) + "  ||"

    elif currentSettingIndexInt == 1:
        overlayString = '||  ISO: ' + str(iso[isoIndex]) + "  || \n || [speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "] || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n ||  info: " + str(
            displayInfo) + "  || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||" + "\n||  RED gain: " + str(round(whiteBalanceGainRED, 2)) + "  ||\n  ||  BLUE gain: " + str(round(whiteBalanceGainBLUE, 2)) + "  ||"
    elif currentSettingIndexInt == 2:
        overlayString = ' || ISO: ' + str(iso[isoIndex]) + "  || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n || [AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "] || \n ||  info: " + str(
            displayInfo) + "  || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||" + "\n||  RED gain: " + str(round(whiteBalanceGainRED, 2)) + "  ||\n  ||  BLUE gain: " + str(round(whiteBalanceGainBLUE, 2)) + "  ||"
    elif currentSettingIndexInt == 3:
        overlayString = ' || ISO: ' + str(iso[isoIndex]) + "  || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n || [info: " + str(
            displayInfo) + "] || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||" + "\n||  RED gain: " + str(round(whiteBalanceGainRED, 2)) + "  ||\n  ||  BLUE gain: " + str(round(whiteBalanceGainBLUE, 2)) + "  ||"
    elif currentSettingIndexInt == 4:
        overlayString = ' || ISO: ' + str(iso[isoIndex]) + "  || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n ||  info: " + str(
            displayInfo) + "  || \n || [format: " + str(fileFormat[fileformatIndex]) + "] || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||" + "\n||  RED gain: " + str(round(whiteBalanceGainRED, 2)) + "  ||\n  ||  BLUE gain: " + str(round(whiteBalanceGainBLUE, 2)) + "  ||"
    elif currentSettingIndexInt == 5:
        overlayString = ' || ISO: ' + str(iso[isoIndex]) + "  || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n ||  info: " + str(
            displayInfo) + "  || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n || [effect: " + str(
            imageEffect[imageEffectIndex]) + "] ||" + "\n||  RED gain: " + str(round(whiteBalanceGainRED, 2)) + "  ||\n  ||  BLUE gain: " + str(round(whiteBalanceGainBLUE, 2)) + "  ||"
    elif currentSettingIndexInt == 6:
        overlayString = ' || ISO: ' + str(iso[isoIndex]) + "  || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n ||  info: " + str(
            displayInfo) + "  || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||" + "\n|| [RED gain: " + str(round(whiteBalanceGainRED, 2)) + "] ||\n  ||  BLUE gain: " + str(round(whiteBalanceGainBLUE, 2)) + "  ||"
    elif currentSettingIndexInt == 7:
        overlayString = ' || ISO: ' + str(iso[isoIndex]) + "  || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n ||  info: " + str(
            displayInfo) + "  || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||" + "\n||  RED gain: " + str(round(whiteBalanceGainRED, 2)) + "  ||\n  || [BLUE gain: " + str(round(whiteBalanceGainBLUE, 2)) + "] ||"
    else:
        print("error: current setting index is out of defined range")


def make_overlaystring_no_WB():
    global currentSettingIndexInt
    global overlayString
    if currentSettingIndexInt == 0:
        overlayString = '|| [ISO: ' + str(iso[isoIndex]) + "] || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n ||  info: " + str(
            displayInfo) + "  || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||"
    elif currentSettingIndexInt == 1:
        overlayString = '||  ISO: ' + str(iso[isoIndex]) + "  || \n || [speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "] || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n ||  info: " + str(
            displayInfo) + "  || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||"
    elif currentSettingIndexInt == 2:
        overlayString = ' || ISO: ' + str(iso[isoIndex]) + "  || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n || [AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "] || \n ||  info: " + str(
            displayInfo) + "  || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||"
    elif currentSettingIndexInt == 3:
        overlayString = ' || ISO: ' + str(iso[isoIndex]) + "  || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n || [info: " + str(
            displayInfo) + "] || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||"
    elif currentSettingIndexInt == 4:
        overlayString = ' || ISO: ' + str(iso[isoIndex]) + "  || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n ||  info: " + str(
            displayInfo) + "  || \n || [format: " + str(fileFormat[fileformatIndex]) + "] || \n ||  effect: " + str(
            imageEffect[imageEffectIndex]) + "  ||"
    elif currentSettingIndexInt == 5:
        overlayString = ' || ISO: ' + str(iso[isoIndex]) + "  || \n ||  speed: " + str(
            shutterSpeedTranslation[shutterSpeedIndex]) + "  || \n ||  AWB: " + str(
            whiteBalance[whiteBalanceIndex]) + "  || \n ||  info: " + str(
            displayInfo) + "  || \n ||  format: " + str(fileFormat[fileformatIndex]) + "  || \n || [effect: " + str(
            imageEffect[imageEffectIndex]) + "] ||"
    else:
        print("error: current setting index is out of defined range")


def update_settings_overlay_display():
    global currentSettingIndexInt
    global overlayString
    if whiteBalanceIndex == 0:
        make_overlaystring_with_WB()
    else:
        make_overlaystring_no_WB()

    camera.annotate_text_size = 160
    camera.annotate_foreground = Color('black')
    camera.annotate_background = Color('white')
    camera.annotate_text = overlayString


def disable_display():
    # disable info display
    camera.annotate_text_size = 160
    camera.annotate_foreground = Color('black')
    camera.annotate_background = Color('white')
    camera.annotate_text = ""

    # lock settings (unlock by pressing button 4)


def setting_toggle_button_press():
    global currentSettingIndexInt
    global whiteBalanceGainRED
    global whiteBalanceGainBLUE
    if whiteBalanceIndex == 0:
        i = currentSettingIndexInt
        if 0 <= i < 7:
            i += 1
        elif i >= 7:
            i = 0
        else:
            print("error: current setting index outside of list range")
        currentSettingIndexInt = i
    else:
        i = currentSettingIndexInt
        if 0 <= i < 5:
            i += 1
        elif i >= 5:
            i = 0
        else:
            print("error: current setting index outside of list range")
        currentSettingIndexInt = i

    print(currentSettingIndexInt)
    print(settings[currentSettingIndexInt])
    sleep(0.3)
    update_settings_overlay_display()
    return currentSettingIndexInt


def print_settings_to_console():
    print("iso: ", iso[isoIndex])
    print("shutterspeed: ", shutterSpeed[shutterSpeedIndex], " (", shutterSpeedTranslation[shutterSpeedIndex] ,")")
    print("white balance:", whiteBalance[whiteBalanceIndex])
    print("display info ", displayInfo)
    print("file format ", fileFormat[fileformatIndex])
    print("RED gains: ", str(round(whiteBalanceGainRED, 2)), " BLUE gains: ", str(round(whiteBalanceGainBLUE, 2)))


def next_up_button_press():
    global currentSettingIndexInt
    global whiteBalanceGainRED
    global whiteBalanceGainBLUE
    i = currentSettingIndexInt
    if 0 <= i <= 7:
        if i == 0:  # ISO index + 1
            global isoIndex
            isoi = isoIndex
            if 0 <= isoi < 9:
                isoi += 1
            elif isoi >= 9:
                isoi = 0
            else:
                print("error: iso index is out of list range")
            isoIndex = isoi
            camera.iso = iso[isoIndex]  # sets the ISO to the value of the index
            sleep(0.3)
        if i == 1:  # shutter speed index + 1
            global shutterSpeedIndex
            sh = shutterSpeedIndex
            if 0 <= sh < 47:
                sh += 1
            elif sh >= 47:
                sh = 0
            else:
                print("error: shutter speed index is out of list range")
            shutterSpeedIndex = sh
            camera.shutter_speed = shutterSpeed[shutterSpeedIndex]  # sets the shutter speed to the value of the index
            sleep(0.3)
        if i == 2:  # white balance index + 1
            global whiteBalanceIndex
            wb = whiteBalanceIndex
            if 0 <= wb < 10:
                wb += 1
            elif wb >= 10:
                wb = 0
            else:
                print("error: white balance index is out of list range")
            whiteBalanceIndex = wb
            if whiteBalanceIndex == 0:
                camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
            camera.awb_mode = whiteBalance[whiteBalanceIndex]  # sets the awb mode to the value of the index
            sleep(0.3)
        if i == 3:  # display info boolean switch
            global displayInfo
            info = not displayInfo
            displayInfo = info
            sleep(0.3)
        if i == 4:
            global fileformatIndex
            ff = fileformatIndex
            if 0 <= ff < 1:
                ff += 1
            elif ff >= 1:
                ff = 0
            else:
                print("error: file format index is out of list range")
            fileformatIndex = ff
            sleep(0.3)
        if i == 5:
            global imageEffectIndex
            eff = imageEffectIndex
            if 0 <= eff < 9:
                eff += 1
            elif eff >= 9:
                eff = 0
            else:
                print("error: effect index is out of list range")
            imageEffectIndex = eff
            camera.image_effect = imageEffect[imageEffectIndex] # sets the image effect to the value of the index
            sleep(0.3)
        if i == 6:
            if 0 <= whiteBalanceGainRED < 8:
                whiteBalanceGainRED += 0.1
            elif whiteBalanceGainRED >= 8:
                whiteBalanceGainRED = 0
            camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
            sleep(0.3)
        if i == 7:
            if 0 <= whiteBalanceGainBLUE < 8:
                whiteBalanceGainBLUE += 0.1
            elif whiteBalanceGainBLUE >= 8:
                whiteBalanceGainBLUE = 0
            camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
            sleep(0.3)
    else:
        print("error: the current setting value is outside of the defined range")
    print_settings_to_console()
    update_settings_overlay_display()


def previous_down_button_press():
    global currentSettingIndexInt
    global whiteBalanceGainRED
    global whiteBalanceGainBLUE
    i = currentSettingIndexInt
    if 0 <= i <= 7:
        if i == 0:  # ISO index + 1
            global isoIndex
            isoi = isoIndex
            if 0 < isoi <= 9:
                isoi -= 1
            elif isoi <= 0:
                isoi = 9
            else:
                print("error: iso index is out of list range")
            isoIndex = isoi
            camera.iso = iso[isoIndex]  # sets the ISO to the value of the index
            sleep(0.3)
        if i == 1:  # shutter speed index + 1
            global shutterSpeedIndex
            sh = shutterSpeedIndex
            if 0 < sh <= 47:
                sh -= 1
            elif sh <= 0:
                sh = 47
            else:
                print("error: shutter speed index is out of list range")
            shutterSpeedIndex = sh
            camera.shutter_speed = shutterSpeed[shutterSpeedIndex]  # sets the shutter speed to the value of the index
            sleep(0.3)
        if i == 2:  # white balance index + 1
            global whiteBalanceIndex
            wb = whiteBalanceIndex
            if 0 < wb <= 10:
                wb -= 1
            elif wb <= 0:
                wb = 10
            else:
                print("error: white balance index is out of list range")
            whiteBalanceIndex = wb
            if whiteBalanceIndex == 0:
                camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
            camera.awb_mode = whiteBalance[whiteBalanceIndex]  # sets the awb mode to the value of the index
            sleep(0.3)
        if i == 3:  # display info boolean switch
            global displayInfo
            info = not displayInfo
            displayInfo = info
            sleep(0.3)
        if i == 4:
            global fileformatIndex
            ff = fileformatIndex
            if 0 < ff <= 1:
                ff -= 1
            elif ff <= 0:
                ff = 1
            else:
                print("error: file format index is out of list range")
            fileformatIndex = ff
            sleep(0.3)
        if i == 5:
            global imageEffectIndex
            eff = imageEffectIndex
            if 0 < eff <= 9:
                eff -= 1
            elif eff <= 0:
                eff = 9
            else:
                print("error: effect index is out of list range")
            imageEffectIndex = eff
            camera.image_effect = imageEffect[imageEffectIndex] # sets the image effect to the value of the index
            sleep(0.3)
        if i == 6:
            if 0 < whiteBalanceGainRED <= 8:
                whiteBalanceGainRED -= 0.1
            elif whiteBalanceGainRED <= 0.1:
                whiteBalanceGainRED = 8
            camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
            sleep(0.3)
        if i == 7:
            if 0 < whiteBalanceGainBLUE <= 8:
                whiteBalanceGainBLUE -= 0.1
            elif whiteBalanceGainBLUE <= 0.1:
                whiteBalanceGainBLUE = 8
            camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
            sleep(0.3)
    else:
        print("error: the current setting value is outside of the defined range")
    print_settings_to_console()
    update_settings_overlay_display()


# software code
print(currentSettingIndexInt)
print(settings[currentSettingIndexInt])

# camera.rotation = -90  # Removed because it crops the sensor.  # TODO
camera.resolution = (3280, 2464)
camera.start_preview()  # (alpha=200) to add transparency)
update_settings_overlay_display()

camera.iso = iso[isoIndex]
camera.shutter_speed = shutterSpeed[shutterSpeedIndex]
camera.awb_mode = whiteBalance[whiteBalanceIndex]
camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)

sleep(3)
# ^we can make the warm up period as short as two seconds, any less and camera does not have time to set ISO and shtr

while True:
    button1.when_pressed = shutter_button_press  # don't call the function with (), leave parentheses out
    button4.when_pressed = setting_toggle_button_press  # changes the editable setting
    button2.when_pressed = next_up_button_press  # next on editable setting
    button3.when_pressed = previous_down_button_press  # previous on editable setting7

    if currentSettingIndexInt == 3 and displayInfo == False:
        disable_display()

    if currentSettingIndexInt != 3:
        displayInfo = True

    if displayInfo == False:
        if button2.is_held and button3.is_held:
            os.system("sudo shutdown -h now")  # sudo shutdown r now to shutdown
            break
    elif button2.is_held and button3.is_held:
        print("camera turning off: script terminated by user")
        sys.exit()
