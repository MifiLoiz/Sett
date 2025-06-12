import pygame 
import random
import sys
import time 
from constants import *
from Create_class2 import *

all_cards = SetAlgorithms.generate_all_cards()
card_to_draw = random.choice(all_cards)[0]
print(card_to_draw)

Colors = {"green":1, "red": 2, "purple":3}
Quantities = {1:1, 2:2, 3:3}
Fillings = {"empty": 1, "striped":2, "filled": 3}
Shapes = {"diamond": 1, "oval": 2, "squiggle": 3}

Color_names = {1: 'green', 2: 'red', 3: 'purple'}
Filling_names = {1: 'empty', 2: 'striped', 3: 'filled'}
Shapes_names = {1: 'diamond', 2: 'oval', 3: 'squiggle'}

#def translator_cardnames(card_to_draw): 
