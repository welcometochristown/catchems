class Card:

    NamedCards = {
        11 : 'Jack',
        12 : 'Queen',
        13 : 'King'
    }

    def img_suit_index(self):
        s = self.suit[0:1]
        if s == "H":
            return 0
        if s == "D":
            return 1
        if s == "C":
            return 2
        if s == "S":
            return 3
    
    def img_value_index(self):
        if self.value == 1:
            return 12
        return self.value - 2
    

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
