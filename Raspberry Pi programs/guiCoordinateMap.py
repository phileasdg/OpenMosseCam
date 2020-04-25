import pygame
import sys
from pygame.locals import*

# Display settings
dX, dY = (640, 480) # display resolution
marginX = int(dX/32)
marginY = int(dY/32)

# GUI settings
GUIx, GUIy = int(dX-marginX), int(dY-marginY)  # GUI display size
# GUI top left = marginX, marginY

# UI building blocks
x8th = (GUIx/8)
x16th = (GUIx/16)
x32nd = (GUIx/32)
y8th = (GUIy/8)
y16th = (GUIy/16)
y32nd = (GUIy/32)

# start pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((dX, dY))
pygame.display.set_caption("Text display test")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
# BLUE = (0, 0, 128)

# Initial UI drawing declarations:
# pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, marginY, int(GUIx-x32nd), int(GUIy-y32nd)), 1)  # rect tuple (coordinates of A, width, height), line thickness
for i in range(32):
    # Reference grid:
    pygame.draw.line(DISPLAYSURF, WHITE, (marginX, int(marginY+i*y32nd)), (GUIx, int(marginY+i*y32nd)), 1)
    # ^^ (surface, colour, (ax, ay), (bx, by), width) (change y to change spacing)
    pygame.draw.line(DISPLAYSURF, WHITE, (int(marginX+i*x32nd), marginY), (int(marginX+i*x32nd), GUIy), 1)
    # ^^ (surface, colour, (ax, ay), (bx, by), width) (change x to change spacing)

# change these values:
pointX = 1
pointY = 1

pygame.draw.circle(DISPLAYSURF, GREEN, (int(pointX*x32nd), int(pointY*y32nd)), 5, 0)  # coordinates of centre, radius, line thickness


while True:  # main game loop

    # game code here:

    # -----------------

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
