from deck import Deck

class Player:
    def __init__(self, name, bot=False, lives=5):
        self.hand = Deck(False)
        self.name = name
        self.lives = lives
        self.bot = bot