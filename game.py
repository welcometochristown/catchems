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
seats = [Seat((WIDTH/2) - (SEAT_WIDTH/2), HEIGHT-SEAT_HEIGHT),
         Seat(0, (HEIGHT/2) - (SEAT_HEIGHT/2)),
         Seat((WIDTH/2) - (SEAT_WIDTH/2), 0),
         Seat(WIDTH-(SEAT_WIDTH), (HEIGHT/2) - (SEAT_HEIGHT/2))] #bottom middle -> clockwise

current_player = None
last_player = None
current_card = None
last_card = None
cursor_marker = None

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
            p.hand.add(mainDeck.take())

# def play_rounds(players, rounds=rules.PLAYER_CARDS):
#     #play [rounds] rounds for each player in [active_players]
#     prevCard = None
#     prevPlayer = None
#     lifelose = rules.MIN_LIFE_LOSS

#     for i in range(rounds):
#         for p in players:
#             if p.lives == 0:
#                 if len(p.hand.cards) > 0:
#                     discard_player_hand(p)
#                 continue
#             c = play_turn(p, prevCard)

#             if compare_turns(prevCard, c):
#                 remove_life(prevPlayer, lifelose)
#                 lifelose +=1
#             else:
#                 lifelose = rules.MIN_LIFE_LOSS
#             prevCard = c
#             prevPlayer = p
#         #end of round
#         discard_turn_deck()

# def compare_turns(prevCard, card):
#     if prevCard is None:
#         return False
#     return (card.value == prevCard.value)

# def play_turn(player, lastCardPlayed):
#     #[player] takes their turn
#     if not player.bot:
#         card = choose_human_card(player)
#     else:
#         card = choose_bot_card(player, lastCardPlayed)

#     print(player.name + ' plays ' + str(card))
#     turnDeck.add(card)
#     return card

# def choose_human_card(player):
#     #human player choses a card (using input)
#     while True:
#         print(player.hand.cards)
#         choice = input('Please enter your card: ')
#         cards = [x for x in player.hand.cards if x.short == choice]
#         if len(cards) != 1:
#             continue
#         return player.hand.takeCard(cards[0])

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

    render_discard_deck()
    draw_cursor_marker()

    pygame.display.update()

def render_player(player):
    render_cards(player)
    render_lives(player)

def render_cards(player):
    gHand.draw(player.hand, win, player.seat.x, player.seat.y+SEAT_HEIGHT-CARD_HEIGHT)

def render_lives(player):
    gLife.draw(player.lives, win, player.seat.x+LIFE_RADIUS, player.seat.y+LIFE_RADIUS)

def render_seat(seat):
    color = BLACK
    if seat == current_player.seat:
        color = BLUE

    gSeat.draw(seat, win, seat.x, seat.y, color)

def render_discard_deck():
    gHand.draw(discardDeck, win, WIDTH/2 - ((CARD_WIDTH*5)/2), HEIGHT/2, True)

def set_current_player(player):
    global current_player
    set_last_player(current_player)
    current_player = player

def set_last_player(player):
    global last_player
    last_player = player

def set_cursor_marker(pos):
    global cursor_marker
    cursor_marker = pos

def set_current_card(card):
    global current_card
    set_last_card(current_card)
    current_card = card

def set_last_card(card):
    global last_card
    last_card = card

def draw_cursor_marker():
    if not cursor_marker == None:
        pygame.draw.circle(win, RED, cursor_marker, 5)

def check_selection():
    card = None
    if current_player.bot == False:
        if not cursor_marker == None and not current_player == None :
            card = gHand.isCardIntersect(current_player.hand, cursor_marker, current_player.seat.x, current_player.seat.y+SEAT_HEIGHT-CARD_HEIGHT)
            
            if not card == None:
                current_player.hand.takeCard(card)

    else:
        card = choose_bot_card(current_player, current_card)

    if not card == None:
        set_current_card(card)
        set_cursor_marker(None)

        if current_card == last_card:
            remove_life(last_player, 1)

        discardDeck.add(current_card)
        return True

    return False

def next_player(players):
    current_number = current_player.number
    for i in range(len(players)):
        tmp = ((current_number + i)+1) % len(players)
        p = players[tmp]
        if p == current_player:
            continue
        if p.lives == 0:
            continue
        set_current_player(p)
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

    shuffle()
    deal(players)
    set_current_player(human_player)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                set_cursor_marker(pos)

        players_with_cards = [x for x in players if len(x.hand.cards) > 0]

        if len(players_with_cards) == 0:
            empty_discard_deck()
            deal(players)
        elif check_selection():
            if not next_player(players):
                print(current_player.name + ' is the Winner! Congratulations!')
                run = False

        render(players)

       # 

while True:
    if __name__ == '__main__':
        main()