import pygame
from gui.gColors import *

LIFE_SIZE = 25
SPACER = 25

def draw(lives, window, x, y):
    for c in range(lives):
        pygame.draw.circle(window, BLACK, (x,y), LIFE_SIZE);
        x += LIFE_SIZE + SPACER;