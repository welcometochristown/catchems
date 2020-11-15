import pygame
from util import rect
from gui.gColors import *
from gui.gConstants import *

def draw(deck, window, x, y, overlap=False):
    for c in deck.cards:
        pygame.draw.rect(window, WHITE, pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT),2)

        if overlap:
            x += CARD_WIDTH - CARD_OVERLAP
        else:
            x += CARD_WIDTH + CARD_SPACER

def isCardIntersect(deck, pos, x, y):
    for c in deck.cards:
        bounds = rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        x += CARD_WIDTH + CARD_SPACER
        if bounds.doesIntersect(pos):
             return c
    return None