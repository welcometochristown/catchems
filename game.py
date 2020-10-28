#import pygame

#game modules
from card import Card
from deck import Deck
from player import Player
import rules

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

players = create_bots()

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

def deal(active_players, cards=rules.PLAYER_CARDS):
    #deal [cards] cards to each player
    print ('dealing..')
    for i in range(cards):
        for p in active_players:
            p.hand.add(mainDeck.take())

def play_rounds(active_players, rounds=rules.PLAYER_CARDS):
    #play [rounds] rounds for each player in [active_players]
    prevCard = None
    prevPlayer = None
    lifelose = rules.MIN_LIFE_LOSS

    for i in range(rounds):
        for p in active_players:
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
        print_lives()

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

def print_lives():
    for p in players:
        lives = ''
        for l in range(p.lives):
            lives += '*'
        print(p.name + ' ' + lives)

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
        play_rounds(active_players)
        empty_discard_deck() 

#while True:
if __name__ == '__main__':
    main()