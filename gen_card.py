import pygame 
import random
import sys
import time 
from constants import *
from Card_class_main_algorithm import *
from convert_card_names import draw_random_card

# Start game 
pygame.init()

# Clock
clock = pygame.time.Clock()     # of: pygame.time.get_ticks()

# Draw card display 
gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Set")
gameDisplay.fill(background_col)

#card_to_draw = random.SetAlgorithms.generate_all_cards()
#print(card_to_draw)

random_card = draw_random_card()
print("random card", random_card)
plaatje = pygame.image.load('kaarten/' + str(random_card) + '.gif').convert()
scrn = pygame.display.set_mode((0,0))
scrn.blit(plaatje, (0,0))
pygame.display.flip()

# Exit
exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()


