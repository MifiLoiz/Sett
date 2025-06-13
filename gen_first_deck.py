import pygame 
import random
import sys
import time 
from constants import *
from Card_class_main_algorithm import *
from convert_card_names import draw_random_card, list_pic_gen

"""
Overview of important functions and variables: 
    gen_first_deck()    - generates 12 random cards, whose names correspond to the filenames in kaarten
    num_cards_table     - keeps track of the number of cards that are present on the table
    display_12_cards()  - given a 12 cards (names correspond to kaarten), display these on the table
"""

# Start game 
pygame.init()

# Clock
clock = pygame.time.Clock()     # of: pygame.time.get_ticks()

# Set screen
gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Set")
gameDisplay.fill(background_col)

# Draw random deck 
random_deck_cards = random.sample(SetAlgorithms.generate_all_cards(), k=12) 

## function that turns any amount of cards into names as in kaarten
def gen_first_deck(a_deck): 
    random_deck_names = []
    for i in range(0, 12): 
        random_deck_names.append(list_pic_gen(a_deck[i]))
    return random_deck_names


random_deck_named = gen_first_deck(random_deck_cards)

def display_12_cards(deck_cards): 
    for i in range(0, len(deck_cards)): 
        card = pygame.image.load(f'kaarten/{deck_cards[i]}.gif').convert()
        num_cards_table = 0
        if 0 <= i <= 3: 
            gameDisplay.blit(card, (100 + i * 120, 100))  # Space them out horizontally
            num_cards_table += 1
        elif 4 <= i <= 7:     
            gameDisplay.blit(card, (-380 + i * 120, 325))
            num_cards_table += 1
        elif 8 <= i <= 11: 
            gameDisplay.blit(card, (-860 + i * 120, 550))
            num_cards_table += 1 

display_12_cards(random_deck_named)


# Display what is drawn 
pygame.display.flip()

# Exit
exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()


