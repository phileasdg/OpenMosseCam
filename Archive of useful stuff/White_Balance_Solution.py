from picamera import PiCamera
from gpiozero import Button
from time import sleep

toggleUpButton = Button(22)
toggleDownButton = Button(23)
camera = PiCamera()

whiteBalanceGainRED = 0
whiteBalanceGainBLUE = 0

WBgainsString = "Gains will appear here"

def get_gains_string():
    WBgainsString = "Red Gains: " + str(whiteBalanceGainRED) + "\nBlue Gains: " + str(
        whiteBalanceGainBLUE)
    print(WBgainsString)


def change_red_gain():
    global whiteBalanceGainRED
    i = whiteBalanceGainRED
    if 0 <= i < 8:
        i += 0.1
    elif i >= 8:
        i = 0
    else:
        print("error: white balance red index is out of range")
    whiteBalanceGainRED = i
    camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
    get_gains_string()
    sleep(0.3)


def change_blue_gain():
    global whiteBalanceGainBLUE
    i = whiteBalanceGainBLUE
    if 0 <= i < 8:
        i += 0.1
    elif i >= 8:
        i = 0
    else:
        print("error: white balance blue index is out of range")
    whiteBalanceGainBLUE = i
    camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)
    get_gains_string()
    sleep(0.3)


camera.start_preview()
camera.awb_mode = "off"
camera.awb_gains = (whiteBalanceGainRED, whiteBalanceGainBLUE)

toggleUpButton.when_pressed = change_blue_gain
toggleDownButton.when_pressed = change_red_gain
