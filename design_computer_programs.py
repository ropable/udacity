'''
CS212 Design of Computer Programs
'''
def poker(hand):
    '''
    Return the highest-ranked hand of a list of poker hands.
    '''
    return None

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    ranks.sort() # Sort lowest to highest.
    for i in xrange(4): # Assume a hand is 5 cards only.
        if ranks[i] != (ranks[i+1]-1):
            return False
    return True

def flush(hand):
    "Return True if all the cards have the same suit."
    #hand = ['6C','7C','8C','9C','TC']
    for i in xrange(4):
        if hand[i][-1] != hand[i+1][-1]:
            return False
    return True

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
