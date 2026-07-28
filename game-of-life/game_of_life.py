import random

PATTERNS = {
    "Glider":     [(0,1),(1,2),(2,0),(2,1),(2,2)],
    "Blinker":    [(0,0),(0,1),(0,2)],
    "Toad":       [(0,1),(0,2),(0,3),(1,0),(1,1),(1,2)],
    "Beacon":     [(0,0),(0,1),(1,0),(2,3),(3,2),(3,3)],
    "Pulsar":     [(0,2),(0,3),(0,4),(0,8),(0,9),(0,10),
                   (2,0),(2,5),(2,7),(2,12),
                   (3,0),(3,5),(3,7),(3,12),
                   (4,0),(4,5),(4,7),(4,12),
                   (5,2),(5,3),(5,4),(5,8),(5,9),(5,10),
                   (7,2),(7,3),(7,4),(7,8),(7,9),(7,10),
                   (8,0),(8,5),(8,7),(8,12),
                   (9,0),(9,5),(9,7),(9,12),
                   (10,0),(10,5),(10,7),(10,12),
                   (12,2),(12,3),(12,4),(12,8),(12,9),(12,10)],
    "R-pentomino":[(0,1),(0,2),(1,0),(1,1),(2,1)],
}

class GameOfLife:

    def __init__(self, rows, cols):

        self.rows = rows   #store dimensions so other methods can reference them without needing
                           # parameters passed in every time.
        self.cols = cols
        self.grid = [[0] * cols for _ in range(rows)] # 2D list of all dead cells.The list comprehension creates

        for l in self.grid:                                              # rows separate row lists, each containing cols zeros.
            print(l)
        self.generation = 0

    def randomise(self):

        self.grid = [[random.choice([0, 0, 0, 1]) for _ in range(self.cols)] # 25% chance of hitting 1
                     for _ in range(self.rows)]
        self.generation = 0

    def count_neighbours(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r = (row + dr) % self.rows  # wraps edges
                c = (col + dc) % self.cols
                count += self.grid[r][c]
        return count

    def step(self):

        # YOUR JOB: build next_grid using the 4 Conway rules, then assign to self.grid
        # Rule 1: live cell with <2 neighbours → dies
        # Rule 2: live cell with 2 or 3 neighbours → survives
        # Rule 3: live cell with >3 neighbours → dies
        # Rule 4: dead cell with exactly 3 neighbours → becomes alive

        new_grid = [[0] * self.cols for _ in range(self.rows)]  # fresh empty grid

        for row in range(self.rows):
            for col in range(self.cols):

                neighbours = self.count_neighbours(row,col)
                alive = self.grid[row][col]

                if alive: # checks if it's 1 = truthy

                    if neighbours <2:
                        new_grid[row][col] = 0

                    elif neighbours in (2,3):
                        new_grid[row][col] = 1

                    else:
                        new_grid[row][col] = 0

                else:
                    if neighbours ==3:
                        new_grid[row][col] = 1

        self.grid = new_grid
        self.generation +=1


    def place_pattern(self, pattern, center_row, center_col):
        for dr, dc in pattern:
            r = (center_row + dr) % self.rows
            c = (center_col + dc) % self.cols
            self.grid[r][c] = 1

    def empty_grid(self):
        return [[0] * self.cols for _ in range(self.rows)]