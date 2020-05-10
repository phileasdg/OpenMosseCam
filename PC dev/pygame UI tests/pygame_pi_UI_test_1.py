# TODO: Make GUI and tie RPI GPIO buttons
# TODO: figure out a way to make the test resize to stay in frame or move to be in frame
# TODO: format text so that if it doesn't fit into the screen on one line it splits into multiple lines automatically.

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

bodyFontObj = pygame.font.Font("freesansbold.ttf", fontSize)  # font, font size
textSurfaceObj = bodyFontObj.render(string, True, WHITE)
# text, anti-aliasing, text colour, bg colour
textRectObj = textSurfaceObj.get_rect()

textWidth = bodyFontObj.size(string)[0]
textHeight = bodyFontObj.size(string)[1]

textRectObj.center = (width - int(1/2*textWidth) - 10, height - int(1/2*textHeight) - 10)

while True:  # main game loop
    # DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
