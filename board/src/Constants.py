import numpy as np

# Initial game positions
RED = np.uint32(0xFFF00000, dtype=np.uint32)
WHITE = np.uint32(0x00000FFF, dtype=np.uint32)
KINGS = np.uint32(0x00000000, dtype=np.uint32)

# Unicode codes for the pieces
RED_MAN = "\u26C2"
RED_KING = "\u26C3"
WHITE_MAN = "\u26C0"
WHITE_KING = "\u26C1"
