import pygame
import random
import time
import sys
from Card_class_main_algorithm import Card, SetAlgorithms
from itertools import combinations

"""
14-06-25, 11.15
Copied from Anouk's code 
"""

CARD_WIDTH = 100
CARD_HEIGHT = 150
MAX_CARDS_PER_ROW = 6
MARGIN = 15
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 600
TIMER_DURATION = 30  # seconds
CARD_FOLDER = "kaarten/"
ICON_PATH = "SET_FamilyGames_digital-1.png"
INITIAL_CARDS = 12  # initial number of cards on the table
CARDS_TO_ADD = 3  # number of cards to add when no set is found
MESSAGE_DURATION = 3  # seconds for message display
COMPUTER_PAUSE = 3 #seconds to pause after computer finds set

#Card naming maps
Color_names = {1: 'green', 2: 'red', 3: 'purple'}
Filling_names = {1: 'empty', 2: 'striped', 3: 'filled'} # striped -> shaded
Shapes_names = {1: 'diamond', 2: 'oval', 3: 'squiggle'}

def card_to_filename(card: Card):
    #convert list of card objects to filenames
    return f"{Color_names[card.col_num]}{Shapes_names[card.sh_num]}{Filling_names[card.fil_num]}{card.qt_num}.gif"

class SetGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("SET Card Game")
        try:
            pygame.display.set_icon(pygame.image.load(ICON_PATH))
        except:
            pass #skip if icon not found

        self.clock = pygame.time.Clock() # pygame.time.Clock() to control the frame rate
        self.font = pygame.font.SysFont('Arial', 28)
        self.small_font = pygame.font.SysFont('Arial', 20)
        
        #game setup
        self.deck = SetAlgorithms.generate_all_cards()
        random.shuffle(self.deck)
        self.table_cards = [self.deck.pop() for _ in range(INITIAL_CARDS)]
        self.selected_indices = []
        self.user_score = 0
        self.computer_score = 0
        self.timer_start = time.time()
        self.time_remaining = TIMER_DURATION
        self.paused = False
        self.pause_time = 0
        self.hint_used = False
        self.hint_cards = []
        #message for user feedback
        self.message = ""
        self.message_time = 0
        self.message_color = (0, 0, 0)  # default color for messages
        self.computer_last_set_indices = [] # indices of the last set found by the computer
        self.game_over = False
        self.scroll_offset = 0 #for scrolling through cards
        self.computer_pause_end = 0
#!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.computer_set_found_time = None # time when computer finds a set
        self.computer_pause_duration = 3 #3 seconds pause
        self.computer_processing = False #To make sure that we can continue the game and the computer does not take over

    def draw_text(self, text, x, y, font=None, color=(0, 0, 0)):
        #helps to draw text on the screen at (x,y) position with specified font and color
        if font is None:
            font = self.small_font
        surface = font.render(text, True, (0, 0, 0))
        #draws the text surface at (x,y) position
        self.screen.blit(surface, (x, y))

    def calculate_card_positions(self):
        positions = []
        cards_per_row = min(MAX_CARDS_PER_ROW, len(self.table_cards))  # ensures we don't exceed the number of cards

        if cards_per_row == 0:
            return positions  # no cards to position
        
        card_spacing = (DISPLAY_WIDTH - (cards_per_row * CARD_WIDTH)) // (cards_per_row + 1)  # calculates spacing between cards
        card_x = card_spacing
        card_y = 80 + self.scroll_offset  # below the score/timer and adjusted for scrolling

        for i in range(len(self.table_cards)):
            if i > 0 and i % cards_per_row == 0:
                card_x = card_spacing  # resets x position for the next row
                card_y += CARD_HEIGHT + MARGIN

            positions.append((card_x, card_y))
            card_x += CARD_WIDTH + card_spacing  # moves to the next card position
        return positions
    
    def draw_cards(self):
        #draw all cards with proper spacing
        self.screen.fill((200, 200, 200))

        #draws current score and timer on top left corner
        self.draw_text(f"User Score: {self.user_score}", 20, 10, self.font) #draws user score on top left corner
        self.draw_text(f"Computer score: {self.computer_score}", 20, 40, self.font) #draws computer score below user score
        self.draw_text(f"time:{int(self.time_remaining)}s", DISPLAY_WIDTH - 100, 50, self.font, (255,0,0)) #draws timer on top right corner
        
        #shows pause 
        if self.paused:
            self.draw_text("Game Paused", DISPLAY_WIDTH - 120, 30, self.small_font, color=(255, 0, 0),)
        
        #draw cards
        positions = self.calculate_card_positions()  # calculates positions for the cards
        for i, (card_x, card_y) in enumerate(positions):
            if i >= len(self.table_cards):
                break # ensures we don't exceed the number of cards
            
            if card_y + CARD_HEIGHT > 0 and card_y < DISPLAY_HEIGHT:
                # only draws cards that are within the visible area of the screen
                card = self.table_cards[i]
                pygame.draw.rect(self.screen, (255, 255, 255), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT))  # draws white rectangle for the card background
                try:
                    card_img = pygame.image.load(f"{CARD_FOLDER}{card_to_filename(card)}")
                    card_img = pygame.transform.scale(card_img, (CARD_WIDTH - 10, CARD_HEIGHT - 10))  # scales the image to fit the card size
                    self.screen.blit(card_img, (card_x + 5, card_y + 5))  # draws the card image with a small margin
                except:
                    #fallback if image is not found
                    pygame.draw.rect(self.screen, (200, 200, 200), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT))  # draws a grey rectangle for missing card image
                    self.draw_text(f"Card{i+1}", card_x + 10, card_y + 60, self.small_font)

                if i in self.selected_indices:
                    # draws red rectangle around selected cards
                    pygame.draw.rect(self.screen, (255, 0, 0), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT), 3)
                elif card in self.hint_cards:
                    # draws green rectangle around hint cards
                    pygame.draw.rect(self.screen, (0, 255, 0), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT), 3)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # Checks if this is the last set the computer has found and marks the found set blue
                elif i in self.computer_last_set_indices and time.time() < self.computer_pause_end:
                    pygame.draw.rect(self.screen, (0,0,255), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT), 3)

        #draw instructions
        instructions = [
            "Hint: H | Pause: P | Confirm: Enter",
            "Select: 1-9 | 0 = 10 | Shift + 1-9 = 11-19",
            "Scroll: up/down arrow keys", #scrolls through cards
        ]

        for i, text in enumerate(instructions):
            self.draw_text(text, MARGIN, DISPLAY_HEIGHT - 80 + i * 25, self.small_font)

        if self.message and time.time() - self.message_time < MESSAGE_DURATION:
            msg_surface = self.font.render(self.message, True, self.message_color) # renders the message text
            self.screen.blit(msg_surface, (DISPLAY_WIDTH // 2 - msg_surface.get_width() // 2, DISPLAY_HEIGHT - 30)) # draws message at the bottom of the screen

        if self.computer_last_set_indices and time.time() < self.computer_pause_end:
            comp_msg = "Computer found set: " + ", ".join(str(i + 1) for i in self.computer_last_set_indices)
            comp_surface = self.small_font.render(comp_msg, True, (200, 0, 0))
            self.screen.blit(comp_surface, (DISPLAY_WIDTH // 2 - comp_surface.get_width() // 2, DISPLAY_HEIGHT - 60))

        #updates the screen
        pygame.display.flip()

    def handle_click(self, pos):
        if time.time() < self.computer_pause_end:
            return  # ignore clicks during computer's pause
        
        positions = self.calculate_card_positions()  # calculates positions for the cards
        for i, (card_x, card_y) in enumerate(positions):
            if i >= len(self.table_cards):
                break

            if card_y + CARD_HEIGHT > 0 and card_y < DISPLAY_HEIGHT:
                # only checks cards that are within the visible area of the screen
                rect = pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
                if rect.collidepoint(pos):
                    # checks if the mouse click was inside the rectangle of the card
                    if i in self.selected_indices:
                        self.selected_indices.remove(i)
                    else:
                        # if the card is not selected, adds the index to the selected indices
                        if len(self.selected_indices) < 3:
                            self.selected_indices.append(i)
                    if len(self.selected_indices) == 3:
                        # if three cards are selected, calls check_user_set to validate the set
                        self.check_user_set()
                    break

    def handle_keyboard_input(self,event):
        if time.time() < self.computer_pause_end:
            return  # ignore keyboard input during computer's pause
        
        if pygame.K_0 <= event.key <= pygame.K_9:
            index = event.key - pygame.K_0 # 0 = 0, 1 = 1, ..., 9 = 9
            if index == 0:
                index = 9 # maps 0 to 10
            else:
                index -= 1  # maps 1-9 to 0-8

            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_SHIFT:
                index += 10 # maps 1-9 to 11-19
            
            self.select_card(index)

        elif event.key == pygame.K_UP:
            # scrolls up through the cards
            self.scroll_offset = min(0, self.scroll_offset + 20)
        elif event.key == pygame.K_DOWN:
            max_offset = -((len(self.table_cards) // MAX_CARDS_PER_ROW) * (CARD_HEIGHT + MARGIN) - DISPLAY_HEIGHT + 200) # calculates max scroll offset based on number of cards
            self.scroll_offset = max(max_offset, self.scroll_offset - 20) #scrolls down through the cards
        
        elif event.key == pygame.K_h:
            #if H is pressed, calls give_hint method
            self.give_hint()
        elif event.key == pygame.K_p:
            # if P is pressed, toggles pause state
            self.toggle_pause()
        elif event.key == pygame.K_RETURN:
            #if Enter is pressed, checks if the selected cards form a valid set
            self.check_user_set()

    def toggle_pause(self):
        if self.paused:
            pause_duration = time.time() - self.pause_time
            self.timer_start += pause_duration  # adjusts the timer start to account for the pause duration
        else:
            self.pause_time = time.time()
        self.paused = not self.paused  # toggles the pause state
    
    def select_card(self, index):
        #selects a card based on the index, if index is valid
        if index < len(self.table_cards):
            if index in self.selected_indices:
                self.selected_indices.remove(index)
            else:
                if len(self.selected_indices) < 3:
                    self.selected_indices.append(index)
            if len(self.selected_indices) == 3:
                self.check_user_set()  # checks if the selected cards form a valid set

    def check_user_set(self):
        #checks if the selected cards form a valid set
        if len(self.selected_indices) != 3:
            return
        
        cards = [self.table_cards[i] for i in self.selected_indices]
        #*cards unpacks the list into individual card objects
        if SetAlgorithms.is_valid_set(*cards):
            self.message = "Valid SET found!" + (" +1 point" if not self.hint_used else "")
            self.message_color = (255, 105, 189) # pink color for valid set message
            if not self.hint_used:
                self.user_score += 1
            self.replace_cards(self.selected_indices)
            self.timer_start = time.time()  # resets the timer on valid set
        else:
            self.message = "Not a valid SET!"
            self.message_color = (255, 0, 0)  # red color for invalid set message
        
        self.message_time = time.time()  # sets the message time to current time
        self.selected_indices.clear()
        self.hint_used = False
        self.hint_cards = []

    def replace_cards(self, indices):
        indices = sorted(indices, reverse=True)  # sort indices in reverse order to avoid index errors
        for i in indices:
            if i < len(self.table_cards) and self.deck: # checks if index is within bounds
                self.table_cards[i] = self.deck.pop()
            
        while len(self.table_cards) < INITIAL_CARDS and self.deck:
            self.table_cards.append(self.deck.pop()) # adds cards until we have the initial number of cards
               
    def add_cards(self,count):
        for _ in range(count):
            if self.deck:
                self.table_cards.append(self.deck.pop())
    
#!!!!!!!!!!!!!!!!!!!!!!
    # Removes the first three cards of the cards on the table when there are more than 12 cards, thus when new cards have been added
    def remove_top_cards(self, count):
        if len(self.table_cards) > count:
            self.table_cards = self.table_cards[count:]
#!!!!!!!!!!!!!!!!!!!!!!!!
    # Removes cards in sets of three until there are only 12 crads   
    def clean_up_table(self):
        while len(self.table_cards) > INITIAL_CARDS and not SetAlgorithms.find_one_set(self.table_cards):
            self.remove_top_cards(CARDS_TO_ADD)
#!!!!!!!!!!!!!!!!!!!!!!!
    # Determines the end of the game
    def check_game_over(self):
        if not SetAlgorithms.find_one_set(self.table_cards) and not self.deck:
            self.game_over = True
            self.message = "Game Over!"
            self.message_color = (50,50,50)
            self.message_time = time.time()

    def give_hint(self):
        #provides a hint by finding a valid set and selecting two of its cards
        found_set = SetAlgorithms.find_one_set(self.table_cards)
        if found_set:
            self.hint_cards = random.sample(found_set,2)
            self.hint_used = True
            self.message = "Hint: Two cards from a valid SET"
            self.message_color = (0, 0, 255)  # blue color for hint message
            self.message_time = time.time()  # sets the message time to current time

    def computer_turn(self):
        if self.computer_processing:
            return #Don't allow new turns during the pause
        #computer's turn to find a set
        found_set = SetAlgorithms.find_one_set(self.table_cards)
        if found_set and SetAlgorithms.is_valid_set(*found_set):
            self.computer_last_set_indices = [self.table_cards.index(card) for card in found_set]
            self.computer_score += 1
            self.message = "Computer found a SET! +1 point"
            self.message_color = (200,0,20) # dark red color for computer's valid set message
            self.message_time = time.time()  # sets the message time to current time
            self.computer_pause_end = time.time() + COMPUTER_PAUSE  # sets the pause end time for computer's turn
            self.computer_set_found_time = time.time()
            self.computer_processing = True # Start pause lock
            return True
        else:
            # if no valid set is found, computer adds 3 cards
            if self.deck:
                self.add_cards(min(CARDS_TO_ADD, len(self.deck))) # max 3 cards can be added
                self.message = "No sets found, added 3 cards."
                self.message_color = (0,0,0)  # black color for no set message
                self.message_time = time.time()
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
                # Checks if the games should end, clean the table, makes sure the computer is done with processing the set
                self.clean_up_table() 
                self.check_game_over()
            self.computer_processing = False
            return False

    def update_timer(self):
        #updates the timer and checks if the time is up
        if self.paused:
            return
        
        if self.computer_set_found_time:
            # Wait for the computer to pause to finish
            if time.time() >= self.computer_pause_end:
                # Time to replace cards after showing computer's found set
                self.replace_cards(self.computer_last_set_indices)
                self.computer_last_set_indices = []
                self.computer_set_found_time = None
                self.computer_pause_end = 0
                self.computer_processing = False # Releases the lock

                self.timer_start = time.time() #Resets time to 30 seconds again
                self.time_remaining = TIMER_DURATION
                self.selected_indices.clear()
                self.hint_used = False
                self.hint_cards = []
            else:
                return 
        
        elapsed_time = time.time() - self.timer_start
        self.time_remaining = max(0, TIMER_DURATION - elapsed_time)
        
        if self.time_remaining <= 0 and not self.computer_processing:
            self.computer_turn()  # computer's turn if time is up
         
#!!!!!!!!!!!!!!!
        if not SetAlgorithms.find_one_set(self.table_cards) and not self.deck:
            self.game_over = True # When there are no more possible sets and the deck is empty, the game will end

    def run(self):
        #main game loop
        running = True
        while running:
            self.clock.tick(30) # limits the frame rate to 30 FPS
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keyboard_input(event)
            
            if not self.game_over:
                self.update_timer() # updates the timer and checks if time is up
                self.draw_cards() # draws the cards on the screen
            else:
                self.draw_text(self.message, DISPLAY_WIDTH // 2-100, DISPLAY_HEIGHT//2, self.font, (200,0,0))
                pygame.display.flip()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SetGame()
    game.run()