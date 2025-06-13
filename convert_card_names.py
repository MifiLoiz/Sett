import pygame 
import random
import sys
import time 
from constants import *
from Card_class_main_algorithm import *

""" 
Important functions and variables from this file: 
    list_pic_gen()      - gets the name of the card as it is stated in kaarten
    gen_named_deck()    - given any amount of cards, match the card correspond to in the filenames in kaarten


"""

Color_names = {1: 'green', 2: 'red', 3: 'purple'}
Filling_names = {1: 'empty', 2: 'shaded', 3: 'filled'}
Shapes_names = {1: 'diamond', 2: 'oval', 3: 'squiggle'}

def list_pic_gen(card): 
    color_pic = Color_names[card[0]]
    shape_pic = Shapes_names[card[3]]
    fill_pic = Filling_names[card[2]]
    quantity_pic = card[1]
    return f"{color_pic}{shape_pic}{fill_pic}{quantity_pic}"

def gen_named_cards(a_deck): 
    random_deck_names = []
    for i in range(0, len(a_deck)): 
        random_deck_names.append(list_pic_gen(a_deck[i]))
    return random_deck_names

print(Card(1,2,3,3))
print(list_pic_gen(Card(1,2,3,3)))

def draw_random_card(): 
    all_cards = SetAlgorithms.generate_all_cards()
    one_card = random.choice(all_cards)
    return list_pic_gen(one_card)

#print(draw_random_card())

#print(f"{draw_random_card()}")