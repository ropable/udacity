# concise definition of the Luhn checksum:
#
# "For a card with an even number of digits, double every odd numbered
# digit and subtract 9 if the product is greater than 9. Add up all
# the even digits as well as the doubled-odd digits, and the result
# must be a multiple of 10 or it's not a valid card. If the card has
# an odd number of digits, perform the same addition doubling the even
# numbered digits instead."
#
# for more details see here:
# http://www.merriampark.com/anatomycc.htm
#
# also see the Wikipedia entry, but don't do that unless you really
# want the answer, since it contains working Python code!
#
# Implement the Luhn Checksum algorithm as described above.

# is_luhn_valid takes a credit card number as input and verifies
# whether it is valid or not. If it is valid, it returns True,
# otherwise it returns False.

def is_luhn_valid(n):
    n = str(n)
    if len(n)%2: # Odd number of digits
        # Extract a list of even-numbered digits and double them.
        l1 = [int(v)*2 for k,v in enumerate(n) if k%2]
        # Subtract 9 for each element in > 9.
        l1 = [i-9 if i>9 else i for i in l1]
        # Extract a list of odd-numbered digits.
        l2 = [int(v) for k,v in enumerate(n) if (not k%2 or k==0)]
    else: # Even number of digits
        # Extract a list of odd-numbered digits and double them.
        l1 = [int(v)*2 for k,v in enumerate(n) if (not k%2 or k==0)]
        # Subtract 9 for each element in > 9.
        l1 = [i-9 if i>9 else i for i in l1]
        # Extract a list of even-numbered digits.
        l2 = [int(v) for k,v in enumerate(n) if k%2]
    # Add the integers in both lists.
    c = sum(l1+l2)
    if c%10:
        return False
    else:
        return True
