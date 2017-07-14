from functools import lru_cache
import matplotlib.pyplot as plt
from tabulate import tabulate
import string

DIGITS = string.digits + string.ascii_lowercase


def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return DIGITS[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(DIGITS[x % base])
        x //= base

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


@lru_cache(maxsize=None)
def collatz(n):
    return 3 * n + 1 if n % 2 else n // 2


@lru_cache(maxsize=None)
def full_collatz(n, depth=0):
    ret = [n]
    while n != 1:
        n = collatz(n)
        ret.append(n)
    return ret


def draw(Xs, semi=True):
    Cs = [full_collatz(x) for x in Xs]
    Ls = [len(c) for c in Cs]
    Ms = [max(c) for c in Cs]
    p = plt.semilogy if semi else plt.plot
    plt.subplot(211)
    p(Xs, Ls, '.', markersize=1)
    plt.title('Chain length')
    plt.subplot(212)
    p(Xs, Ms, '.', markersize=1)
    plt.title('max value')
    plt.show()
    plt.figure()
    plt.loglog(Xs, Ms, '.', markersize=1)
    return Cs, Ls, Ms


def display(walk, pad_zeros=False):
    expanded_walk = [[str(i), int2base(i, 2), int2base(i, 3), int2base(i, 6)] for i in walk]
    if pad_zeros:
        width = max(len(x) for e in expanded_walk for x in e )
        print(width)
        for e in expanded_walk:
            for i, n in enumerate(e):
                e[i] = '0' * (width - len(n)) + n
    return tabulate(expanded_walk, headers=("N", "base2", "base3", "base6"))


def make_gviz(n=100, node_opts=None, edge_opts=None):
    # head
    s = "digraph G {\n"
    if node_opts:
        s += "\t node[{}];\n".format(node_opts)
    if edge_opts:
        s += "\t edge[{}];\n".format(edge_opts)
    # graph
    for i in range(1, n+1):
        s += "\t{} -> {};\n".format(i, collatz(i))
    # tail
    s += "}\n"
    return s


if __name__ == "__main__":
    print(display(full_collatz(25)))
