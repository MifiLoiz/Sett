## Class SetAlgorithms

from class_card import Card
from itertools import combinations
#import threading ROSA ??? is deze nodig? vm niet 
#import time

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
