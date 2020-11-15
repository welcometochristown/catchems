from gui import gHand, gLife, gSeat
from gui.gConstants import *
from gui.gColors import *

import pygame
pygame.init()

class Graphics:
    def __init__(self):
        self.cards_image = pygame.image.load("images/cards.png")
        self.bg_image = pygame.image.load("images/yellow-wood-table-background.jpg")
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.card_images = self.load_card_images()
        
    def load_card_images(self): 
        arr = [[0 for x in range(13)] for y in range(5)] 
        for y in range(5):
            for x in range(13):
                surf = pygame.Surface((CARD_IMAGE_WIDTH, CARD_IMAGE_HEIGHT), pygame.SRCALPHA)
                surf.blit(self.cards_image, (0,0), (x*CARD_IMAGE_WIDTH, y*CARD_IMAGE_HEIGHT, CARD_IMAGE_WIDTH, CARD_IMAGE_HEIGHT) )
                arr[y][x] = surf
        return arr

    def render(self, players, seats, mainDeck, discardDeck, gamestate):
        self.win.fill(WHITE)
        self.win.blit(self.bg_image, (0, 0))

        for seat in seats:
            self.render_seat(seat, gamestate)

        for player in players:
            self.render_player(player)

        self.render_discard_deck(discardDeck)
        self.render_cursor_marker(gamestate)
        self.render_life_value_lose(gamestate)

        pygame.display.update()

    def render_cursor_marker(self, gs):
        if not gs.cursor_marker == None:
            pygame.draw.circle(self.win, RED, gs.cursor_marker, 5)

    def render_player(self, player):
        self.render_cards(player)
        self.render_lives(player)

    def render_cards(self, player):
        gHand.draw(player.hand, self.win, self.font, self.card_images, player.seat.x, player.seat.y+SEAT_HEIGHT-CARD_HEIGHT, not player.bot)

    def render_lives(self, player):
        gLife.draw(player.lives, self.win, player.seat.x+LIFE_RADIUS, player.seat.y+LIFE_RADIUS)

    def render_seat(self, seat, gs):
        color = BLUE if seat == gs.current_player.seat else BLACK
        gSeat.draw(seat, self.win, seat.x, seat.y, color)

    def render_life_value_lose(self, gs):
        text = self.font.render(str(gs.last_life_value_lost), True, BLACK) 
        textRect = text.get_rect()
        textRect.x = 10
        textRect.y = HEIGHT - 20
        self.win.blit(text, textRect)

    def render_discard_deck(self, discardDeck):
        gHand.draw(discardDeck, self.win, self.font, self.card_images, 0, (HEIGHT/2)-(CARD_HEIGHT/2), True, True)

        