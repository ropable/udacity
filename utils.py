from __future__ import division
import time
from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def trace(f):
    indent = '   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level += 1
        try:
            result = f(*args)
            print '%s<-- %s == %s' % ((trace.level-1)*indent,
                                      signature, result)
        finally:
            trace.level -= 1
        return result
    trace.level = 0
    return _f

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
            # some element of args refuses to be a dict key
            return f(args)
    _f.cache = cache
    return _f

def average(numbers):
    '''Return the average (arithmetic mean) of a sequence of numbers.'''
    return sum(numbers) / float(len(numbers))
    
def timedcall(fn, *args):
    '''Call function with args; return the time in seconds and results.'''
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result
    
def timedcalls(n, fn, *args):
    '''Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time.'''
    if (isinstance(n, int)):
        times = [timedcall(fn,*args)[0] for _ in range(n)]
    else:
        times = []
        while sum(times) < n:
            times.append(timedcall(fn,*args)[0])
    return min(times), average(times), max(times)