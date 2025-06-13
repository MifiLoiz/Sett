import pygame 
import random
import sys
import time 
from constants import *
from Card_class_main_algorithm import *
from convert_card_names import *

"""
Overview of important functions and variables: 
    num_cards_table     - keeps track of the number of cards that are present on the table
    display_12_cards()  - given a 12 cards (names correspond to kaarten), display these on the table
    
"""

# Parameters
gameDisplay = pygame.display.set_mode((display_width, display_height))

# Draw random deck 
random_deck_cards = random.sample(SetAlgorithms.generate_all_cards(), k=12) 

## function that turns any amount of cards into names as in kaarten


random_deck_named = gen_named_cards(random_deck_cards)

print("random cards: ", random_deck_cards)
print("random named cards: ", random_deck_named)

# Remove 3 cards and replace them
def replace_3_cards(): 
    pass

# Function that displays 12 given cards 
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

