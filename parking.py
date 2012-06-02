from __future__ import division
import time
from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def trace(f):
    indent = '   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level += 1
        try:
            result = f(*args)
            print '%s<-- %s == %s' % ((trace.level-1)*indent,
                                      signature, result)
        finally:
            trace.level -= 1
        return result
    trace.level = 0
    return _f

@decorator
def memo(f):
    '''Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up.'''
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args refuses to be a dict key
            return f(args)
    _f.cache = cache
    return _f
    
def average(numbers):
    '''Return the average (arithmetic mean) of a sequence of numbers.'''
    return sum(numbers) / float(len(numbers))
    
def timedcall(fn, *args):
    '''Call function with args; return the time in seconds and results.'''
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result
    
def timedcalls(n, fn, *args):
    '''Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time.'''
    if (isinstance(n, int)):
        times = [timedcall(fn,*args)[0] for _ in range(n)]
    else:
        times = []
        while sum(times) < n:
            times.append(timedcall(fn,*args)[0])
    return min(times), average(times), max(times)
'''
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:
'''
N = 8

def solve_parking_puzzle(start, N=N):
    '''Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid.
    '''
    return shortest_path_search(start, grid_successors, is_goal, N)

# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    l = [start]
    for i in range(n-1):
        l.append(start + ((i+1) * incr))
    return tuple(l)

def grid(cars, N=N):
    '''Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs.
    '''
    # First, append the goal square.
    exit = abs(int(N/2))*N-1
    all_cars = [('@', locs(exit, 1))] # Halfway down the right side.
    for c in cars:
        all_cars.append(c)
    # Finally, append the walls.
    wall_squares = [i for i in range(N)] # Top row
    wall_squares += [i for i in range(0, N**2, N)] # Left row
    wall_squares += [i for i in range(N-1, N**2, N)] # Right row
    wall_squares += [i for i in range(N**2-N, N**2)] # Bottom row
    walls = set(wall_squares)
    walls.remove(exit)
    all_cars.append(('|', tuple(walls)))
    return tuple(all_cars)
    
def grid_successors(state, N=N):
    '''Find all successor grids to this state. Return successors as a dict of
    state:action pairs. "Action" is a tuple: (car, move)
    '''
    successors = {}
    board = ['.'] * N**2
    # Construct the board state as a list.
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    for idx, car in enumerate(state):
        if car[0] not in ('@', '|'):
            n = ahead = car[1][1] - car[1][0] # Equals 1 or N.
            # First move each car left/up until we bump into something.
            square = board[car[1][0]-ahead]
            while square in ('.', '@'):
                # Extend the car's move by one square.
                state2 = list(state)
                state2[idx] = (car[0], tuple([i-ahead for i in car[1]]))
                action = (car[0], -ahead)
                successors[frozenset(state2)] = action
                ahead += n
                square = board[car[1][0]-ahead]
                #print(square)
            # Next move it right/down until we bump into something.
            ahead = car[1][1] - car[1][0]
            square = board[car[1][-1]+ahead]
            while square in ('.', '@'):
                # Extend the car's move by one square.
                state2 = list(state)
                state2[idx] = (car[0], tuple([i+ahead for i in car[1]]))
                action = (car[0], ahead)
                successors[frozenset(state2)] = action
                ahead += n
                square = board[car[1][-1]+ahead]
                #print(square)
    return successors
'''
puzzle1 = [
    ('*', (26, 27)), 
    ('G', (9, 10)),
    ('Y', (14, 22, 30)), 
    ('P', (17, 25, 33)), 
    ('O', (41, 49)), 
    ('B', (20, 28, 36)), 
    ('A', (45, 46))
    ]
'''
def is_goal(state):
    goal_square, car_squares = None, None
    for c in state:
        if c[0] == "@":
            goal_square = c[1][0]
    for c in state:
        if c[0] == "*":
            car_squares = c[1]
    if goal_square in car_squares:
        return True
    else:
        return False
    
def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print
    print('')

# Here we see the grid and locs functions in use:
puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))
    ))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))

puzzle4 = grid((
    ('*', locs(28, 2)),
    ('A', locs(21, 3, 9)),
    ('B', locs(22, 3, 9)),
    ('C', locs(23, 3, 9)),
    ('D', locs(24, 3, 9)),
    ('E', locs(25, 3, 9)),
    ), N=9)
    
puzzle5 = grid((
    ('*', locs(41, 2)),
    ('A', locs(33, 3, 10)),
    ('B', locs(34, 3, 10)),
    ('C', locs(35, 3, 10)),
    ('D', locs(36, 3, 10)),
    ('E', locs(37, 3, 10)),
    ('F', locs(38, 3, 10)),
    ), N=10)
# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

@memo
def shortest_path_search(start, successors, is_goal, N=N):
    '''Find the shortest path from start state to a state
    such that is_goal(state) is true.
    '''
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s, N).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

#path = solve_parking_puzzle(puzzle5, N=10)
#print(path_actions(path))
