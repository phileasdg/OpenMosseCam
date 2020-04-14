# TODO: make the overlayString print on multiple lines

import pygame
import sys
from pygame.locals import *

width = 640
height = 480

# UI reference coordinates
a = 25  # top left point of the GUI frame rectangle.
# ^^ Also == the size of the separation between the edge of the screen and the frame
widthOfFrame = width-2*a
heightOfFrame = height-2*a
horizontalThird = int(widthOfFrame/3)
verticalThird = int(heightOfFrame/3)

fontSize = 20
lineThickness = int(a/2)

# Colours
BACKGROUND= (150, 0, 150)
WHITE = (255, 255, 255)

#settings values
ISO = "100"
ShutterSpeed = "1/100"
Mode = "Photo"
Effect = "None"
Format = "png"
Resolution = "1920x1080"
AWB = "greyworld"
REDgain = "off"
BLUEgain = "off"

# settings headers coordinates
settingsValues = {
    "ISO": ISO,
    "Shutter": ShutterSpeed,
    "Mode": Mode,
    "Effect": Effect,
    "Format": Format,
    "Resolution": Resolution,
    "AWB": AWB,
    "Red gain:": REDgain,
    "Blue gain:": BLUEgain,
}
settingsXY = {
"ISO": (a+lineThickness, a+lineThickness),
"Shutter": (a+lineThickness+horizontalThird, a+lineThickness),
"Mode": (a+lineThickness+2*horizontalThird, a+lineThickness),
"Effect": (a+lineThickness, a+lineThickness+verticalThird),
"Format": (a+lineThickness+horizontalThird, a+lineThickness+verticalThird),
"Resolution": (a+lineThickness+2*horizontalThird, a+lineThickness+verticalThird),
"AWB": ((a+lineThickness, a+lineThickness+2*verticalThird)),
"Red:": (a+lineThickness+horizontalThird, a+lineThickness+2*verticalThird),
"Blue:": (a+lineThickness+2*horizontalThird, a+lineThickness+2*verticalThird),
}
settingsValueXY = {
ISO: (a+lineThickness, a+lineThickness+int(verticalThird/3)),
ShutterSpeed: (a+lineThickness+horizontalThird, a+lineThickness+int(verticalThird/3)),
Mode: (a+lineThickness+2*horizontalThird, a+lineThickness+int(verticalThird/3)),
Effect: (a+lineThickness, a+lineThickness+verticalThird+int(verticalThird/3)),
Format: (a+lineThickness+horizontalThird, a+lineThickness+verticalThird+int(verticalThird/3)),
Resolution: (a+lineThickness+2*horizontalThird, a+lineThickness+verticalThird+int(verticalThird/3)),
AWB: ((a+lineThickness, a+lineThickness+2*verticalThird+int(verticalThird/3))),
REDgain: (a+lineThickness+horizontalThird, a+lineThickness+2*verticalThird+int(verticalThird/3)),
BLUEgain: (a+lineThickness+2*horizontalThird, a+lineThickness+2*verticalThird+int(verticalThird/3)),
}

pygame.init()
# pygame.mouse.set_visible(False)
DISPLAYSURF = pygame.display.set_mode((width, height))  # , pygame.FULLSCREEN)
pygame.display.set_caption("Text display test")

DISPLAYSURF.fill(BACKGROUND )

def draw_settings_menu():
    # background grid
    pygame.draw.rect(DISPLAYSURF, WHITE, (a, a, width - (2*a), height - (2*a)), lineThickness)  # rect tuple (coordinates of A, width, height), line thickness
    pygame.draw.line(DISPLAYSURF, WHITE, (a, a+verticalThird), (width-a, a+verticalThird), lineThickness)  # point A, point B, thickness
    pygame.draw.line(DISPLAYSURF, WHITE, (a, a+2*verticalThird), (width-a, a+2*verticalThird), lineThickness)  # point A, point B, thickness
    pygame.draw.line(DISPLAYSURF, WHITE, (a+horizontalThird, a), (a+horizontalThird, a+2*verticalThird), lineThickness)  # point A, point B, thickness
    pygame.draw.line(DISPLAYSURF, WHITE, (a+2*horizontalThird, a), (a+2*horizontalThird, a+2*verticalThird), lineThickness)  # point A, point B, thickness

    # display text settings headers
    fontObjHeaders = pygame.font.Font("freesansbold.ttf", int(widthOfFrame/18))  # font, font size
    fontObjSettings = pygame.font.Font("freesansbold.ttf", int(widthOfFrame/9))  # font, font size

    for k, v in settingsXY.items():
        k = fontObjHeaders.render(k, True, WHITE)  # text, anti-aliasing, text colour, bg colour
        textRectObj = k.get_rect()
        textRectObj.topleft = (v)

        DISPLAYSURF.blit(k, textRectObj)

    for k, v in settingsValueXY.items(): #TODO: edit the dictionary
        k = fontObjSettings.render(k, True, WHITE)  # text, anti-aliasing, text colour, bg colour
        textRectObj = k.get_rect()
        # textRectObjXYtoSum = [(int(horizontalThird/2), int(verticalThird/2)), v]  # TODO: Make this a formula
        # textRectObjXY = [sum(i) for i in zip(*textRectObjXYtoSum)]
        textRectObj.topleft= (v)
        DISPLAYSURF.blit(k, textRectObj)

# setup functions calling
draw_settings_menu()

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
