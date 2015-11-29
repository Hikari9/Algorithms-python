from algorithm.strings.suffix import SuffixArray

def longest_common_prefix_array(text, algo=u'default'):
	return SuffixArray(text, algo=algo).lcp

lcp_array = longest_common_prefix_array
