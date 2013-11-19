#!/usr/bin/env python
# Simple Daikon-style invariant checker
# Andreas Zeller, May 2012
# Complete the provided code, using your code from
# first exercise and adding ability to infer assertions
# for variable type, set and relations
# Modify only the classes Range and Invariants,
# if you need additional functions, make sure
# they are inside the classes.

import sys
import math
import random

def square_root(x, eps = 0.00001):
    assert x >= 0
    y = math.sqrt(x)
    assert abs(square(y) - x) <= eps
    return y

def square(x):
    return x * x

def double(x):
    return abs(20 * x) + 10

# The Range class tracks the types and value ranges for a single variable.
class Range:
    def __init__(self):
        self.min  = None  # Minimum value seen
        self.max  = None  # Maximum value seen
        self.type = None  # Type of variable
        self.set = set()  # Set of values taken

    def track(self, value):
        # Set initial min/max values.
        if not self.min and not self.max:
            self.min, self.max = value, value
        if value < self.min:
            self.min = value
        if value > self.max:
            self.max = value
        #self.type = value.__class__
        self.type = value
        self.set.update([value])

    def __repr__(self):
        return repr(self.type) + " " + repr(self.min) + ".." + repr(self.max)+ " " + repr(self.set)


# The Invariants class tracks all Ranges for all variables seen.
class Invariants:
    def __init__(self):
        # Mapping (Function Name) -> (Event type) -> (Variable Name)
        # e.g. self.vars["sqrt"]["call"]["x"] = Range()
        # holds the range for the argument x when calling sqrt(x)
        self.vars = {}

    def track(self, frame, event, arg):
        #print(frame.f_locals)
        #print(event)
        #print(arg)
        if event == "call" or event == "return":
            # If the event is "return", the return value
            # is kept in the 'arg' argument to this function.
            # Use it to keep track of variable "ret" (return)
            for k, v in frame.f_locals.iteritems():
                #print(k, v)
                if not frame.f_code.co_name in self.vars:
                    self.vars[frame.f_code.co_name] = {}
                if not event in self.vars[frame.f_code.co_name]:
                    self.vars[frame.f_code.co_name][event] = {}
                if not k in self.vars[frame.f_code.co_name][event]:
                    self.vars[frame.f_code.co_name][event][k] = Range()
                self.vars[frame.f_code.co_name][event][k].track(v)
                if event == 'return':
                    if not 'ret' in self.vars[frame.f_code.co_name][event]:
                        self.vars[frame.f_code.co_name][event]['ret'] = Range()
                    self.vars[frame.f_code.co_name][event]['ret'].track(arg)
                print(self.vars[frame.f_code.co_name][event][k])

    def __repr__(self):
        # Return the tracked invariants
        s = ""
        for function, events in self.vars.iteritems():
            for event, vars in events.iteritems():
                s += event + " " + function + ":\n"

                for var, range in vars.iteritems():
                    # isinstance
                    s += "    assert isinstance({0}, type({1})\n".format(var, repr(range.type))
                    # set
                    s += "    asset {0} in {1}\n".format(var, repr(range.set))
                    # range
                    s += "    assert "
                    if range.min == range.max:
                        s += var + " == " + repr(range.min)
                    else:
                        s += repr(range.min) + " <= " + var + " <= " + repr(range.max)
                    s += "\n"
                    # ADD HERE RELATIONS BETWEEN VARIABLES
                    # RELATIONS SHOULD BE ONE OF: ==, <=, >=
                    #s += "    assert " + var + " >= " + var2 + "\n"
        return s

invariants = Invariants()

def traceit(frame, event, arg):
    invariants.track(frame, event, arg)
    return traceit

sys.settrace(traceit)
# Tester. Increase the range for more precise results when running locally
eps = 0.000001
test_vars = [34.6363, 9.348, -293438.402]
for i in test_vars:
#for i in range(1, 10):
    z = double(i)
sys.settrace(None)
print invariants

# Example sample of a correct output:
"""
return double:
    assert isinstance(x, type(-293438.402))
    assert x in set([9.348, -293438.402, 34.6363])
    assert -293438.402 <= x <= 34.6363
    assert x <= ret
"""
