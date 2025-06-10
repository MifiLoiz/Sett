# Create a class for the cards


"""
Progress: 
    Er bestaat nu een class, die een card als een lijst ziet en (tot bepaalde mate) zich ook zo gedraagt. 
        in het vervolg zou len() en iter() kunnen worden toegevoegd
    De output van Card zou mss bijv als string kunnen worden weergegeven met de betekenissen van de waarden, dwz: 
        card:   ("purple", 2, "filled", "oval")

"""

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

    # make the Card behave like a list (this only lets you retrieve the elements)
    def __getitem__(self, index):
        if index == 1:
            return self.col
        elif index == 2:
            return self.qt
        elif index == 3:
            return self.fil        
        elif index == 4:
            return self.sh        
        else:
            raise IndexError("Card only has 4 elements: index 1 through 4")
    
    def __repr__(self):
        # Shows as a list-like string representation
        return repr([self.col, self.qt, self.fil, self.sh])

# dit is ook leuk om te testen:P    > is t nu nog leuker geworden na deze geweldige updates van Card??:D

card1 = Card(1,2,3,3)
print(card1)
print(card1[1])
