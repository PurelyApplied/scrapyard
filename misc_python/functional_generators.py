#!/usr/bin/env python3

from functools import wraps

def functional_generator(g):
    @wraps
    def new_gen(g, *args, **kwargs):
        return g(*args, **kwargs)
    return new_gen(g).next


@functional_generator
def every_n(n):
    i = 0
    while True:
        i = i + 1 if i % n else 0
        yield not i



x = every_n(3)
while True:
    print(x())
