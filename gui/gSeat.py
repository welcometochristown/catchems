import pygame
import seat
from gui.gColors import *
from gui.gConstants import *

def draw(seat, window, x, y):
    pygame.draw.rect(window, BLACK, (x,y, SEAT_WIDTH, SEAT_HEIGHT), 2)
    pygame.draw.circle(window, GREEN, (x,y), MARKER_SIZE);
    pygame.draw.circle(window, WHITE, (x,y), MARKER_SIZE-2);
