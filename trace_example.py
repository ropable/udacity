import sys
import linecache


def remove_html_markup(s):
    # This function is a generic example.
    tag = False
    quote = False
    out = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"':
            quote = not quote
        elif not tag:
            out = out + c
    return out


def traceit(frame, event, arg):
    if event == "line":
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        #print filename, lineno,
        print(linecache.getline(filename, lineno).rstrip())
    return traceit


def test():
    sys.settrace(traceit)
    remove_html_markup('"<b>foo</b>"')
    sys.settrace(None)

test()
