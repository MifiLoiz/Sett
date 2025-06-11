import pygame 
import sys
import time 
from constants import *

pygame.init()

clock = pygame.time.Clock()     # of: pygame.time.get_ticks()

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Set")
gameDisplay.fill(background_col)

pygame.display.flip()

exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()


"""
Source: 
    https://github.com/Mozes721/BlackJack

Code to get images: 
    show_card = pygame.image.load('kaarten/' + self.dealer.card_img[1] + '.png').convert()

Clock info: 
    https://www.geeksforgeeks.org/python-display-images-with-pygame/
    https://nimbusintelligence.com/2023/05/gol-1-understanding-pygame/ 
    
Display your work on the screen: 
    pygame.display.flip()

    

"""