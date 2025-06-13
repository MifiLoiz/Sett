import pygame
import random
import time
import sys
from Card_class_main_algorithm import Card, SetAlgorithms

CARD_WIDTH = 120
CARD_HEIGHT = 180
CARDS_PER_ROW = 4
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
TIMER_DURATION = 30  # seconds
CARD_FOLDER = "kaarten/"
ICON_PATH = "SET_FamilyGames_digital-1.png"

#Card naming maps

Color_names = {1: 'green', 2: 'red', 3: 'purple'}
Filling_names = {1: 'shaded', 2: 'shaded', 3: 'filled'} # striped -> shaded
Shapes_names = {1: 'diamond', 2: 'oval', 3: 'squiggle'}

def card_to_filename(card: Card):
    return f"{Color_names[card.col_num]}{Shapes_names[card.sh_num]}{Filling_names[card.fil_num]}{card.qt_num}.gif"

class SetGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("SET Card Game")
        pygame.display.set_icon(pygame.image.load(ICON_PATH))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        self.deck = SetAlgorithms.generate_all_cards()
        random.shuffle(self.deck)
        self.table_cards = [self.deck.pop() for _ in range(12)]
        self.selected_indices = []
        self.user_score = 0
        self.computer_score = 0
        self.timer_start = time.time()
        self.paused = False
        self.hint_used = False
        self.hint_cards = []

    def draw_cards(self):
        self.screen.fill((200, 200, 200))
        for i, card in enumerate(self.table_cards): #counting from 0, adds counter to each card
            x = (i % CARDS_PER_ROW) * (CARD_WIDTH + 10) + 50 #cards are arranged in rows of 4, so calculates the x position based on the index  
            y = (i // CARDS_PER_ROW) * (CARD_HEIGHT + 10) + 50 #calculates the y position based on the index
            try:
                # loads the card image from \kaarten and draws image at (x,y) position
                card_img = pygame.image.load(f"{CARD_FOLDER}{card_to_filename(card)}")
                self.screen.blit(card_img, (x, y))
            except:
                #if the image file is not found, draws darker grey rectangle with missing 
                pygame.draw.rect(self.screen, (150, 150, 150), (x, y, CARD_WIDTH, CARD_HEIGHT))
                self.draw_text("Missing", x + 10, y + 70)
                
            if i in self.selected_indices:
                #if card is selected, draws a red rectangle around the card
                pygame.draw.rect(self.screen, (255, 0, 0), (x, y, CARD_WIDTH, CARD_HEIGHT), 3)
            if card in self.hint_cards:
                #if card is in hint, draws a green rectangle around the card
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, CARD_WIDTH, CARD_HEIGHT), 3)
        
        #draws current score on top left corner
        self.draw_text(f"User Score: {self.user_score} | Computer score: {self.computer_score}", 10, 10)
        
        #shows remaining time or pause message 
        if not self.paused:
            remaining = max(0, int(TIMER_DURATION - (time.time() - self.timer_start)))
            self.draw_text(f"Time left: {remaining} seconds", 10, 40)
        else: 
            self.draw_text("Game Paused", 10, 40)
        
        #draws instructions at the bottom of the screen
        self.draw_text("Hint: H | Pause: P | Confirm: Enter | Select: 0-9", 10, DISPLAY_HEIGHT - 30)
        
        #updates the screen
        pygame.display.flip()

    def draw_text(self, text, x, y):
        #renders the text string into surface,  in black
        surface = self.font.render(text, True, (0, 0, 0))
        #draws the text surface at (x,y) position
        self.screen.blit(surface, (x, y))

    def handle_click(self, pos):
        #gives both the user and computer the ability to select cards by clicking on them
        #enumerate gives index i and the card
        for i, card in enumerate(self.table_cards):
            #calculates the x and y position of the card based on the index
            x = 50 + (i % CARDS_PER_ROW) * (CARD_WIDTH + 10)
            y = 50 + (i // CARDS_PER_ROW) * (CARD_HEIGHT + 10)
            #creates rectangle for the card, which defines the clickable area
            rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            if rect.collidepoint(pos):
                #returns true if mouse click was inside the rectangle
                if i in self.selected_indices:
                    self.selected_indices.remove(i)
                else:
                    # if the card is not selected, adds the index to the selected indices
                    self.selected_indices.append(i)
                if len(self.selected_indices) == 3:
                    #if three cards are selected, calls check_user_set to validate the set
                    self.check_user_set()

    def handle_keyboard_input(self,event):
        if event.key == pygame.K_h:
            #if H is pressed, calls give_hint method
            self.give_hint()
        elif event.key == pygame.K_p:
            #if P is pressed, pauses the game
            self.paused = not self.paused
        elif event.key == pygame.K_RETURN:
            #if Enter is pressed, checks if the selected cards form a valid set
            self.check_user_set()
        elif pygame.K_0 <= event.key <= pygame.K_9:
            #if a number key is pressed, selects the corresponding card
            index = event.key - pygame.K_0
            if 0 <= index < len(self.table_cards):
                if index in self.selected_indices:
                    self.selected_indices.remove(index)
                else:
                    self.selected_indices.append(index)
                if len(self.selected_indices) == 3:
                    self.check_user_set()

    def check_user_set(self):
        #checks if the selected cards form a valid set
        if len(self.selected_indices) != 3:
            return
        cards = [self.table_cards[i] for i in self.selected_indices]
        #*cards unpacks the list into individual card objects
        if SetAlgorithms.is_valid_set(*cards):
            if not self.hint_used:
                self.user_score += 1
            self.replace_cards(self.selected_indices)
        #if the selected cards form a valid set, replaces them with new cards from the deck
        self.selected_indices.clear()
        self.hint_used = False
        self.hint_cards = []
        self.timer_start = time.time()  # reset timer on valid set

    def replace_cards(self, indices):
        for i in indices:
            if self.deck:
                self.table_cards[i] = self.deck.pop()
            else:
                self.table_cards[i] = None  # no more cards to draw
        # removes None values from table_cards to avoid empty slots    
        self.table_cards = [card for card in self.table_cards if card is not None]
        while len(self.table_cards) < 12 and self.deck:
            self.table_cards.append(self.deck.pop())
    
    def use_hint(self):
        #provides a hint by finding a valid set and selecting two of its cards
        found = set.Algorithms.find_one_set(self.table_cards)
        if found:
            self.hint_cards = random.sample(found,2)
            self.hint_used = True

    def update_timer(self):
        #updates the timer and checks if the time is up
        if not self.paused and time.time() - self.timer_start > TIMER_DURATION:
            # time is up, computer automatically selects a set if available
            found = SetAlgorithms.find_one_set(self.table_cards)
            if found:
                # computer selects a valid set
                self.computer_score += 1
                # gets the indices of the found cards in the table_cards
                indices = [self.table_cards.index(card) for card in found]
                self.replace_cards(indices)
            self.timer_start = time.time()  # reset timer after computer's turn
            self.selected_indices.clear() #helps to clear the selected indices after computer's turn
            self.hint_used = False
            self.hint_cards = []
    
    def run(self):
        #main game loop
        running = True
        while running:
            self.clock.tick(30) # limits the frame rate to 30 FPS
            self.update_timer() # helps to update the timer and check if time is up
            self.draw_cards() # draws the cards on the screen
            for event in pygame.event.get():
                # handles events such as quitting, mouse clicks, and keyboard input
                if event.type == pygame.QUIT:
                    running = False
                #MOUSEBUTTONDOWN checks if the mouse button is pressed down
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # checks if the left mouse button is clicked
                    self.handle_click(event.pos)
                #KEYDOWN checks if a key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # handles keyboard input for hints, pause, confirmation, and card selection
                    self.handle_keyboard_input(event)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SetGame()
    game.run()



            

