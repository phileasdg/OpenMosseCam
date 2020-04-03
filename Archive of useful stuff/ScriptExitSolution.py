from gpiozero import Button
from time import sleep
import sys
import os
from picamera import PiCamera

camera = PiCamera()

button2 = Button(22)
button3 = Button(23)


def stop_code():
    print("code will stop")
    sys.exit()

def turn_off_pi():
    os.system("sudo shutdown -r now")  # sudo shutdown -h now to shutdown

camera.start_preview()

while True:
    sleep(1)
    if button2.is_held and button3.is_held:
        # stop_code()
        turn_off_pi()


