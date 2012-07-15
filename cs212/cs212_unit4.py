import itertools

# HW 4-1
# -----------------
# User Instructions
#
# In this problem you will be refactoring the bsuccessors function.
# Your new function, bsuccessors3, will take a state as an input
# and return a dict of {state:action} pairs.
#
# A state is a (here, there, light) tuple. Here and there are
# frozensets of people (each person is represented by an integer
# which corresponds to their travel time), and light is 0 if
# it is on the `here` side and 1 if it is on the `there` side.
#
# An action is a tuple of (travelers, arrow), where the arrow is
# '->' or '<-'. See the test() function below for some examples
# of what your function's input and output should look like.

def bsuccessors3(state):
    '''Return a dict of {state:action} pairs.  State is (here, there, light)
    where here and there are frozen sets of people, light is 0 if the light is
    on the here side and 1 if it is on the there side.
    Action is a tuple (travelers, arrow) where arrow is '->' or '<-'
    '''
    here, there, light = state
    d = {}
    if not light: # The light in on the "here" side"
        sets = [set([a, b]) for a in here for b in here]
        for s in sets:
            d[(here - s, there | s, 1)] = (s, '->')
    else:
        sets = [set([a, b]) for a in there for b in there]
        for s in sets:
            d[(here | s, there - s, 0)] = (s, '<-')
    return d

def bsuccessors2(state):
    '''Return a dict of {state:action} pairs.  A state is a (here, there) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the light.'''
    here, there = state
    if 'light' in here:
        return dict(((here  - frozenset([a, b, 'light']),
                      there | frozenset([a, b, 'light'])),
                     (a, b, '->'))
                    for a in here if a is not 'light'
                    for b in here if b is not 'light')
    else:
        return dict(((here  | frozenset([a, b, 'light']),
                      there - frozenset([a, b, 'light'])),
                     (a, b, '<-'))
                    for a in there if a is not 'light'
                    for b in there if b is not 'light')

def test_bsuccessors2():
    assert bsuccessors3((frozenset([1]), frozenset([]), 0)) == {(frozenset([]), frozenset([1]), 1)  :  (set([1]), '->')}

    assert bsuccessors3((frozenset([1, 2]), frozenset([]), 0)) == {
            (frozenset([1]), frozenset([2]), 1)    :  (set([2]), '->'),
            (frozenset([]), frozenset([1, 2]), 1)  :  (set([1, 2]), '->'),
            (frozenset([2]), frozenset([1]), 1)    :  (set([1]), '->')}

    assert bsuccessors3((frozenset([2, 4]), frozenset([3, 5]), 1)) == {
            (frozenset([2, 4, 5]), frozenset([3]), 0)   :  (set([5]), '<-'),
            (frozenset([2, 3, 4, 5]), frozenset([]), 0) :  (set([3, 5]), '<-'),
            (frozenset([2, 3, 4]), frozenset([5]), 0)   :  (set([3]), '<-')}
    return 'test_bsuccessors2 pass'

print test_bsuccessors2()

# HW 4-2
# -----------------
# User Instructions
#
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes
# as input capacities, goal, and (optionally) start. This function should
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the
# volume of a glass.
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i),
# ('empty', i), ('pour', i, j) where i and j are indices indicating the
# glass number.

def more_pour_problem(capacities, goal, start=None):
    '''The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number.'''
    if not start:
        # If we didn't receive a start state, assume that all glasses are empty.
        start = tuple([0 for i in range(len(capacities))])
    return shortest_path_search(start, pour_successors, capacities, pour_problem_goal, goal)

def pour_successors(state, capacities):
    '''Return a dict of {state:action} pairs.  State is (here, there, light)
    where here and there are frozen sets of people, light is 0 if the light is
    on the here side and 1 if it is on the there side.
    Action is a tuple (travelers, arrow) where arrow is '->' or '<-'
    '''
    '''Return a dict of all legit successors to the input state.
    E.g {(1, 0):('fill', 0), (0, 2):('fill', 1)}
    '''
    # Actions can be '(fill, x)', '(empty, x)' or '(pour, x, y)'
    successors = {}
    pour = zip(capacities, state) # List of tuples: [(cap, state), ...]
    for i, v in enumerate(pour):
        # Can we fill it?
        if v[0] > v[1]:
            suc = [a[1] for a in pour]
            suc[i] = v[0] # set it to capacity
            successors[tuple(suc)] = ('fill', i)
        # Can we empty it?
        if v[1] > 0:
            suc = [a[1] for a in pour]
            suc[i] = 0 # set it to 0
            successors[tuple(suc)] = ('empty', i)
        # Can we pour it into another glass?
        if len(pour) > 1 and v[1] > 0:
            for i2, v2 in enumerate(pour):
                # Not the same glass?
                if i2 != i:
                    # How much room does i2 have spare?
                    spare = v2[0] - v2[1]
                    if spare > 0:
                        # How much will get transferred?
                        transfer = min(spare, v[1])
                        # Transfer from i to i2
                        suc = [a[1] for a in pour]
                        suc[i] -= transfer
                        suc[i2] += transfer
                        successors[tuple(suc)] = ('pour', i, i2)
    return successors

def pour_problem_goal(state, goal):
    '''Does the tuple contain the desired volume?
    '''
    if goal in state:
        return True
    else:
        return False

Fail = []
def shortest_path_search(start, successors, capacities, is_goal, goal):
    '''Find the shortest path from start state to a state
    such that is_goal(state) is true.'''
    if is_goal(start, goal):
        return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s, capacities).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state, goal):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)]
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print test_more_pour()

# HW 4-3
# -----------------
# User Instructions
#
# Write a function, subway, that takes lines as input (read more about
# the **lines notation in the instructor comments box below) and returns
# a dictionary of the form {station:{neighbor:line, ...}, ... }
#
# For example, when calling subway(boston), one of the entries in the
# resulting dictionary should be 'foresthills': {'backbay': 'orange'}.
# This means that foresthills only has one neighbor ('backbay') and
# that neighbor is on the orange line. Other stations have more neighbors:
# 'state', for example, has 4 neighbors.
#
# Once you've defined your subway function, you can define a ride and
# longest_ride function. ride(here, there, system) takes as input
# a starting station (here), a destination station (there), and a subway
# system and returns the shortest path.
#
# longest_ride(system) returns the longest possible ride in a given
# subway system.

# -------------
# Grading Notes
#
# The subway() function will not be tested directly, only ride() and
# longest_ride() will be explicitly tested. If your code passes the
# assert statements in test_ride(), it should be marked correct.

def subway(**lines):
    '''Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}'''
    d = {}
    # {'foresthills':{'backbay':'orange'}, 'state':{'aquarium':'blue','government':'blue','haymarket':'orange','downtown':'orange'} }
    for k,v in lines.items(): #k=line name, v=stations
        stations = v.split() # List of stations ['one, 'two', 'three']
        line_length = len(stations) - 1
        for i, s in enumerate(stations): #i=station index, s=station name
            # Assumption: lines have at least two stations (i.e. a station has at least one neighbour).
            if d.has_key(s):
                # The station already exists; add neighbours on the new line.
                if i == 0: # First station (one neighbour)
                    t = d[s] # Copy existing
                    d[s] = dict(d[s].items() + [(stations[i+1], k)])
                elif i == line_length: # Last station
                    d[s] = dict(d[s].items() + [(stations[i-1], k)])
                else:
                    d[s] = dict(d[s].items() + [(stations[i-1], k), (stations[i+1], k)])
            else:
                d[s] = {}
                if i == 0: # First station (one neighbour)
                    d[s] = {stations[i+1]:k}
                elif i == line_length: # Last station
                    d[s] = {stations[i-1]:k}
                else: # middle station (two neighbours)
                    d[s] = {stations[i-1]:k, stations[i+1]:k}
    return d

boston = subway(
    blue='bowdoin government state aquarium maverick airport suffolk revere wonderland',
    orange='oakgrove sullivan haymarket state downtown chinatown tufts backbay foresthills',
    green='lechmere science north haymarket government park copley kenmore newton riverside',
    red='alewife davis porter harvard central mit charles park downtown south umass mattapan')

def ride(here, there, system=boston):
    '''Return a path on the subway system from here to there.
    '''
    if here == there: return [here]
    return subway_path_search(here, subway_successors, system, there)

def longest_ride(system=boston):
    '''Return the longest possible 'shortest path' ride between any
    two stops in the system.'''
    longest_ride = None
    for r in [r for r in itertools.combinations(system.keys(), 2)]:
        next_ride = ride(r[0], r[1], system)
        if not longest_ride or len(path_states(next_ride)) > len(path_states(longest_ride)):
            longest_ride = next_ride
    return longest_ride

def subway_successors(system, state):
    '''Return a list of all legit successor stations to the input state.
    Successors are (station, line) tuples.'''
    return system[state].items()
    
def subway_path_search(start, successors, system, is_goal):
    '''Find the shortest path from start state to a state
    such that is_goal(state) is true.'''
    if is_goal == start:
        return [start]
    explored = set()
    frontier = [ [start] ]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(system, s):
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if state == is_goal:
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def test_ride():
    assert ride('mit', 'government') == [
        'mit', 'red', 'charles', 'red', 'park', 'green', 'government']
    assert ride('mattapan', 'foresthills') == [
        'mattapan', 'red', 'umass', 'red', 'south', 'red', 'downtown',
        'orange', 'chinatown', 'orange', 'tufts', 'orange', 'backbay', 'orange', 'foresthills']
    assert ride('newton', 'alewife') == [
        'newton', 'green', 'kenmore', 'green', 'copley', 'green', 'park', 'red', 'charles', 'red',
        'mit', 'red', 'central', 'red', 'harvard', 'red', 'porter', 'red', 'davis', 'red', 'alewife']
    assert (path_states(longest_ride(boston)) == [
        'wonderland', 'revere', 'suffolk', 'airport', 'maverick', 'aquarium', 'state', 'downtown', 'park',
        'charles', 'mit', 'central', 'harvard', 'porter', 'davis', 'alewife'] or
        path_states(longest_ride(boston)) == [
                'alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 'charles',
                'park', 'downtown', 'state', 'aquarium', 'maverick', 'airport', 'suffolk', 'revere', 'wonderland'])
    assert len(path_states(longest_ride(boston))) == 16
    return 'test_ride passes'

print test_ride()