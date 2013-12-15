#!/usr/bin/env python
import sys
#import readline


def remove_html_markup(s):
    # Our buggy program
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


def main():
    # main program that runs the buggy program
    print remove_html_markup('"<b>foo</b>"')

# globals
breakpoints = {}
watchpoints = {"quote": True}
watch_values = {}
stepping = True


def debug(command, my_locals):
    """
    Our debug function
    """
    global stepping
    global breakpoints
    global watchpoints
    global watch_values

    if command.find(' ') > 0:
        cmd = command.split(' ')
        if cmd[0].startswith('d'):  # delete - expects d <type> <argument>
            d_type = cmd[1]
            arg = cmd[2]
        else:
            arg = command.split(' ')[1]
    else:
        arg = None

    if command.startswith('s'):  # step
        stepping = True
        return True
    elif command.startswith('c'):  # continue
        stepping = False
        return True
    elif command.startswith('p'):  # print
        if arg and arg in my_locals:
            print('{0} = {1}'.format(arg, repr(my_locals[arg])))
        elif arg and arg not in my_locals:
            print('No such variable: {0}'.format(arg))
        else:
            print(repr(my_locals))
    elif command.startswith('b'):  # breakpoint
        if arg:
            try:
                breakpoints[int(arg)] = True  # Try to cast arg as as integer.
            except ValueError:
                print('You must supply a line number')
        else:
            print('You must supply a line number')
    elif command.startswith('w'):  # watch
        if arg:
            watchpoints[arg] = True
        else:
            print('You must supply a variable name')
    elif command.startswith('d'):
        if d_type == 'b':
            try:
                arg = int(arg)
            except ValueError:
                print('You must supply a line number')
            if not isinstance(arg, int):  # Mismatch
                print "Incorrect command"
            if arg in breakpoints:
                breakpoints.pop(arg)
            else:
                print "No such breakpoint defined", repr(arg)
        if d_type == 'w':
            if not isinstance(arg, str):  # Mismatch
                print "Incorrect command"
                breakpoints[int(arg)] = True
            if arg in watchpoints:
                watchpoints.pop(arg)
            else:
                print arg, "is not defined as watchpoint"
    elif command.startswith('q'):   # quit
        print "Exiting my-spyder..."
        sys.exit(0)
    else:
        print "No such command", repr(command)

    return False

commands = ["w c", "c", "c", "w out", "c", "c", "c", "q"]


def input_command():
    #command = raw_input("(my-spyder) ")
    global commands
    command = commands.pop(0)
    return command

"""
Our traceit function
Improve the traceit function to watch for variables in the watchpoint
dictionary and print out (literally like that):
event, frame.f_lineno, frame.f_code.co_name
and then the values of the variables, each in new line, in a format:
somevar ":", "Initialized"), "=>", repr(somevalue)
if the value was not set, and got set in the line, or
somevar ":", repr(old-value), "=>", repr(new-value)
when the value of the variable has changed.
If the value is unchanged, do not print anything.
"""


def traceit(frame, event, trace_arg):
    global stepping
    global watchpoints
    global watch_values

    if event == 'line':
        # Check if watched variables have changed, or need to be initialised.
        for k, v in frame.f_locals.iteritems():
            if k in watchpoints and watchpoints[k]:  # Watched variable == True
                if k in watch_values and v != watch_values[k]:  # Initialised, changed.
                    stepping = True  # Begin stepping.
                    print event, frame.f_lineno, frame.f_code.co_name
                    print("{0} : {1} => {2}".format(k, repr(watch_values[k]), repr(frame.f_locals[k])))
                    watch_values[k] = frame.f_locals[k]
                elif k not in watch_values:  # Variable needs to be initialised.
                    stepping = True  # Begin stepping.
                    print event, frame.f_lineno, frame.f_code.co_name
                    print("{0} : Initialized => {1}".format(k, repr(frame.f_locals[k])))
                    watch_values[k] = frame.f_locals[k]

        if stepping or frame.f_lineno in breakpoints:
            resume = False
            while not resume:
                command = input_command()
                resume = debug(command, frame.f_locals)

    return traceit

# Using the tracer
sys.settrace(traceit)
main()
sys.settrace(None)

# with the commands = ["w c", "c", "c", "w out", "c", "c", "c", "q"],
# the output should look like this (line numbers may be different):
#line 26 main {}
#line 10 remove_html_markup
#quote : Initialized => False
#line 13 remove_html_markup
#c : Initialized => '"'
#line 19 remove_html_markup
#quote : False => True
#line 13 remove_html_markup
#c : '"' => '<'
#line 21 remove_html_markup
#out : '' => '<'
#Exiting my-spyder...
