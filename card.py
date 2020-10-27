class Card:

    NamedCards = {
        11 : 'Jack',
        12 : 'Queen',
        13 : 'King'
    }

    def __init__(self, suit, value):
        self.suit = suit;
        self.value = value;
        self.name = str(value);
        self.short = self.name + suit[0:1]

        if(value > 10):
            self.name = Card.NamedCards[value]
            self.short = self.name[0:1] + suit[0:1]

    def __repr__(self):
         return str(self.name) + ' of ' + str(self.suit) + ' (' + self.short + ')'
