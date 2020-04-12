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
BACKGROUND= (0, 150, 0)
WHITE = (255, 255, 255)

# # Settings lists
# iso = 100
# shutterSpeedTranslation = "auto"
# whiteBalance = "greyworld"
# displayInfo = True
# fileFormat = "png"
# imageEffect = "none"
#
# whiteBalanceGainRED = 0.9
# whiteBalanceGainBLUE = 0.9
#
# # ignore the bits above
#
# currentSettingIndexInt: int = 7  # saves the current editable setting
# highlightBracketList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
#
# for i in range(16):
#     if currentSettingIndexInt * 2 == i:
#         highlightBracketList[i] = "["
#     elif currentSettingIndexInt * 2 + 1 == i:
#         highlightBracketList[i] = "]"
#     else:
#         highlightBracketList[i] = " "
#
# overlayString = " || " + highlightBracketList[0] + "ISO: " + str(iso) + highlightBracketList[1] + \
#          " || \n || " + highlightBracketList[2] + "speed: " + str(shutterSpeedTranslation) + highlightBracketList[3] +\
#          " || \n || " + highlightBracketList[4] + "AWB: " + str(whiteBalance) + highlightBracketList[5] +\
#          " || \n || " + highlightBracketList[6] + "info: " + str(displayInfo) + highlightBracketList[7] +\
#          " || \n || " + highlightBracketList[8] + "format: " + str(fileFormat) + highlightBracketList[9] + \
#          " || \n || " + highlightBracketList[10] + "effect: " + str(imageEffect) + highlightBracketList[11] +\
#          " || \n || " + highlightBracketList[12] + "RED gain: " + str(round(whiteBalanceGainRED, 2)) + highlightBracketList[13] +\
#          " || \n || " + highlightBracketList[14] + "BLUE gain: " + str(round(whiteBalanceGainBLUE, 2)) + highlightBracketList[15] +\
#          "  ||"

pygame.init()
# pygame.mouse.set_visible(False)
DISPLAYSURF = pygame.display.set_mode((width, height))  # , pygame.FULLSCREEN)
pygame.display.set_caption("Text display test")

DISPLAYSURF.fill(BACKGROUND )

# background grid
pygame.draw.rect(DISPLAYSURF, WHITE, (a, a, width - (2*a), height - (2*a)), lineThickness)  # rect tuple (coordinates of A, width, height), line thickness
pygame.draw.line(DISPLAYSURF, WHITE, (a, a+verticalThird), (width-a, a+verticalThird), lineThickness)  # point A, point B, thickness
pygame.draw.line(DISPLAYSURF, WHITE, (a, a+2*verticalThird), (width-a, a+2*verticalThird), lineThickness)  # point A, point B, thickness
pygame.draw.line(DISPLAYSURF, WHITE, (a+horizontalThird, a), (a+horizontalThird, a+2*verticalThird), lineThickness)  # point A, point B, thickness
pygame.draw.line(DISPLAYSURF, WHITE, (a+2*horizontalThird, a), (a+2*horizontalThird, a+2*verticalThird), lineThickness)  # point A, point B, thickness

# display text settings headers
fontObj = pygame.font.Font("freesansbold.ttf", 40)  # font, font size TODO: figure out formuma for font size
ISOtextSurfaceObj = fontObj.render("ISO", True, WHITE)  # text, anti-aliasing, text colour, bg colour
ISOtextRectObj = ISOtextSurfaceObj.get_rect()
ISOtextRectObj.topleft = (a+lineThickness, a+lineThickness)



# fontObj = pygame.font.Font("freesansbold.ttf", fontSize)  # font, font size
# textSurfaceObj = fontObj.render(overlayString, True, WHITE)
# # text, anti-aliasing, text colour, bg colour
# textRectObj = textSurfaceObj.get_rect()
#
# textWidth = fontObj.size(overlayString)[0]
# textHeight = fontObj.size(overlayString)[1]
#
# textRectObj.center = (width - int(1/2*textWidth) - 10, height - int(1/2*textHeight) - 10)

while True:  # main game loop
    DISPLAYSURF.blit(ISOtextSurfaceObj, ISOtextRectObj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
