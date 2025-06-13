import pygame 
import sys
import time 
from constants import *
from Card_class_main_algorithm import *
from gen_first_deck import *
from convert_card_names import * 

# Initialize game and set parameters
pygame.init()

clock = pygame.time.Clock()     # of: pygame.time.get_ticks()

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Set")
gameDisplay.fill(background_col)

# The game
a_first_deck = random.sample(SetAlgorithms.generate_all_cards(), k=12) 
a_first_named_deck = gen_named_cards(a_first_deck)
display_12_cards(random_deck_named)

possible_sets = SetAlgorithms.find_all_set(a_first_deck)
if not len(possible_sets) > 0: 
    print("no sets possible!")
    replace_3_cards() 
    
#print("fin all sets", SetAlgorithms.find_all_set(a_first_deck))

# Display drawings
pygame.display.flip()

# Exit the game
exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()


"""
Source: 
    https://github.com/Mozes721/BlackJack

Code to get images: 
    show_card = pygame.image.load('kaarten/' + self.dealer.card_img[1] + '.png').convert()

Clock info: 
    https://www.geeksforgeeks.org/python-display-images-with-pygame/
    https://nimbusintelligence.com/2023/05/gol-1-understanding-pygame/ 
    
Display your work on the screen: 
    pygame.display.flip()

    

"""