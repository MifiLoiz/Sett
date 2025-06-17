## Stand alone code 

from class_card import Card

#Card naming maps
Color_names = {1: 'green', 2: 'red', 3: 'purple'}
Filling_names = {1: 'empty', 2: 'striped', 3: 'filled'} # striped -> shaded
Shapes_names = {1: 'diamond', 2: 'oval', 3: 'squiggle'}

def card_to_filename(card: Card):
    #convert list of card objects to filenames
    return f"{Color_names[card.col_num]}{Shapes_names[card.sh_num]}{Filling_names[card.fil_num]}{card.qt_num}.gif"
