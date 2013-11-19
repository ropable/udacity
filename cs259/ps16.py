#!/usr/bin/env python
# Simple debugger
# See instructions around line 36

import sys
import readline

# Our buggy program
def remove_html_markup(s):
    tag   = False
    quote = False
    out   = ""

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

# main program that runs the buggy program
def main():
    print remove_html_markup('xyz')
    print remove_html_markup('"<b>foo</b>"')
    print remove_html_markup("'<b>foo</b>'")

# globals
breakpoints = {14: True}
watchpoints = {'c': True}
stepping = False

"""
Our debug function
Improve and expand the debug function to accept
a watchpoint command 'w <var name>'.
Add the variable name to the watchpoints dictionary
or print 'You must supply a variable name'
if 'w' is not followed by a string.
"""
def debug(command, my_locals):
    global stepping
    global breakpoints
    global watchpoints
    watched_vars = {}

    if command.find(' ') > 0:
        arg = command.split(' ')[1]
    else:
        arg = None

    if command.startswith('s'):     # step
        stepping = True
        return True
    elif command.startswith('c'):   # continue
        stepping = False
        return True
    elif command.startswith('p'):    # print
        if arg and arg in my_locals:
            print('{0} = {1}'.format(arg, repr(my_locals[arg])))
        elif arg and arg not in my_locals:
            print('No such variable: {0}'.format(arg))
        else:
            print(repr(my_locals))
    elif command.startswith('b'):    # breakpoint
        if arg:
            try:
                breakpoints[int(arg)] = True
            except ValueError:
                print('You must supply a line number')
        else:
            print('You must supply a line number')
    elif command.startswith('w'):    # watch variable
        if arg and arg in my_locals:
            watchpoints[arg] = True
            watched_vars[arg] = my_locals[arg]
        else:
            print('You must supply a variable name')
    elif command.startswith('q'):   # quit
        print "Exiting my-spyder..."
        sys.exit(0)
    else:
        print "No such command", repr(command)
    # Check if watched variables have changed.
    for k, v in my_locals.iteritems():
        if k in watched_vars and v != watched_vars[k]:
            print(repr(my_locals[k]))
            watched_vars[k] = my_locals[k]
    return False

commands = ["w out", "c", "c", "c", "c", "c", "c", "q"]

def input_command():
    #command = raw_input("(my-spyder) ")
    global commands
    command = commands.pop(0)
    return command

def traceit(frame, event, trace_arg):
    global stepping

    if event == 'line':
        if stepping or breakpoints.has_key(frame.f_lineno):
            resume = False
            while not resume:
                print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals
                command = input_command()
                resume = debug(command, frame.f_locals)
    return traceit

# Using the tracer
sys.settrace(traceit)
main()
sys.settrace(None)

#Simple test
print watchpoints
debug("w s", {'s': 'xyz', 'tag': False})
print watchpoints
#>>> {'c': True}
#>>> {'c': True, 's': True}
