# CS 212, hw1-1: 7-card stud

# -----------------
# User Instructions
#
# Write a function best_hand(hand) that takes a seven
# card hand as input and returns the best possible 5
# card hand. The itertools library has some functions
# that may help you solve this problem.
#
# -----------------
# Grading Notes
#
# Muliple correct answers will be accepted in cases
# where the best hand is ambiguous (for example, if
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).

import itertools

def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand."
    all_hands = itertools.combinations(hand, 5)
    return max(all_hands, key=hand_rank)

# CS 212, hw1-2: Jokers Wild
#
# -----------------
# User Instructions
#
# Write a function best_wild_hand(hand) that takes as
# input a 7-card hand and returns the best 5 card hand.
# In this problem, it is possible for a hand to include
# jokers. Jokers will be treated as 'wild cards' which
# can take any rank or suit of the same color. The
# black joker, '?B', can be used as any spade or club
# and the red joker, '?R', can be used as any heart
# or diamond.
#
# The itertools library may be helpful. Feel free to
# define multiple functions if it helps you solve the
# problem.
#
# -----------------
# Grading Notes
#
# Muliple correct answers will be accepted in cases
# where the best hand is ambiguous (for example, if
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).
def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    # First get all combos of 5 cards.
    all_hands = [list(x) for x in itertools.combinations(hand, 5)]
    # Now, for all hands with a red joker in them,
    # replace the joker with every possible replacement.
    all_hands_red = []
    for hand in all_hands:
        if '?R' not in hand:
            all_hands_red.append(hand)
        else:
            hand.remove('?R')
            for i in [r+s for r in '23456789TJQKA' for s in 'HD']:
                all_hands_red.append(hand + [i])
    # Replace all hands with a black joker with
    all_hands_black = []
    for hand in all_hands_red:
        if '?B' not in hand:
            all_hands_black.append(hand)
        else:
            hand.remove('?B')
            for i in [r+s for r in '23456789TJQKA' for s in 'SC']:
                all_hands_black.append(hand + [i])
    # Finally, return the max ranked hand.
    return max(all_hands_black, key=hand_rank)

# ------------------
# Provided Functions
#
# You may want to use some of the functions which
# you have already defined in the unit to write
# your best_hand function.

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    """Return True if the ordered
    ranks form a 5-card straight."""
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has
    exactly n-of-a-kind of. Return None if there
    is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair here, return the two
    ranks of the two pairs, else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None

def test_best_hand():
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_hand passes'

print test_best_hand()

def test_best_wild_hand():
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_wild_hand passes'

print test_best_wild_hand()

# CS 212, hw2-1: No leading zeroes

# --------------
# User Instructions
#
# Modify the function compile_formula so that the function
# it returns (f) does not allow numbers where the first digit
# is zero. So if the formula contained YOU, f would return
# False anytime that Y was 0

import re
import string

def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str,
    in same order as params of function. The first digit of a multi-digit
    number can't be 0. So if YOU is a word in the formula, and the function
    is called with Y equal to 0, the function should return False."""
    # Finds all the unique capital letters.
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    # Find all the unique words.
    unique_words = set(re.findall('[A-Z]+', formula))
    # Find all the unique starting letters of these words.
    firstletters = set(i[0] for i in unique_words)
    # Need to generate a string like: "X!=0 and Y!=0 and Z!=0" to append to the lambda.
    if firstletters:
        not_zero = ' and '.join(i+'!=0' for i in firstletters)
    else:
        not_zero = ''
    params = ', '.join(letters)
    tokens = map(compile_word, re.split('([A-Z]+)', formula))
    body = ''.join(tokens)
    if not_zero: body = ' and '.join([not_zero, body])
    f = 'lambda {0}: {1}'.format(params, body)
    if verbose: print f
    return eval(f), letters

def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    if word.isupper():
        terms = [('%s*%s' % (10**i, d)) for (i, d) in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    else:
        return word

def faster_solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula; only one eval per formula."""
    f, letters = compile_formula(formula)
    for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
        try:
            if f(*digits) is True:
                table = string.maketrans(letters, ''.join(map(str, digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass

def test():
    assert faster_solve('A + B == BA') == None # should NOT return '1 + 0 == 01'
    assert faster_solve('YOU == ME**2') == ('289 == 17**2' or '576 == 24**2' or '841 == 29**2')
    assert faster_solve('X / X == X') == '1 / 1 == 1'
    return 'tests pass'

# CS 212, hw2-2: Floor puzzle

#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on
# different floors of a five-floor apartment building.
#
# Hopper does not live on the top floor.
# Kay does not live on the bottom floor.
# Liskov does not live on either the top or the bottom floor.
# Perlis lives on a higher floor than does Kay.
# Ritchie does not live on a floor adjacent to Liskov's.
# Liskov does not live on a floor adjacent to Kay's.
#
# Where does everyone live?
#
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay,
# Liskov, Perlis, and Ritchie.
def floor_puzzle():
    all_perms = list(itertools.permutations(['Hopper', 'Kay', 'Liskov', 'Perlis', 'Ritchie']))
    perms = []
    for i in all_perms:
        if i[4] != 'Hopper' and i[0] != 'Kay' and (i[0] != 'Liskov' and i[4] != 'Liskov'):
            perms.append(i) # Limit the permutations to ~30.
    for i in perms:
        if (i.index('Perlis') > i.index('Kay')) and (abs(i.index('Ritchie')-i.index('Liskov')) != 1) and (abs(i.index('Liskov')-i.index('Kay')) != 1):
            result = list(i)
    # Turn result into a list of floor numbers.
    floor_nos = []
    floor_nos.append(result.index('Hopper'))
    floor_nos.append(result.index('Kay'))
    floor_nos.append(result.index('Liskov'))
    floor_nos.append(result.index('Perlis'))
    floor_nos.append(result.index('Ritchie'))
    return floor_nos
    #return [1, 2, 3, 4, 5] or [0, 1, 2, 3, 4]
