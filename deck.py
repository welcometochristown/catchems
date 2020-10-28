import card
import random

class Deck:

    suits = ['Club', 'Diamond', 'Heart', 'Spade']

    def clear(self):
        self.cards = []

    def add_deck(self, deck):
        self.addrange(deck.cards)
        deck.clear()

    def add(self, card):
        self.cards.append(card)

    def addrange(self, cards):
         for c in cards:
            self.cards.append(c)

    def takeOne(self):
        if len(self.cards) == 0:
            return None

        card = self.cards[0]
        del self.cards[0]
        return card

    def takeCard(self, card):
        c = [(i,x) for i, x in enumerate(self.cards) if x.short == card.short]
        if len(c) == 0:
            return None
        ret = c[0][1]
        del self.cards[c[0][0]]
        return ret
            
    def take(self, amount=1):
        if amount == 1:
            return self.takeOne()

        cards = self.cards[:amount]
        del self.cards[:amount]
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def init_suit(self, suit):
        for i in range(13):
            self.cards.append(card.Card(suit, (i+1)))

    def __init__(self, fill=True):
        self.cards = []

        #should we fill the deck
        if(fill):
            for s in Deck.suits:
                self.init_suit(s)