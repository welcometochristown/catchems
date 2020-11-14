import pygame
from gui.gColors import *
from gui.gConstants import *

def printHello():
    print ("hello")
def draw(deck, window, x, y):
    for c in deck.cards:
        pygame.draw.rect(window, BLACK, pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT),2)
        x += CARD_WIDTH + CARD_SPACER

