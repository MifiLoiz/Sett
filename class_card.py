## Class Card

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

    def __getitem__(self, index):
        if index == 0:
            return self.col_num
        elif index == 1:
            return self.qt_num
        elif index == 2:
            return self.fil_num       
        elif index == 3:
            return self.sh_num      
        else:
            raise IndexError("Card only has 4 elements: index 0 through 3")
