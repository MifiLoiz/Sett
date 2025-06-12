import pygame 
import random
import sys
import time 
from constants import *
from Card_class_main_algorithm import *

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

def list_pic_gen(card): 
    color_pic = Color_names[card[0]]
    shape_pic = Shapes_names[card[3]]
    fill_pic = Filling_names[card[2]]
    quantity_pic = card[1]
    return f"{color_pic}{shape_pic}{fill_pic}{quantity_pic}"

print(Card(1,2,3,3))

all_cards = SetAlgorithms.generate_all_cards()
card_to_draw = random.choice(all_cards)

print(list_pic_gen(card_to_draw))