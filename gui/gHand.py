import pygame
from gui.gColors import *

CARD_WIDTH = 50
CARD_HEIGHT = 100
SPACER = 5

def draw(deck, window, x, y):
    x+=(CARD_WIDTH/2)
    for c in deck.cards:
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT),2)
        pygame.draw.rect(window, WHITE, pygame.Rect((x+1), (y+1), CARD_WIDTH-1, CARD_HEIGHT-1))
        x += CARD_WIDTH + SPACER

