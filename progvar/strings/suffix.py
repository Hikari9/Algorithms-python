from progvar.strings.utils import isstring, uni

class SuffixArray(list):
    '''
    Class: SuffixArray
    '''
    
    def __init__(self, text, algo=u'default', transform=True):
        '''
        Function: SuffixArray.__init__
        Summary: Initializes a suffix array data structure.
        Examples:
            print SuffixArray('abaab', algo='radix sort')
            # [5, 2, 3, 0, 4, 1]
        Attributes: 
            @param (self):
                The SuffixArray object.
            @param (text):
                The text vector to be transformed into a suffix array.
                Can be a single string, a list of strings, or a list of integers.
            @param (algo) default=u'default':
                The algorithm to be used by the suffix array.
                A list of available algorithms can be found in SuffixArray.algorithms.
            @param (transform) default=True:
                Optimization argument whether to transform the text using the method transform_characters or not.
                Set to false when you're working with a string of integers.
        Returns: None
        '''
        
        # check if algo is valid
        
        algo = algo.lower()
        if algo not in SuffixArray.algorithms:
            raise ValueError(u"invalid argument: algo='%s' is not in %s" % (algo, str(SuffixArray.algorithms.keys())))
        
        self.text = text
        self.algorithm = SuffixArray.algorithms[algo]

        # get suffix array from given algorithm
        list.__init__(self, self.algorithm(self.text, transform=transform))

        # post prepare properties
        from progvar.arrays import inverse_array

        self.string = SuffixArray._last_transformed_text if transform else text
        self.position = inverse_array(self)

        # prepare least common prefix
        n = len(self)
        self.lcp = [0] * n
        k = 0
        for i in xrange(n):
            if self.position[i] + 1 != n:
                j = self[self.position[i] + 1]
                while self.string[i + k] == self.string[j + k]:
                    k += 1
                self.lcp[self.position[i]] = k
                if k: k -= 1

    def suffix(self, index):
        '''
        Function: SuffixArray.suffix
        Summary:
            Gets the index-th string suffix in the suffix array.
            Uses the dollar sign '$' as a delimiter.
        Examples:
            print SuffixArray('abaab').suffix(1)
            # u'aab$'
        Attributes: 
            @param (self):
                The SuffixArray object.
            @param (index):
                The suffix array integer index.
        Returns: unicode
        '''
        return u''.join(map(lambda num: u'$' if num < 0 else chr(num), self.string[self[index]:]))

    _last_transformed_text = None


def transform_characters(text):
    '''
    Function: transform_characters
    Summary:
        Transform string or list of strings into a single list of ASCII values.
        Every list of strings will be appended with a negative integer (starting from -1)
    Attributes: 
        @param (text):
            The string or list of strings to transform.
    Returns: list
    '''
    import collections 

    if isstring(text):
        array = map(ord, text)
        array.append(-1)

    elif isinstance(text, collections.Iterable):
        if len(text) == 0:
            array = []
        elif isstring(text[0]):
            array = []
            delim = -1
            for subtext in text:
                array.extend(map(ord, subtext))
                array.append(delim)
                delim -= 1
        else:
            array = text[:]

    # save in SuffixArray object cache
    SuffixArray._last_transformed_text = array
    return array

def suffix_array_default(text, transform=True):
    '''
    Function: suffix_array_default
    Summary: Compute for the suffix array by using the most efficient algorithm given the nature of the string input.
    Attributes: 
        @param (text):
            The text vector to be transformed into a suffix array.
            Can be a single string, a list of strings, or a list of integers.
        @param (transform) default=True:
            Optimization argument whether to transform the text using the method transform_characters or not.
            Set to false when you're working with a string of integers.
    Returns: list
    '''

    string = transform_characters(text) if transform else text
    letters = len(set(x for x in string if x >= 0)) if transform else len(set(string))
    length = len(string)

    if letters == 1: # special case
        return reversed(range(length))

    elif letters == 2 and length <= 100: # counting sort for small binary cases
        return suffix_array_counting_sort(string, transform=False)

    elif length <= 100 or (length <= 1000 and letters >= 10): # brute force for general small cases
        return suffix_array_brute(string, transform=False)
    
    else: # DC3 for the rest
        return suffix_array_dc3(string, transform=False)

def suffix_array_brute(text, transform=True):
    '''
    Function: suffix_array_brute
    Summary: Compute for the suffix array by using brute force string comparison in O(n^2 log n).
    Attributes: 
        @param (text):
            The text vector to be transformed into a suffix array.
            Can be a single string, a list of strings, or a list of integers.
        @param (transform) default=True:
            Optimization argument whether to transform the text using the method transform_characters or not.
            Set to false when you're working with a string of integers.
    Returns: list
    '''
    
    # transform characters first into array of integers
    string = transform_characters(text) if transform else text
    n = len(string)

    # special case: one character
    single = string[0]
    for i in xrange(1, n - 1):
        if single != string[i]:
            single = None
            break

    if single:
        return reversed(range(n))

    # brute force comparator
    def compare(i, j):
        while i < n and j < n:
            if string[i] != string[j]: return cmp(string[i], string[j])
            i += 1
            j += 1
    
    return sorted(range(n), cmp=compare)


def suffix_array_counting_sort(text, transform=True):
    '''
    Function: suffix_array_counting_sort
    Summary: Compute for the suffix array by using counting sort in O(n log n).
    Attributes: 
        @param (text):
            The text vector to be transformed into a suffix array.
            Can be a single string, a list of strings, or a list of integers.
        @param (transform) default=True:
            Optimization argument whether to transform the text using the method transform_characters or not.
            Set to false when you're working with a string of integers.
    Returns: list
    '''

    # transform text into list of integers
    string = transform_characters(text) if transform else text
    n = len(string)

    # create initial list of indices
    sa = range(n)
    pos = string
    val = [0] * n
    count = [0] * n

    # stable sort according to character index
    # O(n log n)
    sa.sort(key=lambda index: (string[index], -index))

    # perform counting sort, iterate for each power of two offset
    # O(n log n)
    gap = 1
    while gap < n:
        val[sa[0]] = 0
        for I in xrange(1, n):
            i, j = sa[I - 1], sa[I]
            val[j] = val[i] if pos[i] == pos[j] and i + gap < n and pos[i + (gap >> 1)] == pos[j + (gap >> 1)] else I
        pos, val, count = val, sa[:], range(n)
        for i in xrange(n):
            index = val[i] - gap
            if index >= 0:
                sa[count[pos[index]]] = index
                count[pos[index]] += 1
        gap <<= 1

    return sa

def suffix_array_radix_sort(text, transform=True):
    '''
    Function: suffix_array_radix_sort
    Summary: Compute for the suffix array by using radix sort in O(n log^2 n).
    Attributes: 
        @param (text):
            The text vector to be transformed into a suffix array.
            Can be a single string, a list of strings, or a list of integers.
        @param (transform) default=True:
            Optimization argument whether to transform the text using the method transform_characters or not.
            Set to false when you're working with a string of integers.
    Returns: list
    '''

    # transform text into list of integers
    string = transform_characters(text) if transform else text
    n = len(string)
    
    # create the initial list of indices
    sa = range(n)
    pos = string[:]
    tmp = [0] * n
    gap = 1
    
    # comparator for radix sort
    def compare(i, j):
        if pos[i] != pos[j]: return cmp(pos[i], pos[j])
        i, j = i + gap, j + gap
        return cmp(pos[i], pos[j]) if i < n and j < n else cmp(j, i)
    
    # radix sort until each position is valid
    # O(n log^2 n)
    while True:
        sa.sort(cmp=compare)
        for i in xrange(1, n): tmp[i] = tmp[i - 1] + (1 if compare(sa[i - 1], sa[i]) < 0 else 0)
        for i in xrange(n): pos[sa[i]] = tmp[i]
        if tmp[n - 1] == n - 1: break
        gap <<= 1
    
    return sa

def suffix_array_dc3(text, transform=True):
    '''
    Function: suffix_array_dc3
    Summary: Compute for the suffix array by using DC3 algorithm in O(n log^2 n).
    Attributes: 
        @param (text):
            The text vector to be transformed into a suffix array.
            Can be a single string, a list of strings, or a list of integers.
        @param (transform) default=True:
            Optimization argument whether to transform the text using the method transform_characters or not.
            Set to false when you're working with a string of integers.
    Returns: list
    '''

    # transform text into offsetted list of integers
    string = transform_characters(text) if transform else text
    n = len(string)
    
    # find offset to compress array
    letters = sorted(set(string))
    compress = {letter: i + 1 for i, letter in enumerate(letters)}

    # helper functions
    # sort a, b according to radix r
    def radix_sort(a, b, r, offset, n, K):
        # counter array
        c = [0] * (K + 1)
        #count occurences
        for i in xrange(n):
            c[r[a[i] + offset]] += 1
        # exclusive sum prefix
        S = 0
        for i in xrange(K + 1):
            t = c[i]
            c[i] = S
            S += t
        # K'arrka'ainnen and P. Sanders
        for i in xrange(n):
            b[c[r[a[i] + offset]]] = a[i] # sort
            c[r[a[i] + offset]] += 1

    def DC3algorithm(s, sa, n, K):
        # sizes
        nL = (n + 2) // 3
        nM = (n + 1) // 3
        nR = n // 3
        nLR = nL + nR

        # dummy subarrays
        sL = [0] * nL
        saL = [0] * nL
        sMR = [0] * (nLR + 3)
        saMR = [0] * (nLR + 3)

        # radix sort those not divisible by 3
        j = 0
        for i in xrange(n + nL - nM):
            if i % 3 != 0:
                sMR[j] = i
                j += 1

        # swap indices
        radix_sort(sMR, saMR, s, 2, nLR, K)
        radix_sort(saMR, sMR, s, 1, nLR, K)
        radix_sort(sMR, saMR, s, 0, nLR, K)

        # assign bucket names
        name = 0
        c = [-1] * 3
        for i in xrange(nLR):
            equal = True
            for j in xrange(3):
                equal &= (c[j] == s[saMR[i] + j])
                c[j] = s[saMR[i] + j]
            if not equal: name += 1
            if saMR[i] % 3 == 1:
                sMR[saMR[i] // 3] = name
            else:
                sMR[saMR[i] // 3 + nL] = name


        # ternary partition
        if name < nLR:
            DC3algorithm(sMR, saMR, nLR, name)
            for i in xrange(nLR):
                sMR[saMR[i]] = i + 1
        else:
            for i in xrange(nLR):
                saMR[sMR[i] - 1] = i
        j = 0
        for i in xrange(nLR):
            if saMR[i] < nL:
                sL[j] = 3 * saMR[i]
                j += 1
        radix_sort(sL, saL, s, 0, nL, K)
        p, k, t = 0, 0, nL - nM
        while k < n:
            i = 3 * saMR[t] + 1 if saMR[t] < nL else 3 * (saMR[t] - nL) + 2
            j = saL[p]
            comp = ((s[i], sMR[saMR[t] + nL]) <= (s[j], sMR[j // 3])) if saMR[t] < nL else ((s[i], s[i + 1], sMR[saMR[t] - nL + 1]) <= (s[j], s[j + 1], sMR[j // 3 + nL]))
            if comp:
                sa[k] = i
                t += 1
                if t == nLR:
                    k += 1
                    while p < nL:
                        sa[k] = saL[p]
                        k += 1
                        p += 1
            else:
                sa[k] = j
                p += 1
                if p == nL:
                    k += 1
                    while t < nLR:
                        sa[k] = 3 * saMR[t] + 1 if saMR[t] < nL else 3 * (saMR[t] - nL) + 2
                        k += 1
                        t += 1
            k += 1
    
    sa = [0] * n
    sn = [compress[letter] for letter in string]
    sn.extend([0, 0, 0])

    DC3algorithm(sn, sa, n, len(letters))
    return sa

SuffixArray.algorithms = {
    u'brute': suffix_array_brute,
    u'counting sort': suffix_array_counting_sort,
    u'radix sort': suffix_array_radix_sort,
    u'dc3': suffix_array_dc3,
    u'default': suffix_array_default,
}