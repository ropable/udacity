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
    assert test(s) == "FAIL"

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
the_state = {}
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

    failure_vars = []  # List to store candicate failing vars (var, value)

    # Test over multiple locations
    for (line, iteration) in locations:

        # Get the passing and the failing state
        state_pass = get_state(html_pass, line, iteration)
        state_fail = get_state(html_fail, line, iteration)

        # Compute the differences
        # diffs is a list of (var, val) pairs from a failing test, that differ
        # from those in a passing test.
        diffs = []
        for var, value in state_fail.iteritems():
            if var in state_pass and state_pass[var] != value:
                diffs.append((var, value))

        # Minimize the failure-inducing set of differences
        the_input = html_pass
        the_line = line
        the_iteration = iteration

        # ddmin will return an Exception if diffs is empty.
        # In this instance, just pass diffs through as the cause.
        try:
            cause = ddmin(diffs)
        except:
            cause = diffs

        if cause:
            for var in cause:
                if var not in failure_vars:
                    failure_vars.append(var)

    print "The program was started with", repr(html_fail)
    for var in failure_vars:
        print("Then {0} became {1}".format(repr(var[0]), repr(var[1])))
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
