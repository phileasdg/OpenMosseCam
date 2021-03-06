import pygame
import sys
from pygame.locals import*

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Text display test")

# WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
# BLUE = (0, 0, 128)

bodyFontObj = pygame.font.Font("freesansbold.ttf", 32)  # font, font size
textSurfaceObj = bodyFontObj.render("Hello world!", True, GREEN)  # text, anti-aliasing, text colour, bg colour
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)

while True:  # main game loop
    # DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
