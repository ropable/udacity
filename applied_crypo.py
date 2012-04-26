#!/usr/bin/env python
'''
CS387 Applied Cryptography
'''
def convert_to_bits(n, pad=7):
	'''
	Takes an integer and returns it as a list of bits (padded to the defined amount).
	Use convert_to_bits(ord('s')) to convert ascii/unicode characters.
	'''
	if not isinstance(n, int):
		return 'Please pass in an integer.'
	result = []
	while n > 0:
		if n%2 == 0:
			result = [0] + result
		else:
			result = [1] + result
		n = n/2
	while len(result) < pad:
		result = [0] + result
	return result

def string_to_bits(s):
	'''
	Take a string and return it as a list of bits.
	'''
	result = []
	for c in s:
		result += convert_to_bits(ord(c), 7)
	return result

def display_bits(li):
	'''
	Take an iterable of bits and return them as one string.
	'''
	bits = ''
	for bit in li:
		bits += unicode(bit)
	return bits
