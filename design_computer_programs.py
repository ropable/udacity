#!/usr/bin/env python
'''
CS212 Design of Computer Programs
'''
def poker(hand):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return max(hands, key=hand_rank)

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

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return ranks
    
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

print test()
