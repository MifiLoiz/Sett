import pygame 
import random
import sys
import time 
from constants import *
from Card_class_main_algorithm import *
from convert_card_names import draw_random_card, list_pic_gen

# Start game 
pygame.init()

# Clock
clock = pygame.time.Clock()     # of: pygame.time.get_ticks()

# Set screen
gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Set")
gameDisplay.fill(background_col)

# Draw random deck 
random_deck_cards = random.choices(SetAlgorithms.generate_all_cards(), k=12) 
print("random cards", random_deck_cards)

## function that turns any amount of cards into names as in kaarten
def gen_first_deck(a_deck): 
    random_deck_names = []
    for i in range(0, 12): 
        random_deck_names.append(list_pic_gen(a_deck[i]))
    return random_deck_names

print("generate names as in kaarten", gen_first_deck(random_deck_cards))

random_deck_named = gen_first_deck(random_deck_cards)

for i in range(0, len(random_deck_named)): 
    card = pygame.image.load(f'kaarten/{random_deck_named[i]}.gif').convert()
    if 0 <= i <= 3: 
        gameDisplay.blit(card, (100 + i * 120, 100))  # Space them out horizontally
    elif 4 <= i <= 7:     
        gameDisplay.blit(card, (-380 + i * 120, 325))
    elif 8 <= i <= 11: 
        gameDisplay.blit(card, (-860 + i * 120, 550)) 



# Display what is drawn 
pygame.display.flip()

# Exit
exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()


