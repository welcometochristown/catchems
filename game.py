import random
#import pygame

#game modules
from card import Card
from deck import Deck
from player import Player

# # Initializing Pygame
# pygame.init()

# # Screen
# WIDTH = 750

# win = pygame.display.set_mode((WIDTH, WIDTH))
# pygame.display.set_caption("Catchem's")

# # Colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GRAY = (200, 200, 200)
# RED = (255, 0, 0)
# BLUE = (0, 0, 255)

mainDeck = Deck()
discardDeck = Deck(False)
turnDeck = Deck(False)
players = [Player('bot1', True), Player('bot2', True), Player('bot3', True)]

def discard_player_hand(player):
    for c in range(len(player.cards)):
        card = player.cards.pop()
        discardDeck.cards.append(card)

def discard_turn_deck():
    for c in range(len(turnDeck.cards)):
        card = turnDeck.cards.pop()
        discardDeck.cards.append(card)

def empty_discard_deck():
    for c in range(len(discardDeck.cards)):
        card = discardDeck.cards.pop()
        mainDeck.cards.append(card)

def shuffle():
    #shuffle the deck
    print ('shuffling..')
    random.shuffle(mainDeck.cards)

def deal(active_players, cards=5):
    #deal [cards] cards to each player
    print ('dealing..')
    for i in range(cards):
        for p in active_players:
            p.cards.append(mainDeck.cards.pop())

def play_round(active_players, cards=5):
    prevCard = None
    prevPlayer = None
    
    for i in range(cards):
        for p in active_players:
            if p.lives == 0:
                if len(p.cards) > 0:
                    discard_player_hand(p)
                continue
            c = play_turn(p)
            compare_turns(prevPlayer, prevCard, p, c)
            prevCard = c
            prevPlayer = p
        discard_turn_deck()     
    empty_discard_deck() 

def play_turn(player):
    if not player.bot:
        print(player.cards)
        while True:
            choice = input('Please enter your card: ')
            cards = [(i,x) for i, x in enumerate(player.cards) if x.short == choice]

            if len(cards) != 1:
                continue

            card = cards[0][1]
            del player.cards[cards[0][0]]

            break
    else:
        card = player.cards.pop()
    
    print(player.name + 'plays ' + str(card))
    turnDeck.cards.append(card)
    return card

def compare_turns(prevPlayer, prevCard, player, card):
    if prevPlayer is None or player is None:
        return

    if card.value == prevCard.value:
        prevPlayer.lives-=1
        print(prevPlayer.name + ' loses a life!')
        if prevPlayer.lives == 0:
            print(prevPlayer.name + ' is out of the game!')


# font = pygame.font.Font('freesansbold.ttf', 32) 
  
# def render():
#     win.fill(WHITE)

#     render_cards()
#     render_gui()

#     pygame.display.update()

# def render_cards():
#     pass

# def render_gui():
#     for p in range(len(players)):
#         text = font.render(players[p].name, True, BLUE, WHITE) 
#         textRect = text.get_rect()  
#         textRect.center = (700 // 2, (p*100)+ textRect.height/2) 
#         win.blit(text, textRect) 

def main():

    # run = True

    # while run:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()

    #     render()

    #add human player
    name = input('Please enter your name: ')
    players.insert(0, Player(name))

    while True:
        active_players = [x for x in players if x.lives > 0]
        
        if len(active_players) == 1:
            print(active_players[0].name + ' is the Winner! Congratulations!')
            break

        shuffle()
        deal(active_players)
        play_round(active_players)

#while True:
    if __name__ == '__main__':
        main()