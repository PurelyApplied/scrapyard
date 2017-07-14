#!/usr/bin/env python
from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n):
    assert isinstance(n, int) and n >= 0
    if n in (0, 1):
        return 1
    return fib(n - 1) + fib(n - 2)


def dec_to_fib(n):
    if n == 0:
        return "0"
    # range out to the largest necessary number
    i = 0
    while fib(i) < n:
        i += 1
    # We're now one past the mark.  Back up.
    i -= 1
    # build up converted
    as_fib = ""
    while i >= 0:
        if fib(i) <= n:
            as_fib += "1"
            n -= fib(i)
        else:
            as_fib += "0"
        i -= 1
    return as_fib


def fib_to_dec(n):
    return sum(fib(i)
               for i in range(len(n))
               if n[-i - 1] == "1")
