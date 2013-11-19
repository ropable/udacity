from udacity.utils import memo

def anagrams(phrase, shortest=2):
    '''Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words 
    have length >= shortest. Phrases in answer must have words in 
    lexicographic order (not all permutations).'''
    anagrams = set()
    frontier = []
    phrase = phrase.replace(' ', '').upper() # Replace spaces, convert to uppercase.
    # Get our frontier started.
    for t in extend_anagram(phrase, shortest):
        frontier.append( (t[0], [t[1]]) ) # Tuple: ([], remaining phrase)
    while frontier:
        path = frontier.pop(0)
        if not path[0]: # No remaining letters in the phrase.
            anagrams.add(' '.join(sorted(path[1]))) # Add the to set of discovered anagrams.
        else:
            for t in extend_anagram(path[0], shortest):
                path2 = (t[0], [t[1]] + path[1])
                frontier.append(path2)
    return anagrams

@memo
def extend_anagram(phrase, shortest):
    '''
    Pass in a word, return a list of tuples: [(remainder, word1), (remainder, word2),...]
    '''
    result = []
    words = sorted([w for w in find_words(phrase) if len(w) >= shortest])
    for word in words:
        result.append((removed(phrase, word), word))
    return result

@memo
def xanagrams(phrase, prevword, shortest=2):
    '''Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words 
    have length >= shortest. Phrases in answer must have words in 
    lexicographic order (not all permutations).'''
    plen = len(phrase)  
    if plen < shortest:
        return set()
    words = [(word, extra) for (word, extra) in find_words2(phrase)]
    result = set()    
    for (word, extra) in words:        
        wordlen = len(word)        
        if wordlen < shortest or word < prevword:
            continue
        if wordlen == plen:
            result.add(word)
        else:     
            for ritem in xanagrams(extra, word, shortest):
                result.add(word + ' ' + ritem)
    return result
    
def anagrams2(phrase, shortest=2):
    phrase = "".join(sorted(phrase.replace(' ','')))
    return xanagrams(phrase,'',shortest)    
# ------------
# Helpful functions
# 
# You may find the following functions useful. These functions
# are identical to those we defined in lecture. 

def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

@memo
def find_words(letters):
    return extend_prefix('', letters, set())

@memo
def find_words2(letters):
    return extend_prefix2('', letters, set())
    
def extend_prefix(pre, letters, results):
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            extend_prefix(pre+L, letters.replace(L, '', 1), results)
    return results

def extend_prefix2(pre, letters, results):
    # letters are pre-sorted, so it becomes easy not to extend the same
    # letter at the same level more than once
    if pre in WORDS: results.add((pre, letters))  # save letters too! then use this instead of replacing later
    if pre in PREFIXES:
        pletter = None
        for L in letters:
            if L != pletter:
                extend_prefix2(pre+L, letters.replace(L, '', 1), results)
                pletter = L            
    return results
    
def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]

def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = frozenset(open(filename).read().upper().split())
    prefixset = frozenset(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

# ------------
# Testing
# 
# Run the function test() to see if your function behaves as expected.
def test_anagrams():
    assert 'DOCTOR WHO' in anagrams('TORCHWOOD')
    assert 'BOOK SEC TRY' in anagrams('OCTOBER SKY')
    assert 'SEE THEY' in anagrams('THE EYES')
    assert 'LIVES' in anagrams('ELVIS')
    assert anagrams('PYTHONIC') == set([
        'NTH PIC YO', 'NTH OY PIC', 'ON PIC THY', 'NO PIC THY', 'COY IN PHT',
        'ICY NO PHT', 'ICY ON PHT', 'ICY NTH OP', 'COP IN THY', 'HYP ON TIC',
        'CON PI THY', 'HYP NO TIC', 'COY NTH PI', 'CON HYP IT', 'COT HYP IN',
        'CON HYP TI'])
    return 'tests pass'

#print test_anagrams()

print(len(anagrams2('ADMINISTRATION')))

def anagram_count(phrase):
    return len(anagrams2(phrase)), phrase

#from multiprocessing import Pool
#if __name__ == '__main__':
#    pool = Pool().map(anagrams2, 'ADMINISTRATION')
#    report(pool)