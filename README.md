# Name: Rediet Kifle

# Id: UGR/8926/16

# section 2

# Maze Generator and Solver

A Python implementation of a maze generator and solver using a stack-based DFS "mouse" algorithm, built with Pygame.
Description
This program generates a random, proper rectangular maze of R rows and C columns — meaning every cell is connected by a unique path to every other cell — and then finds and displays a path from the start cell to the end cell using a backtracking algorithm. The maze is built and solved step-by-step with live animation so you can watch the mouse eat through walls and navigate to the goal.

# Features

. Proper Maze Generation — Every cell is reachable from every other cell via a unique path (no isolated regions)
. Stack-Based DFS Mouse — An invisible mouse eats through walls using iterative DFS, carving the maze one step at a time
. Animated Generation — Watch the maze form in real time as walls are removed cell by cell
. Backtracking Solver — The mouse navigates the maze with full visual feedback:

    Red — current mouse position
    Blue — dead-end cells the mouse has abandoned
    Green — start cell (left edge)
    Orange — goal cell (right edge)

. Customizable Dimensions — Pass rows and cols as command-line arguments or edit the defaults in constants.py

# Data Structures

The maze is represented using two 2D arrays:

    northWall[R][C] # 1 if the cell's north wall is intact, 0 if removed
    eastWall[R][C] # 1 if the cell's east wall is intact, 0 if removed

# Wall logic:

. northWall[i][j] == 1 → the top wall of cell (i, j) is solid
. South wall of cell (i, j) is the north wall of cell (i+1, j): northWall[i+1][j]
. West wall of cell (i, j) is the east wall of the cell to its left: eastWall[i][j-1]
. The zeroth row's north walls form the bottom edge of the maze
. eastWall[i][0] controls gaps along the left edge of the maze

# How It Works

Maze Generation (maze_generator.py)
All walls start intact. The DFS mouse then carves paths step by step:

1.Place the mouse at a random starting cell and mark it visited
2.Find all four neighbors (N, E, S, W) that are within bounds and unvisited
3.Randomly choose one unvisited neighbor
4.Eat through the connecting wall (northWall or eastWall set to 0)
5.Push the current cell onto the stack and move to the chosen neighbor
6.If no unvisited neighbors exist (dead end), pop from the stack and backtrack
7.Repeat until the stack is empty — every cell has been visited

The result is a spanning tree over all cells, guaranteeing a unique path between any two cells (a proper maze).

# Eating a wall — direction logic:

    NORTH → northWall[row][col] = 0
    SOUTH → northWall[row + 1][col] = 0 # south wall = north wall of cell below
    EAST → eastWall[row][col] = 0
    WEST → eastWall[row][col - 1] = 0 # west wall = east wall of cell to left

# Stack vs Queue?

The stack produces deep, winding DFS corridors with long passages. A queue (BFS) would instead produce many short branches radiating outward from the start — a wider but shallower maze where all paths stay roughly the same length from the origin.

# Maze Solving (maze_solver.py)

The solver uses a randomized backtracking algorithm:

1.Start the mouse at the start cell (left edge, random row)
2.Mark current cell as visited
3.Collect all valid moves — adjacent cells reachable through an open wall that are neither visited nor marked as dead ends
4.Randomly choose a valid move, push current cell onto the path stack, and move forward
5.If no valid moves exist (dead end), mark the current cell blue (dead_ends[row][col] = True) and pop the stack to backtrack
6.Continue until the mouse reaches the end cell (right edge, random row) or the stack empties (no solution)

# Checking open walls:

    North: northWall[row][col] == 0
    South: northWall[row + 1][col] == 0
    East: eastWall[row][col] == 0
    West: eastWall[row][col - 1] == 0

# Controls

# Key **\***Action

    SPACE: Generate a new maze
    S: Start solving (after generation completes)
    ESC: Quit

# Running the Program

    pip install pygame
    python main.py # default 20x25 maze
    python main.py 15 20 # custom 15 rows x 20 cols

# Defaults can also be changed in constants.py:

    DEFAULT_ROWS = 20
    DEFAULT_COLS = 25
    CELL_SIZE = 30
    GENERATION_DELAY = 50 # ms per generation step
    SOLVING_DELAY = 100 # ms per solving step

# Project Structure

    main.py # Entry point and Pygame game loop
    maze_generator.py # Stack-based DFS maze generation (northWall / eastWall)
    maze_solver.py # Backtracking solver with dead-end marking
    constants.py # Colors, directions, animation delays, defaults
