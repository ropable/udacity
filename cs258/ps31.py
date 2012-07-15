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

def parse_grid(grid):
    # Check for malformed sudoku grids.
    # First check that that grid is a list of length 9.
    if not isinstance(grid, list) or len(grid) != 9:
        return False
    # For each row in the grid, check that it's a list.
    # Also check each element in the row is an integer between 0 and 9 inclusive.
    for row in grid:
        if not isinstance(row, list) or len(row) != 9:
            return False
        for i in row:
            if not isinstance(i, int) or not -1 < i < 10:
                return False
    return True

def parse_unit(unit):
    # Parse a list of nine integers for duplicates (ignores 0).
    unit = filter(lambda a: a!=0, unit)
    # Any duplicates? Return False.
    if len(set(unit)) != len(unit): return False
    return True

def parse_rows(grid):
    # Check each row in a valid grid for validity.
    for row in grid:
        if not parse_unit(row): return False
    return True

def parse_columns(grid):
    # Check each column in the grid.
    for i in range(9):
        col = [row[i] for row in grid]
        if not parse_unit(col): return False
    return True

def parse_subgrids(grid):
    # Check each 3x3 subgrid in the grid.
    # Top 3:
    s1, s2, s3 = [], [], []
    for i in range(3):
        for j in range(3):
            s1.append(grid[i][j])
            s2.append(grid[i][j+3])
            s3.append(grid[i][j+6])
    if not parse_unit(s1) or not parse_unit(s2) or not parse_unit(s3): return False
    # Middle 3
    s1, s2, s3 = [], [], []
    for i in range(3, 6):
        for j in range(3):
            s1.append(grid[i][j])
            s2.append(grid[i][j+3])
            s3.append(grid[i][j+6])
    if not parse_unit(s1) or not parse_unit(s2) or not parse_unit(s3): return False
    # Bottom 3
    s1, s2, s3 = [], [], []
    for i in range(6, 9):
        for j in range(3):
            s1.append(grid[i][j])
            s2.append(grid[i][j+3])
            s3.append(grid[i][j+6])
    if not parse_unit(s1) or not parse_unit(s2) or not parse_unit(s3): return False
    return True

def check_sudoku(grid):
    if not parse_grid(grid): return None
    if not parse_rows(grid): return False
    if not parse_columns(grid): return False
    if not parse_subgrids(grid): return False
    return True

'''
print check_sudoku(ill_formed) # --> None
print check_sudoku(valid)      # --> True
print check_sudoku(invalid)    # --> False
print check_sudoku(easy)       # --> True
print check_sudoku(hard)       # --> True
# Everything after here should return None.
print check_sudoku(None)
print check_sudoku([])
print check_sudoku([0])
print check_sudoku([0] * 9)
print check_sudoku([[]] * 9)
print check_sudoku([[str(a) for a in b] for b in valid])
print check_sudoku([[max(0.0, float(a) - 0.5) for a in b] for b in valid])
'''
