# solve_sudoku should return None
ill_formed = [[5,3,4,6,7,8,9,1,2],
              [6,7,2,1,9,5,3,4,8],
              [1,9,8,3,4,2,5,6,7],
              [8,5,9,7,6,1,4,2,3],
              [4,2,6,8,5,3,7,9],  # <---
              [7,1,3,9,2,4,8,5,6],
              [9,6,1,5,3,7,2,8,4],
              [2,8,7,4,1,9,6,3,5],
              [3,4,5,2,8,6,1,7,9]]

# solve_sudoku should return valid unchanged
valid = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,8],
         [1,9,8,3,4,2,5,6,7],
         [8,5,9,7,6,1,4,2,3],
         [4,2,6,8,5,3,7,9,1],
         [7,1,3,9,2,4,8,5,6],
         [9,6,1,5,3,7,2,8,4],
         [2,8,7,4,1,9,6,3,5],
         [3,4,5,2,8,6,1,7,9]]

# solve_sudoku should return False
invalid = [[5,3,4,6,7,8,9,1,2],
           [6,7,2,1,9,5,3,4,8],
           [1,9,8,3,8,2,5,6,7],
           [8,5,9,7,6,1,4,2,3],
           [4,2,6,8,5,3,7,9,1],
           [7,1,3,9,2,4,8,5,6],
           [9,6,1,5,3,7,2,8,4],
           [2,8,7,4,1,9,6,3,5],
           [3,4,5,2,8,6,1,7,9]]

# solve_sudoku should return a
# sudoku grid which passes a
# sudoku checker. There may be
# multiple correct grids which
# can be made from this starting
# grid.
easy = [[2,9,0,0,0,0,0,7,0],
        [3,0,6,0,0,8,4,0,0],
        [8,0,0,0,4,0,0,0,2],
        [0,2,0,0,3,1,0,0,7],
        [0,0,0,0,8,0,0,0,0],
        [1,0,0,9,5,0,0,6,0],
        [7,0,0,0,9,0,0,0,1],
        [0,0,1,2,0,0,3,0,6],
        [0,3,0,0,0,0,0,5,9]]

# Note: this may timeout
# in the Udacity IDE! Try running
# it locally if you'd like to test
# your solution with it.
#
hard = [[1,0,0,0,0,7,0,9,0],
        [0,3,0,0,2,0,0,0,8],
        [0,0,9,6,0,0,5,0,0],
        [0,0,5,3,0,0,9,0,0],
        [0,1,0,0,8,0,0,0,2],
        [6,0,0,0,0,4,0,0,0],
        [3,0,0,0,0,0,0,1,0],
        [0,4,0,0,0,0,0,0,7],
        [0,0,7,0,0,0,3,0,0]]

def parse_grid_valid(grid):
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
    if not parse_grid_valid(grid): return None
    if not parse_rows(grid): return False
    if not parse_columns(grid): return False
    if not parse_subgrids(grid): return False
    return True

def cross(A, B):
    return [a+b for a in A for b in B]

rows = 'ABCDEFGHI'
cols = '123456789'
digits = '123456789'
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(s2 for u in units[s] for s2 in u if s2 != s))
             for s in squares)

def all(seq):
    for e in seq:
        if not e: return False
    return True

def some(seq):
    for e in seq:
        if e: return e
    return False

def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    _,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])

def assign(values, s, d):
    "Eliminate all the other values (except d) from values[s] and propagate."
    if all(eliminate(values, s, d2) for d2 in values[s] if d2 != d):
        return values
    else:
        return False

def eliminate(values, s, d):
    "Eliminate d from values[s]; propagate when values or places <= 2."
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        ## If there is only one value (d2) left in square, remove it from peers
        d2, = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## Now check the places where d appears in the units of s
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values

def parse_grid(grid):
    "Given a string of 81 digits (or .0-), return a dict of {cell:values}"
    grid = [c for c in grid if c in '0.-123456789']
    values = dict((s, digits) for s in squares) ## Each square can be any digit
    for s,d in zip(squares, grid):
        if d in digits and not assign(values, s, d):
            return False
    return values

def solve_sudoku(grid):
    # The solver should return None for broken
    # input, False for inputs that have no valid solutions, and a valid
    # 9x9 Sudoku grid containing no 0 elements otherwise.
    # Test for valid grid.
    if not parse_grid_valid(grid): return None
    if not check_sudoku(grid): return False
    # Turn the grid into an 81-char string and solve using search().
    s = ''
    for row in grid:
        for square in row:
            s += str(square)
    solution = search(parse_grid(s))
    # Turn solution back into a list of lists.
    grid2 = []
    for r in rows:
        row = []
        for s in squares:
            if s[0] == r:
                row.append(int(solution[s]))
        grid2.append(row)
    return grid2

print solve_sudoku(ill_formed) # --> None
print solve_sudoku(invalid)    # --> False
print solve_sudoku(valid)
print solve_sudoku(easy)
print solve_sudoku(hard)
