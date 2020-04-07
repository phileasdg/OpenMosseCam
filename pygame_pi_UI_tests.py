# TODO: Make GUI and tie RPI GPIO buttons
# TODO: figure out a way to make the test resize to stay in frame or move to be in frame

import pygame
import sys
from pygame.locals import *

width = 640
height = 480

fontSize = 20

# Colours
WHITE = (255, 255, 255)

pygame.init()
# pygame.mouse.set_visible(False)
DISPLAYSURF = pygame.display.set_mode((width, height))  # , pygame.FULLSCREEN)
pygame.display.set_caption("Text display test")

fontObj = pygame.font.Font("freesansbold.ttf", fontSize)  # font, font size
textSurfaceObj = fontObj.render("width: " + str(width) + " height : " + str(height) +
                                " size: " + str(fontSize), True, WHITE)
# text, anti-aliasing, text colour, bg colour
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (width - 150, 20)

while True:  # main game loop
    # DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
