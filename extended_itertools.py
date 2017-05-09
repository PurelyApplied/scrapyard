from itertools import tee


def k_wise(k, iterable):
    """"s -> (s0, s1, ..., sk), (s1, s2, ..., sk+1),  ..."""
    iterators = tee(iterable, k)
    for i in range(k):
        for _ in range(i):
            next(iterators[i], None)
    return zip(*iterators)
