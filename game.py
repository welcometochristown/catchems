import pygame

#game modules
from card import Card
from deck import Deck
from player import Player
from seat import Seat

import rules
import random
from gui import gHand, gLife, gSeat
from gui.gConstants import *
from gui.gColors import *

# Screen
WIDTH = 1350
HEIGHT = 650

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catchem's")

mainDeck = Deck()
discardDeck = Deck(False)

#circular seating
# seats = [Seat((WIDTH/2) - (SEAT_WIDTH/2), HEIGHT-SEAT_HEIGHT), #human_player
#          Seat(0, (HEIGHT/2) - (SEAT_HEIGHT/2)),
#          Seat((WIDTH/2) - (SEAT_WIDTH/2), 0),
#          Seat(WIDTH-(SEAT_WIDTH), (HEIGHT/2) - (SEAT_HEIGHT/2))] #bottom middle -> clockwise

#bot vs human seating
seats = [Seat((WIDTH/2) - (SEAT_WIDTH/2), HEIGHT-SEAT_HEIGHT), #human_player
         Seat(0, 0),
         Seat((WIDTH/2) - (SEAT_WIDTH/2), 0),
         Seat(WIDTH-(SEAT_WIDTH), 0)] #bottom middle -> clockwise


current_player = None
last_player = None
current_card = None
last_card = None
cursor_marker = None
last_life_value_lost = 0
bot_thinking_time = 0

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
    if bot_thinking_time > 0:
        set_bot_thinking_time(bot_thinking_time-1)
        return

    #bot player choses a card (using ai)
    matches = [x for x in player.hand.cards if x.value == lastCardPlayed.value]
    if len(matches) > 0:
        return player.hand.takeCard(matches[0])
    return player.hand.take()

def remove_life(player, lifelose):
        player.lives-=lifelose
        set_last_life_value_lost(lifelose)
        print(player.name + ' loses ' + str(lifelose) + 'x life!')
        if player.lives == 0:
            print(player.name + ' is out of the game!')
            discard_player_hand(player)

font = pygame.font.Font('freesansbold.ttf', 16)
bg = pygame.image.load("images/yellow-wood-table-background.jpg")
cards = pygame.image.load("images/cards.png")

def load_card_images(): 
    arr  = [[0 for x in range(13)] for y in range(5)] 
    for y in range(5):
        for x in range(13):
            surf = pygame.Surface((CARD_IMAGE_WIDTH, CARD_IMAGE_HEIGHT), pygame.SRCALPHA)
            surf.blit(cards, (0,0), (x*CARD_IMAGE_WIDTH, y*CARD_IMAGE_HEIGHT, CARD_IMAGE_WIDTH, CARD_IMAGE_HEIGHT) )
            arr[y][x] = surf

    return arr

card_images = load_card_images()

def render(players):
    win.fill(WHITE)
    win.blit(bg, (0, 0))

    for seat in seats:
        render_seat(seat)

    for player in players:
        render_player(player)

    render_discard_deck()
    draw_cursor_marker()
    render_life_value_lose()

    pygame.display.update()

def render_player(player):
    render_cards(player)
    render_lives(player)

def render_cards(player):
    gHand.draw(player.hand, win, font, card_images, player.seat.x, player.seat.y+SEAT_HEIGHT-CARD_HEIGHT, not player.bot)

def render_lives(player):
    gLife.draw(player.lives, win, player.seat.x+LIFE_RADIUS, player.seat.y+LIFE_RADIUS)

def render_seat(seat):
    color = BLACK
    if seat == current_player.seat:
        color = BLUE

    gSeat.draw(seat, win, seat.x, seat.y, color)

def render_life_value_lose():
    text = font.render(str(last_life_value_lost), True, BLACK) 
    textRect = text.get_rect()
    textRect.x = 10
    textRect.y = HEIGHT - 20
    win.blit(text, textRect)

def render_discard_deck():
    gHand.draw(discardDeck, win, font, card_images, 0, (HEIGHT/2)-(CARD_HEIGHT/2), True, True)
 
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

def set_bot_thinking_time(time):
    global bot_thinking_time
    bot_thinking_time = time

def set_last_life_value_lost(value):
    global last_life_value_lost
    last_life_value_lost = value

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

        if not last_card == None and current_card.value == last_card.value:
            remove_life(last_player, last_life_value_lost + 1)
        else:
            set_last_life_value_lost(0)

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
        if p.bot:
            set_bot_thinking_time(200+random.randint(0,300))
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

    set_current_player(human_player)

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
                    set_cursor_marker(pos)

        if shuffle_and_deal:
            empty_discard_deck()
            shuffle()
            deal(players)
            shuffle_and_deal = False
        elif check_selection():
            if not next_player(players):
                print(current_player.name + ' is the Winner! Congratulations!')
                run = False

        render(players)

while True:
    if __name__ == '__main__':
        main()