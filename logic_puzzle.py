"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools

def day_after(d1, d2):
    "Day d1 is the day after d2 if d1-d2 == 1"
    return d1-d2 == 1

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    days = [Monday, Tuesday, Wednesday, Thursday, Friday] = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(days))
    d = next((Hamming, Knuth, Minsky, Simon, Wilkes)
        for (laptop, droid, tablet, iphone, lunch) in orderings
            if laptop is Wednesday and tablet is not Friday and (iphone is Tuesday or tablet is Tuesday)
        for (programmer, writer, manager, designer, admin) in orderings
            if designer is not Thursday and designer is not droid and manager is not tablet
        for (Hamming, Knuth, Minsky, Simon, Wilkes) in orderings
            if day_after(Knuth, Simon) and day_after(Knuth, manager) and Wilkes is not programmer and Minsky is not writer and Knuth is not manager and ((Wilkes is laptop and writer is Monday) or (Wilkes is Monday and writer is laptop)) and ((Wilkes is programmer and Hamming is droid) or (Wilkes is droid and Hamming is programmer))
    )
    l = sorted(zip(d, ['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']))
    return [b for a, b in l]
