import card

class Deck:

    suits = ['Club', 'Diamond', 'Heart', 'Spade']

    def init_suit(self, suit):
        for i in range(13):
            self.cards.append(card.Card(suit, (i+1)))

    def __init__(self, full=True):
        self.cards = []

        if(full):
            for s in Deck.suits:
                self.init_suit(s)