import random
from constants import NORTH, EAST, SOUTH, WEST, DIR_VECTORS


class MazeSolver:
    def __init__(self, maze_generator):
      
        self.maze = maze_generator
        self.rows = maze_generator.rows
        self.cols = maze_generator.cols
        
        # Get start and end positions
        self.start, self.end = maze_generator.get_start_end_positions()
        
        # Solver state
        self.stack = []
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.dead_ends = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_pos = self.start
        self.complete = False
        self.found = False
        
    def reset(self):
       
        self.stack = []
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.dead_ends = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_pos = self.start
        self.complete = False
        self.found = False
        
    def get_available_moves(self, row, col):
      
        moves = []
        
        # North
        if row > 0 and self.maze.northWall[row][col] == 0:
            moves.append((row - 1, col))
        
        # South (check north wall of cell below)
        if row < self.rows - 1 and self.maze.northWall[row + 1][col] == 0:
            moves.append((row + 1, col))
        
        # East
        if col < self.cols - 1 and self.maze.eastWall[row][col] == 0:
            moves.append((row, col + 1))
        
        # West (check east wall of cell to left)
        if col > 0 and self.maze.eastWall[row][col - 1] == 0:
            moves.append((row, col - 1))
        
        return moves
    
    def solve_step(self):
       
        if self.complete:
            return (True, self.found, self.current_pos)
        
        row, col = self.current_pos
        
        # Check if we reached the end
        if (row, col) == self.end:
            self.complete = True
            self.found = True
            return (True, True, self.current_pos)
        
        # Mark current as visited
        self.visited[row][col] = True
        
        # Get all unvisited moves
        available_moves = []
        for next_row, next_col in self.get_available_moves(row, col):
            if not self.visited[next_row][next_col] and not self.dead_ends[next_row][next_col]:
                available_moves.append((next_row, next_col))
        
        if available_moves:
            # Choose random direction
            next_row, next_col = random.choice(available_moves)
            
            # Push current to stack
            self.stack.append((row, col))
            
            # Move to next cell
            self.current_pos = (next_row, next_col)
            
            return (False, False, self.current_pos)
        elif self.stack:
            # Dead end - mark as blue
            self.dead_ends[row][col] = True
            
            # Backtrack
            self.current_pos = self.stack.pop()
            
            return (False, False, self.current_pos)
        else:
            # No path found
            self.complete = True
            self.found = False
            return (True, False, self.current_pos)