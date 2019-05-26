import numpy as np

# Players
RED_PLAYER = 1 # True for if's sake
WHITE_PLAYER = 0 # False for if's sake

# Initial game positions
INITIAL_REDS = np.uint32(0xFFF00000)
INITIAL_WHITES = np.uint32(0x00000FFF)
INITIAL_KINGS = np.uint32(0x00000000)
EMPTY_BOARD = np.uint32(0x00000000)

# Bitwise helpers
MSB_SET = np.uint32(0x80000000)

# Names of the pieces
RED_MAN = "Red Man"
RED_KING = "Red King"
WHITE_MAN = "White Man"
WHITE_KING = "White King"

# Unicode codes for the pieces
RED_MAN_UNICODE = "\u26C2"
RED_KING_UNICODE = "\u26C3"
WHITE_MAN_UNICODE = "\u26C0"
WHITE_KING_UNICODE = "\u26C1"

# Color code for the squares
WHITE_COLOR = "#FFFFFF"
BLACK_COLOR = "#000000"

# Path to the pieces' images
RED_MAN_ICON = "../gui/res/red_man.png"
RED_KING_ICON = "../gui/res/red_king.png"
WHITE_MAN_ICON = "../gui/res/white_man.png"
WHITE_KING_ICON = "../gui/res/white_king.png"

