from deck import Deck
import rules

class Player:
    def __init__(self, name, number, bot=False, lives=rules.PLAYER_LIVES):
        self.hand = Deck(False)
        self.name = name
        self.number = number
        self.lives = lives
        self.bot = bot
        self.seat = None