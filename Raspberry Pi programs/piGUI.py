import pygame
import sys
from pygame.locals import*

# // Display settings
pygame.display.init()
info = pygame.display.Info()
dX, dY = info.current_w, info.current_h # display resolution
# dX, dY = 640, 480 # use if you want to set the display res to custom values
marginX = int(dX/32)
marginY = int(dY/32)

# // GUI settings
GUIx, GUIy = int(dX-6*marginX), int(dY-6*marginY)  # GUI display size (dX or dY - at least 2* margin of X or Y)
# GUI top left = marginX, marginY

# // UI BUILDING BLOCKS:
# Settings block:
x4thSettings = (GUIx / 4)
y3rdSettings = (GUIy / 3)
# Settings cell:
# TODO: Button cell useful references to build icons
# Buttons Block:
y4thButtons = ((GUIy+4*marginY) / 4)

# // Start Pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((dX, dY), pygame.FULLSCREEN)
pygame.display.set_caption("Text display test")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
# BLUE = (0, 0, 128)


# // Initial UI drawing declarations:

# Draw Background
pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, marginY, GUIx, GUIy), 1)  # settings rect
pygame.draw.rect(DISPLAYSURF, WHITE, (2*marginX+GUIx, marginY, 3*marginX, GUIy+4*marginY), 1)  # buttons rect
pygame.draw.rect(DISPLAYSURF, WHITE, (marginX, 2*marginY+GUIy, GUIx, 3*marginY), 1)  # bottom rect (current setting description)
for i in range(3):
    pygame.draw.line(DISPLAYSURF, WHITE, (int(marginX + (i+1) * x4thSettings), marginY), (int(marginX + (i + 1) * x4thSettings), GUIy + marginY), 1)  # x4ths
    pygame.draw.line(DISPLAYSURF, WHITE, (marginX, int(marginY + i * y3rdSettings)), (GUIx + marginX, int(marginY + i * y3rdSettings)), 1)  # y3rds
    # point 2 is always GUIsize + margin because we are matching with a rect declared using xy of A followed by
    # width and height rather than xy of point D
    pygame.draw.line(DISPLAYSURF, WHITE, (2*marginX+GUIx, int(marginY + (i+1) * y4thButtons)), (5 * marginX + GUIx, int(marginY + (i + 1) * y4thButtons)), 1)  # y4ths
# Fill background with text




while True:  # main game loop
    # game code here:

    # -----------------

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
