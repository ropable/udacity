import functools
import re

# Homework 3-1
# ---------------
# User Instructions
#
# In this problem, you will be using many of the tools and techniques
# that you developed in unit 3 to write a grammar that will allow
# us to write a parser for the JSON language. 
#
# You will have to visit json.org to see the JSON grammar. It is not 
# presented in the correct format for our grammar function, so you 
# will need to translate it.

# ---------------
# Provided functions
#
# These are all functions that were built in unit 3. They will help
# you as you write the grammar.
def grammar(description, whitespace = r'\s*'):
    '''
    Convert a description to a grammar. Each line is a rule for a
    non-terminal symbol; it looks like this:

        Symbol => A1 A2 ... | B1 B2 ... | C1 C2 ...

    where the right-hand side is one or more alternatives, separated by
    the '|' sign. Each alternative is a sequence of atoms, separated by
    spaces.  An atom is either a symbol on syme left-hand side, or it is a
    regular expression that will be passed to re.match to match a token.
    
    Notation for *, +, or ? not allowed in a rule alternative (but ok within a
    token). Use '\' to continue long lines. You must include spaces or tabs
    around '=>' and '|'. That's within the grammar description itself(...?). The
    grammar that gets defined allows whitespace between tokens by default or
    specify '' as the second argument to grammar() to disallow this (or supply
    any regular expression to describe allowable whitespace between
    tokens).'''
    G = {' ': whitespace}
    description = description.replace('\t', ' ') # no tabs allowed!
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def split(text, sep = None, maxsplit = -1):
    '''Like str.split applied to text, but strips whitespace from each piece.'''
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

def parse(start_symbol, text, grammar):
    '''Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure if remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'

    See: http://en.wikipedia.org/wiki/Parsing_expression_grammar
    '''

    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        '''
        Try to match the sequence of atoms against text.
        
        Parameters:
        sequence : an iterable of atoms
        text : a string

        Returns:
        Fail : if any atom in sequence does not match
        (tree, remainder) : the tree and remainder if the entire sequence matches text
        '''
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        '''
        Parameters:
        atom : either a key in grammar or a regular expression
        text : a string

        Returns:
        Fail : if no match can be found
        (tree, remainder) : if a match is found
            tree is the parse tree of the first match found
            remainder is the text that was not matched
        '''
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem  
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            return Fail if (not m) else (m.group(1), text[m.end():])
    
    return parse_atom(start_symbol, text)

Fail = (None, None)

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return functools.update_wrapper(d(fn), fn)
    functools.update_wrapper(_d, d)
    return _d

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
            # some element of args can't be a dict key
            return f(args)
    return _f

G = grammar(r'''
    Exp => Term [+-] Exp | Term
    Term => Factor [*/] Term | Factor
    Factor => Funcall | Var | Num | [(] Exp [)]
    Funcall => Var [(] Exps [)]
    Exps => Exp [,] Exps | Exp
    Var => [a-zA-Z_]\w*
    Num => [-+]?[0-9]+([.][0-9]*)?
''')

## Parsing URLs
## See http://www.w3.org/Addressing/URL/5_BNF.html

URL = grammar('''
    url => httpaddress | ftpaddress | mailtoaddress
    httpaddress => http:// hostport /path? ?search?
    ftpaddress => ftp:// login / path ; ftptype | ftp:// login / path
    /path? => / path | ()
    ?search? => [?] search | ()
    mailtoaddress => mailto: xalphas @ hostname
    hostport => host : port | host
    host => hostname | hostnumber
    hostname => ialpha . hostname | ialpha
    hostnumber => digits . digits . digits . digits
    ftptype => A formcode | E formcode | I | L digits
    formcode => [NTC]
    port => digits | path
    path => void | segment / path | segment
    segment => xalphas
    search => xalphas + search | xalphas
    login => userpassword hostport | hostport
    userpassword => user : password @ | user @
    user => alphanum2 user | alphanum2
    password => alphanum2 password | password
    path => void | segment / path | segment
    void => ()
    digits => digit digits | digit
    digit => [0-9]
    alpha => [a-zA-Z]
    safe => [-$_@.&+]
    extra => [()!*''""]
    escape => % hex hex
    hex => [0-9a-fA-F]
    alphanum => alpha | digit
    alphanums => alphanum alphanums | alphanum
    alphanum2 => alpha | digit | [-_.+]
    ialpha => alpha xalphas | alpha
    xalphas => xalpha xalphas | xalpha
    xalpha => alpha | digit | safe | extra | escape
''', whitespace = '()')

def verify(G):
    lhstokens = set(G) - set([' '])
    print(G.values())
    rhstokens = set(t for alts in G.values() for alt in alts for t in alt)
    def show(title, tokens): print title, '=', ' '.join(map(repr, sorted(tokens)))
    show('Non-Terms', G)
    show('Terminals', rhstokens - lhstokens)
    show('Suspects', [t for t in (rhstokens-lhstokens) if t.isalnum()])
    show('Orphans ', lhstokens-rhstokens)

JSON = grammar(r'''
    object => \{ members \} | \{\}
    members => pair , members | pair
    pair => string [\:] value
    array => \[ elements \] | \[\]
    elements => value [,] elements | value
    value => string | number | object | array
    string => \"[^"\\\\]*\" | \"\"
    number => int frac exp | int exp | int frac | int
    int => [-]?[\d][\d]*
    frac => \.[\d]*
    exp => [eE][+-]?[\d]+
''', whitespace='\s*')

#chars => char chars | char
#char => ^\\"\/\b\f\r\t\n
    
#string => " ([^"\\\\]*|\\\\["\\\\bfnrt\/]|\\\\u[0-9a-f]{4})* "
#number => -?(?=[1-9]|0(?!\d))\d+(\.\d+)?([eE][+-]?\d+)

def json_parse(text):
    return parse('value', text, JSON)

#["testing", 1, 2, 3]
#-123.456e+789
#{"age": 21, "state":"CO","occupation":"rides the rodeo"}
def test():
    # my new tests
    assert json_parse('-123') == (['value', ['number', ['int', '-123']]], '')
    assert json_parse('0.023') == (['value', ['number', ['int', '0'], ['frac', '.023']]], '')
    assert json_parse('1e023') == (['value', ['number', ['int', '1'], ['exp', 'e023']]], '')
    assert json_parse('1.03e023') == (['value', ['number', ['int', '1'], ['frac', '.03'], ['exp', 'e023']]], '')
    assert json_parse('"ab"') == (['value', ['string', '"ab"']], '')
    assert json_parse('{}') == (['value', ['object', '{', '}']], '')
    assert json_parse('{"name": 2}') == (['value', ['object', '{', ['members', ['pair', ['string', '"name"'], ':', ['value', ['number', ['int', '2']]]]], '}']], '')
    assert json_parse('{"age": "cool"}') == (['value', ['object', '{', ['members', ['pair', ['string', '"age"'], ':', ['value', ['string', '"cool"']]]], '}']], '')
    assert json_parse('[]') == (['value', ['array', '[', ']']], '')
    assert json_parse('[1]') == (['value', ['array', '[', ['elements', ['value', ['number', ['int', '1']]]], ']']], '')
    assert json_parse('[1, "new"]') == (['value', ['array', '[', ['elements', ['value', ['number', ['int', '1']]], ',', ['elements', ['value', ['string', '"new"']]]], ']']], '')
    # Original tests
    assert json_parse('["testing", 1, 2, 3]') == (                      
                       ['value', ['array', '[', ['elements', ['value', 
                       ['string', '"testing"']], ',', ['elements', ['value', ['number', 
                       ['int', '1']]], ',', ['elements', ['value', ['number', 
                       ['int', '2']]], ',', ['elements', ['value', ['number', 
                       ['int', '3']]]]]]], ']']], '')
    assert json_parse('-123.456e+789') == (
                       ['value', ['number', ['int', '-123'], ['frac', '.456'], ['exp', 'e+789']]], '')
    assert json_parse('{"age": 21, "state":"CO","occupation":"rides the rodeo"}') == (
                      ['value', ['object', '{', ['members', ['pair', ['string', '"age"'], 
                       ':', ['value', ['number', ['int', '21']]]], ',', ['members', 
                      ['pair', ['string', '"state"'], ':', ['value', ['string', '"CO"']]], 
                      ',', ['members', ['pair', ['string', '"occupation"'], ':', 
                      ['value', ['string', '"rides the rodeo"']]]]]], '}']], '')
    return 'tests pass'

#print test()

if __name__ == '__main__':
    # print(G)
    verify(G)    
    print(parse('Exp', '3*x + b', G))

    # print(URL)
    # verify(URL)
    # print(parse('url', 'http://www.w3.org/Addressing/URL/5_BNF.html', URL))

# Homework 3-2
# --------------
# User Instructions
#
# Write a function, inverse, which takes as input a monotonically
# increasing (always increasing) function that is defined on the 
# non-negative numbers. The runtime of your program should be 
# proportional to the LOGARITHM of the input. You may want to 
# do some research into binary search and Newton's method to 
# help you out.
#
# This function should return another function which computes the
# inverse of the input function. 
#
# Your inverse function should also take an optional parameter, 
# delta, as input so that the computed value of the inverse will
# be within delta of the true value.

# -------------
# Grading Notes
#
# Your function will be called with three test cases. The 
# input numbers will be large enough that your submission
# will only terminate in the allotted time if it is 
# efficient enough. 

def slow_inverse(f, delta=1/128.):
    '''Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta.'''
    def f_1(y):
        x = 0
        #count = 0
        while f(x) < y:
            x += delta
            #count += 1
        #print(count)
        return x if (f(x)-y < y-f(x-delta)) else x-delta
    return f_1 

from copy import copy
def inverse(f, delta = 1/128.):
    '''Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta.'''
    def f_1(y):
        x, x_min = 0, 0
        #count = 0
        delta2 = copy(delta)
        while True:
            # Reset x to the value of x_min; this result will be successively closer 
            # to correct with each completed "child" while loop (below).
            x = x_min
            while f(x) < y:
                x_min = x
                x += delta2
                #count += 1
                delta2 *= 2
            if abs(x-x_min) <= delta: break # Breaks out of the parent "True" loop.
            delta2 = copy(delta) # Take a new copy of delta.
        #print(count)
        return x if (f(x)-y < y-f(x-delta)) else x-delta
    return f_1
    
def square(x): return x*x
sqrt = slow_inverse(square)
sqrt2 = inverse(square)

# Homework 3-3
# ---------------
# User Instructions
#
# Write a function, findtags(text), that takes a string of text
# as input and returns a list of all the html start tags in the 
# text. It may be helpful to use regular expressions to solve
# this problem.

import re

def findtags(text):
    # your code here
    pass
    #<([^/]+)>|<[^\d]> Works on text 1
    #<[^/][ ]* WIP

testtext1 = '''
My favorite website in the world is probably 
<a href="www.udacity.com">Udacity</a>. If you want 
that link to open in a <b>new tab</b> by default, you should
write <a href="www.udacity.com"target="_blank">Udacity</a>
instead!
'''

testtext2 = '''
Okay, so you passed the first test case. <let's see> how you 
handle this one. Did you know that 2 < 3 should return True? 
So should 3 > 2. But 2 > 3 is always False.
'''

testtext3 = '''
It's not common, but we can put a LOT of whitespace into 
our HTML tags. For example, we can make something bold by
doing <         b           > this <   /b    >, Though I 
don't know why you would ever want to.
'''

def test():
    assert findtags(testtext1) == ['<a href="www.udacity.com">', 
                                   '<b>', 
                                   '<a href="www.udacity.com"target="_blank">']
    assert findtags(testtext2) == []
    assert findtags(testtext3) == ['<         b           >']
    return 'tests pass'

print test()