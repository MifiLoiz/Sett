# test code

import pygame 
import random
import sys
import time 
from constants import *
from Create_class2 import *

all_cards = SetAlgorithms.generate_all_cards()
card_to_draw = random.choice(all_cards)[0]
print(card_to_draw)