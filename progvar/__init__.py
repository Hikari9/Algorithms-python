from progvar.strings.suffix import SuffixArray

def isstring(variable):
	return isinstance(variable, (str, unicode))

def uni(variable):
	return unicode(variable, 'ascii', 'ignore')

def least_common_prefix_array(text, algo=u'default'):
	return SuffixArray(text, algo=algo).lcp

lcp_array = least_common_prefix_array