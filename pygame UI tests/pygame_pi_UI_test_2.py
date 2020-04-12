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

settingsList = ["ISO", "Shutter", "Mode", "Effect", "Format", "Resolution", "AWB", "Red:", "Blue:"]

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
fontObj = pygame.font.Font("freesansbold.ttf", 40)  # font, font size TODO: figure out formula for font size

numberOfHorizontalThirds = 0
numberOfVerticalThirds = 0

for i in range(8):
    i = fontObj.render(settingsList[i], True, WHITE)  # text, anti-aliasing, text colour, bg colour
    textRectObj = i.get_rect()
    textRectObj.topleft = (a + lineThickness), (a + lineThickness)

    DISPLAYSURF.blit(i, textRectObj)

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
