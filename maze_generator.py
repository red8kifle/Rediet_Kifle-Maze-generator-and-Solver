

import random
from constants import NORTH, EAST, SOUTH, WEST, DIR_VECTORS, OPPOSITE


class MazeGenerator:
    def __init__(self, rows, cols):
      
        self.rows = rows
        self.cols = cols
        
        # Initialize all walls as intact (1 = wall present)
        self.northWall = [[1 for _ in range(cols)] for _ in range(rows)]
        self.eastWall = [[1 for _ in range(cols)] for _ in range(rows)]
        
        # Visited tracking
        self.visited = [[False for _ in range(cols)] for _ in range(rows)]
        
        # For animation
        self.stack = []
        self.current_cell = None
        
    def reset(self):
       
        self.northWall = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.eastWall = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.stack = []
        self.current_cell = None
    
    def get_unvisited_neighbors(self, row, col):
      
        neighbors = []
        
        for direction in [NORTH, EAST, SOUTH, WEST]:
            dr, dc = DIR_VECTORS[direction]
            new_row, new_col = row + dr, col + dc
            
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                if not self.visited[new_row][new_col]:
                    neighbors.append((new_row, new_col, direction))
        
        return neighbors
    
    def eat_wall(self, row, col, direction):
      
        if direction == NORTH:
            self.northWall[row][col] = 0  # Remove north wall of current
        elif direction == SOUTH:
            self.northWall[row + 1][col] = 0  # Remove north wall of cell below
        elif direction == EAST:
            self.eastWall[row][col] = 0  # Remove east wall of current
        elif direction == WEST:
            self.eastWall[row][col - 1] = 0  # Remove east wall of cell to left
    
    def generate_step(self):
     
        # Initialize if just starting
        if self.current_cell is None:
            start_row = random.randint(0, self.rows - 1)
            start_col = random.randint(0, self.cols - 1)
            self.current_cell = (start_row, start_col)
            self.visited[start_row][start_col] = True
            return (False, self.current_cell)
        
        row, col = self.current_cell
        neighbors = self.get_unvisited_neighbors(row, col)
        
        if neighbors:
            # Choose random unvisited neighbor
            new_row, new_col, direction = random.choice(neighbors)
            
            # Eat the wall between them
            self.eat_wall(row, col, direction)
            
            # Push current cell to stack
            self.stack.append((row, col))
            
            # Move to new cell
            self.current_cell = (new_row, new_col)
            self.visited[new_row][new_col] = True
            
            return (False, self.current_cell)
        elif self.stack:
            # Backtrack - pop from stack
            self.current_cell = self.stack.pop()
            return (False, self.current_cell)
        else:
            # Generation complete
            return (True, None)
    
    def get_start_end_positions(self):
      
        start_row = random.randint(0, self.rows - 1)
        start_col = 0
        end_row = random.randint(0, self.rows - 1)
        end_col = self.cols - 1
        return (start_row, start_col), (end_row, end_col)