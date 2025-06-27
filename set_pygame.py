"""
Welcome to our game SET! 
In order to play the game, all prerequisites must be installed, please consult the manual for more information. 
Then, all that is needed to start the game is to hit the "Run"-button in the top right corner of VScode and enjoy. 

About the file, it contains two classes, which we have positioned together since they are both inherently about the functionality of the game. 
It contains the class for the play button and the whole interface of the game. 
These classes also use functions from other files, so please consult these to get a better understanding of the function.  
"""

# Packages 
import pygame
import random
import time
import sys
from class_card import Card
from class_setalgorithms import SetAlgorithms
from constants_pygame import * 
from stand_alone_code import card_to_filename

# Creates play button
# For the play button we needed to create an individual class
class Play_again_button:
    def __init__(self, CARDWITH, CARDHEIGHT, image_path):
        # Loads the image and defines the size of the image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (600,240))
        # Positions the button on the bottom right of the screen
        self.rect = self.image.get_rect(center = (CARD_WIDTH // 2 + 800, CARD_HEIGHT // 2 + 380))

    def draw(self, screen):
        # Draws the image of the button onto the screen
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        # Detects if the button image is clicked, if yes the game restarts, if not nothing happens
        return self.rect.collidepoint(pos)

class SetGame:
    def __init__(self):
        # Starts the game 
        pygame.init()
        
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption("SET")
        try:
            pygame.display.set_icon(pygame.image.load(ICON_PATH))
        except:
            pass #skip if icon not found
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        self.clock = pygame.time.Clock() # pygame.time.Clock() to control the frame rate
        self.font = pygame.font.SysFont('Arial', 28) 
        self.small_font = pygame.font.SysFont('Arial', 20)
        
        # Game setup
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
        # Message for user feedback
        self.message = ""
        self.message_time = 0
        self.message_color = (0, 0, 0)  # Default color for messages
        self.computer_last_set_indices = [] # Indices of the last set found by the computer
        self.game_over = False
        self.scroll_offset = 0 # For scrolling through cards
        self.computer_pause_end = 0
        self.computer_set_found_time = None # Time when computer finds a set
        self.computer_pause_duration = 3 # 3 seconds pause
        self.computer_processing = False # To make sure that we can continue the game and the computer does not take over
        self.game_over_image = None # Image that is shown when the game has ended
        self.play_again_button = Play_again_button(DISPLAY_WIDTH // 2-100, DISPLAY_HEIGHT // 2+160, "play_again.png")

    # Draws text in the game
    def draw_text(self, text, x, y, font=None, color=(0, 0, 0)):
        # Helps to draw text on the screen at (x,y) position with specified font and color
        if font is None:
            font = self.small_font
        surface = font.render(text, True, (0, 0, 0))
        # Draws the text surface at (x,y) position
        self.screen.blit(surface, (x, y))

    # Calculates the positions of the cards
    def calculate_card_positions(self):
        positions = []
        cards_per_row = min(MAX_CARDS_PER_ROW, len(self.table_cards))  # Ensures we don't exceed the number of cards

        if cards_per_row == 0:
            return positions  # No cards to position
        
        card_spacing = (DISPLAY_WIDTH - (cards_per_row * CARD_WIDTH)) // (cards_per_row + 1)  # Calculates spacing between cards
        card_x = card_spacing
        card_y = 80 + self.scroll_offset  # Below the score/timer and adjusted for scrolling

        # Creates the positions of the cards, with a maximum of 6 cards per row after that limit is reached it puts the cards on the next row
        for i in range(len(self.table_cards)):
            if i > 0 and i % cards_per_row == 0:
                card_x = card_spacing  # Resets x position for the next row
                card_y += CARD_HEIGHT + MARGIN

            positions.append((card_x, card_y))
            card_x += CARD_WIDTH + card_spacing  # Moves to the next card position
        return positions
    
    # Draws the cards on the screen
    def draw_cards(self):
        global pause_switch
        # Draws all cards with proper spacing
        self.screen.fill((200, 200, 200))

        # Draws current score and timer on top left corner
        self.draw_text(f"User Score: {self.user_score}", 20, 10, self.font) # Draws user score on top left corner
        self.draw_text(f"Computer score: {self.computer_score}", 20, 40, self.font) # Draws computer score below user score
        self.draw_text(f"Time: {int(self.time_remaining)}s", DISPLAY_WIDTH - 180, 45, self.font, (255,0,0)) # Draws timer on top right corner
        self.draw_text(f"Cards left: {int(len(self.deck))}", DISPLAY_WIDTH - 180, 15, self.font) # Draws the number of cards left in the deck on the top right corner
        
        #shows pause 
        if self.paused:
            pause_switch = True 
            try: 
                pause_png = pygame.image.load(f"paused_blop.png")
                pause_png = pygame.transform.scale(pause_png, (900, 600))  # Scales the image to fit the card size
                self.screen.blit(pause_png, (10, 5))  # Draws the card image with a small margin 
            except:
                self.draw_text("PAUSED", DISPLAY_WIDTH // 2 -50, DISPLAY_HEIGHT // 2, self.font, (255,0,0))
            
            pygame.display.flip()
            return # Prevents drawing cards and hints while being paused
        else: 
            pause_switch = False
        
        # Draw cards
        positions = self.calculate_card_positions()  # Calculates positions for the cards
        for i, (card_x, card_y) in enumerate(positions):
            if i >= len(self.table_cards):
                break # Ensures we don't exceed the number of cards
            
            if card_y + CARD_HEIGHT > 0 and card_y < DISPLAY_HEIGHT:
                # Only draws cards that are within the visible area of the screen
                card = self.table_cards[i]
                pygame.draw.rect(self.screen, (255, 255, 255), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT))  # Draws white rectangle for the card background
                try:
                    card_img = pygame.image.load(f"{CARD_FOLDER}{card_to_filename(card)}")
                    card_img = pygame.transform.scale(card_img, (CARD_WIDTH - 10, CARD_HEIGHT - 10))  # Scales the image to fit the card size
                    self.screen.blit(card_img, (card_x + 5, card_y + 5))  # Draws the card image with a small margin
                except:
                    # Fallback if image is not found
                    pygame.draw.rect(self.screen, (200, 200, 200), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT))  # Draws a grey rectangle for missing card image
                    self.draw_text(f"Card{i+1}", card_x + 10, card_y + 60, self.small_font)

                # Gives the card a number of its position, to make keyboard use easier for users
                card_number_text = self.small_font.render(str(i+1), True, (0,0,0))
                self.screen.blit(card_number_text, (card_x + 5, card_y +5))

                if i in self.selected_indices:
                    # Draws red rectangle around selected cards
                    pygame.draw.rect(self.screen, (255, 0, 0), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT), 3)
                elif card in self.hint_cards:
                    # Draws green rectangle around hint cards
                    pygame.draw.rect(self.screen, (0, 255, 0), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT), 3)
                # Checks if this is the last set the computer has found and marks the found set blue
                elif i in self.computer_last_set_indices and time.time() < self.computer_pause_end:
                    pygame.draw.rect(self.screen, (0,0,255), (card_x, card_y, CARD_WIDTH, CARD_HEIGHT), 3)

        # Draw instructions on the bottom left
        instructions = [
            "Hint: H | Pause: P | Confirm: Enter", # How to use the hint and pause function, and how to submit your set
            "Select: 1-9 | 0 = 10 | Shift + 1-9 = 11-19", # How to use the keyboard to select cards on the table
            "Scroll: up/down arrow keys", # Scrolls through cards
        ]

        # Shows the instructions above on the screen
        for i, text in enumerate(instructions):
            self.draw_text(text, MARGIN, DISPLAY_HEIGHT - 80 + i * 25, self.small_font)
        
        if self.message and time.time() - self.message_time < MESSAGE_DURATION:
            if isinstance(self.message, pygame.Surface):
                # self.message is an image not text
                self.screen.blit(self.message, (250, 375))  # Draws the card image with a small margin 
            else:
                # self.message is a text
                msg_surface = self.font.render(self.message, True, self.message_color) # Renders the message text
                self.screen.blit(msg_surface, (DISPLAY_WIDTH // 2 - msg_surface.get_width() // 2, DISPLAY_HEIGHT - 30)) # Draws message at the bottom of the screen

        if self.computer_last_set_indices and time.time() < self.computer_pause_end:
            comp_msg = "Computer found set: " + ", ".join(str(i + 1) for i in self.computer_last_set_indices)
            comp_surface = self.small_font.render(comp_msg, True, (200, 0, 0))
            self.screen.blit(comp_surface, (DISPLAY_WIDTH // 2 - comp_surface.get_width() // 2, DISPLAY_HEIGHT - 115)) # Shows the message that the computer has found a set with the number of the cards of the set

        # Updates the screen
        pygame.display.flip()

    # Handles mouseclicks on the screen
    def handle_click(self, pos):
        if self.paused or time.time() < self.computer_pause_end:
            return # Ignores clicks during pauses and computer processing

        if time.time() < self.computer_pause_end:
            return  # Ignore clicks during computer's pause
        
        positions = self.calculate_card_positions()  # Calculates positions for the cards
        for i, (card_x, card_y) in enumerate(positions):
            if i >= len(self.table_cards):
                break

            if card_y + CARD_HEIGHT > 0 and card_y < DISPLAY_HEIGHT:
                # Only checks cards that are within the visible area of the screen
                rect = pygame.Rect(card_x, card_y, CARD_WIDTH, CARD_HEIGHT)
                if rect.collidepoint(pos):
                    # Checks if the mouse click was inside the rectangle of the card
                    if i in self.selected_indices:
                        self.selected_indices.remove(i)
                    else:
                        # If the card is not selected, adds the index to the selected indices
                        if len(self.selected_indices) < 3:
                            self.selected_indices.append(i)
                    if len(self.selected_indices) == 3:
                        # If three cards are selected, calls check_user_set to validate the set
                        self.check_user_set()
                    break

    # Handles input from the keyboard
    def handle_keyboard_input(self,event):
        if event.key == pygame.K_p:
            # Makes sure that you can unpause when being paused even though the system ignores any clicks of the keyboard
            self.toggle_pause()
            return 
        
        if self.paused or time.time() < self.computer_pause_end:
            return # Ignores all other clicks during pauses and computer processing
        
        if time.time() < self.computer_pause_end:
            return  # Ignores keyboard input during computer's pause
        
        if pygame.K_0 <= event.key <= pygame.K_9:
            index = event.key - pygame.K_0 # 0 = 0, 1 = 1, ..., 9 = 9
            if index == 0:
                index = 9 # Maps 0 to 10
            else:
                index -= 1  # Maps 1-9 to 0-8

            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_SHIFT:
                index += 10 # Maps 1-9 to 11-19
            
            self.select_card(index)

        elif event.key == pygame.K_UP:
            # Scrolls up through the cards
            self.scroll_offset = min(0, self.scroll_offset + 20)
        elif event.key == pygame.K_DOWN:
            max_offset = -((len(self.table_cards) // MAX_CARDS_PER_ROW) * (CARD_HEIGHT + MARGIN) - DISPLAY_HEIGHT + 200) # Calculates max scroll offset based on number of cards
            self.scroll_offset = max(max_offset, self.scroll_offset - 20) # Scrolls down through the cards
        
        elif event.key == pygame.K_h:
            # If H is pressed, calls give_hint method
            self.give_hint()
        elif event.key == pygame.K_p:
            # If P is pressed, toggles pause state
            self.toggle_pause()
        elif event.key == pygame.K_RETURN:
            # If Enter is pressed, checks if the selected cards form a valid set
            self.check_user_set()

    # Enter and exit the pause state
    def toggle_pause(self):
        if self.paused:
            pause_duration = time.time() - self.pause_time
            self.timer_start += pause_duration  # Adjusts the timer start to account for the pause duration
        else:
            self.pause_time = time.time()
        self.paused = not self.paused  # Toggles the pause state
    
    # Selects and deselects cards
    def select_card(self, index):
        # Selects a card based on the index, if index is valid
        if index < len(self.table_cards):
            if index in self.selected_indices:
                self.selected_indices.remove(index)
            else:
                if len(self.selected_indices) < 3:
                    self.selected_indices.append(index)
            if len(self.selected_indices) == 3:
                self.check_user_set()  # Checks if the selected cards form a valid set

    # Checks if the three selected cards of the user form a set
    def check_user_set(self):
        # Checks if the selected cards form a valid set
        if len(self.selected_indices) != 3:
            return
        
        cards = [self.table_cards[i] for i in self.selected_indices]
        # *cards unpacks the list into individual card objects
        if SetAlgorithms.is_valid_set(*cards):         
            set_self_img = pygame.image.load(f"set_1point.png")
            set_self_img = pygame.transform.scale(set_self_img, (450, 250))  # Scales the image to fit the card size

            set_hint_img = pygame.image.load(f"set_hint.png")
            set_hint_img = pygame.transform.scale(set_hint_img, (450, 250))  # Scales the image to fit the card size        

            self.message = (set_self_img if not self.hint_used else set_hint_img) # If the hint button is used it displays the image for the hint, if not it won't display anything

            if not self.hint_used:
                self.user_score += 1
            self.replace_cards(self.selected_indices)
            self.timer_start = time.time()  # Resets the timer on valid set
        else:
            self.message = pygame.image.load("Invalid_set.png")
            self.message = pygame.transform.scale(self.message, (570, 270))
            self.screen.blit(self.message, (0, 0))  # Draws the card image with a small margin 
        
        self.message_time = time.time()  # Sets the message time to current time
        self.selected_indices.clear()

        # Makes sure that when a hint is used the user cannot get a point
        if SetAlgorithms.is_valid_set(*cards):
            self.hint_used = False
            self.hint_cards = []
        self.check_game_over()

    # Replaces the cards from the found set with cards from the deck until the deck is empty
    def replace_cards(self, indices):
        indices = sorted(indices, reverse=True)  # Sort indices in reverse order to avoid index errors

        # Checks if it is necessary to replace cards
        replacing = len(self.table_cards) <= INITIAL_CARDS

        for i in indices:
            if i < len(self.table_cards):
                if replacing and self.deck:
                    self.table_cards[i] = self.deck.pop()
                else:
                    self.table_cards.pop(i)
        # Makes sure that there are only cards added when the table is below 12
        if replacing:
            while len(self.table_cards) < INITIAL_CARDS and self.deck:
                self.table_cards.append(self.deck.pop())

    # Adds cards to the table from the deck
    def add_cards(self,count):
        for _ in range(count):
            if self.deck:
                self.table_cards.append(self.deck.pop())

    # Determines the end of the game
    def check_game_over(self):
        if not SetAlgorithms.find_one_set(self.table_cards) and not self.deck:
            self.game_over = True
            self.gameover_text = [f"User: {self.user_score}", f"Computer: {self.computer_score}"]
            self.large_font = pygame.font.SysFont('Arial', 60)

            if self.user_score > self.computer_score:
                winner_image = "gameover_user.png" 
            elif self.user_score < self.computer_score:
                winner_image = "gameover_comp.png"
            else:
                winner_image = "gameover_tie.png" 
            
            # Displays the game over screen according to who wins, which is determined by the final score
            try:
                self.game_over_image = pygame.image.load(winner_image)
                self.game_over_image = pygame.transform.scale(self.game_over_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
            except:
                self.message = "Game Over! Could not load image"
                self.message_color = (255, 0, 0)
                self.message_time = time.time()

    # Gives a hint when hint button has been pressed
    def give_hint(self):
        # Makes sure only two cards are surrounded with a green line 
        if self.hint_cards:
            return
        
        # Provides a hint by finding a valid set and selecting two of its cards
        found_set = SetAlgorithms.find_one_set(self.table_cards)
        if found_set:
            self.hint_cards = random.sample(found_set,2)
            self.hint_used = True        
            hint_img = pygame.image.load("hint_green.png")
            hint_img = pygame.transform.scale(hint_img, (450,250))
            self.message = hint_img
            self.message_time = time.time()  # Sets the message time to current time

    # Turn of the computer
    def computer_turn(self):
        if self.computer_processing:
            return #Don't allow new turns during the pause
        
        # Computer's turn to find a set
        found_set = SetAlgorithms.find_one_set(self.table_cards)
        if found_set and SetAlgorithms.is_valid_set(*found_set):
            self.computer_last_set_indices = [self.table_cards.index(card) for card in found_set]
            self.computer_score += 1
            
            # Shows the image for when computer finds a set
            comp_img = pygame.image.load("set_computer.png")
            comp_img = pygame.transform.scale(comp_img, (450,250))
            self.message = comp_img

            self.message_time = time.time()  # Sets the message time to current time
            self.computer_pause_end = time.time() + COMPUTER_PAUSE  # Sets the pause end time for computer's turn
            self.computer_set_found_time = time.time()
            self.computer_processing = True # Start pause lock for the computer
            return True
        else:
            # If no valid set is found, computer adds 3 cards
            if self.deck:
                self.add_cards(min(CARDS_TO_ADD, len(self.deck))) # Maximum of 3 cards can be added
                added_img = pygame.image.load(f"need_3cards.png")
                added_img = pygame.transform.scale(added_img, (450, 150))
                self.message = added_img
                self.message_time = time.time()

                self.timer_start = time.time() # Makes sure that user gets 30 seconds for their turn after 3 new cards have been added
                self.time_remaining = TIMER_DURATION

                # Checks if the game should end and makes sure the computer is done with processing the set
                self.check_game_over()
            self.computer_processing = False
            return False

    # Timer
    def update_timer(self):
        # Updates the timer and checks if the time is up
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

                self.timer_start = time.time() # Resets time to 30 seconds again
                self.time_remaining = TIMER_DURATION
                self.selected_indices.clear()
                self.hint_used = False
                self.hint_cards = []
                self.check_game_over()
                # Makes sure the game is finished, before adding the game over message
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
            self.computer_turn()  # Computer's turn if time is up
         
        if not SetAlgorithms.find_one_set(self.table_cards) and not self.deck:
            self.game_over = True # When there are no more possible sets on the table and the deck is empty, the game will end

    # Main game loop
    def run(self):
        running = True
        while running:
            self.clock.tick(30) # Limits the frame rate to 30 FPS
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.play_again_button.is_clicked(event.pos):
                            self.__init__() # Makes sure the game is reinitialized
                    continue # Makes sure all input after the game is ingnored

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keyboard_input(event)
            
            if not self.game_over:
                self.update_timer() # Updates the timer and checks if time is up
                self.draw_cards() # Draws the cards on the screen
            else:
                # Screen when the game ends
                self.screen.fill((255,255,255))
                if self.game_over_image:
                    self.screen.blit(self.game_over_image, (0,0)) 
                    for i, text in enumerate(self.gameover_text):
                        self.draw_text(text, DISPLAY_WIDTH/2 - 130, DISPLAY_HEIGHT/2 + 70 + i * 50, self.large_font,(200, 0, 0))
                else:
                    self.draw_text(self.message, DISPLAY_WIDTH // 2-100, DISPLAY_HEIGHT//2, self.font, (200,0,0))
                
                self.play_again_button.draw(self.screen)
                
                pygame.display.flip()
        pygame.quit()
        sys.exit()

# Runs the game
if __name__ == "__main__":
    game = SetGame()
    game.run()