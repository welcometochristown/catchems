import pygame
from gui import gCard
from util import rect
from gui.gColors import *
from gui.gConstants import *

def draw(deck, window, font, card_images, x, y, faceup=False, overlap=False):
    for c in deck.cards:
        gCard.draw(c, window, font, card_images, x, y, faceup)
        x += CARD_WIDTH + (-CARD_OVERLAP if overlap else CARD_SPACER)

def isCardIntersect(deck, pos, x, y):
    for c in deck.cards:
        bounds = rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        x += CARD_WIDTH + CARD_SPACER
        if bounds.doesIntersect(pos):
             return c
    return None