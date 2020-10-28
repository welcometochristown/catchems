from deck import Deck
import rules

class Player:
    def __init__(self, name, bot=False, lives=rules.PLAYER_LIVES):
        self.hand = Deck(False)
        self.name = name
        self.lives = lives
        self.bot = bot