# SPECIFICATION:
#
# check_sudoku() determines whether its argument is a valid Sudoku
# grid. It can handle grids that are completely filled in, and also
# grids that hold some empty cells where the player has not yet
# written numbers.
#
# First, your code must do some sanity checking to make sure that its
# argument:
#
# - is a 9x9 list of lists
#
# - contains, in each of its 81 elements, an integer in the range 0..9
#
# If either of these properties does not hold, check_sudoku must
# return None.
#
# If the sanity checks pass, your code should return True if all of
# the following hold, and False otherwise:
#
# - each number in the range 1..9 occurs only once in each row 
#
# - each number in the range 1..9 occurs only once in each column
#
# - each number the range 1..9 occurs only once in each of the nine
#   3x3 sub-grids, or "boxes", that make up the board
#
# This diagram (which depicts a valid Sudoku grid) illustrates how the
# grid is divided into sub-grids:
#
# 5 3 4 | 6 7 8 | 9 1 2
# 6 7 2 | 1 9 5 | 3 4 8
# 1 9 8 | 3 4 2 | 5 6 7 
# ---------------------
# 8 5 9 | 7 6 1 | 4 2 3
# 4 2 6 | 8 5 3 | 7 9 1
# 7 1 3 | 9 2 4 | 8 5 6
# ---------------------
# 9 6 1 | 5 3 7 | 0 0 0
# 2 8 7 | 4 1 9 | 0 0 0
# 3 4 5 | 2 8 6 | 0 0 0
# 
# Please keep in mind that a valid grid (i.e., one for which your
# function returns True) may contain 0 multiple times in a row,
# column, or sub-grid. Here we are using 0 to represent an element of
# the Sudoku grid that the player has not yet filled in.

import math
import copy
from collections import defaultdict


# check_sudoku should return None
ill_formed = [[5,3,4,6,7,8,9,1,2],
              [6,7,2,1,9,5,3,4,8],
              [1,9,8,3,4,2,5,6,7],
              [8,5,9,7,6,1,4,2,3],
              [4,2,6,8,5,3,7,9],  # <---
              [7,1,3,9,2,4,8,5,6],
              [9,6,1,5,3,7,2,8,4],
              [2,8,7,4,1,9,6,3,5],
              [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return True
valid = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,8],
         [1,9,8,3,4,2,5,6,7],
         [8,5,9,7,6,1,4,2,3],
         [4,2,6,8,5,3,7,9,1],
         [7,1,3,9,2,4,8,5,6],
         [9,6,1,5,3,7,2,8,4],
         [2,8,7,4,1,9,6,3,5],
         [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return False
invalid = [[5,3,4,6,7,8,9,1,2],
           [6,7,2,1,9,5,3,4,8],
           [1,9,8,3,8,2,5,6,7],
           [8,5,9,7,6,1,4,2,3],
           [4,2,6,8,5,3,7,9,1],
           [7,1,3,9,2,4,8,5,6],
           [9,6,1,5,3,7,2,8,4],
           [2,8,7,4,1,9,6,3,5],
           [3,4,5,2,8,6,1,7,9]]

# check_sudoku should return True
easy = [[2,9,0,0,0,0,0,7,0],
        [3,0,6,0,0,8,4,0,0],
        [8,0,0,0,4,0,0,0,2],
        [0,2,0,0,3,1,0,0,7],
        [0,0,0,0,8,0,0,0,0],
        [1,0,0,9,5,0,0,6,0],
        [7,0,0,0,9,0,0,0,1],
        [0,0,1,2,0,0,3,0,6],
        [0,3,0,0,0,0,0,5,9]]

# check_sudoku should return True
hard = [[1,0,0,0,0,7,0,9,0],
        [0,3,0,0,2,0,0,0,8],
        [0,0,9,6,0,0,5,0,0],
        [0,0,5,3,0,0,9,0,0],
        [0,1,0,0,8,0,0,0,2],
        [6,0,0,0,0,4,0,0,0],
        [3,0,0,0,0,0,0,1,0],
        [0,4,0,0,0,0,0,0,7],
        [0,0,7,0,0,0,3,0,0]]



def nums_unique_per_subgrid(grid):
    unique_sets = {}

    def insert_unique_value(unique_sets, set_id, value):
        if set_id not in unique_sets:
            unique_sets[set_id] = []
        
        if value in unique_sets[set_id]:
            return False
        
        unique_sets[set_id].append(value)
        return True

    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            value = grid[row_index][col_index]

            if value == 0:
                continue

            set_id = make_subgrid_id(row_index, col_index)
            result = insert_unique_value(unique_sets, set_id, value)
            
            if not result:
                return False 
    
    return True



def nums_unique_per_row(grid):
    for row in grid:
        seen = []

        for col in row: 
            if col == 0:
                continue

        if col in seen:
            return False

        seen.append(col)

    return True


def nums_unique_per_column(grid):
    for x in range(0, 9):
        seen = []

        for row in grid:
            if row[x] == 0:
                continue 

            if row[x] in seen:
                return False

            seen.append(row[x])
    
    return True


def is_9x9_grid(grid):
    if len(grid) != 9:
        return False 

    for row in grid:
        if len(row) != 9:
            return False 
    
    return True 


def contains_only_0_to_9(grid):
    for row in grid:
        for col in row:
            if not isinstance(col, int):
                return False 
            if col < 0 or col > 9:
                return False 
    
    return True 


def check_sudoku(grid):
    if not is_9x9_grid(grid):
        return None 

    if not contains_only_0_to_9(grid):
        return None 

    if not nums_unique_per_row(grid):
        return False 

    if not nums_unique_per_column(grid):
        return False 

    if not nums_unique_per_subgrid(grid):
        return False 

    return True 


def make_subgrid_id(row_val, col_val):
    row_num = int( math.floor(row_val / 3) )
    col_num = int( math.floor(col_val / 3) )
    return str(row_num) + str(col_num)


def get_open_positions(grid):
    subgrid_sets = defaultdict(lambda: [])
    col_sets = defaultdict(lambda: [])
    row_sets = defaultdict(lambda: [])

    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            value = grid[row_index][col_index]

            if value == 0:
                continue

            subgrid_id = make_subgrid_id(row_index, col_index)
            subgrid_sets[subgrid_id].append(value)
            row_sets[row_index].append(value)
            col_sets[col_index].append(value)
    
    zero_positions = {}

    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            value = grid[row_index][col_index]
            if value != 0: continue

            pos_id = str(row_index) + '-' + str(col_index)
            zero_positions[pos_id] = []
            subgrid_id = make_subgrid_id(row_index, col_index)

            for num in range(1,10):
                if num in subgrid_sets[subgrid_id]:
                    continue
                
                if num in col_sets[col_index]:
                    continue
                
                if num in row_sets[row_index]:
                    continue
                 
                zero_positions[pos_id].append(num)

            if len(zero_positions[pos_id]) == 0:
                raise Exception('FAIL')

    return zero_positions



def get_possible_values(row, col, open_positions):
    key = str(row) + '-' + str(col)
    return open_positions[key]


def _solve(__grid, open_positions):
    grid = copy.deepcopy(__grid)

    for row in range(0,9):
        for col in range(0,9):
            if grid[row][col] == 0:
                for n in  get_possible_values(row, col, open_positions):
                    grid[row][col] = n 
                    new = _solve(grid, open_positions)
                    if new is not False:
                        return new 
                return False

    return grid


def solve_sudoku(grid, open_positions=None):
    open_positions = open_positions or get_open_positions(grid)
    return _solve(grid, open_positions)

    

print solve_sudoku(easy)       # --> True
print solve_sudoku(hard)       # --> True
