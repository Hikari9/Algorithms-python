from algorithm.strings.suffix import SuffixArray

def longest_common_prefix_array(text, algo=u'default'):
	return SuffixArray(text, algo=algo).lcp

def longest_common_substring(first_text, second_text, all=False, return_string=True):

	# collect data
	suffix = SuffixArray([first_text, second_text])
	lcp = suffix.lcp
	first_group, length = len(first_text), len(suffix)

	# iterate through the lcp array
	max_lcp, max_index = 0, 0
	for i in xrange(2, length - 1):
		if lcp[i] > max_lcp and (suffix[i] <= first_group) != (suffix[i + 1] <= first_group):
			max_lcp = lcp[i]
			max_index = i

	if all:

		if max_lcp == 0:
			return []
		indices = [i for i in xrange(2, length - 1) if lcp[i] == max_lcp and (suffix[i] <= first_group) != (suffix[i + 1] <= first_group) and (lcp[i - 1] != max_lcp or (suffix[i] <= first_group) == (suffix[i + 1] <= first_group))]
		
		if return_string:
			return [first_text[suffix[i]:suffix[i] + max_lcp] if suffix[i] <= first_group else first_text[suffix[i + 1]:suffix[i + 1] + max_lcp] for i in indices]
		else:
			return indices
	
	else:
		if return_string:
			i = max_index
			return first_text[suffix[i]:suffix[i] + max_lcp] if suffix[i] <= first_group else first_text[suffix[i + 1]:suffix[i + 1] + max_lcp]
		else:
			return max_lcp


lcp_array = longest_common_prefix_array
