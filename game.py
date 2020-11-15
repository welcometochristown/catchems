import pygame

#game modules
from card import Card
from deck import Deck
from player import Player
from seat import Seat
from gamestate import GameState
from gui.graphics import Graphics

import rules
import random
from gui import gHand, gLife, gSeat
from gui.gConstants import *
from gui.gColors import *

gs = GameState()
gfx = Graphics()

pygame.init()
pygame.display.set_caption("Catchem's")

mainDeck = Deck()
discardDeck = Deck(False)
seats = [Seat((WIDTH/2) - (SEAT_WIDTH/2), HEIGHT-SEAT_HEIGHT), #human_player
         Seat(0, 0),
         Seat((WIDTH/2) - (SEAT_WIDTH/2), 0),
         Seat(WIDTH-(SEAT_WIDTH), 0)] #bottom middle -> clockwise

def create_bots():
    arr = []
    for i in range(rules.MAX_BOTS):
        arr.append(Player('bot'+str(i), i, True))
    return arr

def discard_player_hand(player):
    discardDeck.add_deck(player.hand)

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
            if p.lives > 0:
                p.hand.add(mainDeck.take())

def choose_bot_card(player, lastCardPlayed):
    if gs.bot_thinking_time > 0:
        gs.bot_thinking_time-=1
        return

    #bot player choses a card (using ai)
    matches = [x for x in player.hand.cards if x.value == lastCardPlayed.value]
    if len(matches) > 0:
        return player.hand.takeCard(matches[0])
    return player.hand.take()

def remove_life(player, lifelose):
        print('taking life ' + str(lifelose))
        player.lives-=lifelose
        gs.last_life_value_lost = lifelose
        if player.lives == 0:
            discard_player_hand(player)

def check_selection():
    card = None
    if gs.current_player.bot == False:
        if not gs.cursor_marker == None and not gs.current_player == None :
            card = gHand.isCardIntersect(gs.current_player.hand, gs.cursor_marker, gs.current_player.seat.x, gs.current_player.seat.y+SEAT_HEIGHT-CARD_HEIGHT)
            
            if not card == None:
                gs.current_player.hand.takeCard(card)

    else:
        card = choose_bot_card(gs.current_player, gs.current_card)

    if not card == None:
        gs.current_card = card
        gs.cursor_marker = None

        if not gs.last_card == None and gs.current_card.value == gs.last_card.value:
            remove_life(gs.last_player, gs.last_life_value_lost + 1)
        else:
            gs.last_life_value_lost = 0

        gs.last_card = gs.current_card
        discardDeck.add(gs.current_card)
        return True  

    return False

def next_player(players):
    current_number = gs.current_player.number
    for i in range(len(players)):
        tmp = ((current_number + i)+1) % len(players)
        p = players[tmp]
        if p == gs.current_player:
            continue
        if p.lives == 0:
            continue
        gs.last_player = gs.current_player
        gs.current_player = p
        if p.bot:
            gs.bot_thinking_time = 200+random.randint(0,300)

        return True
    return False

def main():

    #add bots
    bots = create_bots()

    #add human player
    name = 'chris'#input('Please enter your name: ')
    human_player = Player(name, len(bots))

    players = [human_player] + bots

    #assign seat to each player
    for p in range(len(players)):
        players[p].seat = seats[p]

    run = True
    shuffle_and_deal = True
    gs.current_player = human_player

    while run:

        active_players_with_cards = [x for x in players if x.lives > 0 and len(x.hand.cards) > 0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if len(active_players_with_cards) == 0:
                    shuffle_and_deal = True
                else:
                    pos = pygame.mouse.get_pos()
                    gs.cursor_marker = pos

        if shuffle_and_deal:
            empty_discard_deck()
            shuffle()
            deal(players)
            shuffle_and_deal = False
        elif check_selection():
            if not next_player(players):
                print(gs.current_player.name + ' is the Winner! Congratulations!')
                run = False

        gfx.render(players, seats, mainDeck, discardDeck, gs)

while True:
    if __name__ == '__main__':
        main()