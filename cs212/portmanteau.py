# Unit 6: Fun with Words

'''
A portmanteau word is a blend of two or more words, like 'mathelete',
which comes from 'math' and 'athelete'.  You will write a function to
find the 'best' portmanteau word from a list of dictionary words.
Because 'portmanteau' is so easy to misspell, we will call our
function 'natalie' instead:

    natalie(['word', ...]) == 'portmanteauword' 

In this exercise the rules are: a portmanteau must be composed of
three non-empty pieces, start+mid+end, where both start+mid and
mid+end are among the list of words passed in.  For example,
'adolescented' comes from 'adolescent' and 'scented', with
start+mid+end='adole'+'scent'+'ed'. A portmanteau must be composed
of two different words (not the same word twice).

That defines an allowable combination, but which is best? Intuitively,
a longer word is better, and a word is well-balanced if the mid is
about half the total length while start and end are about 1/4 each.
To make that specific, the score for a word w is the number of letters
in w minus the difference between the actual and ideal lengths of
start, mid, and end. (For the example word w='adole'+'scent'+'ed', the
start,mid,end lengths are 5,5,2 and the total length is 12.  The ideal
start,mid,end lengths are 12/4,12/2,12/4 = 3,6,3. So the final score is

    12 - abs(5-3) - abs(5-6) - abs(2-3) = 8.

yielding a score of 12 - abs(5-(12/4)) - abs(5-(12/2)) - abs(2-(12/4)) = 8.

The output of natalie(words) should be the best portmanteau, or None
if there is none.
'''
import itertools

def overlaps(words):
    "Get tuple of 2 words; return a list of all the overlaps (start, mid, end), or None."
    w1, w2 = words
    if w1 == w2: return None
    mashups = []
    count = 1
    # Test a progressively larger slice of the first word's end.
    while count <= len(w2):
        if w1.endswith(w2[0:count]) and w1[0:-count]: # Can't use all of the first word.
            mashups.append((w1[0:-count], w2[0:count], w2[count:]))
        count += 1
    return mashups

def mashup_score(mashup):
    "Get a 3-tuple of (start, mid, end); return the score."
    start, mid, end = mashup
    l = len(''.join(mashup))
    return l - abs(len(start)-(l/4)) - abs(len(mid)-(l/2)) - abs(len(end)-(l/4))
    
def natalie(words):
    "Find the best Portmanteau word formed from any two of the list of words."
    if not words: return None
    p = [p for p in itertools.permutations(words, 2)] # Yield a list of all word pairs.
    score = 0
    winner = None
    for pair in p:
        mashups = overlaps(pair)
        for mashup in mashups:
            score2 = mashup_score(mashup)
            if score2 > score:
                score = score2
                winner = ''.join(mashup)
    return winner

def test_natalie():
    "Some test cases for natalie"
    assert natalie(['adolescent', 'scented', 'centennial', 'always', 'ado']) in ('adolescented','adolescentennial')
    assert natalie(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese']) == 'eskimono'
    assert natalie(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage']) == 'kimcheese'
    assert natalie(['circus', 'elephant', 'lion', 'opera', 'phantom']) == 'elephantom'
    assert natalie(['programmer', 'coder', 'partying', 'merrymaking']) == 'programmerrymaking'
    assert natalie(['int', 'intimate', 'hinter', 'hint', 'winter']) == 'hintimate'
    assert natalie(['morass', 'moral', 'assassination']) == 'morassassination'
    assert natalie(['entrepreneur', 'academic', 'doctor', 'neuropsychologist', 'neurotoxin', 'scientist', 'gist']) in ('entrepreneuropsychologist', 'entrepreneurotoxin')
    assert natalie(['perspicacity', 'cityslicker', 'capability', 'capable']) == 'perspicacityslicker'
    assert natalie(['backfire', 'fireproof', 'backflow', 'flowchart', 'background', 'groundhog']) == 'backgroundhog'
    assert natalie(['streaker', 'nudist', 'hippie', 'protestor', 'disturbance', 'cops']) == 'nudisturbance'
    assert natalie(['night', 'day']) == None
    assert natalie(['dog', 'dogs']) == None
    assert natalie(['test']) == None
    assert natalie(['']) ==  None
    assert natalie(['ABC', '123']) == None
    assert natalie([]) == None
    return 'tests pass'


print test_natalie()
