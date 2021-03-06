#!/usr/bin/env python
import sys
import math
# INSTRUCTIONS !
# This provided, working code calculates phi coefficients for each code line.
# Make sure that you understand how this works, then modify the traceit
# function to work for function calls instead of lines. It should save the
# function name and the return value of the function for each function call.
# Use the mystery function that can be found at line 155 and the
# test cases at line 180 for this exercise.
# Modify the provided functions to use this information to calculate
# phi values for the function calls as described in the video.
# You should get 3 phi values for each function - one for positive values (1),
# one for 0 values and one for negative values (-1), called "bins" in the video.
# When you have found out which function call and which return value type (bin)
# correlates the most with failure, fill in the following 3 variables,
# Do NOT set these values dynamically.

answer_function = "X"   # One of f1, f2, f3
answer_bin = 42         # One of 1, 0, -1
answer_value = 1.0000   # precision to 4 decimal places.


def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:

        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c

    return out


# global variable to keep the coverage data in
coverage = {}
# Tracing function that saves the coverage data
# To track function calls, you will have to check 'if event == "return"', and in
# that case the variable arg will hold the return value of the function,
# and frame.f_code.co_name will hold the function name
return_arg = None
func_name = None


def traceit(frame, event, arg):
    #global coverage
    global return_arg
    global func_name

    #if event == "line":
    if event == "return":
        return_arg = arg
        func_name = frame.f_code.co_name
        #filename = frame.f_code.co_filename
        #lineno   = frame.f_lineno
        #if not coverage.has_key(filename):
        #    coverage[filename] = {}
        #coverage[filename][lineno] = True

    return traceit


def phi(n11, n10, n01, n00):
    # Calculate phi coefficient from given values
    return ((n11 * n00 - n10 * n01) / math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))


def print_tables(tables):
    # Print out values of phi, and result of runs for each covered line
    for filename in tables.keys():
        lines = open(filename).readlines()
        for i in range(23, 40):  # lines of the remove_html_markup in this file
            if (i + 1) in tables[filename]:
                (n11, n10, n01, n00) = tables[filename][i + 1]
                try:
                    factor = phi(n11, n10, n01, n00)
                    prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
                except:
                    prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)

            else:
                prefix = "               "

            print prefix, lines[i],


def run_tests(inputs):
    runs = []
    for input in inputs:
        global coverage
        coverage = {}
        sys.settrace(traceit)
        result = remove_html_markup(input)
        sys.settrace(None)

        if result.find('<') == -1:
            outcome = "PASS"
        else:
            outcome = "FAIL"

        runs.append((input, outcome, coverage))
    return runs


def init_tables(runs):
    # Create empty tuples for each covered line
    tables = {}
    for (input, outcome, coverage) in runs:
        for filename, lines in coverage.iteritems():
            for line in lines.keys():
                if not filename in tables:
                    tables[filename] = {}
                if not line in tables[filename]:
                    tables[filename][line] = (0, 0, 0, 0)

    return tables


def compute_n(tables):
    # Compute n11, n10, etc. for each line
    for filename, lines in tables.iteritems():
        for line in lines.keys():
            (n11, n10, n01, n00) = tables[filename][line]
            for (input, outcome, coverage) in runs:
                if filename in coverage and line in coverage[filename]:
                    # Covered in this run
                    if outcome == "FAIL":
                        n11 += 1  # covered and fails
                    else:
                        n10 += 1  # covered and passes
                else:
                    # Not covered in this run
                    if outcome == "FAIL":
                        n01 += 1  # uncovered and fails
                    else:
                        n00 += 1  # uncovered and passes
            tables[filename][line] = (n11, n10, n01, n00)
    return tables

# Now compute (and report) phi for each line. The higher the value,
# the more likely the line is the cause of the failures.

# These are the test cases
inputs_line = [
    'foo',
    '<b>foo</b>',
    '"<b>foo</b>"',
    '"foo"',
    "'foo'",
    '<em>foo</em>',
    '<a href="foo">foo</a>',
    '""',
    "<p>"]
runs = run_tests(inputs_line)

tables = init_tables(runs)
print tables

tables = compute_n(tables)

print_tables(tables)

###### MYSTERY FUNCTION
returns = []


def mystery(magic):
    global return_arg
    global func_name
    global returns

    assert type(magic) == tuple
    assert len(magic) == 3

    l, s, n = magic

    tmp = []
    sys.settrace(traceit)
    r1 = f1(l)
    sys.settrace(None)
    tmp.append([func_name, return_arg])

    sys.settrace(traceit)
    r2 = f2(s)
    sys.settrace(None)
    tmp.append([func_name, return_arg])

    sys.settrace(traceit)
    r3 = f3(n)
    sys.settrace(None)
    tmp.append([func_name, return_arg])

    if -1 in [r1, r2, r3]:
        i = "FAIL"
    elif r3 < 0:
        i = "FAIL"
    elif not r1 or not r2:
        i = "FAIL"
    else:
        i = "PASS"

    for t in tmp:
        t.append(i)
        returns.append(tuple(t))
    # Now we have a list of tuples: (function, return, PASS/FAIL)

    return i


# These are the input values you should test the mystery function with
inputs = [
    ([1, 2], "ab", 10),
    ([1, 2], "ab", 2),
    ([1, 2], "ab", 12),
    ([1, 2], "ab", 21),
    ("a", 1, [1]),
    ([1], "a", 1),
    ([1, 2], "abcd", 8),
    ([1, 2, 3, 4, 5], "abcde", 8),
    ([1, 2, 3, 4, 5], "abcdefgijkl", 18),
    ([1, 2, 3, 4, 5, 6, 7], "abcdefghij", 5)]


def f1(ml):
    if type(ml) is not list:
        return -1
    elif len(ml) < 6:
        return len(ml)
    else:
        return 0


def f2(ms):
    if type(ms) is not str:
        return -1
    elif len(ms) < 6:
        return len(ms)
    else:
        return 0


def f3(mn):
    if type(mn) is not int:
        return -1
    if mn > 10:
        return -100
    else:
        return mn


# Actually run the mystery function with the inputs
for i in inputs:
    mystery(i)


#{'n11': 0, 'n10': 0, 'n01': 0, 'n00': 0}
d = {
    'f1': {
        'pos': [0, 0, 0, 0],
        'zero': [0, 0, 0, 0],
        'neg': [0, 0, 0, 0]
    },
    'f2': {
        'pos': [0, 0, 0, 0],
        'zero': [0, 0, 0, 0],
        'neg': [0, 0, 0, 0]
    },
    'f3': {
        'pos': [0, 0, 0, 0],
        'zero': [0, 0, 0, 0],
        'neg': [0, 0, 0, 0]
    },
}

for i in returns:
    if i[0] == 'f1':  # f1
        if i[1] > 0:  # Positive
            if i[2] == 'PASS':
                d['f1']['pos'][0] += 1
            else:
                d['f1']['pos'][1] += 1
        else:  # Zero or negative.
            if i[2] == 'PASS':
                d['f1']['pos'][2] += 1
            else:
                d['f1']['pos'][3] += 1
        if i[1] == 0:  # Zero
            if i[2] == 'PASS':
                d['f1']['zero'][0] += 1
            else:
                d['f1']['zero'][1] += 1
        else:  # Positive or negative.
            if i[2] == 'PASS':
                d['f1']['zero'][2] += 1
            else:
                d['f1']['zero'][3] += 1
        if i[1] < 0:  # negative
            if i[2] == 'PASS':
                d['f1']['neg'][0] += 1
            else:
                d['f1']['neg'][1] += 1
        else:  # Positive or negative.
            if i[2] == 'PASS':
                d['f1']['neg'][2] += 1
            else:
                d['f1']['neg'][3] += 1
    if i[0] == 'f2':  # f2
        if i[1] > 0:  # Positive
            if i[2] == 'PASS':
                d['f2']['pos'][0] += 1
            else:
                d['f2']['pos'][1] += 1
        else:  # Zero or negative.
            if i[2] == 'PASS':
                d['f2']['pos'][2] += 1
            else:
                d['f2']['pos'][3] += 1
        if i[1] == 0:  # Zero
            if i[2] == 'PASS':
                d['f2']['zero'][0] += 1
            else:
                d['f2']['zero'][1] += 1
        else:  # Positive or negative.
            if i[2] == 'PASS':
                d['f2']['zero'][2] += 1
            else:
                d['f2']['zero'][3] += 1
        if i[1] < 0:  # negative
            if i[2] == 'PASS':
                d['f2']['neg'][0] += 1
            else:
                d['f2']['neg'][1] += 1
        else:  # Positive or negative.
            if i[2] == 'PASS':
                d['f2']['neg'][2] += 1
            else:
                d['f2']['neg'][3] += 1
    if i[0] == 'f3':  # f3
        if i[1] > 0:  # Positive
            if i[2] == 'PASS':
                d['f3']['pos'][0] += 1
            else:
                d['f3']['pos'][1] += 1
        else:  # Zero or negative.
            if i[2] == 'PASS':
                d['f3']['pos'][2] += 1
            else:
                d['f3']['pos'][3] += 1
        if i[1] == 0:  # Zero
            if i[2] == 'PASS':
                d['f3']['zero'][0] += 1
            else:
                d['f3']['zero'][1] += 1
        else:  # Positive or negative.
            if i[2] == 'PASS':
                d['f3']['zero'][2] += 1
            else:
                d['f3']['zero'][3] += 1
        if i[1] < 0:  # negative
            if i[2] == 'PASS':
                d['f3']['neg'][0] += 1
            else:
                d['f3']['neg'][1] += 1
        else:  # Positive or negative.
            if i[2] == 'PASS':
                d['f3']['neg'][2] += 1
            else:
                d['f3']['neg'][3] += 1


answer_function = "X"   # One of f1, f2, f3
answer_bin = 42         # One of 1, 0, -1
answer_value = 0   # precision to 4 decimal places.

print d

for func, tables in d.iteritems():
    for group, values in tables.iteritems():
        try:
            phi_val = round(phi(*values), 4)
        except:
            phi_val = None
        #print('{0}: {1} phi={2}'.format(func, group, phi_val))

        if phi_val and phi_val > answer_value:
            answer_value = phi_val
            answer_function = func
            answer_bin = group

print answer_function
print answer_bin
print answer_value
