

# Screen dimensions 
CELL_SIZE = 30

# Maze dimensions 
DEFAULT_ROWS = 20
DEFAULT_COLS = 25

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Directions: N, E, S, W
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# Direction vectors (row, col)
DIR_VECTORS = {
    NORTH: (-1, 0),
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1)
}

# Opposite directions
OPPOSITE = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST
}

# Animation speeds (milliseconds)
GENERATION_DELAY = 50
SOLVING_DELAY = 100