#!/usr/bin/env python
import sys
import copy


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


def ddmin(s):
    # you may need to use this to test if the values you pass actually make
    # test fail.
    try:
        assert test(s) == "FAIL"
    except:
        return None

    n = 2     # Initial granularity
    while len(s) >= 2:
        start = 0
        subset_length = len(s) / n
        some_complement_is_failing = False

        while start < len(s):
            complement = s[:start] + s[start + subset_length:]

            if test(complement) == "FAIL":
                s = complement
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break

            start += subset_length

        if not some_complement_is_failing:
            if n == len(s):
                break
            n = min(n * 2, len(s))

    return s


# Use this function to record the covered lines in the program, in order of
# their execution and save in the list coverage
coverage = []


def traceit(frame, event, arg):
    global coverage

    if event == 'line':
        coverage.append(frame.f_lineno)

    return traceit

# We use these variables to communicate between callbacks and drivers
the_line = None
the_iteration = None
the_state = None
the_diff = None
the_input = None


def trace_fetch_state(frame, event, arg):
    # Stop at THE_LINE/THE_ITERATION and store the state in THE_STATE
    global the_line
    global the_iteration
    global the_state

    if frame.f_lineno == the_line:
        the_iteration = the_iteration - 1
        if the_iteration == 0:
            the_state = copy.deepcopy(frame.f_locals)
            the_line = None  # Don't get called again
            return None      # Don't get called again

    return trace_fetch_state


def get_state(input_str, line, iteration):
    # Get the state at LINE/ITERATION
    global the_line
    global the_iteration
    global the_state

    the_line = line
    the_iteration = iteration
    sys.settrace(trace_fetch_state)
    remove_html_markup(input_str)
    sys.settrace(None)
    assert isinstance(the_state, dict)

    return the_state


def trace_apply_diff(frame, event, arg):
    # Stop at THE_LINE/THE_ITERATION and apply the differences in THE_DIFF
    global the_line
    global the_diff
    global the_iteration

    if frame.f_lineno == the_line:
        the_iteration = the_iteration - 1
        if the_iteration == 0:
            frame.f_locals.update(the_diff)
            the_line = None
            return None  # Don't get called again

    return trace_apply_diff


def test(diffs):
    # Testing function: Call remove_html_output, stop at THE_LINE/THE_ITERATION,
    # and apply the diffs in DIFFS at THE_LINE
    global the_diff
    global the_input
    global the_line
    global the_iteration

    line = the_line
    iteration = the_iteration

    the_diff = diffs
    sys.settrace(trace_apply_diff)
    y = remove_html_markup(the_input)
    sys.settrace(None)

    the_line = line
    the_iteration = iteration

    if y.find('<') == -1:
        return "PASS"
    else:
        return "FAIL"


def make_locations(coverage):
    # This function should return a list of tuples in the format
    # [(line, iteration), (line, iteration) ...], as auto_cause_chain
    # expects.
    locations, tmp = [], []

    for l in coverage:
        tmp.append(l)  # Append the item into tmp, to derive counts/iterations.
        locations.append((l, tmp.count(l)))

    return locations


def auto_cause_chain(locations):
    global html_fail, html_pass, the_input, the_line, the_iteration, the_diff
    print "The program was started with", repr(html_fail)

    candidates = []  # List to store candicate failing vars (var, value)

    # Test over multiple locations
    for (line, iteration) in locations:

        # Get the passing and the failing state
        state_pass = get_state(html_pass, line, iteration)
        state_fail = get_state(html_fail, line, iteration)

        # Compute the differences
        diffs = []
        for var in state_fail:
            if not var in state_pass or state_pass[var] != state_fail[var]:
                diffs.append((var, state_fail[var]))
        # diffs is a list of tuples (var, value) that differ from a passing test.

        # Minimize the failure-inducing set of differences
        the_input = html_pass
        the_line = line
        the_iteration = iteration

        cause = ddmin(diffs)  # You have to check out if cause has more than one tuple in it,
                            # one may cause a failure and one may not.
        # if length of cause is greater than one, you have to send it through ddmin again.

        if cause:
            if len(cause) > 1:
                for tup in cause:
                    newcause = ddmin(tup)
                    if newcause:
                        if newcause[0] not in candidates:   # candidates is a list of tuples
                                # it is initialized just above the for loop in auto_cause_chain.
                            candidates.append(newcause[0])

            else:
                if cause[0] not in candidates:
                    candidates.append(cause[0])

    for tup in candidates:
        var = tup[0]
        value = tup[1]
        print "Then", repr(var), 'became', repr(value)
    print "Then the program failed."

###### Testing runs

# We will test your function with different strings and on a different function
html_fail = '"<b>foo</b>"'
html_pass = "'<b>foo</b>'"

# This will fill the coverage variable with all lines executed in a failing run
sys.settrace(traceit)
remove_html_markup(html_fail)
sys.settrace(None)

locations = make_locations(coverage)
auto_cause_chain(locations)
