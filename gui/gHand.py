import pygame
import deck
from gui.gColors import *

CARD_WIDTH = 50
CARD_HEIGHT = 100
SPACER = 5

def draw(deck, window, x, y):
    for c in deck.cards:
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT),2)
        x += CARD_WIDTH + SPACER

