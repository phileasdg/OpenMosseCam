# TODO: Make GUI and tie RPI GPIO buttons
# TODO: figure out a way to make the test resize to stay in frame or move to be in frame

import pygame
import sys
from pygame.locals import *

width = 640
height = 480

fontSize = 20
string = "width: " + str(width) + " height : " + str(height) + " size: " + str(fontSize)

# Colours
WHITE = (255, 255, 255)

pygame.init()
# pygame.mouse.set_visible(False)
DISPLAYSURF = pygame.display.set_mode((width, height))  # , pygame.FULLSCREEN)
pygame.display.set_caption("Text display test")

fontObj = pygame.font.Font("freesansbold.ttf", fontSize)  # font, font size
textSurfaceObj = fontObj.render(string, True, WHITE)
# text, anti-aliasing, text colour, bg colour
textRectObj = textSurfaceObj.get_rect()

textWidth = fontObj.size(string)[0]
textHeight = fontObj.size(string)[1]

textRectObj.center = (width - int(1/2*textWidth) - 10, height - int(1/2*textHeight) - 10)

while True:  # main game loop
    # DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
