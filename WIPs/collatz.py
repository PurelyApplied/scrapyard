from functools import lru_cache
import matplotlib.pyplot as plt


def next_collatz(n):
    return 3 * n + 1 if n % 2 else n // 2


@lru_cache(maxsize=256)
def collatz(n):
    if n == 1:
        return [1]
    return [n] + collatz(next_collatz(n))


def draw():
    Xs = list(range(1, 300))
    Cs = [collatz(x) for x in Xs]
    Ls = [len(c) for c in Cs]
    Ms = [max(c) for c in Cs]
    plt.subplot(211)
    plt.plot(Xs, Ls)
    plt.subplot(212)
    plt.plot(Xs, Ms)
