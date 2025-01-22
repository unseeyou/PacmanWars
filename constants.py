# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
# Cell Types
WALKABLE_CELL = 'G'         # bot can walk on this cell
OUT_OF_BOUNDS_CELL = 'R'    # this region is not a part of the map
MOUNTAIN_CELL = 'O'         # bot cannot walk on this cell
FOOD_CELL = 'F'             # bot can walk on this cell, but it is a food source
PLAYER_CELL = 'W'           # bot can walk on this cell, but it is another player so they will battle
UNKNOWN_CELL = 'U'          # bot does not know what is in this cell

# Bot movements
MOVE_UP = 0                 # bot moves up
MOVE_DOWN = 1               # bot moves down
MOVE_LEFT = 2               # bot moves left
MOVE_RIGHT = 3              # bot moves right
MOVE_HALT = 4               # bot does not move
MOVEMENTS = {MOVE_UP: (-1, 0), MOVE_DOWN: (1, 0), MOVE_LEFT: (0, -1), MOVE_RIGHT: (0, 1), MOVE_HALT: (0, 0)}

# Bot states
BOT_ALIVE = 1
BOT_DEAD = 0

# =======================================================================================================
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
# Generation of the map
MAX_OUT_OF_BOUND_PROBABILITY = 0.8

# =======================================================================================================
# (YOU CAN CHANGE THESE VALUES)
# Screen dimensions
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 40, 40
CELL_SIZE = WIDTH // COLS

# Define colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

COLOR_MAP = {
    WALKABLE_CELL: GREEN,
    OUT_OF_BOUNDS_CELL: BLACK,
    MOUNTAIN_CELL: RED,
    FOOD_CELL: BLUE,
    PLAYER_CELL: WHITE,
    UNKNOWN_CELL: WHITE
}