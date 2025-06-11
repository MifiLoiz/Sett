import pygame 
import sys
import time 
from constants import *

pygame.init()

clock = pygame.time.Clock() 

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Set")
gameDisplay.fill(background_col)

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

"""