## Create a deck and table 
# first draft 

""" 
For now, I just want it to create all possible cards and randomly pick 12 of these in order to create a table. 

Problems: 
    dk how to import Card; 
        https://graphite.dev/guides/how-to-pull-from-another-branch-in-git
    dk how to print the cards; 
    dk if anything works at this point, but seems like an idea for a good code:P

"""

# green     red     purple
# 1         2       3 
# empty     striped filled
# diamond   oval    squigle

# Imports
import random
#from Create_class2 import Card

# Manual card import
class Card: 
    def __init__(self, color, quantity, filling, shape): 
        self.col = color
        self.qt = quantity
        self.fil = filling
        self.sh = shape

#tes = Card(1,2,2,1)
#print(tes)

# Create a deck
class Deck: 
    def __init__(self, colors = 3, quantities = 3, fillings = 3, shapes = 3):
        self.col = colors
        self.qt = quantities
        self.fil = fillings
        self.sh = shapes

    def deck_o_card(self):
        deck = []
        for c in range(1, self.col + 1):
            for q in range(1, self.qt + 1):
                for f in range(1, self.fil + 1): 
                    for s in range(1, self.sh + 1): 
                        return deck.append(Card(c, q, f, s))

deck = Deck()
print(deck)

# Create a table
class Table: 
    def __init__(self): 
        pass

    def table_gen(self): 
        not_picked = Deck()

        for i in range(0, 13): 
            pick = choice(not_picked)
            not_picked = remove(pick)

table = Table()
print(table)


