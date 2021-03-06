# -----------------
# User Instructions
#
# Write a function, csuccessors, that takes a state (as defined below)
# as input and returns a dictionary of {state:action} pairs.
#
# A state is a tuple with six entries: (M1, C1, B1, M2, C2, B2), where
# M1 means 'number of missionaries on the left side.'
#
# An action is one of the following ten strings:
#
# 'MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-M', '<-C'
# where 'MM->' means two missionaries travel to the right side.
#
# We should generate successor states that include more cannibals than
# missionaries, but such a state should generate no successors.

def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state
    d = {}
    # Return 'dining' state.
    if C1 > M1 or C2 > M2:
        return d
    if B1 == 1:
        #for each person in M1 or C1, find each possible successor state.
        if M1:
            if M1 > 1:
                # Two missionaries
                d[(M1-2, C1, 0, M2+2, C2, 1)] = 'MM->'
            # One missionary
            d[(M1-1, C1, 0, M2+1, C2, 1)] = 'M->'
        if C1:
            if C1 > 1:
                d[(M1, C1-2, 0, M2, C2+2, 1)] = 'CC->'
            d[(M1, C1-1, 0, M2, C2+1, 1)] = 'C->'
        # Both a cannibal and a missionary
        if M1 and C1:
            d[(M1-1, C1-1, 0, M2+1, C2+1, 1)] = 'MC->'
    else:
        if M2:
            if M2 > 1:
                d[(M1+2, C1, 1, M2-2, C2, 0)] = '<-MM'
            d[(M1+1, C1, 1, M2-1, C2, 0)] = '<-M'
        if C2:
            if C2 > 1:
                d[(M1, C1+2, 1, M2, C2-2, 0)] = '<-CC'
            d[(M1, C1+1, 1, M2, C2-1, 0)] = '<-C'
        if M2 and C2:
            d[(M1+1, C1+1, 1, M2-1, C2-1, 0)] = '<-MC'
    return d

def test():
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C',
                                               (2, 1, 1, 3, 3, 0): '<-M',
                                               (3, 1, 1, 2, 3, 0): '<-MM',
                                               (1, 3, 1, 4, 1, 0): '<-CC',
                                               (2, 2, 1, 3, 2, 0): '<-MC'}
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->',
                                               (1, 2, 0, 1, 0, 1): 'M->',
                                               (0, 2, 0, 2, 0, 1): 'MM->',
                                               (1, 1, 0, 1, 1, 1): 'MC->',
                                               (2, 0, 0, 0, 2, 1): 'CC->'}
    return 'tests pass'

print test()
