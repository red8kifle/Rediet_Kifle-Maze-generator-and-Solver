

import pygame
import sys
from constants import *
from maze_generator import MazeGenerator
from maze_solver import MazeSolver


class MazeGame:
    def __init__(self, rows=DEFAULT_ROWS, cols=DEFAULT_COLS):
        
        pygame.init()
        
        self.rows = rows
        self.cols = cols
        
        # Calculate window size 
        self.cell_size = CELL_SIZE
        self.window_width = self.cell_size * cols
        self.window_height = self.cell_size * rows
        
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Maze Generator and Solver")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        
        # Initialize maze components
        self.maze_generator = MazeGenerator(rows, cols)
        self.maze_solver = None
        
        # Game state
        self.state = "GENERATING"  # GENERATING, SOLVING, COMPLETE
        self.auto_mode = True
        self.generation_timer = 0
        self.solving_timer = 0
        
        # Start and end positions
        self.start_pos = None
        self.end_pos = None
        
        # Start generation
        self.start_generation()
        
    def start_generation(self):
       
        self.maze_generator.reset()
        self.state = "GENERATING"
        
    def start_solving(self):
       
        self.maze_solver = MazeSolver(self.maze_generator)
        self.maze_solver.reset()
        self.state = "SOLVING"
        
    def reset_maze(self):
       
        self.start_generation()
        
    def draw_cell(self, row, col, is_current=False, is_dead_end=False):
        
        x = col * self.cell_size
        y = row * self.cell_size
        
        # Fill cell background
        if is_current:
            color = RED
        elif is_dead_end:
            color = BLUE
        else:
            color = WHITE
            
        pygame.draw.rect(self.window, color, (x, y, self.cell_size, self.cell_size))
        
        # Draw north wall
        if self.maze_generator.northWall[row][col]:
            pygame.draw.line(
                self.window, BLACK,
                (x, y), (x + self.cell_size, y), 2
            )
        
        # Draw east wall
        if self.maze_generator.eastWall[row][col]:
            pygame.draw.line(
                self.window, BLACK,
                (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2
            )
        
        # Draw south wall (if last row or if cell below has north wall)
        if row == self.rows - 1 or self.maze_generator.northWall[row + 1][col]:
            pygame.draw.line(
                self.window, BLACK,
                (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 2
            )
        
        # Draw west wall (if first col or if cell to left has east wall)
        if col == 0 or self.maze_generator.eastWall[row][col - 1]:
            pygame.draw.line(
                self.window, BLACK,
                (x, y), (x, y + self.cell_size), 2
            )
        
        # Draw start marker (green circle on left edge)
        if self.start_pos and (row, col) == self.start_pos:
            pygame.draw.circle(
                self.window, GREEN,
                (x + 5, y + self.cell_size // 2),
                self.cell_size // 5
            )
        
        # Draw end marker (orange circle on right edge)
        if self.end_pos and (row, col) == self.end_pos:
            pygame.draw.circle(
                self.window, ORANGE,
                (x + self.cell_size - 5, y + self.cell_size // 2),
                self.cell_size // 5
            )
    
    def draw_maze(self, current_pos=None, dead_ends=None):
        
        # Get positions from solver if in solving mode
        if self.state == "SOLVING" and self.maze_solver:
            current_pos = current_pos or self.maze_solver.current_pos
            dead_ends = dead_ends or self.maze_solver.dead_ends
            self.start_pos = self.maze_solver.start
            self.end_pos = self.maze_solver.end
        elif self.state in ["GENERATING", "COMPLETE"]:
            self.start_pos, self.end_pos = self.maze_generator.get_start_end_positions()
        
        # Draw all cells
        for row in range(self.rows):
            for col in range(self.cols):
                is_current = (current_pos == (row, col)) if current_pos else False
                is_dead_end = dead_ends[row][col] if dead_ends else False
                self.draw_cell(row, col, is_current, is_dead_end)
    
    def draw_status(self):
       
        if self.state == "GENERATING":
            text = "Generating maze... Press SPACE to reset, S to solve when done"
        elif self.state == "SOLVING":
            text = "Solving... Red=current, Blue=dead end"
        elif self.state == "COMPLETE":
            text = "Complete! Press SPACE for new maze, S to solve"
        else:
            text = "Press SPACE to reset, S to solve"
        
        status = self.font.render(text, True, BLACK)
        status_rect = status.get_rect(center=(self.window_width // 2, self.window_height - 10))
        
        # Draw background for text
        pygame.draw.rect(self.window, WHITE, (0, self.window_height - 25, self.window_width, 25))
        self.window.blit(status, status_rect)
    
    def update_generation(self):
        """Update the maze generation process"""
        if self.state != "GENERATING":
            return
        
        result = self.maze_generator.generate_step()
        
        if result is None:
            return
        
        is_complete, current_pos = result
        
        if is_complete:
            self.state = "COMPLETE"
    
    def update_solving(self):
        """Update the maze solving process"""
        if self.state != "SOLVING" or not self.maze_solver:
            return
        
        result = self.maze_solver.solve_step()
        is_complete, found, current_pos = result
        
        if is_complete:
            self.state = "COMPLETE"
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.reset_maze()
                elif event.key == pygame.K_s:
                    if self.state == "COMPLETE":
                        self.start_solving()
        
        return True
    
    def run(self):
        """Main game loop"""
        running = True
        last_update = pygame.time.get_ticks()
        
        while running:
            running = self.handle_events()
            
            current_time = pygame.time.get_ticks()
            
            # Auto-update based on mode
            if self.auto_mode:
                if self.state == "GENERATING" and current_time - last_update > GENERATION_DELAY:
                    self.update_generation()
                    last_update = current_time
                elif self.state == "SOLVING" and current_time - last_update > SOLVING_DELAY:
                    self.update_solving()
                    last_update = current_time
            
            # Draw everything
            self.window.fill(WHITE)
            
            if self.state == "SOLVING" and self.maze_solver:
                self.draw_maze(
                    current_pos=self.maze_solver.current_pos,
                    dead_ends=self.maze_solver.dead_ends
                )
            else:
                current = self.maze_generator.current_cell if self.state == "GENERATING" else None
                self.draw_maze(current_pos=current)
            
            self.draw_status()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


def main():
    """Main entry point"""
    rows = DEFAULT_ROWS
    cols = DEFAULT_COLS
    
    if len(sys.argv) > 2:
        try:
            rows = int(sys.argv[1])
            cols = int(sys.argv[2])
        except ValueError:
            print("Usage: python main.py [rows] [cols]")
    
    game = MazeGame(rows, cols)
    game.run()


if __name__ == "__main__":
    main()