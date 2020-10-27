class Player:
    def __init__(self, name, bot=False, lives=5):
        self.cards = []
        self.name = name
        self.lives = lives
        self.bot = bot