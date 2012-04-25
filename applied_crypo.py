'''
CS387 Applied Cryptography
'''
def convert_to_bits(n, pad):
	result = []
	while n > 0:
		if n%2 == 0:
			result = [0] + result
		else:
			result = [1] + result
		n = n/2
	while len(results) < pad:
		result = [0] + result
	return result

