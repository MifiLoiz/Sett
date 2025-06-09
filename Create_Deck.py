## Create a deck and table 
# first draft 

""" 
For now, I just want it to create all possible cards and randomly pick 12 of these in order to create a table. 

Problems: 
    dk how to import Card; 
        https://graphite.dev/guides/how-to-pull-from-another-branch-in-git
        
        Setp-by-step guide: 
            git checkout First_Class
            git add first_class.py
            git commit -m "Add First_Class implementation"
            git push origin First_Class

            git checkout Second_Class
            git merge First_Class

            git merge First_Branch --no-edit

    dk if anything works at this point, but seems like an idea for a good code:P

    My additions to the file are not run, I always get printed: 
        [1, 2, 3, 3]
        1

"""

# green     red     purple
# 1         2       3 
# empty     striped filled
# diamond   oval    squigle

# Imports
import random
from Create_class2 import Card

# Manual card import
#class Card: 
#    def __init__(self, color, quantity, filling, shape): 
#        self.col = color
#        self.qt = quantity
#        self.fil = filling
#        self.sh = shape

#Card(0,1,2,3)
#tes = Card(1,2,2,1)
#print(tes)
#print(tes[0])

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
                        print("dit is: ", s)
                        return deck.append(Card(c, q, f, s))


Deck()
#print(deck)

# Create a table
class Table: 
    def __init__(self): 
        pass

    def table_gen(self): 
        not_picked = Deck()

        for i in range(0, 13): 
            pick = random.choice(not_picked)
            #not_picked = remove(pick)

#Table()
#print(table)


