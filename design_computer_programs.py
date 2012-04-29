#!/usr/bin/env python
'''
CS212 Design of Computer Programs
'''

'''
UNIT 1 scripts
-----------------------------------------------------------------
'''
import random
# Generate a standard deck of cards.
std_deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

def deal(numhands, n=5, deck=std_deck):
    "Shuffle the desk and deal out numhands n-card hands."
    # My solution
    if numhands < 1:
        raise Exception('Number of hands must be greater than 0.')
    random.shuffle(deck) # Shuffle the deck of cards.
    return [deck[n*i:n*(i+1)] for i in range(numhands)]
    hands = []
    for i in range(numhands):
        # We're not handling the case of running out of cards just yet.
        hand = []
        for j in range(n):
            hand.append(deck.pop())
        hands.append(hand)
    return hands
    # Instructor solution
    #random.shuffle(deck)
    #return [deck[n*i:n*(i+1)] for i in range(numhands)]
    
def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    # My solution - as far as I can tell, this passes the tests OK.
    all_hands = []
    max_hands = []
    for hand in iterable:
        all_hands.append(key(hand))
    all_hands.sort(reverse=True)
    max_hands.append(all_hands[0])
    for hand_rank in all_hands[1:]:
        if hand_rank[0] == max_hands[0][0]:
            max_hands.append(hand_rank)
    return max_hands
    # Instructor solution
    '''result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result'''

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

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    # My solution:
    ranks.sort() # Sort lowest to highest.
    for i in range(4): # Assume a hand is 5 cards only.
        if ranks[i] != (ranks[i+1]-1):
            return False
    return True
    # Instructor solution:
    #return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def flush(hand):
    "Return True if all the cards have the same suit."
    # My solution:
    for i in range(4):
        if hand[i][-1] != hand[i+1][-1]:
            return False
    return True
    # Instructor solution:
    #suits = [s for r,s in hand]
    #return len(set(suits)) == 1

def two_pair(ranks):
    "If there are two pair here, return the two ranks of the two pairs, else None."
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None

def kind(n, ranks):
    """Return the first rank that this hand has exactly n-of-a-kind of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r,s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks
    
def test():
    "Test cases for the functions in poker program."
    sf = "6C 7C 8C 9C TC".split()
    fk = "9D 9H 9S 9C 7D".split()
    fh = "TD TC TH 7C 7D".split()
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert flush(sf) == True
    assert flush(fk) == False
    return 'tests pass'

def test2():
    "Test cases for the functions in poker program."
    sf1 = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2] 
    return 'tests pass'

print test()
'''
UNIT 2 scripts
-----------------------------------------------------------------
'''
