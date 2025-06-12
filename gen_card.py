import pygame 
import random
import sys
import time 
from constants import *
from Card_class_main_algorithm import *
from convert_card_names import draw_random_card, list_pic_gen

""" 
Ideëen voor later: 
    De eerste deck kan gwn random zijn, maar de de volgende kaarten mogen niet nog een keer opgelegd worden. 
    Het spel zou in theorie moeten kunnen eindigen als alle kaarten op zijn gedeeld (en er geen zetten meer mogelijk zijn)
    Buttons: pauze, hint 

"""

# Start game 
pygame.init()

# Clock
clock = pygame.time.Clock()     # of: pygame.time.get_ticks()

# Set screen
gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Set")
gameDisplay.fill(background_col)

# Draw random card  
random_card = draw_random_card()

plaatje = pygame.image.load('kaarten/' + str(random_card) + '.gif').convert()
gameDisplay.blit(plaatje, (500, 100))

# Display what is drawn 
pygame.display.flip()

# Exit
exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()


