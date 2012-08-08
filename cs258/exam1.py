import random
import math

content = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Phasellus sollicitudin condimentum libero,
sit amet ultrices lacus faucibus nec.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Cum sociis natoque penatibus et magnis dis parturient montes,
nascetur ridiculus mus. Cras nulla nisi, accumsan gravida commodo et,
venenatis dignissim quam. Mauris rutrum ullamcorper consectetur.
Nunc luctus dui eu libero fringilla tempor. Integer vitae libero purus.
Fusce est dui, suscipit mollis pellentesque vel, cursus sed sapien.
Duis quam nibh, dictum ut dictum eget, ultrices in tortor.
In hac habitasse platea dictumst. Morbi et leo enim.
Aenean ipsum ipsum, laoreet vel cursus a, tincidunt ultrices augue.
Aliquam ac erat eget nunc lacinia imperdiet vel id nulla."""
fuzz_factor = 2

def fuzzit(content):
    # Sanity check.
    if not isinstance(content, str): return []
    strings = []
    buf = bytearray(content)
    numwrites = random.randrange(math.ceil((float(len(buf))/fuzz_factor))) + 1
    #for n in range(numwrites): # Would not pass!
    for n in range(100): # Passed!
        buf[random.randrange(len(buf))] = random.randrange(256)
        strings.append(str(buf))
    return strings, numwrites
