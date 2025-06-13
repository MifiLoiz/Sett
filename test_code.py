# test code

import pygame 
import random
import sys
import time 
from constants import *
from Card_class_main_algorithm import *

all_cards = SetAlgorithms.generate_all_cards()
card_to_draw = random.choice(all_cards)[0]
print(card_to_draw[0])

def gen_first_deck(a_deck): 
    random_deck_names = ""
    for i in range(0, len(a_deck)): 
        if i < len(a_deck) - 1: 
            random_deck_names += list_pic_gen(a_deck[i])
            random_deck_names += ","
        else: 
            random_deck_names += list_pic_gen(a_deck[i])

lijst = [14,18,156,13]
print(random.choices(lijst, k=2))



#plaatje = pygame.image.load('kaarten/' + "greendiamondempty1" + '.gif').convert()
#scrn = pygame.display.set_mode((0,0))
#scrn.blit(plaatje, (0,0))