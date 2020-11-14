import pygame
from gui.gColors import *
from gui.gConstants import *

def draw(lives, window, x, y):
    for c in range(lives):
        pygame.draw.circle(window, BLACK, (x,y), LIFE_RADIUS);
        x += (LIFE_RADIUS*2) + LIFE_SPACER;