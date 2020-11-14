import pygame

#game modules
from card import Card
from deck import Deck
from player import Player
from seat import Seat

import rules
from gui import gHand, gLife, gSeat
from gui.gConstants import *
from gui.gColors import *


# import gui.gHand
# from gui import *
# from gui.gColors import *
# from gui.gHand import *
# from gui.gLife import *
# from gui.gSeat import *

# Screen
WIDTH = 1000
HEIGHT = 650
EDGE_PADDING = 100

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catchem's")

mainDeck = Deck()
discardDeck = Deck(False)
turnDeck = Deck(False)
seats = [Seat((WIDTH/2) - (SEAT_WIDTH/2), HEIGHT-SEAT_HEIGHT),
         Seat(0, (HEIGHT/2) - (SEAT_HEIGHT/2)),
         Seat((WIDTH/2) - (SEAT_WIDTH/2), 0),
         Seat(WIDTH-(SEAT_WIDTH), (HEIGHT/2) - (SEAT_HEIGHT/2))] #bottom middle -> clockwise

def create_bots():
    arr = []
    for i in range(rules.MAX_BOTS):
        arr.append(Player('bot'+str(i), True))
    return arr

def discard_player_hand(player):
    discardDeck.add_deck(player.hand)

def discard_turn_deck():
    discardDeck.add_deck(turnDeck)

def empty_discard_deck():
    mainDeck.add_deck(discardDeck)

def shuffle():
    #shuffle the deck
    print ('shuffling..')
    mainDeck.shuffle()

def deal(players, cards=rules.PLAYER_CARDS):
    #deal [cards] cards to each player
    print ('dealing..')
    for i in range(cards):
        for p in players:
            p.hand.add(mainDeck.take())

def play_rounds(players, rounds=rules.PLAYER_CARDS):
    #play [rounds] rounds for each player in [active_players]
    prevCard = None
    prevPlayer = None
    lifelose = rules.MIN_LIFE_LOSS

    for i in range(rounds):
        for p in players:
            if p.lives == 0:
                if len(p.hand.cards) > 0:
                    discard_player_hand(p)
                continue
            c = play_turn(p, prevCard)

            if compare_turns(prevCard, c):
                remove_life(prevPlayer, lifelose)
                lifelose +=1
            else:
                lifelose = rules.MIN_LIFE_LOSS
            prevCard = c
            prevPlayer = p
        #end of round
        discard_turn_deck()

def compare_turns(prevCard, card):
    if prevCard is None:
        return False
    return (card.value == prevCard.value)

def play_turn(player, lastCardPlayed):
    #[player] takes their turn
    if not player.bot:
        card = choose_human_card(player)
    else:
        card = choose_bot_card(player, lastCardPlayed)

    print(player.name + ' plays ' + str(card))
    turnDeck.add(card)
    return card

def choose_human_card(player):
    #human player choses a card (using input)
    while True:
        print(player.hand.cards)
        choice = input('Please enter your card: ')
        cards = [x for x in player.hand.cards if x.short == choice]
        if len(cards) != 1:
            continue
        return player.hand.takeCard(cards[0])

def choose_bot_card(player, lastCardPlayed):
    #bot player choses a card (using ai)
    matches = [x for x in player.hand.cards if x.value == lastCardPlayed.value]
    if len(matches) > 0:
        return player.hand.takeCard(matches[0])
    return player.hand.take()

def remove_life(player, lifelose):
        player.lives-=lifelose
        print(player.name + ' loses ' + str(lifelose) + 'x life!')
        if player.lives == 0:
            print(player.name + ' is out of the game!')

font = pygame.font.Font('freesansbold.ttf', 32)

def render(players):
    win.fill(WHITE)

    for seat in seats:
        render_seat(seat)

    for player in players:
        render_player(player)

    pygame.display.update()

def render_player(player):
    render_cards(player)
    render_lives(player)

def render_cards(player):
    gHand.draw(player.hand, win, player.seat.x, player.seat.y+SEAT_HEIGHT-CARD_HEIGHT)

def render_lives(player):
    gLife.draw(player.lives, win, player.seat.x+LIFE_RADIUS, player.seat.y+LIFE_RADIUS)

def render_seat(seat):
    gSeat.draw(seat, win, seat.x, seat.y)

def main():

    #add bots
    bots = create_bots()

    #add human player
    name = 'chris'#input('Please enter your name: ')
    human_player = Player(name)

    players = [human_player] + bots

    #assign seat to each player
    for p in range(len(players)):
        players[p].seat = seats[p]

    run = True

    shuffle()
    deal(players)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
          

        # active_players = [x for x in players if x.lives > 0]

        # if len(active_players) == 1:
        #     print(active_players[0].name + ' is the Winner! Congratulations!')
        #     break

        render(players)

       # play_rounds(active_players)
       # empty_discard_deck()

while True:
    if __name__ == '__main__':
        main()