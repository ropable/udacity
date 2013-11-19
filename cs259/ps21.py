#!/usr/bin/env python
# Simple Daikon-style invariant checker
# Andreas Zeller, May 2012
# Complete the provided code around lines 28 and 44
# Do not modify the __repr__ functions.
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

# The Range class tracks the types and value ranges for a single variable.
class Range:
    def __init__(self):
        self.min  = None  # Minimum value seen
        self.max  = None  # Maximum value seen

    # Invoke this for every value
    def track(self, value):
        # Set initial min/max values.
        if not self.min and not self.max:
            self.min, self.max = value, value
        if value < self.min:
            self.min = value
        if value > self.max:
            self.max = value

    def __repr__(self):
        return repr(self.min) + ".." + repr(self.max)


# The Invariants class tracks all Ranges for all variables seen.
class Invariants:
    def __init__(self):
        # Mapping (Function Name) -> (Event type) -> (Variable Name)
        # e.g. self.vars["sqrt"]["call"]["x"] = Range()
        # holds the range for the argument x when calling sqrt(x)
        self.vars = {}

    def track(self, frame, event, arg):
        if event == "call" or event == "return":
            # If the event is "return", the return value
            # is kept in the 'arg' argument to this function.
            # Use it to keep track of variable "ret" (return)
            for k, v in frame.f_locals.iteritems():
                if not frame.f_code.co_name in self.vars:
                    self.vars[frame.f_code.co_name] = {}
                if not event in self.vars[frame.f_code.co_name]:
                    self.vars[frame.f_code.co_name][event] = {}
                if not k in self.vars[frame.f_code.co_name][event]:
                    self.vars[frame.f_code.co_name][event][k] = Range()
                if event == 'return':
                    if not 'ret' in self.vars[frame.f_code.co_name][event]:
                        self.vars[frame.f_code.co_name][event]['ret'] = Range()
                    self.vars[frame.f_code.co_name][event]['ret'].track(arg)
                self.vars[frame.f_code.co_name][event][k].track(v)

    def __repr__(self):
        # Return the tracked invariants
        s = ""
        for function, events in self.vars.iteritems():
            for event, vars in events.iteritems():
                s += event + " " + function + ":\n"
                # continue

                for var, range in vars.iteritems():
                    s += "    assert "
                    if range.min == range.max:
                        s += var + " == " + repr(range.min)
                    else:
                        s += repr(range.min) + " <= " + var + " <= " + repr(range.max)
                    s += "\n"

        return s

invariants = Invariants()

def traceit(frame, event, arg):
    invariants.track(frame, event, arg)
    return traceit

sys.settrace(traceit)
# Tester. Increase the range for more precise results when running locally
eps = 0.000001
for i in range(1, 10):
    r = int(random.random() * 1000) # An integer value between 0 and 999.99
    z = square_root(r, eps)
    z = square(z)
sys.settrace(None)
print invariants
