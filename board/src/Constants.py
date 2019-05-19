import numpy as np

# Players
RED_PLAYER = 1 # True for if's sake
WHITE_PLAYER = 0 # False for if's sake

# Initial game positions
RED = np.uint32(0xFFF00000)
WHITE = np.uint32(0x00000FFF)
KINGS = np.uint32(0x00000000)
EMPTY_BOARD = np.uint32(0x00000000)

# Unicode codes for the pieces
RED_MAN = "\u26C2"
RED_KING = "\u26C3"
WHITE_MAN = "\u26C0"
WHITE_KING = "\u26C1"
