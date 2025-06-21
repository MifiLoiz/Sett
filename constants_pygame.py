## Constants 

"""
In this file we have put some constants we will use in other parts of the code. 

Under the section "Time", the user can adjust playtime and message duration to enhance their gaming experience. 
Beware, for changing message duration, it is important to set both MESSAGE_DURATION and COMPUTER_PAUSE must be set to the same amount of time! 
Make sure that all durations must be at least 1 second.  
"""

# Time 
TIMER_DURATION = 30         # seconds
MESSAGE_DURATION = 3        # seconds for message display
COMPUTER_PAUSE = 3          #seconds to pause after computer finds set

# Layout 
CARD_WIDTH = 100
CARD_HEIGHT = 150
MAX_CARDS_PER_ROW = 6
MARGIN = 15
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 600

# Game settings
ICON_PATH = "SET_FamilyGames_digital-1.png"
CARDS_TO_ADD = 3            # number of cards to add when no set is found
CARD_FOLDER = "kaarten/"
INITIAL_CARDS = 12          # initial number of cards on the table
