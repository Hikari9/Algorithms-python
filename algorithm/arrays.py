def inverse_array(array):
	n = max(array) + 1
	inverse = [-1] * n
	for i in xrange(n):
		inverse[array[i]] = i
	return inverse

def inverse_table(array):
	return {array[i]: i for i in xrange(len(array))}

def frequency_array(array):
	n = max(array) + 1
	frequency = [0] * n
	for i in xrange(n):
		frequency[array[i]] += 1
	return frequency

def frequency_table(array):
	from collections import defaultdict
	frequency = defaultdict(int)
	for x in array:
		frequency[x] += 1
	return frequency