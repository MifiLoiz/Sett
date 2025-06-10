# Class for the cards
class Card: 
    # Alle mogelijke waardes voor elk deel van de kaart
    Colors = ["green", "red", "purple"]
    Numbers = [1,2,3]
    Filling = ["empty", "striped", "filled"]
    Shape = ["diamond", "oval", "squiggle"]

    def __init__(self, color, number, filling, shape): 
        # Zorgen ervoor dat elke kaart de juiste eigenschappen heeft
        if color not in self.Colors:
            raise ValueError("Error: invalid color, it must either be green, red or purple")
        if number not in self.Numbers:
            raise ValueError("Error: invalid number, it must either be 1,2 or 3")
        if filling not in self.Filling:
            raise ValueError("Error: invalid filling, it must either be empty, striped or filled")
        if shape not in self.Shape:
            raise ValueError("Error: invalid shape, it must either be diamond, oval or squiggle")

        self.color = color
        self.number = number
        self.filling = filling
        self.shape = shape

    @classmethod
    # Zorgt ervoor dat er een list ontstaat met alle 81 unieke kaarten
    def all_cards(cls):
        return [cls(color, number, filling, shape)
                for color in cls.Colors
                for number in cls.Numbers
                for filling in cls.Filling
                for shape in cls.Shape]

    # Geeft ons alle aspecten van één kaart in de vorm van een list
    def features(self):
        return[self.color, self.number, self.filling, self.shape]