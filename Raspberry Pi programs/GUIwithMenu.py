# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# GENERAL TO DO LIST:
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# TODO: update all the comments and dependencies when the code is finished and make sure it is all correct.
# TODO: make the current setting highlighted in the settings menu on the GUI
# TODO: Change update_ui_display() to blit pictures or text depending on the setting
# TODO: make the camera setup

import RPi.GPIO as GPIO
from time import sleep
import pygame
import sys
from pygame.locals import *

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# CAMERA SETUP (PICAMERA)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# TODO: MAKE CAMERA SETUP

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# GPIO AND FUNCTIONS SETUP:
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

buttons = {1: 17, 2: 22, 3: 23, 4: 27}
GPIO.setmode(GPIO.BCM)
for v in buttons.values():
    GPIO.setup(v, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Global variables
infoOverlay = True
currentDisplay = "viewFinder"

# current setting index
csi = 0  # defaults to ISO


# Function definitions
def take_picture():
    print("taking picture")


def toggle_info():
    global infoOverlay
    infoOverlay = not infoOverlay
    print("infoOverlay is " + str(infoOverlay))
    # TODO: if infoOverlay is False: hide GUI until a button is pressed.


def settings_menu():

    # TODO: make the new drawing discard the old drawing
    # || Terminal output: ||
    global currentDisplay
    currentDisplay = "settingsMenu"

    print("you have pressed 'settings menu'")

    # || GUI declarations: ||

    DISPLAYSURF.fill(BLACK)
    # draw settings box
    pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, marginY, GUIx, GUIy), 1)  # settings rect
    pygame.draw.rect(DISPLAYSURF, WHITE, (2 * marginX + GUIx, marginY, 3 * marginX, GUIy + 4 * marginY), 1)  # buttons rect
    pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, 2 * marginY + GUIy, GUIx, 3 * marginY), 1)  # bottom rect (current setting description)

    for i in range(3):
        pygame.draw.line(DISPLAYSURF, WHITE, (int(marginX + (i + 1) * x4thSettings), marginY), (int(marginX + (i + 1) * x4thSettings), GUIy + marginY), 1)  # x4ths
        pygame.draw.line(DISPLAYSURF, WHITE, (marginX, int(marginY + i * y3rdSettings)), (GUIx + marginX, int(marginY + i * y3rdSettings)), 1)  # y3rds
        # point 2 is always GUIsize + margin because we are matching with a rect declared using xy of A followed by
        # width and height rather than xy of point D
        pygame.draw.line(DISPLAYSURF, WHITE, (2 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)), (5 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)), 1)  # y4ths

    # draw settings names
    for k in sd.keys():
        fontObj = pygame.font.Font(None, 30)  # font, font size
        textSurfaceObj = fontObj.render(k, True, WHITE)  # text, anti-aliasing, text colour, bg colour
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = sd[k][0][0]
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    # draw settings values
    for setting in sl:
        fontObj = pygame.font.Font(None, 30)  # font, font size
        textSurfaceObj = fontObj.render(str(sd[setting][1][scvil[sl.index(setting)]]), True, WHITE)  # text, anti-aliasing, text colour, bg colour
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = sd[setting][0][1]
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def gallery():
    global currentDisplay
    currentDisplay = "gallery"

    print("you have pressed 'gallery'")

    # || GUI declarations: ||

    DISPLAYSURF.fill(BLACK)
    # draw settings box
    pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, marginY, GUIx, GUIy), 1)  # settings rect
    pygame.draw.rect(DISPLAYSURF, WHITE, (2 * marginX + GUIx, marginY, 3 * marginX, GUIy + 4 * marginY), 1)  # buttons rect
    pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, 2 * marginY + GUIy, GUIx, 3 * marginY), 1)  # bottom rect (current setting description)

    for i in range(3):
        pygame.draw.line(DISPLAYSURF, WHITE, (2 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)), (5 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)), 1)  # y4ths


def return_to_viewfinder():
    global currentDisplay
    currentDisplay = "viewFinder"

    # change the value of the buttons

    # || GUI declarations: ||
    # TODO: have it draw the image from the viewfinder over the display
    DISPLAYSURF.fill(BLACK) # TODO: Replace with camera overlay
    draw_ui_background()


def next_up():
    if currentDisplay == "settingsMenu":
        if 0 <= scvil[csi] < len(sd[sl[csi]][1]) - 1:  # note the "-1", it is important.
            # current setting value from index in list of values in dictionary += 1
            scvil[csi] += 1
        # sets setting index value to 0
        else:
            scvil[csi] = 0

        print("you have pressed 'up'")
        print(sl[csi] + " = " + str(sd[sl[csi]][1][scvil[csi]]))
        # add 1 to setting value
    else:  # can only be called from the gallery
        print("next picture up")

    # || GUI declarations: ||
    settings_menu()


def next_down():
    if currentDisplay == "settingsMenu":
        if 0 < scvil[csi] <= len(sd[sl[csi]][1]):
            scvil[csi] -= 1
        else:
            scvil[csi] = len(sd[sl[csi]][1]) - 1

        print("you have pressed 'down'")
        print(sl[csi] + " = " + str(sd[sl[csi]][1][scvil[csi]]))
    else:  # can only be called from the gallery
        print("next picture down")

    # || GUI declarations: ||
    settings_menu()


def change_setting():
    global csi
    if 0 <= csi < 11:  # between 0 and highest index in settingsList (9 for now)
        csi += 1
    else:
        csi = 0
    print("you have pressed 'change selected setting' \nthe new setting is " + sl[csi])
    # go down to change the setting


def delete():
    print("content deleted")


def draw_ui_background():
    pygame.draw.rect(DISPLAYSURF, WHITE, (2 * marginX + GUIx, marginY, 3 * marginX, GUIy + 4 * marginY), 1)  # buttons rect
    pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, 2 * marginY + GUIy, GUIx, 3 * marginY), 1)  # bottom rect (current setting description)
    for i in range(3):
        pygame.draw.line(DISPLAYSURF, WHITE, (2 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)), (5 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)), 1)  # y4ths


def update_ui_display():
    # button function descriptions print
    for i in range(4):
        print(displayDescriptions[currentDisplay]["Button" + str(i + 1)])
    print("please press a button:")

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# PYGAME SETUP:
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# // Display settings
pygame.display.init()
info = pygame.display.Info()
dX, dY = info.current_w, info.current_h  # display resolution
# dX, dY = 640, 480 # use if you want to set the display res to custom values
marginX = int(dX / 32)
marginY = int(dY / 32)

# // GUI settings
GUIx, GUIy = int(dX - 6 * marginX), int(dY - 6 * marginY)  # GUI display size (dX or dY - at least 2* margin of X or Y)
# GUI top left = marginX, marginY

# // UI BUILDING BLOCKS:
# Settings block (the settings rectangle):
x4thSettings = (GUIx / 4)
y3rdSettings = (GUIy / 3)
# Settings cell:
# TODO: Button cell useful references to build icons
# Buttons Block:
y4thButtons = ((GUIy + 4 * marginY) / 4)

# // Start Pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((dX, dY))  # , pygame.FULLSCREEN)
pygame.display.set_caption("Text display test") # TODO: change

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
# BLUE = (0, 0, 128)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# MENU STRUCTURE AND SETTINGS SETUP
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# Dictionaries and lists (camera settings and UI)
displayFunctions = {
    "viewFinder": {
        "Button1": take_picture,  # the name of the function without the brackets
        "Button2": toggle_info,
        "Button3": settings_menu,
        "Button4": gallery
    },
    "settingsMenu": {
        "Button1": return_to_viewfinder,
        "Button2": next_up,
        "Button3": next_down,
        "Button4": change_setting
    },
    "gallery": {
        "Button1": return_to_viewfinder,
        "Button2": next_up,
        "Button3": next_down,
        "Button4": delete
    }
}  # contains map of functions and their button assignment for different displays
displayDescriptions = {
    "viewFinder": {
        "Button1": "1: take_picture",  # the name of the function without the brackets
        "Button2": "2: toggle_info",
        "Button3": "3: settingsMenu",
        "Button4": "4: gallery"
    },
    "settingsMenu": {
        "Button1": "1: back",
        "Button2": "2: next_up",
        "Button3": "3: next_down",
        "Button4": "4: change_setting"
    },
    "gallery": {
        "Button1": "1: back",
        "Button2": "2: next_up",
        "Button3": "3: next_down",
        "Button4": "4: delete"
    }
}  # primarily for dev purposes: reference dict of the descriptions of btn functions to print

# settings list
sl = ["Mode", "Active Camera(s)", "Shutter", "ISO", "AWB", "Red gain", "Blue gain", "Effect", "Resolution", "Crop", "Format", "fps"]  # TODO: framerate and crop

sd = {
    # TODO: reformat and clean up when finished
    # "Reference": [["key blit xy (x, y)", "value blit xy (x, y)"], ["list of setting values"]], TODO!!!!!!!!!!!!!!!!!!
    "Mode": [[(marginX, marginY), (marginX, marginY+(y3rdSettings/2))], ["photo", "video"]],
    "Active Camera(s)": [[(marginX+x4thSettings, marginY),(marginX+x4thSettings, marginY+(y3rdSettings/2))], ["left camera", "right camera", "stereo", "3D overlap"]],
    "Shutter": [[(marginX+(2*x4thSettings), marginY), (marginX+(2*x4thSettings), marginY+(y3rdSettings/2))], [("auto", 0), ("1/8000", 125), ("1/6400", 156),
                ("1/5000", 200), ("1/4000", 250), ("1/3200", 312), ("1/2500", 400), ("1/2000", 500), ("1/1600", 625),
                ("1/1250", 800), ("1/1000", 1000), ("1/800", 1250), ("1/640", 1562), ("1/500", 2000), ("1/400", 2500),
                ("1/320", 3125), ("1/250", 4000), ("1/200", 5000), ("1/160", 6250), ("1/125", 8000), ("1/100", 10000),
                ("1/80", 12500), ("1/60", 16666), ("1/50", 20000), ("1/40", 25000), ("1/30", 33333), ("1/25", 40000),
                ("1/20", 50000), ("1/15", 66666), ("1/13", 76923), ("1/10", 100000), ("1/8", 125000), ("1/6", 166666),
                ("1/5", 200000), ("1/4", 250000), ("0.3", 300000), ("0.4", 400000), ("0.5", 500000), ("0.6", 600000),
                ("0.8", 800000), ("1", 1000000), ("1.3", 1300000), ("1.6", 1600000), ("2", 2000000), ("2.5", 2500000),
                ("3.2", 3200000), ("4", 4000000), ("5", 5000000), ("6", 6000000)]],
    "ISO": [[(marginX+(3*x4thSettings), marginY), (marginX+(3*x4thSettings), marginY+(y3rdSettings/2))], [0, 100, 160, 200, 250, 320, 400, 500, 640, 800]],
    "AWB": [[(marginX, marginY+y3rdSettings), (marginX, marginY+y3rdSettings+(y3rdSettings/2))], ["off", "greyworld", "auto", "sunlight", "cloudy", "shade", "tungsten",
                                       "fluorescent", "incandescent", "flash", "horizon"]],
    # TODO: the solution for blue gain and red gain above is pretty poor. To improve.
    "Red gain": [[(marginX+x4thSettings, marginY+y3rdSettings), (marginX+x4thSettings, marginY+y3rdSettings+(y3rdSettings/2))], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1,
                 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2,
                 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0]],
    "Blue gain": [[(marginX+(2*x4thSettings), marginY+y3rdSettings), (marginX+(2*x4thSettings), marginY+y3rdSettings+(y3rdSettings/2))], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                  2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1,
                  4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2,
                  6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0]],
    "Effect": [[(marginX+(3*x4thSettings), marginY+y3rdSettings), (marginX+(3*x4thSettings), marginY+y3rdSettings+(y3rdSettings/2))], ["none", "negative", "solarize", "hatch", "gpen", "film", "colorswap",
                                          "washedout", "colorbalance", "cartoon"]],
    # effects availablee: 'none', 'negative', 'solarize', 'sketch', 'denoise', 'emboss', 'oilpaint', 'hatch', 'gpen',
    # 'pastel', 'watercolor', 'film', 'blur', 'saturation', 'colorswap', 'washedout', 'posterise', 'colorpoint',
    # 'colorbalance', 'cartoon', 'deinterlace1', 'deinterlace2'

    "Resolution": [[(marginX, marginY+(2*y3rdSettings)), (marginX, marginY+(2*y3rdSettings)+(y3rdSettings/2))], [(1980, 1080), (1080, 720)]],  # limited number of tuples, different
    "Crop": [[(marginX+x4thSettings, marginY+(2*y3rdSettings)), (marginX+x4thSettings, marginY+(2*y3rdSettings)+(y3rdSettings/2))], [(0, 0)]],  # TODO
    "Format": [[(marginX+(2*x4thSettings), marginY+(2*y3rdSettings)), (marginX+(2*x4thSettings), marginY+(2*y3rdSettings)+(y3rdSettings/2))], ["jpg", "png"]],
    "fps": [[(marginX+(3*x4thSettings), marginY+(2*y3rdSettings)), (marginX+(3*x4thSettings), marginY+(2*y3rdSettings)+(y3rdSettings/2))], [30]]  # TODO

}
# settings current value index list
scvil = [
    0,  # Mode index from list of strings (only two)
    0,  # Active Camera index from list of strings
    0,  # Shutter index from list of tuples: [("human value", computer value), ...]
    0,  # ISO index from list of integers
    0,  # AWB index from list of strings
    0,  # Red gain value = value between 1 and 9
    0,  # Blue gain value = value between 1 and 9
    0,  # Effect index from list of strings
    0,  # Resolution index from list of tuples [(x, y),(x, y), ...]
    0,  # Crop (TBD) TODO
    0,  # Format index from list of strings
    0,  # fps (TBD) TODO
]

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #
# PYGAME LOOP
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////// #

# // Initial UI drawing:

draw_ui_background()
update_ui_display()
# TODO: make the update_ui_display() overwrite the current display rather than add to it.

while True:  # main game loop
    # game code here:

    # Menu code
    for k, v in buttons.items():
        if GPIO.input(v) == False: # for any GPIO input equal to a value from the button dictionary
            print("button " + str(k) + " pressed") # print the action taken to the terminal
            displayFunctions[currentDisplay]["Button" + str(k)]() # run function associated with button
            update_ui_display()
            sleep(0.3)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
