## Class SetAlgorithms

from class_card import Card
from itertools import combinations

""" 
Welcome to the file of the Class SetAlgorithms. This class contains the foundation of the structure of the game.

Firstly, the function generate_all_cards() generates all possible cards of the SET game. Each card is of the class Card, making it convenient to work with. 
This function will be used in other files to generate a deck of cards. 
Then, the function is_valid_set() checks whether a suggested SET is valid or not. 
This function is used in find_all_set() to check whether the current cards on the table form a SET or not. 
In some other parts of the code it turns out it is convenient to have a function that checks if a valid SET is present at all, which is what find_one_set() and is_cap_set() are responsible for.
"""

class SetAlgorithms:
    @staticmethod
    # Generate all 81 cards of the game SET
    def generate_all_cards():
        # Initiate a list that will consist all 81 cards at the end
        cards = []
        
        # Create combinations with all properties
        for color in [1,2,3]:
            for quantity in [1,2,3]:
                for filling in [1,2,3]:
                    for shape in [1,2,3]:
                        cards.append(Card(color, quantity, filling, shape))     # Return cards as Card for convenience later on
        return cards
    
    @staticmethod
    # Checks if a given combination of cards is a valid SET
    def is_valid_set(card1: Card, card2: Card, card3: Card):
        # Retrieve properties of each card by getting its vector
        v1 = card1.get_vector()
        v2 = card2.get_vector()
        v3 = card3.get_vector()

        # For each type of property, check whether the cards are all alike, all different or not. 
        for i in range(4):
            prop1, prop2, prop3 = v1[i],v2[i],v3[i]
            all_same = (prop1 == prop2 == prop3)    
            all_different = (prop1 != prop2 and prop2 != prop3 and prop1 != prop3)

            # Once one False occurs, the SET is not valid (regardless of the other properties) 
            if not (all_same or all_different): 
                return False
        
        # If all properties are either the same or different, return True
        return True
    
    @staticmethod
    # Find all sets in a collection; returns a list of tuples, each containing 3 cards that form a valid SET
    def find_all_set(cards):
        # Initiate the list that will be returned
        sets = []

        # Check for all possible combinations of cards whether they form a set or not 
        for combo in combinations(cards, 3):
            if SetAlgorithms.is_valid_set(*combo):
                sets.append(combo)  # Only append if it is a valid SET
        return sets
    
    @staticmethod
    # Find one valid SET from the collection of cards
    def find_one_set(cards):
        # Check for all possible combinations 
        for combo in combinations(cards,3):
            if SetAlgorithms.is_valid_set(*combo):
                return combo    # Once a valid SET is found, return this one and stop here
        return None
    
    @staticmethod
    def is_cap_set(cards):
        #check if there are no sets in collection
        return SetAlgorithms.find_one_set(cards) is None
