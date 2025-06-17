## the game

import pygame
import random
import time
import sys
from class_card import Card
from class_setalgorithms import SetAlgorithms
from constants_pygame import * 
from stand_alone_code import card_to_filename

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
        self.computer_set_found_time = None # time when computer finds a set
        self.computer_pause_duration = 3 #3 seconds pause
        self.computer_processing = False #To make sure that we can continue the game and the computer does not take over
        self.game_over_image = None #Image that is shown when the game has ended

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
        global pause_switch
        #draw all cards with proper spacing
        self.screen.fill((200, 200, 200))

        #draws current score and timer on top left corner
        self.draw_text(f"User Score: {self.user_score}", 20, 10, self.font) #draws user score on top left corner
        self.draw_text(f"Computer score: {self.computer_score}", 20, 40, self.font) #draws computer score below user score
        self.draw_text(f"Time: {int(self.time_remaining)}s", DISPLAY_WIDTH - 160, 45, self.font, (255,0,0)) #draws timer on top right corner
        self.draw_text(f"Cards left: {int(len(self.deck))}", DISPLAY_WIDTH - 160, 15, self.font)
        
        #shows pause 
        if self.paused:
            pause_switch = True 
            try: 
            ## ELIZA WAS HERE: works!! 
                pause_png = pygame.image.load(f"paused_blop.png")
                pause_png = pygame.transform.scale(pause_png, (900, 600))  # scales the image to fit the card size
                self.screen.blit(pause_png, (10, 5))  # draws the card image with a small margin 
            except:
                self.draw_text("PAUSED", DISPLAY_WIDTH // 2 -50, DISPLAY_HEIGHT // 2, self.font, (255,0,0))
            
            pygame.display.flip()
            return # Prevents drawing cards and hints while being paused
        else: 
            pause_switch = False
        
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

                # Gives the card a number of its position, to make keyboard use easier for users
                card_number_text = self.small_font.render(str(i+1), True, (0,0,0))
                self.screen.blit(card_number_text, (card_x + 5, card_y +5))

                if i in self.selected_indices:
                    # draws red rectangle around selected cards
                    pygame.draw.rect(self.screen, (255, 0, 0), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT), 3)
                elif card in self.hint_cards:
                    # draws green rectangle around hint cards
                    pygame.draw.rect(self.screen, (0, 255, 0), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT), 3)
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

## ELIZA WAS HERE - dit moet goed worden 
## !!!!!!Anouk was here - dit werkt nu ook, ik heb zegmaar if, else conditie toegeoegt
# Hij crashde volgensmij omdat hij niet wist hoe hij verschil tussen image en tekst moest detecten
        if self.message and time.time() - self.message_time < MESSAGE_DURATION:
            if isinstance(self.message, pygame.Surface):
                # Self.message is an image not text
                self.screen.blit(self.message, (250, 375))  # draws the card image with a small margin 
            else:
                # Self.message is a text
                msg_surface = self.font.render(self.message, True, self.message_color) # renders the message text
                self.screen.blit(msg_surface, (DISPLAY_WIDTH // 2 - msg_surface.get_width() // 2, DISPLAY_HEIGHT - 30)) # draws message at the bottom of the screen

        if self.computer_last_set_indices and time.time() < self.computer_pause_end:
            comp_msg = "Computer found set: " + ", ".join(str(i + 1) for i in self.computer_last_set_indices)
            comp_surface = self.small_font.render(comp_msg, True, (200, 0, 0))
            self.screen.blit(comp_surface, (DISPLAY_WIDTH // 2 - comp_surface.get_width() // 2, DISPLAY_HEIGHT - 115))

        #updates the screen
        pygame.display.flip()

    def handle_click(self, pos):
        if self.paused or time.time() < self.computer_pause_end:
            return # Ignores clicks during pauses and computer processing

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
        if event.key == pygame.K_p:
            # Makes sure that you can unpause when being paused even though the system ignores any clicks of the keyboard
            self.toggle_pause()
            return 
        
        if self.paused or time.time() < self.computer_pause_end:
            return # Ignores all other clicks during pauses and computer processing
        
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
            set_self_img = pygame.image.load(f"set_1point.png")
            set_self_img = pygame.transform.scale(set_self_img, (450, 250))  # scales the image to fit the card size
            #self.screen.blit(set_self_img, (250, 375))  # draws the card image with a small margin 

            set_hint_img = pygame.image.load(f"set_hint.png")
            set_hint_img = pygame.transform.scale(set_hint_img, (450, 250))  # scales the image to fit the card size
            #self.screen.blit(set_hint_img, (250, 375))  # draws the card image with a small margin             

            self.message = (set_self_img if not self.hint_used else set_hint_img)
            #self.message_color = (255, 105, 189) # pink color for valid set message

            if not self.hint_used:
                self.user_score += 1
            self.replace_cards(self.selected_indices)
#!!!!!!!!!!!!!!Anouk was here
            self.clean_up_table()
            self.timer_start = time.time()  # resets the timer on valid set
        else:
            self.message = "Not a valid SET!"
            self.message_color = (255, 0, 0)  # red color for invalid set message
        
        self.message_time = time.time()  # sets the message time to current time
        self.selected_indices.clear()
# !!!!!!!!!! Anouk was here
# Dit was die hint issue die ik heb gestuurd in de groepsapp
        # Makes sure that when a hint is used the user cannot get a point
        if SetAlgorithms.is_valid_set(*cards):
            self.hint_used = False
            self.hint_cards = []
        self.check_game_over()

    def replace_cards(self, indices):
        indices = sorted(indices, reverse=True)  # sort indices in reverse order to avoid index errors

# Checks if it is necessary to replace or remove cards
        replacing = len(self.table_cards) <= INITIAL_CARDS

        for i in indices:
            if i < len(self.table_cards):
                if replacing and self.deck:
                    self.table_cards[i] = self.deck.pop()
                else:
                    self.table_cards.pop(i)
#!!!!!!!!!!!!!Anouk was here
# Removed the while loop for an if while loop, so that it does not keep adding cards constantly
# Makes sure that there are only cards added when the table is below 12
        if replacing:
            while len(self.table_cards) < INITIAL_CARDS and self.deck:
                self.table_cards.append(self.deck.pop())        
        self.clean_up_table()

    def add_cards(self,count):
        for _ in range(count):
            if self.deck:
                self.table_cards.append(self.deck.pop())
    
    # Removes the first three cards of the cards on the table when there are more than 12 cards, thus when new cards have been added
    def remove_top_cards(self, count):
        if len(self.table_cards) > count:
            self.table_cards = self.table_cards[count:]

    # Removes cards in sets of three until there are only 12 crads   
    def clean_up_table(self):
        while len(self.table_cards) > INITIAL_CARDS and not SetAlgorithms.find_one_set(self.table_cards):
            self.remove_top_cards(CARDS_TO_ADD)

    # Determines the end of the game
    # We need to add a gelijkspel image still
    def check_game_over(self):
        if not SetAlgorithms.find_one_set(self.table_cards) and not self.deck:
            self.game_over = True

            if self.user_score > self.computer_score:
                winner_image = "gameover_user.png" 
            elif self.user_score < self.computer_score:
                winner_image = "gameover_comp.png"
            else:
                winner_image = "gameover_tie.png" # STILL NEED TO ADD THIS IMAGE
            
            try:
                self.game_over_image = pygame.image.load(winner_image)
                self.game_over_image = pygame.transform.scale(self.game_over_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
            except:
                self.message = "Game Over! Could not load image"
                self.message_color = (255, 0, 0)
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
            
            # Shows the image for when computer finds a set
            comp_img = pygame.image.load("set_computer.png")
            comp_img = pygame.transform.scale(comp_img, (450,250))
            self.message = comp_img

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

                self.timer_start = time.time() # Makes sure that user get 30 second for their turn after 3 new added cards
                self.time_remaining = TIMER_DURATION

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
#!!!!!!!!!!!!!!!Anouk was here
                self.clean_up_table()
                self.computer_last_set_indices = []
                self.computer_set_found_time = None
                self.computer_pause_end = 0
                self.computer_processing = False # Releases the lock

                self.timer_start = time.time() #Resets time to 30 seconds again
                self.time_remaining = TIMER_DURATION
                self.selected_indices.clear()
                self.hint_used = False
                self.hint_cards = []
                self.check_game_over()
                # Makes sure the game if finished, before adding the game over message
                if not self.computer_processing and not self.computer_set_found_time:
                    if not SetAlgorithms.find_one_set(self.table_cards) and not self.deck:
                        self.game_over = True
                        self.message = "Game Over!"
                        self.message_color = (50,50,50)
                        self.message_time = time.time()
            else:
                return 
        
        elapsed_time = time.time() - self.timer_start
        self.time_remaining = max(0, TIMER_DURATION - elapsed_time)
        
        if self.time_remaining <= 0 and not self.computer_processing:
            self.computer_turn()  # computer's turn if time is up
         
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
                if self.game_over:
                    continue #Makes sure all input after the game is ingnored

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keyboard_input(event)
            
            if not self.game_over:
                self.update_timer() # updates the timer and checks if time is up
                self.draw_cards() # draws the cards on the screen
            else:
                # Screen when the game ends
                self.screen.fill((0,0,0))
                if self.game_over_image:
                    self.screen.blit(self.game_over_image, (0,0))
                else:
                    self.draw_text(self.message, DISPLAY_WIDTH // 2-100, DISPLAY_HEIGHT//2, self.font, (200,0,0))
                pygame.display.flip()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SetGame()
    game.run()