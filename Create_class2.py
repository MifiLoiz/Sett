#Rosas poging om te uploaden
# Create a class for the cards
# Now for real 

# green     red     purple
# 1         2       3 
# empty     striped filled
# diamond   oval    squigle

class Card: 
    def __init__(self, color, quantity, filling, shape): 
        self.col = color
        self.qt = quantity
        self.fil = filling
        self.sh = shape