def isstring(variable):
	return isinstance(variable, (str, unicode))

def uni(variable):
	return unicode(str(variable), 'ascii', 'ignore')

def random_text(length, letters=26):
	from random import randint

	if isinstance(length, int):
		length = (length, length)

	basis = ord('A') if letters <= 26 else 1
	return u''.join(chr(randint(basis, basis + letters - 1)) for i in xrange(randint(length[0], length[1])))
