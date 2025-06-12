# Create a class and algorithm for the cards and to find them

# green     red     purple
# 1         2       3 
# empty     striped filled
# diamond   oval    squigle

import random
from itertools import combinations
import threading
import time

class Card: 
    Colors = {"green":1, "red": 2, "purple":3}
    Quantities = {1:1, 2:2, 3:3}
    Fillings = {"empty": 1, "striped":2, "filled": 3}
    Shapes = {"diamond": 1, "oval": 2, "squiggle": 3}

    Color_names = {1: 'green', 2: 'red', 3: 'purple'}
    Filling_names = {1: 'empty', 2: 'striped', 3: 'filled'}
    Shapes_names = {1: 'diamond', 2: 'oval', 3: 'squiggle'}

    def __init__(self, color, quantity, filling, shape): 
        self.col_num = self.Colors.get(color,color) if isinstance(color, str) else color
        self.qt_num = quantity
        self.fil_num = self.Fillings.get(filling,filling) if isinstance(filling, str) else filling
        self.sh_num = self.Shapes.get(shape,shape) if isinstance(shape,str) else shape

        if self.col_num not in self.Colors.values():
            raise ValueError(f"Invalid color, must be one of{list(self.Colors.keys())}")
        if self.qt_num not in self.Quantities.values():
            raise ValueError(f"Invalid quantity, must be one of{list(self.Quantities.keys())}")
        if self.fil_num not in self.Fillings.values():
            raise ValueError(f"Invalid filling, must be one of{list(self.Fillings.keys())}")
        if self.sh_num not in self.Shapes.values():
            raise ValueError(f"Invalid shape, must be one of{list(self.Shapes.keys())}")

    @property
    def color(self):
        return self.Color_names[self.col_num]
    
    @property
    def filling(self):
        return self.Filling_names[self.fil_num]
    
    @property
    def shape(self):
        return self.Shapes_names[self.sh_num]
    
    @property
    def quantity(self):
        return self.qt_num
    
    def __eq__(self,other):
        if not isinstance(other,Card):
            return False
        return (self.col_num == other.col_num and
                self.qt_num == other.qt_num and
                self.fil_num == other.fil_num and
                self.sh_num == other.sh_num)
    
    def __hash__(self):
        return hash((self.col_num, self.qt_num, self.fil_num, self.sh_num))
    
    def __repr__(self):
        return f"Card({self.color}, {self.quantity}, {self.filling}, {self.shape})"
    
    def get_vector(self):
        return (self.col_num, self.qt_num, self.fil_num, self.sh_num)

class SetAlgorithms:
    @staticmethod
    def generate_all_cards():
        cards = []
        for color in [1,2,3]:
            for quantity in [1,2,3]:
                for filling in [1,2,3]:
                    for shape in [1,2,3]:
                        cards.append(Card(color, quantity, filling, shape))
        return cards
    
    @staticmethod
    def is_valid_set(card1: Card, card2: Card, card3: Card):
        #returns true if are all same or all different for each property
        v1 = card1.get_vector()
        v2 = card2.get_vector()
        v3 = card3.get_vector()

        for i in range(4):
            prop1, prop2, prop3 = v1[i],v2[i],v3[i]
            all_same = (prop1 == prop2 == prop3)
            all_different = (prop1 != prop2 and prop2 != prop3 and prop1 != prop3)

            if not (all_same or all_different):
                return False
            
        return True
    
    @staticmethod
    def find_all_set(cards):
        #find all sets in collection, returns list of tuples, each containing 3 cards form Set
        sets = []

        for combo in combinations(cards, 3):
            if SetAlgorithms.is_valid_set(*combo):
                sets.append(combo)
        return sets
    
    @staticmethod
    def find_one_set(cards):
        #find one set from collections card, so stops at first found
        for combo in combinations(cards,3):
            if SetAlgorithms.is_valid_set(*combo):
                return combo
        return None
    
    @staticmethod
    def is_cap_set(cards):
        #check if tehre are no sets in collection
        return SetAlgorithms.find_one_set(cards) is None
