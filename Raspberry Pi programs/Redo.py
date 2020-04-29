import RPi.GPIO as GPIO
from time import sleep

# TODO: redo the menu structure and settings lookup system
# TODO: redo the GUI entirely in OpenCV
# Todo: redo the camera setup and tie it to OpenCV and the GUI

# GPIO setup:
buttons = {1: 17, 2: 22, 3: 23, 4: 27}
GPIO.setmode(GPIO.BCM)
for v in buttons.values():
    GPIO.setup(v, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def listen_for_button_press():
    for k, v in buttons.items():
        if GPIO.input(v) == False: # for any GPIO input equal to a value from the button dictionary
            print("button " + str(k) + " pressed") # print the action taken to the terminal
            # displayFunctions[currentDisplay]["Button" + str(k)]() # run function associated with button
            update_ui_display()
            sleep(0.3)
