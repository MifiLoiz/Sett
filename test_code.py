# test code

import pygame 
import random
import sys
import time 
from constants import *
from Card_class_main_algorithm import *

all_cards = SetAlgorithms.generate_all_cards()
card_to_draw = random.choice(all_cards)[0]
print(card_to_draw)