import pygame
import sys
from pygame.locals import *

# ctrl + alt + shift + t to reformat variables

width = 500
height = 400

pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hello world!')

# set up the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CUSTOMCOLOR = (0, 255, 255)

# draw on the surface object (THIS IS WHERE THE DRAWING HAPPENS)
DISPLAYSURF.fill(WHITE)
pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
# ^^ polygon, in this case a pentagon (point A, point B... , line thickness
pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 4)  # point A, point B, thickness
pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, 120))  # point A, point B
pygame.draw.line(DISPLAYSURF, BLUE, (60, 120), (120, 120), 4)  # point A, point B, thickness
pygame.draw.circle(DISPLAYSURF, BLUE, (300, 50), 20, 0)  # coordinates of centre, radius, line thickness
pygame.draw.ellipse(DISPLAYSURF, RED, (300, 250, 40, 80), 1)  # bounding rectangle, line thickness
pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))  # rect tuple (coordinates of A, width, height), line thickness

pixObj = pygame.PixelArray(DISPLAYSURF)
pixObj[480][380] = BLACK
pixObj[482][382] = BLACK
pixObj[484][384] = BLACK
pixObj[488][388] = BLACK
del pixObj

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
