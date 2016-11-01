from collections import Counter

def answer(l):
    '''Given a list l, return the number tuples (x, y, z) where x divides
y and y divides z, with x, y, and z in l

    '''
    # For each value in the list, identify the number of factors of
    # that value that exist prior to that value's position.  The total
    # counter then increases by the number of factors of that value's
    # factor.  That is, assume your current value is "z", identify a
    # possible "y", and increment by the recorded number of seen
    # factors / possible "x" values.
    my_factors = {}
    count = 0
    for j, value_j in enumerate(l):
        factor_count = 0
        for i in range(j):
            value_i = l[i]
            if not value_j % value_i:
                factor_count += 1
                count += my_factors[i]
        my_factors[j] = factor_count
    return count
