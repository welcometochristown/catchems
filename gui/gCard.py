import pygame
from util import rect
from gui.gColors import *
from gui.gConstants import *

def draw(card, window, font, card_images, x, y, faceup=False):
    if not faceup:
        window.blit(card_images[4][0], (x, y))
    else:
        window.blit(card_images[card.img_suit_index()][card.img_value_index()], (x, y))
  