import random
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

# -----------------
# User Instructions
# 
# In this problem, you will use a faster version of Pwin, which we will call
# Pwin2, that takes a state as input but ignores whether it is player 1 or 
# player 2 who starts. This will reduce the number of computations to about 
# half. You will define a function, Pwin3, which will be called by Pwin2.
#
# Pwin3 will only take me, you, and pending as input and will return the 
# probability of winning. 
#
# Keep in mind that the probability that I win from a position is always
# (1 - probability that my opponent wins).
goal = 40
other = {1:0, 0:1}

def roll(state, d):
    '''Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points.'''
    (p, me, you, pending) = state
    if d == 1:
        return (other[p], you, me+1, 0) # pig out; other player's turn
    else:
        return (p, me, you, pending+d)  # accumulate die roll in pending

def hold(state):
    '''Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn.'''
    (p, me, you, pending) = state
    return (other[p], you, me+pending, 0)

def pig_actions(state):
    '''The legal actions from a state.'''
    _, _, _, pending = state
    return ['roll', 'hold'] if pending else ['roll']

def Q_pig(state, action, Pwin):  
    '''The expected value of choosing action in state.'''
    if action == 'hold':
        return 1 - Pwin(hold(state))
    if action == 'roll':
        return (1 - Pwin(roll(state, 1))
                + sum(Pwin(roll(state, d)) for d in (2,3,4,5,6))) / 6.
    raise ValueError

@memo
def Pwin(state):
    '''The utility of a state; here just the probability that an optimal player
    whose turn it is to move can win from the current state.'''
    # Assumes opponent also plays with optimal strategy.
    (p, me, you, pending) = state
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        return max(Q_pig(state, action, Pwin) for action in pig_actions(state))

def Q_pig2(state, action, Pwin2):  
    '''The expected value of choosing action in state.'''
    (p, me, you, pending) = state
    if action == 'hold':
        return 1 - Pwin2(hold(state))
    if action == 'roll':
        return (1 - Pwin2(roll(state, 1))
                + sum(Pwin2(roll(state, d)) for d in (2,3,4,5,6))) / 6.
    raise ValueError

def Pwin2(state):
    '''The utility of a state; here just the probability that an optimal player
    whose turn it is to move can win from the current state.'''
    _, me, you, pending = state
    return Pwin3(me, you, pending)

@memo
def Pwin3(me, you, pending):
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        state = (0, me, you, pending)
        return max(Q_pig2(state, action, Pwin2) for action in pig_actions(state))


def test_pwin2():
    epsilon = 0.00000001 # used to make sure that floating point errors don't cause test() to fail
    assert goal == 40
    assert len(Pwin3.cache) <= 50000
    assert Pwin2((0, 42, 25, 0)) == 1
    assert Pwin2((1, 12, 43, 0)) == 0
    assert Pwin2((0, 34, 42, 1)) == 0
    assert abs(Pwin2((0, 25, 32, 8)) - 0.736357188272) <= epsilon
    assert abs(Pwin2((0, 19, 35, 4)) - 0.493173612834) <= epsilon
    return 'Pwin2 tests pass'

#print test_pwin2()

# -----------------
# User Instructions
# 
# In this problem, we introduce doubling to the game of pig. 
# At any point in the game, a player (let's say player A) can
# offer to 'double' the game. Player B then has to decide to 
# 'accept', in which case the game is played through as normal,
# but it is now worth two points, or 'decline,' in which case
# player B immediately loses and player A wins one point. 
#
# Your job is to write two functions. The first, pig_actions_d,
# takes a state (p, me, you, pending, double), as input and 
# returns all of the legal actions.
# 
# The second, strategy_d, is a strategy function which takes a
# state as input and returns one of the possible actions. This
# strategy needs to beat hold_20_d in order for you to be
# marked correct. Happy pigging!

def Q_pig_d(state, action, Pwin_d):
    state2 = (state[0], state[1], state[2], state[3])
    if action == 'hold':
        return 1 - Pwin_d(hold(state2))
    if action == 'roll':
        return (1 - Pwin_d(roll(state2, 1)) + sum(Pwin_d(roll(state2, d)) for d in (2,3,4,5,6))) / 6.
    raise ValueError
    
@memo
def Pwin_d(state):
    (p, me, you, pending, double) = state
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        return max(Q_pig_d(state, action, Pwin_d) for action in pig_actions_d(state))

def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U."
    def EU(action): return Q(state, action, U)
    return max(actions(state), key=EU)
    
def max_wins(state):
    "The optimal pig strategy chooses an action with the highest win probability."
    return best_action(state, pig_actions_d, Q_pig_d, Pwin_d)

def pig_actions_d(state):
    '''The legal actions from a state. Usually, ["roll", "hold"].
    Exceptions: If double is "double", can only "accept" or "decline".
    Can't "hold" if pending is 0.
    If double is 1, can "double" (in addition to other moves).
    (If double > 1, cannot "double").
    '''
    # state is like before, but with one more component, double,
    # which is 1 or 2 to denote the value of the game, or 'double'
    # for the moment at which one player has doubled and is waiting
    # for the other to accept or decline
    (p, me, you, pending, double) = state 
    if double == '2' or double == 'double':
        return ['accept', 'decline']
    actions = ['roll']
    if pending != 0: actions.append('hold')
    if double == 1: actions.append('double')
    return actions
    
def strategy_d(state):
    (p, me, you, pending, double) = state
    return ('hold' if (pending >= 20 or me + pending >= goal) else
            'double' if (me > you > 0 and double != 2) else
            'roll')

def hold_20_d(state):
    "Hold at 20 pending.  Always accept; never double."
    (p, me, you, pending, double) = state
    return ('accept' if double == 'double' else
            'hold' if (pending >= 20 or me + pending >= goal) else
            'roll')

def stupid_d(state):
    '''Always declines, never doubles, otherwise normal.'''
    (p, me, you, pending, double) = state
    return ('decline' if double == 'double' else
            'hold' if (pending >= 20 or me + pending >= goal) else
            'roll')

def clueless_d(state):
    return random.choice(pig_actions_d(state))
 
def dierolls():
    "Generate die rolls."
    while True:
        yield random.randint(1, 6)

def play_pig_d(A, B, dierolls=dierolls()):
    '''Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player.'''
    strategies = [A, B]
    state = (0, 0, 0, 0, 1)
    while True:
        (p, me, you, pending, double) = state
        if me >= goal:
            return strategies[p], double
        elif you >= goal:
            return strategies[other[p]], double
        else:
            action = strategies[p](state)
            #print(state)
            #print(action)
            state = do(action, state, dierolls)

## No more roll() and hold(); instead, do:

def do(action, state, dierolls):
    '''Return the state that results from doing action in state.
     If action is not legal, return a state where the opponent wins.
    Can use dierolls if needed.'''
    (p, me, you, pending, double) = state
    if action not in pig_actions_d(state):
        return (other[p], goal, 0, 0, double)
    elif action == 'roll':
        d = next(dierolls)
        if d == 1:
            return (other[p], you, me+1, 0, double) # pig out; other player's turn
        else:
            return (p, me, you, pending+d, double)  # accumulate die in pending
    elif action == 'hold':
        return (other[p], you, me+pending, 0, double)
    elif action == 'double':
        return (other[p], you, me, pending, 'double')
    elif action == 'decline':
        return (other[p], goal, 0, 0, 1)
    elif action == 'accept':
        return (other[p], you, me, pending, 2)

def strategy_compare(A, B, N=1000):
    '''Takes two strategies, A and B, as input and returns the percentage
    of points won by strategy A.'''
    A_points, B_points = 0, 0
    for i in range(N):
        if i % 2 == 0:  # take turns with who goes first
            winner, points = play_pig_d(A, B)
        else: 
            winner, points = play_pig_d(B, A)
        if winner.__name__ == A.__name__:
            A_points += points
        else: B_points += points
    A_percent = 100*A_points / float(A_points + B_points)
    print 'In %s games of pig, strategy %s took %s percent of the points against %s.' % (N, A.__name__, A_percent, B.__name__)
    return A_percent
    
def test_double_pig():
    assert set(pig_actions_d((0, 2, 3, 0, 1)))          == set(['roll', 'double'])
    assert set(pig_actions_d((1, 20, 30, 5, 2)))        == set(['hold', 'roll']) 
    assert set(pig_actions_d((0, 5, 5, 5, 1)))          == set(['roll', 'hold', 'double'])
    assert set(pig_actions_d((1, 10, 15, 6, 'double'))) == set(['accept', 'decline']) 
    #assert strategy_compare(strategy_d, hold_20_d) > 60 # must win 60% of the points      
    return 'test_double_pig tests pass'

#print test_double_pig()
#print(strategy_compare(strategy_d, hold_20_d))
#print(strategy_compare(clueless_d, hold_20_d))
#print(strategy_compare(strategy_d, hold_20_d))

# -----------------
# User Instructions
# 
# This problem deals with the one-player game foxes_and_hens. This 
# game is played with a deck of cards in which each card is labelled
# as a hen 'H', or a fox 'F'. 
# 
# A player will flip over a random card. If that card is a hen, it is
# added to the yard. If it is a fox, all of the hens currently in the
# yard are removed.
#
# Before drawing a card, the player has the choice of two actions, 
# 'gather' or 'wait'. If the player gathers, she collects all the hens
# in the yard and adds them to her score. The drawn card is discarded.
# If the player waits, she sees the next card. 
#
# Your job is to define two functions. The first is do(action, state), 
# where action is either 'gather' or 'wait' and state is a tuple of 
# (score, yard, cards). This function should return a new state with 
# one less card and the yard and score properly updated.
#
# The second function you define, strategy(state), should return an 
# action based on the state. This strategy should average at least 
# 1.5 more points than the take5 strategy.

def foxes_and_hens(strategy, foxes=7, hens=45):
    '''Play the game of foxes and hens.'''
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, 'F'*foxes + 'H'*hens)
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard

def do(action, state):
    "Apply action to state, returning a new state."
    # Make sure you always use up one card.
    # action is either 'gather' or 'wait'
    (score, yard, cards) = state
    if action == 'gather':
        score += yard
        yard = 0
    # From here 'gather' and 'wait' are the same.
    card = random.choice(cards)
    if card == 'H' and action == 'wait':
        yard += 1
    elif card == 'F': # We drew a fox
        yard = 0
    cards = cards.replace(card, '', 1)
    return (score, yard, cards)
    
def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'

def average_score(strategy, N=1000):
    return sum(foxes_and_hens(strategy) for _ in range(N)) / float(N)

def superior(A, B=take5):
    "Does strategy A have a higher average score than B, by more than 1.5 point?"
    return average_score(A) - average_score(B) > 1.5

def P_hen(state):
    '''Probability of drawing a hen.'''
    (score, yard, cards) = state
    foxes = float(cards.count('F'))
    hens = float(cards.count('H'))
    if not hens:
        return 0
    elif not foxes:
        return 1
    else:
        return hens/len(cards)

def strategy(state):
    (score, yard, cards) = state
    # We can count cards
    # Count the number of hens and foxes left; while it's more likely to draw a hen: wait.
    if P_hen(state) == 1:
        return 'wait'
    elif P_hen(state) > ((1-P_hen(state)) * yard * 2.2):
        return 'wait'
    else:
        return 'gather'

def test_foxes_and_hens():
    gather = do('gather', (4, 5, 'F'*4 + 'H'*10))
    assert (gather == (9, 0, 'F'*3 + 'H'*10) or gather == (9, 0, 'F'*4 + 'H'*9))
    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or wait == (10, 0, 'FHH'))
    assert superior(strategy)
    return 'Foxes and hens tests pass'

print test_foxes_and_hens()
#print(average_score(take5))
        
def Q_hen(state, action, P_hen):
    '''The expected value of choosing action in state.'''
    if action == 'gather':
        return 1 - P_hen(state)
    if action == 'wait':
        return (1 - Pwin(roll(state, 1))
                + sum(Pwin(roll(state, d)) for d in (2,3,4,5,6))) / 6.
    raise ValueError
